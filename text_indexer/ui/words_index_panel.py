import wx
import os

import  wx.grid
from text_indexer.orm.group import Group

class WordsIndexPanel(wx.Panel):
    
    def __init__(self, parent):
        from text_indexer.orm.base import session
        from text_indexer.orm.word_position import WordPosition
        
        wx.Panel.__init__(self, parent, -1)
        
        self.grid = wx.grid.Grid(self, -1, (100, 50), (1220, 400))
        
        self.wps = session.query(WordPosition).order_by(WordPosition.song_id, WordPosition.line_number,WordPosition.row_word_number).all()
        
        self.grid.CreateGrid(len(self.wps), 8)
        
        self.grid.SetColSize(0, 130)
        self.grid.SetColSize(1, 130)
        self.grid.SetColSize(2, 130)
        self.grid.SetColSize(3, 130)
        self.grid.SetColSize(4, 130)
        self.grid.SetColSize(5, 130)
        self.grid.SetColSize(6, 130)
        self.grid.SetColSize(7, 130)
        
        self.grid.SetColLabelValue(0, "Song")
        self.grid.SetColLabelValue(1, "Words")
        self.grid.SetColLabelValue(2, "Number in song")
        self.grid.SetColLabelValue(3, "Paragraph")
        self.grid.SetColLabelValue(4, "Number in paragraph")
        self.grid.SetColLabelValue(5, "Line number")
        self.grid.SetColLabelValue(6, "number in line")
        self.grid.SetColLabelValue(7, "word occurrence")
        
        
        group_text = wx.StaticText(self, -1, "Select Group", (100, 480))
        self.groups_list = [g.name for g in Group.get_groups(type='group')]
        
        self.select_group = wx.ComboBox(self, 500, "", (100, 500), 
                                        (160, -1), self.groups_list, wx.CB_DROPDOWN)
        
        self.group_button = wx.Button(self, -1, "Show Group Index", (320, 500))
        self.Bind(wx.EVT_BUTTON, self.groupChosen, self.group_button)
        
        self.refresh_button = wx.Button(self, -1, "Refresh", (500, 500))
        self.Bind(wx.EVT_BUTTON, self.refresh, self.refresh_button)
        
        self.show_words()
            
    
    def groupChosen(self, evt):
        self.grid.ClearGrid()
        name = self.select_group.Items[self.select_group.GetSelection()]
        print name
        group = Group.get_groups(name,type='group')[0]
        words = group.words
        words_text = [word.word for word in words]
        self.show_words(words_text)
    
    def refresh(self, evt):
        self.show_words()
            
    def show_words(self, words=None):
        song = self.wps[0].song.name
        number=0
        number_in_song = 1
        paragraph=1
        number_in_paragraph = 1
        for w in self.wps:
            if words is not None and w.word.word not in words:
                continue
            if w.song.name != song:
                song = w.song.name
                number_in_song = 1
                paragraph=1
                number_in_paragraph = 1
            if w.stanza_number > paragraph:
                paragraph = w.stanza_number
                number_in_paragraph = 1
            self.grid.SetCellValue(number, 0, song)
            self.grid.SetCellValue(number, 1, w.word.word)
            self.grid.SetCellValue(number, 2, str(number_in_song))
            self.grid.SetCellValue(number, 3, str(paragraph))
            self.grid.SetCellValue(number, 4, str(number_in_paragraph))
            self.grid.SetCellValue(number, 5, str(w.line_number))
            self.grid.SetCellValue(number, 6, str(w.row_word_number))
            self.grid.SetCellValue(number, 7, str(len(w.word.word_positions)))
            number+=1
            number_in_paragraph+=1
            number_in_song+=1
                
        