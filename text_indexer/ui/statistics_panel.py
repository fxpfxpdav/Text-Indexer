import wx
import os
from text_indexer.orm.word_position import WordPosition
from text_indexer.orm.song import Song

class StatisticsPanel(wx.Panel):
    
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, -1)
        
        text = "Statistics"
        text = wx.StaticText(self, -1, text, (600, 50))
        font = wx.Font(24, wx.SWISS, wx.NORMAL, wx.NORMAL, underline=True)
        text.SetFont(font)
        
        self.grid = wx.grid.Grid(self, -1, (200, 150), (900, 140))
        
        self.grid.CreateGrid(2, 4)
        
        self.grid.SetColSize(0, 200)
        self.grid.SetColSize(1, 200)
        self.grid.SetColSize(2, 200)
        self.grid.SetColSize(3, 200)

        
        self.grid.SetColLabelValue(0, "Word")
        self.grid.SetColLabelValue(1, "Line")
        self.grid.SetColLabelValue(2, "Paragraph")
        self.grid.SetColLabelValue(3, "Song")
        
        self.grid.SetRowSize(0, 50)
        self.grid.SetRowSize(1, 50)
        
        self.grid.SetRowLabelValue(0, "Chars")
        self.grid.SetRowLabelValue(1, "Words")
        
        from text_indexer.orm.base import session
        
        number_of_words = 0
        number_of_chars = 0
        number_of_lines = 0
        number_of_paragraphs = 0
        line=0
        stanza=0
        song_id=0
        for wp in session.query(WordPosition).order_by(WordPosition.song_id, WordPosition.line_number).all():
            number_of_words+=1
            number_of_chars+=len(wp.word.word)
            if wp.song_id != song_id:
                line = wp.line_number
                stanza = wp.stanza_number
                song_id = wp.song_id
                number_of_lines+=1
                number_of_paragraphs+=1
            elif wp.stanza_number != stanza:
                stanza = wp.stanza_number
                line= wp.line_number
                number_of_lines+=1
                number_of_paragraphs+=1
            elif wp.line_number != line:
                number_of_lines+=1
        
        chars_per_word = float(number_of_chars)/number_of_words
        self.grid.SetCellValue(0, 0, str(chars_per_word))
        self.grid.SetCellValue(0, 1, str(chars_per_word*number_of_words/number_of_lines))
        self.grid.SetCellValue(0, 2, str(chars_per_word*number_of_words/number_of_paragraphs))
        self.grid.SetCellValue(0, 3, str(number_of_words * chars_per_word/len(Song.get_songs())))
        self.grid.SetCellValue(1, 0, '1')
        self.grid.SetCellValue(1, 1, str(float(number_of_words)/number_of_lines))
        self.grid.SetCellValue(1, 2, str(float(number_of_words)/number_of_paragraphs))
        self.grid.SetCellValue(1, 3, str(float(number_of_words)/len(Song.get_songs())))
        