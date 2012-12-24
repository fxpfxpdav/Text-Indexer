import sys
import os
import db

import lxml.etree as e
PREFIX = "CONCORDANCE"
#is phrase must be BOOL
def export_db_to_xml(ofile, cursor, enc, pas):
    cursor.execute("SELECT table_name, table_type, engine FROM information_schema.tables WHERE table_type = 'BASE TABLE' AND engine = 'InnoDB'")
    tables = cursor.fetchall()
    try:
        f = open(ofile,'wb')
    except Exception():
        return
    output = PREFIX
    output += ('<?xml version="1.0"?>\n')#encoding="UTF-16"?>\n')
    output += ('\t<tables>\n')
    for i in tables:
        table = i['table_name']
        output += ('\t\t<table name="%s">\n' % table)
        cursor.execute("SELECT * FROM %s" %table)
        res = cursor.fetchall()
        for row in res:
            output += ('\t\t\t<row>\n')
            for key in row.keys():
                
                #solve the utf problem. try to solve it another way.
                
                try:
                    for i in row[key]:
                        if ord(i) >= 128:
                            row[key] = "UTF8"
                            break
                except:
                    pass
                
                output += ('\t\t\t\t<%s>%s</%s>\n' % (key, str(row[key]),key))
            output += ('\t\t\t</row>\n')
        output += ('\t\t</table>\n')
    output += ('\t</tables>\n')
    if enc:
        encrypted_output = rc4crypt(output, pas)
    else:
        encrypted_output = output
    f.write(encrypted_output)
    f.close()

#export_db_to_xml("myxml.xml", cursor)

def import_xml_to_db(input_s, cursor, enc, pas):
    if enc == False:
        decrypted_s = input_s
    else:
        decrypted_s = rc4crypt(input_s, pas)
    if decrypted_s[:len(PREFIX)] != PREFIX:
        return False
    db.init_db()
    s = decrypted_s[len(PREFIX):]
    xml = e.fromstring(s)
    #root = xml.getroot()
    root = xml
    tables = root.iterchildren()
    for table in tables:
        table_name = table.attrib['name']
        rows = table.iterchildren()
        for row in rows:
            keys = row.iterchildren()
            keys_names = []
            values = []
            for key in keys:            
                keys_names.append(key.tag)
                values.append(key.text)
            query = "INSERT INTO %s (" %table_name
            for key in keys_names[:-1]:
                query += key + ","
            query += keys_names[-1] + ")"
            query += " VALUES ("
            for value in values:
                if isinstance(value,str):
                    query += '"%s"' % value + ','
                else:
                    query += "%d" %value + ','
            query = query[:-1] + ')'
            cursor.execute(query)

    cursor.connection.commit()

#import_xml_to_db("myxml.xml", cursor)
def rc4crypt(data, key):
    x = 0
    box = range(256)
    for i in range(256):
        x = (x + box[i] + ord(key[i % len(key)])) % 256
        box[i], box[x] = box[x], box[i]
    x = 0
    y = 0
    out = []
    for char in data:
        x = (x + 1) % 256
        y = (y + box[x]) % 256
        box[x], box[y] = box[y], box[x]
        out.append(chr(ord(char) ^ box[(box[x] + box[y]) % 256]))
    
    return ''.join(out)
