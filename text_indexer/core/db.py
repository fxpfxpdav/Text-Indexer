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
from text_indexer.orm.base import DBBase
import text_indexer.orm
DBBase.metadata.create_all(text_indexer.orm.base.engine)