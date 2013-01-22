import wx
import os
import re
from text_indexer.orm.song import Song
from text_indexer.orm.word import Word
from text_indexer.orm.expression import Expression
from text_indexer.orm.group import Group

class AnalysisPanel(wx.Panel):
    
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, -1)
        self.words = Word.get_words()
        self.songs = []
        
        song_text = wx.StaticText(self, -1, "Select Song", (100, 30))
        songList = [s.name for s in Song.get_songs()]
        self.lb1 = wx.ListBox(self, 60, (100, 50), (200, 200), songList, wx.LB_EXTENDED)
        self.lb1.SetSelection(0)
        
#        btn1 = wx.Button(self, -1, "Show words", (330, 120))
#        self.Bind(wx.EVT_BUTTON, self.songChosen, btn1) 
        
        words_text = wx.StaticText(self, -1, "Select Word", (450, 30))
        self.lb2 = wx.ListBox(self, 70, (450, 50), (90, 200), [], wx.LB_SINGLE)
        
        words = self.words
        for word in words:
            self.lb2.Append(word.word)
        
        btn2 = wx.Button(self, -1, "Search Word", (450, 280))
        self.Bind(wx.EVT_BUTTON, self.wordChosen, btn2) 
        
        occurrences_text = wx.StaticText(self, -1, "Occurrences", (750, 30))
        self.t3 = wx.TextCtrl(self, -1,
                        "", (750, 50),
                       size=(400, 400), style=wx.TE_MULTILINE|wx.TE_RICH2)
        
        group_text = wx.StaticText(self, -1, "Select Group", (100, 380))
        self.groups_list = [g.name for g in Group.get_groups(type='group')]
        
        self.select_group = wx.ComboBox(self, 500, "", (100, 400), 
                                        (160, -1), self.groups_list, wx.CB_DROPDOWN)
        
        btn4 = wx.Button(self, -1, "Search Group", (100, 500))
        self.Bind(wx.EVT_BUTTON, self.groupChosen, btn4)
        
        btn2 = wx.Button(self, -1, "Search Phrase", (750, 500))
        self.Bind(wx.EVT_BUTTON, self.phraseChosen, btn2)
        
        expression_text = wx.StaticText(self, -1, "Select Expression", (450, 380))
        
        expression_list = [e.name for e in Expression.get_expressions()]
        self.lb3 = wx.ListBox(self, 70, (450, 410), (90, 50), expression_list, wx.LB_SINGLE)
        
        btn3 = wx.Button(self, -1, "Search Expression", (450, 500))
        self.Bind(wx.EVT_BUTTON, self.expressionChosen, btn3)
        
#    def songChosen(self, evt):
#        self.lb2.Clear()
#        self.words = []
#        self.songs = []
#        selections = self.lb1.GetSelections()
#        for selection in selections:
#            song = Song.get_songs(name=self.lb1.Items[selection])[0]
#            self.songs.append(song)
#            for word in song.words:
#                if word not in self.words:
#                    self.words.append(word)
#                    self.lb2.Append(word.word)
#        self.lb2.SetSelection(0)
                
    def wordChosen(self, evt):
        text = ''
        selection = self.lb2.GetSelection()
        word = self.words[selection]
        wps = set()
        songs = [self.lb1.Items[song_selection] for song_selection in self.lb1.Selections]
        for song in songs:
            added_song_name = False
            for wp in word.word_positions:
                if wp.song.name == song:
                    if not added_song_name:
                        text+= song + ':\n\n'
                        added_song_name = True
                    if (wp.song.id, wp.stanza_number) not in wps:
                        wps.add((wp.song.id, wp.stanza_number))
                        text+= wp.song.get_stanza(wp.stanza_number)
                        text+= '\n\n\n'
        
        self.t3.SetValue(text)
        self.t3.SetScrollPos(1,1)
        for m in re.finditer(" " + word.word, text ):
            self.t3.SetStyle(m.start()+1, m.end(), wx.TextAttr("RED", "YELLOW"))
        for m in re.finditer("\n" + word.word, text ):
                self.t3.SetStyle(m.start()+1, m.end(), wx.TextAttr("RED", "YELLOW"))
            
    
    def phraseChosen(self, evt):
        from text_indexer.orm.base import session
        text = self.t3.GetValue()
        start,end = self.t3.GetSelection()
        selected = text[start:end]
        words = selected.replace('\n',' ').strip().replace('  ', ' ').split(' ')
        matches = set()
        number_of_words = len(words)
        word = session.query(Word).filter_by(word=words[0])[0]
        wps = word.word_positions
        for w in wps:
            i = 1
            wp = w.get_next_word()
            while i < number_of_words and wp.word.word == words[i]:
                i+=1
                wp = wp.get_next_word()
            if i == number_of_words:
                matches.add(w)
        
            
        wps = set()
        text = ''
        songs = [self.lb1.Items[song_selection] for song_selection in self.lb1.Selections]
        for song in songs:
            added_song_name = False
            for wp in matches:
                if wp.song.name == song:
                    if not added_song_name:
                        text+= song + ':\n\n'
                        added_song_name = True
                    if (wp.song.id, wp.stanza_number) not in wps:
                        wps.add((wp.song.id, wp.stanza_number))
                        text+= wp.song.get_stanza(wp.stanza_number)
                        text+= '\n\n\n'
#        
#        self.t3.SetValue(str(words))
        self.t3.SetValue(text)
        self.t3.SetScrollPos(1,1)
        for m in re.finditer(" " + selected, text):
            self.t3.SetStyle(m.start()+1, m.end(), wx.TextAttr("RED", "YELLOW"))
        for m in re.finditer("\n" + word.word, text ):
                self.t3.SetStyle(m.start()+1, m.end(), wx.TextAttr("RED", "YELLOW"))
            
            
    def groupChosen(self, evt):
        name = self.select_group.Items[self.select_group.GetSelection()]
        group = Group.get_groups(name,type='group')[0]
        words = group.words
        text = ""
        wps = set()
        songs = [self.lb1.Items[song_selection] for song_selection in self.lb1.Selections]
        for song in songs:
            added_song_name = False
            for word in words:
                for wp in word.word_positions:
                    if wp.song.name == song:
                        if not added_song_name:
                            text+= song + ':\n\n'
                            added_song_name = True
                        if (wp.song.id, wp.stanza_number) not in wps:
                            wps.add((wp.song.id, wp.stanza_number))
                            text+= wp.song.get_stanza(wp.stanza_number)
                            text+= '\n\n\n'
        
        self.t3.SetValue(text)
        self.t3.SetScrollPos(1,1)
        for word in words:
            for m in re.finditer(" " + word.word, text ):
                self.t3.SetStyle(m.start()+1, m.end(), wx.TextAttr("RED", "YELLOW"))
            for m in re.finditer("\n" + word.word, text ):
                self.t3.SetStyle(m.start()+1, m.end(), wx.TextAttr("RED", "YELLOW"))

        
    def expressionChosen(self, evt):
        from text_indexer.orm.base import session
        selected = self.lb3.Items[self.lb3.Selection]
        words = selected.replace('\n',' ').strip().replace('  ', ' ').split(' ')
        matches = set()
        number_of_words = len(words)
        word = session.query(Word).filter_by(word=words[0])[0]
        wps = word.word_positions
        for w in wps:
            i = 1
            wp = w.get_next_word()
            while i < number_of_words and wp and wp.word.word == words[i]:
                i+=1
                wp = wp.get_next_word()
            if i == number_of_words:
                matches.add(w)
        
            
        wps = set()
        text = ''
        songs = [self.lb1.Items[song_selection] for song_selection in self.lb1.Selections]
        for song in songs:
            added_song_name = False
            for wp in matches:
                if wp.song.name == song:
                    if not added_song_name:
                        text+= song + ':\n\n'
                        added_song_name = True
                    if (wp.song.id, wp.stanza_number) not in wps:
                        wps.add((wp.song.id, wp.stanza_number))
                        text+= wp.song.get_stanza(wp.stanza_number)
                        text+= '\n\n\n'
                    
#        
#        self.t3.SetValue(str(words))
        self.t3.SetValue(text)
        self.t3.SetScrollPos(1,1)
        for m in re.finditer(selected, text):
            self.t3.SetStyle(m.start(), m.end(), wx.TextAttr("RED", "YELLOW"))
        for m in re.finditer("\n" + word.word, text ):
                self.t3.SetStyle(m.start()+1, m.end(), wx.TextAttr("RED", "YELLOW"))
                        
        