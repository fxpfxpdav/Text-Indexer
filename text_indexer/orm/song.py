from text_indexer.orm.base import DBBase
from sqlalchemy.schema import Column
from sqlalchemy.types import Integer, String
from sqlalchemy.orm import relationship
from text_indexer.orm.word_song_association import word_song_associations

class Song(DBBase):
    __tablename__ = 'songs'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    writer = Column(String(255), nullable=False)
    
    words = relationship('Word', secondary=word_song_associations, backref='songs')


    def __init__(self, name, writer):
        self.name = name
        self.writer = writer
    
    def __repr__(self):
        return "Song(%r)" % (self.name)