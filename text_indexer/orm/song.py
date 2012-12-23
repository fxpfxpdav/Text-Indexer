from text_indexer.orm.base import DBBase
from sqlalchemy.schema import Column
from sqlalchemy.types import Integer, String
from sqlalchemy.orm import relationship
from text_indexer.orm import word_position

class Song(DBBase):
    __tablename__ = 'songs'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    writer = Column(String(255), nullable=False)
    
    words = relationship('Word', secondary=word_position.WordPosition.__table__, backref='songs')


    def __init__(self, name, writer):
        self.name = name
        self.writer = writer
    
    def __repr__(self):
        return "Song(%r)" % (self.name)
    
    def get_stanza(self, stanza_number):
        from text_indexer.orm.base import session
        from text_indexer.orm.word_position import WordPosition
        wps = session.query(WordPosition).filter_by(song_id=self.id, stanza_number=stanza_number).order_by(WordPosition.stanza_line_number,WordPosition.row_word_number).all()
        words = [wp.word.word for wp in wps]
        return words
        
    @staticmethod
    def get_songs(name="", writer="", word=""):
        from text_indexer.orm.base import session
        songs = session.query(Song)
        if name:
            songs = songs.filter_by(name=name)
        if writer:
            songs = songs.filter_by(writer=writer)
        if word:
            songs = songs.join(Song.words).filter_by(word=word)
        return songs.all()
            