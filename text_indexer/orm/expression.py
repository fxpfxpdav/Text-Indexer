
from text_indexer.orm.group import Group
from text_indexer.orm.word_expression_association import WordExpressionAssocaition


class Expression(Group):
    __mapper_args__ = {'polymorphic_identity': 'expression'}
    
    
    def __repr__(self):
        return "Expression(%r)" % (self.name)
    
    @staticmethod
    def get_expressions(expression=""):
        from text_indexer.orm.base import session
        expressions = session.query(Expression)
        if expression:
            expressions = expressions.filter_by(name=expression)
        return expressions.all()
    
    @staticmethod
    def add_expression(expression):
        from text_indexer.orm.word import Word
        from text_indexer.orm.base import session
        db_words = []
        for word in expression.split(' '):
            db_word = session.query(Word).filter_by(word=word).first()
            if not db_word:
                db_word = Word(word=word)
                session.add(db_word)
            db_words.append(db_word)
        session.commit()
        
        db_expression = Expression(name=expression)
        session.add(db_expression)
        session.commit()
        number=1
        for db_word in db_words:
            word_expression = WordExpressionAssocaition(word_id=db_word.id, expression_id=db_expression.id, place=number)
            session.add(word_expression)
            number+=1
        session.commit()
        return db_expression
            