from text_indexer.orm.base import DBBase
from sqlalchemy.schema import Column
from sqlalchemy.types import Integer, String
from sqlalchemy.orm import relationship
from text_indexer.orm import word_group_association
#from text_indexer.orm.word_group_association import word_group_associations

class Group(DBBase):
    __tablename__ = 'groups'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    type = Column(String(255), nullable=False)
    
    __mapper_args__ = {'polymorphic_on': type, 'polymorphic_identity': 'group'}
    words = relationship('Word', secondary=word_group_association.WordGroupAssociation.__table__, backref='groups')
    
    @staticmethod
    def get_groups(name="", type=""):
        from text_indexer.orm.base import session
        groups = session.query(Group).filter(Group.type != 'expression')
        if name:
            groups = groups.filter_by(name=name)
        if type:
            groups = groups.filter_by(type=type)
        return groups.all()



    def __init__(self, name):
        self.name = name
    
    def __repr__(self):
        return "Group(%r)" % (self.name)
    
    @staticmethod
    def add_group(name):
        from text_indexer.orm.base import session
        db_group = Group(name=name)
        session.add(db_group)
        session.commit()
        return db_group
    
    
