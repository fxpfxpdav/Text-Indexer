
import wx
import wx.aui
from text_indexer.ui.manage_songs_panel import ManageSongsPanel
from text_indexer.ui.analysis_panel import AnalysisPanel
from text_indexer.ui.words_index_panel import WordsIndexPanel
from text_indexer.ui.statistics_panel import StatisticsPanel
from text_indexer.ui.search_panel import SearchPanel
from text_indexer.ui.expressions_panel import GroupAndExpressionsPanel
from text_indexer.ui.search_song_panel import SearchSongPanel


#----------------------------------------------------------------------

class ParentFrame(wx.aui.AuiMDIParentFrame):
    def __init__(self, parent):
        wx.aui.AuiMDIParentFrame.__init__(self, parent, -1,
                                          title="Text Indexer",
                                          size=(1400, 700),
                                          style=wx.DEFAULT_FRAME_STYLE)
        self.count = 0
        mb = self.MakeMenuBar()
        self.SetMenuBar(mb)
        self.CreateStatusBar()
        #self.Bind(wx.EVT_CLOSE)
        
    def MakeMenuBar(self):
        mb = wx.MenuBar()
        file_menu = wx.Menu()
        item = file_menu.Append(-1, "Manage Songs\tCtrl-M")
        self.Bind(wx.EVT_MENU, self.OnManageSongs, item)

        
        item = file_menu.Append(-1, "Groups and Expressions\tCtrl-G")
        self.Bind(wx.EVT_MENU, self.OnExpressions, item)
        
        item = file_menu.Append(-1, "Words Index\tCtrl-I")
        self.Bind(wx.EVT_MENU, self.OnWordsIndex, item)
        
        item = file_menu.Append(-1, "Statistics\tCtrl-T")
        self.Bind(wx.EVT_MENU, self.OnStatistics, item)
             
        item = file_menu.Append(-1, "Close")
        self.Bind(wx.EVT_MENU, self.OnDoClose, item)
        
        seacrh_menu = wx.Menu()
        item = seacrh_menu.Append(-1, "Word\tCtrl-W")
        self.Bind(wx.EVT_MENU, self.onSearch, item)
        
        item = seacrh_menu.Append(-1, "Occurrences\tCtrl-O")
        self.Bind(wx.EVT_MENU, self.OnTextAnalysis, item)
        
        item = seacrh_menu.Append(-1, "Song\tCtrl-S")
        self.Bind(wx.EVT_MENU, self.OnSearchSong, item)
        
        mb.Append(file_menu, "&File")
        mb.Append(seacrh_menu, "&Search")
        return mb
        
    def OnManageSongs(self, evt):
        self.count += 1
        child = ChildFrame(self, self.count, "Manage Songs", ManageSongsPanel)
        child.Show()

    def OnExpressions(self, evt):
        self.count += 1
        child = ChildFrame(self, self.count, "Groups and Expressions", GroupAndExpressionsPanel)
        child.Show()
        
    def onSearch(self, evt):
        self.count += 1
        child = ChildFrame(self, self.count, "Search For Word", SearchPanel)
        child.Show()
     
    def OnTextAnalysis(self, evt):
        self.count += 1
        child = ChildFrame(self, self.count, "Search For Occurrence", AnalysisPanel)
        child.Show()
        
    def OnWordsIndex(self, evt):
        self.count += 1
        child = ChildFrame(self, self.count, "Words Index", WordsIndexPanel)
        child.Show()
        
    def OnStatistics(self, evt):  
        self.count += 1
        child = ChildFrame(self, self.count, "Statistics", StatisticsPanel)
        child.Show()

    def OnSearchSong(self, evt):  
        self.count += 1
        child = ChildFrame(self, self.count, "Search For Song", SearchSongPanel)
        child.Show()

    def OnDoClose(self, evt):
        # Close all ChildFrames first else Python crashes
        for m in self.GetChildren():
            if isinstance(m, wx.aui.AuiMDIClientWindow):
                for k in m.GetChildren():
                    if isinstance(k, ChildFrame):
                        k.Close()  
        evt.Skip()
        self.Close(True)
        

#----------------------------------------------------------------------

class ChildFrame(wx.aui.AuiMDIChildFrame):
    def __init__(self, parent, count, title, panel):
        wx.aui.AuiMDIChildFrame.__init__(self, parent, -1,
                                         title=title)
        
        p = panel(self)

        sizer = wx.BoxSizer()
        sizer.Add(p, 1, wx.EXPAND)
        self.SetSizer(sizer)
        
        wx.CallAfter(self.Layout)


if __name__ == '__main__':
    class MyApp(wx.App):
        def OnInit(self):
            wx.InitAllImageHandlers()
            frame = ParentFrame(None)
            frame.Show(True)
            self.SetTopWindow(frame) 
            return True
        
        
    app = MyApp(False)
    
    app.MainLoop()  
