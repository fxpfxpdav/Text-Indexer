
from text_indexer.orm.group import Group

class Expression(Group):
    __mapper_args__ = {'polymorphic_identity': 'expression'}
    
    
    def __repr__(self):
        return "Expression(%r)" % (self.name)