'''
Created on Jul 12, 2012

@author: dav
'''
#import text_indexer.orm.base as base
#from sqlalchemy.schema import MetaData
#import text_indexer.orm
#from sqlalchemy import create_engine
#engine = None
#session = None
#
import MySQLdb
import lxml
import lxml.etree
#def connect():
#    engine = create_engine('mysql+mysqldb://root:root@localhost:3306/text_indexer')
#    engine.connect()
#    print engine.execute('select * from tttt').fetchall()
#    from sqlalchemy.orm import sessionmaker
#    session = sessionmaker(bind=engine)
#    
#    
#def create():
#    connect()
#    meta_data = MetaData()
#    db_base = base.Base
#    db_base.create_base(meta_data)
#    db_base.DBBase.metadata.bind = engine
#    db_base.DBBase.metadata.create_all()
#    
#create()

table_order = ['songs', 'words', 'word_positions','groups', 'relations']

def sort_tables(x,y):
    x = x['table_name']
    y = y['table_name']
    if x in table_order:
        if y not in table_order:
            return -1
        else:
            return cmp(table_order.index(x), table_order.index(y))
    elif y in table_order:
        return 1
    else:
        return 0
        
    pass

def export_db(path):
    cursor = create_cursor()
    cursor.execute("SELECT table_name, table_type, engine FROM information_schema.tables WHERE table_type = 'BASE TABLE' AND engine = 'InnoDB'")
    tables = cursor.fetchall()
    tables = [x for x in tables]
    tables.sort(cmp=sort_tables)
    try:
        f = open(path,'wb')
    except Exception():
        return
    output=""
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
    f.write(output)
    f.close()

def import_db(path):
    cursor = create_cursor()
    input_xml = open(path,'rb').read()
    xml = lxml.etree.fromstring(input_xml)
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

    pass

def create_cursor():
    con = MySQLdb.Connection(host = '10.0.0.129', user = 'root', 
                           passwd = 'root' , db = 'text_indexer')
    cursor = con.cursor(MySQLdb.cursors.DictCursor)
    
    return cursor

def delete_song(song):
    for wp in song.word_positions:
        session.delete(wp)
    session.commit()
    session.delete(song) 
    session.commit()

from text_indexer.orm.base import DBBase
import text_indexer.orm
from text_indexer.orm.song import Song
from text_indexer.orm.word import Word
DBBase.metadata.create_all(text_indexer.orm.base.engine)
from text_indexer.orm.base import session

#s = Song.get_songs(name='some nights', writer='Fun', word='some')[0]
#print s.writer
#word = session.query(Word).first()
#print word
#print word.get_indexes()
#wp = word.word_positions[1]
#print wp
#print wp.get_stanza()
#import_db(r'c:/db.xml')
#print 'exported db'
