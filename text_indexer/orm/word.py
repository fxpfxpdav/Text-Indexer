from text_indexer.orm.base import DBBase
from sqlalchemy.schema import Column
from sqlalchemy.types import Integer, String

class Word(DBBase):
    __tablename__ = 'words'
    
    id = Column(Integer, primary_key=True)
    word = Column(String(255), nullable=False)
    
    
    def __init__(self, word):
        self.word = word
    
    def __repr__(self):
        return "Word(%r)" % (self.word)