from text_indexer.orm.base import DBBase
from sqlalchemy.schema import Column, ForeignKey
from sqlalchemy.types import Integer

    
class WordExpressionAssocaition(DBBase):
    __tablename__ = 'word_expression_associations'
    
    id = Column(Integer, primary_key=True)
    word_id = Column('word_id', Integer, ForeignKey('words.id'), primary_key=True)
    expression_id = Column('expression_id', Integer, ForeignKey('groups.id'), primary_key=True)
    place = Column('place', Integer, nullable=False, primary_key=True)
    
    
    def __init__(self, name):
        self.name = name
    
    def __repr__(self):
        return "WordExpressionAssocaition"


