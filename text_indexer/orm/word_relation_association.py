from text_indexer.orm.base import DBBase
from sqlalchemy.schema import Column, ForeignKey
from sqlalchemy.types import Integer
from sqlalchemy.orm import relationship
from text_indexer.orm.word import Word

class WordRelationAssociation(DBBase):
    __tablename__ = 'word_relation_associations'
    
    id = Column('id', Integer, primary_key=True)
    relation_id = Column('relation_id', Integer, ForeignKey('groups.id'), primary_key=True)
    first_word_id = Column('first_word_id', Integer, ForeignKey('words.id'), primary_key=True)
    second_word_id = Column('second_word_id', Integer, ForeignKey('words.id'), primary_key=True)
    
    first_word = relationship('Word', primaryjoin='WordRelationAssociation.first_word_id==Word.id', backref='word_relation_associations_as_first')
    second_word = relationship('Word', primaryjoin='WordRelationAssociation.second_word_id==Word.id', backref='word_relation_associations_as_second')
    relation = relationship('Relation', backref='word_relation_associations')
    



    def __init__(self, relation, first, second):
        self.relation_id = relation.id
        self.first_word_id = first.id
        self.second_word_id = second.id
    
    def __repr__(self):
        return "WordRelationAssociation"
