from text_indexer.orm.group import Group

class Relation(Group):
    __mapper_args__ = {'polymorphic_identity': 'relation'}
    
    
    def __repr__(self):
        return "Relation(%r)" % (self.name)