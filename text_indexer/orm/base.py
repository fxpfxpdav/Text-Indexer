'''
Created on Jul 12, 2012

@author: dav
'''
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.schema import MetaData
engine = None
session = None

def connect():
    """
    This method connects to the db.
    """
    global session, engine
    engine = create_engine('mysql+mysqldb://root:root@localhost:3306/text_indexer')
    #engine = create_engine('mysql+mysqldb://root:root@10.0.0.129:3306/text_indexer')
#    engine.echo=True
    engine.connect()
    from sqlalchemy.orm import sessionmaker
    Session = sessionmaker(bind=engine)
    session = Session()
    
    
def create():
    """
    This methods creats a sesson with the db.
    """
    global engine, DBBase
    connect()
    meta_data = MetaData()
    meta_data.bind = engine

    DBBase = declarative_base(metadata=meta_data)

DBBase = None

create()




