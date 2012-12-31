from text_indexer.orm.base import DBBase
from sqlalchemy.schema import Column
from sqlalchemy.types import Integer, String

class Word(DBBase):
    __tablename__ = 'words'
    
    id = Column(Integer, primary_key=True)
    word = Column(String(255), nullable=False)
    
    @staticmethod
    def add_word(word):
        from text_indexer.orm.base import session
        db_word = session.query(Word).filter_by(word=word).first()
        if not db_word:
            db_word = Word(word)
            session.add(db_word)
            session.commit()
        return db_word
    
    @staticmethod
    def get_words(word=""):
        from text_indexer.orm.base import session
        words = session.query(Word).order_by(Word.word)
        if word:
            words = words.filter_by(word=word)
        return words.all()
    
    def __init__(self, word):
        self.word = word
    
    def __repr__(self):
        return "Word(%r)" % (self.word)
    
    def get_indexes(self):
        return [{"row_word_number":wp.row_word_number,"line_number":wp.line_number,"stanza_number":wp.stanza_number,"stanza_line_number":wp.stanza_line_number} for wp in self.word_positions]
    
