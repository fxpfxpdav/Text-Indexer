
import wx
import wx.aui
from text_indexer.ui.manage_songs_panel import ManageSongsPanel
from text_indexer.ui.analysis_panel import AnalysisPanel
from text_indexer.ui.words_index_panel import WordsIndexPanel
from text_indexer.ui.statistics_panel import StatisticsPanel
from text_indexer.ui.search_panel import SearchPanel
from text_indexer.ui.expressions_panel import GroupAndExpressionsPanel


#----------------------------------------------------------------------

class ParentFrame(wx.aui.AuiMDIParentFrame):
    def __init__(self, parent):
        wx.aui.AuiMDIParentFrame.__init__(self, parent, -1,
                                          title="Stress",
                                          size=(1400, 700),
                                          style=wx.DEFAULT_FRAME_STYLE)
        self.count = 0
        mb = self.MakeMenuBar()
        self.SetMenuBar(mb)
        self.CreateStatusBar()
        #self.Bind(wx.EVT_CLOSE)
        
    def MakeMenuBar(self):
        mb = wx.MenuBar()
        menu = wx.Menu()
        item = menu.Append(-1, "Manage songs\tCtrl-M")
        self.Bind(wx.EVT_MENU, self.OnManageSongs, item)
        
        item = menu.Append(-1, "Search\tCtrl-S")
        self.Bind(wx.EVT_MENU, self.onSearch, item)
        
        item = menu.Append(-1, "Text analysis\tCtrl-A")
        self.Bind(wx.EVT_MENU, self.OnTextAnalysis, item)
        
        item = menu.Append(-1, "Groups and Expressions\tCtrl-G")
        self.Bind(wx.EVT_MENU, self.OnExpressions, item)
        
        item = menu.Append(-1, "Words index\tCtrl-W")
        self.Bind(wx.EVT_MENU, self.OnWordsIndex, item)
        
        item = menu.Append(-1, "Statistics\tCtrl-T")
        self.Bind(wx.EVT_MENU, self.OnStatistics, item)
             
        item = menu.Append(-1, "Close")
        self.Bind(wx.EVT_MENU, self.OnDoClose, item)
        mb.Append(menu, "&File")
        return mb
        
    def OnManageSongs(self, evt):
        self.count += 1
        child = ChildFrame(self, self.count, "Manage songs", ManageSongsPanel)
        child.Show()

    def OnExpressions(self, evt):
        self.count += 1
        child = ChildFrame(self, self.count, "Expressions", GroupAndExpressionsPanel)
        child.Show()
        
    def onSearch(self, evt):
        self.count += 1
        child = ChildFrame(self, self.count, "Search", SearchPanel)
        child.Show()
     
    def OnTextAnalysis(self, evt):
        self.count += 1
        child = ChildFrame(self, self.count, "Analysis text", AnalysisPanel)
        child.Show()
        
    def OnWordsIndex(self, evt):
        self.count += 1
        child = ChildFrame(self, self.count, "Words index", WordsIndexPanel)
        child.Show()
        
    def OnStatistics(self, evt):  
        self.count += 1
        child = ChildFrame(self, self.count, "Statistics", StatisticsPanel)
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
        """
        mb = parent.MakeMenuBar()
        menu = wx.Menu()
        item = menu.Append(-1, "This is child %d's menu" % count)
        mb.Append(menu, title + " menu")
        self.SetMenuBar(mb)
        """
        
        p = panel(self)
        #p.SetBackgroundColour('YELLOW GREEN')       

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
