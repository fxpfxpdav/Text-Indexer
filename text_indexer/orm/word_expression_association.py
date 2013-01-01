from text_indexer.orm.base import DBBase
from sqlalchemy.schema import Column, ForeignKey
from sqlalchemy.types import Integer
from sqlalchemy.orm import relationship

    
class WordExpressionAssocaition(DBBase):
    __tablename__ = 'word_expression_associations'
    
    id = Column(Integer, primary_key=True)
    word_id = Column('word_id', Integer, ForeignKey('words.id'), primary_key=True)
    expression_id = Column('expression_id', Integer, ForeignKey('groups.id'), primary_key=True)
    place = Column('place', Integer, nullable=False, primary_key=True)
    
    word = relationship('Word', backref='word_expression_associations')
    expression = relationship('Expression', backref='word_expression_associations')
    
    
    def __init__(self, word_id, expression_id, place):
        self.word_id = word_id
        self.expression_id = expression_id
        self.place = place
    
    def __repr__(self):
        return "WordExpressionAssocaition"


