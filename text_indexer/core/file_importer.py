import re
import db
from text_indexer.orm.song import Song
from text_indexer.orm import word
from text_indexer.orm.base import session
from text_indexer.orm.word import Word
from text_indexer.orm.word_position import WordPosition

class FileImporter(object):
    """
    This class imports and exports the db from and into files.
    """
    
    def __init__(self):
        self.word_positions = []
    
    
    def import_file(self, name, writer, performer, path):
        """
        @param name: The name of the song
        @param writer: The song writer.
        @param path: The path of the song.
        """
        db_song = session.query(Song).filter_by(name=name).first()
        if not db_song: 
            db_song = Song(name=name,writer=writer, performer=performer)
            session.add(db_song)
        self.load_file_into_song(path, db_song)
        
    
    def load_file_into_song(self, path, db_song):
        """
        This function loads the song into the db
        @param path: The path of the song
        @param db_song: The instance of the song in the db
        """
        f = open(path, "r")
        text = f.read()
        f.close()
        
        words = []
        stanzas = text.split("\n\n")
        rows = 1
        line_number = 1
        for stanza_number, stanza in enumerate(stanzas):
            
            stanza_line_number = 1
            rows = stanza.split("\n")
            for row in rows:
                row_word_number = 1
                words = re.findall(r'(\b[^\s]+\b)', row)
                for word in words:
                    self._create_word_in_DB(word, db_song, stanza_number, row_word_number, 
                                            line_number, stanza_line_number)
#                    print "Add word %s to song %s" % (word, db_song.name)
#                    print "line", line_number
#                    print "stanza", stanza_number
#                    print "line number in stanza", stanza_line_number 
#                    print "word number in row", row_word_number
#                    print "="*30 
                    
                    row_word_number += 1

                stanza_line_number += 1
                line_number += 1
                
        for word_position in self.word_positions:
            session.add(word_position)
        session.commit()
        
        
    def _create_word_in_DB(self, word, db_song, stanza_number, row_word_number, line_number, stanza_line_number):
        db_word = session.query(Word).filter_by(word=word).first()
        if not db_word:
            db_word = Word(word=word)
            session.add(db_word)
            session.commit()
            
        word_position = WordPosition(word=db_word, song=db_song, row_word_number=row_word_number, stanza_number=stanza_number, line_number=line_number, stanza_line_number=stanza_line_number)
        self.word_positions.append(word_position)
        
if __name__ == '__main__':
#    FileImporter().import_file("Call Me Maybe", "Carly Rae Jepsen", r"C:\text\text_indexer\songs\call_me_maybe.txt")
    song = session.query(Song).first()
    song.get_stanza(2)
        