from text_indexer.orm.base import DBBase
from sqlalchemy.schema import Column, ForeignKey, Table
from sqlalchemy.types import Integer

    
word_song_associations = Table('word_song_associations', DBBase.metadata,
    Column('id', Integer, primary_key=True)
    , Column('word_id', Integer, ForeignKey('words.id'))
    , Column('song_id', Integer, ForeignKey('songs.id'))
    )