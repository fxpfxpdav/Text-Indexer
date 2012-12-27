import wx
import os
from text_indexer.orm.song import Song

class AnalysisPanel(wx.Panel):
    
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, -1)
        self.words = []
        self.songs = []
        
        songList = [s.name for s in Song.get_songs()]
        self.lb1 = wx.ListBox(self, 60, (100, 50), (200, 400), songList, wx.LB_EXTENDED)
        
        btn1 = wx.Button(self, -1, "Show words", (350, 100))
        self.Bind(wx.EVT_BUTTON, self.songChosen, btn1) 
        
        self.lb2 = wx.ListBox(self, 70, (450, 50), (90, 400), [], wx.LB_SINGLE)
        
        btn2 = wx.Button(self, -1, "Show context", (600, 100))
        self.Bind(wx.EVT_BUTTON, self.wordChosen, btn2) 
        
        self.t3 = wx.TextCtrl(self, -1,
                        "Choose a word from the songs.\n\n", (850, 50),
                       size=(400, 400), style=wx.TE_MULTILINE|wx.TE_PROCESS_ENTER)
        
    def songChosen(self, evt):
        self.lb2.Clear()
        self.words = []
        self.songs = []
        selections = self.lb1.GetSelections()
        for selection in selections:
            song = Song.get_songs(name=self.lb1.Items[selection])[0]
            self.songs.append(song)
            for word in song.words:
                if word not in self.words:
                    self.words.append(word)
                    self.lb2.Append(word.word)
                
    def wordChosen(self, evt):
        text = ''
        selection = self.lb2.GetSelection()
        word = self.words[selection]
        wps = set()
        for wp in word.word_positions:
            if wp.song in self.songs:
                if (wp.song.id, wp.stanza_number) not in wps:
                    wps.add((wp.song.id, wp.stanza_number))
                    text+= wp.song.get_stanza(wp.stanza_number)
                    text+= '\n\n\n'
        self.t3.Clear()
        self.t3.AppendText(text)
                        
        