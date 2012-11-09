from text_indexer.orm.base import DBBase
from sqlalchemy.schema import Column, ForeignKey
from sqlalchemy.types import Integer

class WordRelationAssocaition(DBBase):
    __tablename__ = 'word_relation_associations'
    
    id = Column('id', Integer, primary_key=True)
    relation_id = Column('relation_id', Integer, ForeignKey('groups.id'), primary_key=True)
    first_word_id = Column('first_word_id', Integer, ForeignKey('words.id'), primary_key=True)
    second_word_id = Column('second_word_id', Integer, ForeignKey('words.id'), primary_key=True)
    place = Column('place', Integer, nullable=False, primary_key=True)
    



    def __init__(self, name):
        self.name = name
    
    def __repr__(self):
        return "WordRelationAssocaition"
