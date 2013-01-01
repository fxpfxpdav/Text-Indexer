from text_indexer.orm.group import Group
from text_indexer.orm.word_relation_association import WordRelationAssociation
from text_indexer.orm import word_relation_association
from sqlalchemy.orm import relationship

class Relation(Group):
    __mapper_args__ = {'polymorphic_identity': 'relation'}
    
    
    def __init__(self, name):
        self.name = name
    
    def __repr__(self):
        return "Relation(%r)" % (self.name)
    
    @property
    def first_word(self):
        return self.word_relation_associations[0].first_word
    
    @property
    def second_word(self):
        return self.word_relation_associations[0].second_word
    
    @staticmethod
    def add_relation(name, first, second):
        from text_indexer.orm.word import Word
        from text_indexer.orm.base import session
        db_first = Word.add_word(first)
        db_second = Word.add_word(first)
        
        relation = Relation(name)
        session.add(relation)
        
        session.commit()
        
        word_relation = WordRelationAssociation(relation, db_first, db_second)
        session.add(word_relation)
        session.commit()
        
        