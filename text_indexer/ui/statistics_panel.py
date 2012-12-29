import wx
import os

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
        