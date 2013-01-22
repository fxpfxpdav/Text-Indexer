import wx
from text_indexer.orm.song import Song
from text_indexer.orm.word_position import WordPosition


class SearchSongPanel(wx.Panel):
    
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, -1)
        
        text = "Search For Song"
        text = wx.StaticText(self, -1, text, (50, 50))
        font = wx.Font(18, wx.SWISS, wx.NORMAL, wx.NORMAL, underline=True)
        text.SetFont(font)
        
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        option_sizer = wx.BoxSizer(wx.VERTICAL)
        result_sizer = wx.BoxSizer(wx.VERTICAL)
        
        box1_title = wx.StaticBox( self, -1, "Search Options" )
        box1 = wx.StaticBoxSizer( box1_title, wx.VERTICAL )
        
        grid1 = wx.FlexGridSizer( 0, 2, 30, 10 )
        
        
        o_sizer0 = wx.BoxSizer(wx.VERTICAL)
        o_sizer1 = wx.BoxSizer(wx.VERTICAL)
        o_sizer2 = wx.BoxSizer(wx.VERTICAL)
        o_sizer3 = wx.BoxSizer(wx.VERTICAL)
        
        self.group1_ctrls = []
        self.radio0 = wx.CheckBox(self, -1, " Song Name  " )
        self.radio1 = wx.CheckBox(self, -1, " Song Writer  " )
        self.radio2 = wx.CheckBox(self, -1, " Song Performer    " )
        self.radio3 = wx.CheckBox(self, -1, " Contains The Word         " )
        self.radio_selected = self.radio0
        
        self.text0 = wx.TextCtrl( self, -1, "" )
        o_sizer0.AddSpacer(5)
        o_sizer0.Add(self.text0)
        
        self.text1 = wx.TextCtrl( self, -1, "" )
        o_sizer1.AddSpacer(5)
        o_sizer1.Add(self.text1)
        
        self.text2 = wx.TextCtrl( self, -1, "" )
        
        o_sizer2.AddSpacer(5)
        o_sizer2.Add(self.text2)
        
        self.text3 = wx.TextCtrl( self, -1, "" )
        
        o_sizer3.AddSpacer(5)
        o_sizer3.Add(self.text3)
        
        self.group1_ctrls.append((self.radio0, [self.text0], o_sizer0))
        self.group1_ctrls.append((self.radio1, [self.text1], o_sizer1))
        self.group1_ctrls.append((self.radio2, [self.text2], o_sizer2))
        self.group1_ctrls.append((self.radio3, [self.text3], o_sizer3))
        
        for radio, text_group, o_sizer in self.group1_ctrls:
            grid1.Add( radio, 0, wx.ALIGN_LEFT|wx.LEFT|wx.RIGHT|wx.TOP, 5 )
            self.Bind(wx.EVT_CHECKBOX, self.OnGroupSelect, radio )
            grid1.Add( o_sizer, 0, wx.ALIGN_LEFT|wx.LEFT|wx.RIGHT|wx.TOP, 5 )
                 
            for text in text_group:
                text.Enable(False)
                
        
        btn1 = wx.Button(self, -1, "Search", (380, 200))
        self.Bind(wx.EVT_BUTTON, self.onSearch, btn1) 

        btn2 = wx.Button(self, -1, "Show Song", (670, 200))
        self.Bind(wx.EVT_BUTTON, self.onShowSong, btn2) 
        
        
        self.text_result = "results"
        self.text_result = wx.StaticText(self, -1, self.text_result, (100,20))
        font = wx.Font(14, wx.SWISS, wx.NORMAL, wx.NORMAL)
        self.text_result.SetFont(font)
        
        self.song_list = wx.ListBox(self, 60, (50, 100), (150, 200), [], wx.LB_SINGLE)
        
        result_sizer.AddSpacer(100)
        result_sizer.Add(self.text_result)
        result_sizer.AddSpacer(10)
        result_sizer.Add(self.song_list)
        
        
        box1.Add( grid1, 0, wx.ALIGN_CENTRE|wx.ALL, 5 )
        option_sizer.AddSpacer(120)
        option_sizer.Add(box1)
        
        sizer.AddSpacer(50)
        sizer.Add(option_sizer)
        sizer.AddSpacer(150)
        sizer.Add(result_sizer)
        
        self.song_text_headline = wx.StaticText(self, -1, "The Song", (800, 100))
        font = wx.Font(14, wx.SWISS, wx.NORMAL, wx.NORMAL)
        self.song_text_headline.SetFont(font)
        self.t3 = wx.TextCtrl(self, -1, "", (800, 130), size=(500, 400), style=wx.TE_MULTILINE|wx.TE_READONLY)
        
        
        self.SetSizer(sizer)  
        
        
    def OnGroupSelect( self, event ):
        radio_selected = event.GetEventObject()
        is_checked =  event.IsChecked()

        for radio, text_group, o_sizer in self.group1_ctrls:
            if radio is radio_selected:
                if is_checked:
                    for text in text_group:
                        text.Enable(True)
                    self.radio_selected = radio
                else:
                    for text in text_group:
                        text.Enable(False)
        
    def onSearch(self, evt):
        from text_indexer.orm.base import session
        name = None
        writer = None
        performer = None
        word = None
        if self.radio0.IsChecked():
            name = self.text0.Value
        if self.radio1.IsChecked():
            writer = self.text1.Value
        if self.radio2.IsChecked():
            performer = self.text2.Value
        if self.radio3.IsChecked():
            word = self.text3.Value
        songs = [s.name for s in Song.get_songs(name, writer, performer, word)]
        self.song_list.Clear()
        self.song_list.AppendItems(songs)
            
    def onShowSong(self, evt):
        selection = self.song_list.GetSelection()
        if selection != -1:
            song = Song.get_songs(name=self.song_list.Items[selection])[0]
            self.t3.SetValue(song.get_text())
            self.t3.SetScrollPos(1,1)
    
        
        