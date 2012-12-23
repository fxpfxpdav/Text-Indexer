from text_indexer.orm.base import DBBase
from sqlalchemy.schema import Column, ForeignKey
from sqlalchemy.types import Integer
from sqlalchemy.orm import relationship

class WordPosition(DBBase):
    __tablename__ = 'word_positions'
    
    id = Column(Integer, primary_key=True)
#    word_song_association_id = Column(Integer, ForeignKey('word_song_associations.id'))
    word_id = Column(Integer, ForeignKey('words.id'), nullable=False)
    song_id = Column(Integer, ForeignKey('songs.id'), nullable=False)
    row_word_number = Column('row_word_number', Integer, nullable=False)
    stanza_number = Column('stanza_number', Integer, nullable=False)
    line_number = Column('line_number', Integer, nullable=False)
    stanza_line_number = Column('stanza_line_number', Integer, nullable=False)
    
    word = relationship('Word', backref='word_positions')
    song = relationship('Song', backref='word_positions')
    
    

    def __init__(self, word, song, row_word_number, stanza_number, line_number, stanza_line_number):
        self.word = word
        self.song = song
        self.row_word_number = row_word_number
        self.stanza_number = stanza_number
        self.line_number = line_number
        self.stanza_line_number = stanza_line_number
    
    def __repr__(self):
        return "WordPosition(Word(%r) in Song(%r) line(%d), word(%d))" % (self.word.word, self.song.name, self.line_number, self.row_word_number)
    
    def get_stanza(self):
        return self.song.get_stanza(self.stanza_number)