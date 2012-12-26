import wx
import os

class AnalysisPanel(wx.Panel):
    
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, -1)
        
        sampleList = [str(i) for i in range(5)]
        self.lb1 = wx.ListBox(self, 60, (100, 50), (200, 400), sampleList, wx.LB_EXTENDED)
        
        btn1 = wx.Button(self, -1, "Show words", (350, 100))
        #self.Bind(wx.EVT_BUTTON, self.OnImportSong, btn1) 
        
        self.lb2 = wx.ListBox(self, 70, (450, 50), (90, 400), sampleList, wx.LB_SINGLE)
        
        btn2 = wx.Button(self, -1, "Show context", (600, 100))
        #self.Bind(wx.EVT_BUTTON, self.OnImportSong, btn1) 
        
        t3 = wx.TextCtrl(self, -1,
                        "Here is a looooooooooooooong line of text set in the control.\n\n"
                        "The quick brown fox jumped over the lazy dog...", (850, 50),
                       size=(400, 400), style=wx.TE_MULTILINE|wx.TE_PROCESS_ENTER)
        
        