from text_indexer.orm.base import DBBase
from sqlalchemy.schema import Column, ForeignKey
from sqlalchemy.types import Integer
import word_song_association

class WordPosition(DBBase):
    __tablename__ = 'word_positions'
    
    id = Column(Integer, primary_key=True)
    word_song_association_id = Column(Integer, ForeignKey('word_song_associations.id'))
#    word_song_association_id = Column(Integer, ForeignKey(word_song_association.word_song_associations.c['id']))
    row_position = Column('row_position', Integer, nullable=False)
    stanza_position = Column('Stanza_position', Integer, nullable=False)
    line_position = Column('line_position', Integer, nullable=False)
    stanza_line_position = Column('stanza_line_position', Integer, nullable=False)
    
    

    def __init__(self, word_song_association_id, row_position, stanza_position, line_position, stanza_line_position):
        self.word_song_association_id = word_song_association_id
        self.row_position = row_position
        self.stanza_position = stanza_position
        self.line_position = line_position
        self.stanza_line_position = stanza_line_position
    
    def __repr__(self):
        return "WordPosition"