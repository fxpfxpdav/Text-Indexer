from text_indexer.orm.base import DBBase
from sqlalchemy.schema import Column
from sqlalchemy.types import Integer, String
from sqlalchemy.orm import relationship
from text_indexer.orm.word_group_association import word_group_associations

class Group(DBBase):
    __tablename__ = 'groups'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    type = Column(String(255), nullable=False)
    
    __mapper_args__ = {'polymorphic_on': type, 'polymorphic_identity': 'group'}
    words = relationship('Word', secondary=word_group_associations, backref='groups')



    def __init__(self, name):
        self.name = name
    
    def __repr__(self):
        return "Group(%r)" % (self.name)