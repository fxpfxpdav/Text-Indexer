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
from text_indexer.orm.word_expression_association import WordExpressionAssocaition
from text_indexer.orm.word_group_association import WordGroupAssociation
from text_indexer.orm.word_relation_association import WordRelationAssociation
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
    """
        This method sorts the tables, so that tables with dependecies will be exported in the rifht place
    """
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
    """
    This method exports the db to a xml file
    @param path: The path to save the db in.
    """
    cursor = create_cursor()
    
    # select all of the tables from the db
    cursor.execute("SELECT table_name, table_type, engine FROM information_schema.tables WHERE table_type = 'BASE TABLE' AND engine = 'InnoDB'")
    tables = cursor.fetchall()
    tables = [x for x in tables]
    #sort the tables by dependencies.
    tables.sort(cmp=sort_tables)
    #create the output.
    output=""
    output += ('<?xml version="1.0"?>\n')
    output += ('\t<tables>\n')
    for i in tables:
        # save the tables in the  file.
        table = i['table_name']
        output += ('\t\t<table name="%s">\n' % table)
        cursor.execute("SELECT * FROM %s" %table)
        results = cursor.fetchall()
        for result in results:
            output += ('\t\t\t<result>\n')
            for key in result.keys():
                output += ('\t\t\t\t<%s>%s</%s>\n' % (key, str(result[key]),key))
            output += ('\t\t\t</result>\n')
        output += ('\t\t</table>\n')
    output += ('\t</tables>\n')
    
    #save the output to a file
    f = open(path,'wb')
    f.write(output)
    f.close()

def import_db(path):
    """
    This method imports the db from a xml file
    @param path: The path of the saved db.
    """
    cursor = create_cursor()
    
    #read the file and parse the xml
    input_xml_file = open(path,'rb').read()
    root_xml = lxml.etree.fromstring(input_xml_file)
    tables = root_xml.iterchildren()
    for table in tables:
        table_name = table.attrib['name']
        results = table.iterchildren()
        for result in results:
            keys = result.iterchildren()
            key_names = []
            values = []
            for key in keys:            
                key_names.append(key.tag)
                values.append(key.text)
                
            #insert the data
            query = "INSERT INTO %s (" %table_name
            
            #add the keys
            for key in key_names[:-1]:
                query += key + ","
            query += key_names[-1] + ")"
            query += " VALUES ("
            
            #add the values
            for value in values:
                if isinstance(value,str):
                    query += '"%s"' % value + ','
                else:
                    query += "%d" %value + ','
            query = query[:-1] + ')'
            #run the query
            cursor.execute(query)

    # commit the results into the db.\z
    cursor.connection.commit()

def create_cursor():
    """
    This method creats a connector to the db.
    """
    con = MySQLdb.Connection(host = 'localhost', user = 'root', 
                           passwd = 'root' , db = 'text_indexer')
    cursor = con.cursor(MySQLdb.cursors.DictCursor)
    
    return cursor

def delete_song(song):
    for wp in song.word_positions:
        session.delete(wp)
    session.commit()
    session.delete(song) 
    session.commit()
    
def delete_expression(expression):
    for wea in session.query(WordExpressionAssocaition).filter_by(expression_id=expression.id).all():
        session.delete(wea)
    session.commit()
    session.delete(expression) 
    session.commit()
    
def delete_relation(relation):
    for wra in session.query(WordRelationAssociation).filter_by(relation_id=relation.id).all():
        session.delete(wra)
    session.commit()
    session.delete(relation) 
    session.commit()
    
def delete_group(group):
    for wga in session.query(WordGroupAssociation).filter_by(group_id=group.id).all():
        session.delete(wga)
    session.commit()
    session.delete(group) 
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
