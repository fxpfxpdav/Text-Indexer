import wx
import os

import  wx.grid

class WordsIndexPanel(wx.Panel):
    
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, -1)
        
        self.grid = wx.grid.Grid(self, -1, (100, 50), (1200, 400))
        
        self.grid.CreateGrid(100000, 4)
        
        self.grid.SetColSize(0, 300)
        self.grid.SetColSize(1, 300)
        self.grid.SetColSize(2, 300)
        self.grid.SetColSize(3, 300)
        
        self.grid.SetColLabelValue(0, "Words")
        self.grid.SetColLabelValue(1, "Number in song")
        self.grid.SetColLabelValue(2, "Paragraph")
        self.grid.SetColLabelValue(3, "Number in paragraph")
                
        self.grid.SetCellValue(0, 0, "First cell")
        self.grid.SetCellValue(1, 1, "Another cell")
        self.grid.SetCellValue(2, 2, "Yet another cell")
        self.grid.SetCellValue(3, 3, "This cell is read-only")