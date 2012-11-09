from text_indexer.orm.base import DBBase
from sqlalchemy.schema import Column, ForeignKey, Table
from sqlalchemy.types import Integer

    
word_group_associations = Table('word_group_associations', DBBase.metadata,
    Column('id', Integer, primary_key=True)
    , Column('word_id', Integer, ForeignKey('words.id'))
    , Column('group_id', Integer, ForeignKey('groups.id'))
    )

