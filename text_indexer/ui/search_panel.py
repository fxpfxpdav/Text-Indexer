import wx
import os
from text_indexer.orm.song import Song
from text_indexer.orm.word_position import WordPosition



class SearchPanel(wx.Panel):
    
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, -1)
        
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        song_sizer = wx.BoxSizer(wx.VERTICAL)
        option_sizer = wx.BoxSizer(wx.VERTICAL)
        result_sizer = wx.BoxSizer(wx.VERTICAL)
        
        text = "Choose song"
        text = wx.StaticText(self, -1, text, (100,20))
        font = wx.Font(14, wx.SWISS, wx.NORMAL, wx.NORMAL)
        text.SetFont(font)
        
        songList = [s.name for s in Song.get_songs()]
        self.lb1 = wx.ListBox(self, 60, wx.DefaultPosition, (200, 400), songList, wx.LB_SINGLE)
        
        song_sizer.AddSpacer(20)
        song_sizer.Add(text)
        song_sizer.AddSpacer(20)
        song_sizer.Add(self.lb1)
        
        box1_title = wx.StaticBox( self, -1, "Search Options" )
        box1 = wx.StaticBoxSizer( box1_title, wx.VERTICAL )
        
        grid1 = wx.FlexGridSizer( 0, 2, 30, 10 )
        
        
        o_sizer1 = wx.BoxSizer(wx.VERTICAL)
        o_sizer2 = wx.BoxSizer(wx.VERTICAL)
        o_sizer3 = wx.BoxSizer(wx.VERTICAL)
        
        self.group1_ctrls = []
        self.radio1 = wx.RadioButton(self, -1, " Word number  " )
        self.radio2 = wx.RadioButton(self, -1, " Paragraph    " )
        self.radio3 = wx.RadioButton(self, -1, " Line         " )
        self.radio_selected = self.radio1
        
        l1 = wx.StaticText(self, -1, "Number in song")
        text1 = wx.TextCtrl( self, -1, "" )
        o_sizer1.Add(l1)
        o_sizer1.AddSpacer(5)
        o_sizer1.Add(text1)
        
        l2_1 = wx.StaticText(self, -1, "Line number")
        l2_2 = wx.StaticText(self, -1, "Number in line")
        text2_1 = wx.TextCtrl( self, -1, "" )
        text2_2 = wx.TextCtrl( self, -1, "" )
        o_sizer2.Add(l2_1)
        o_sizer2.AddSpacer(5)
        o_sizer2.Add(text2_1)
        o_sizer2.Add(l2_2)
        o_sizer2.AddSpacer(5)
        o_sizer2.Add(text2_2)
        
        l3_1 = wx.StaticText(self, -1, "Paragraph number")
        l3_2 = wx.StaticText(self, -1, "Number in paragraph")
        text3_1 = wx.TextCtrl( self, -1, "" )
        text3_2 = wx.TextCtrl( self, -1, "" )
        o_sizer3.Add(l3_1)
        o_sizer3.AddSpacer(5)
        o_sizer3.Add(text3_1)
        o_sizer3.Add(l3_2)
        o_sizer3.AddSpacer(5)
        o_sizer3.Add(text3_2)
        
        self.group1_ctrls.append((self.radio1, [text1], o_sizer1))
        self.group1_ctrls.append((self.radio2, [text2_1, text2_2], o_sizer2))
        self.group1_ctrls.append((self.radio3, [text3_1, text3_2], o_sizer3))
        
        for radio, text_group, o_sizer in self.group1_ctrls:
            grid1.Add( radio, 0, wx.ALIGN_LEFT|wx.LEFT|wx.RIGHT|wx.TOP, 5 )
            self.Bind(wx.EVT_RADIOBUTTON, self.OnGroupSelect, radio )
            grid1.Add( o_sizer, 0, wx.ALIGN_LEFT|wx.LEFT|wx.RIGHT|wx.TOP, 5 )
                 
            for text in text_group:
                text.Enable(False)
                
        
        btn1 = wx.Button(self, -1, "Search", (700, 275))
        self.Bind(wx.EVT_BUTTON, self.onSearch, btn1) 
        
        
        self.text_result = "result"
        self.text_result = wx.StaticText(self, -1, self.text_result, (100,20))
        font = wx.Font(14, wx.SWISS, wx.NORMAL, wx.NORMAL)
        self.text_result.SetFont(font)
        
        self.word_text = wx.TextCtrl(self, -1, "", size=(125, -1))
        
        result_sizer.AddSpacer(250)
        result_sizer.Add(self.text_result)
        result_sizer.AddSpacer(10)
        result_sizer.Add(self.word_text)
        
        
        box1.Add( grid1, 0, wx.ALIGN_CENTRE|wx.ALL, 5 )
        option_sizer.AddSpacer(120)
        option_sizer.Add(box1)
        
        sizer.AddSpacer(100)
        sizer.Add(song_sizer)
        sizer.AddSpacer(100)
        sizer.Add(option_sizer)
        sizer.AddSpacer(200)
        sizer.Add(result_sizer)
        
        
        self.SetSizer(sizer)  
        
        
    def OnGroupSelect( self, event ):
        radio_selected = event.GetEventObject()

        for radio, text_group, o_sizer in self.group1_ctrls:
            if radio is radio_selected:
                for text in text_group:
                    text.Enable(True)
                self.radio_selected = radio
            else:
                for text in text_group:
                    text.Enable(False)
        
    def onSearch(self, evt):
        from text_indexer.orm.base import session
        song_name = self.lb1.Items[self.lb1.GetSelection()]
        song = Song.get_songs(name=song_name)[0]
        self.word_text.Value = song.name
        query = session.query(WordPosition)
        query = query.join(Song).filter(song=song)
        if self.radio_selected == self.radio1:
            query = query.filter_by()
        pass
    
        
        