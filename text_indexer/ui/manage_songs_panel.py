import wx
import os

class ManageSongsPanel(wx.Panel):
    
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, -1)
    
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        text = "Songs List"
        text = wx.StaticText(self, -1, text, (20, 20))
        font = wx.Font(18, wx.SWISS, wx.NORMAL, wx.NORMAL, underline=True)
        text.SetFont(font)
        
        sampleList = [str(i) for i in range(5)]
        
        self.lb1 = wx.ListBox(self, 60, (100, 100), (150, 200), sampleList, wx.LB_SINGLE)
        
        btn1 = wx.Button(self, -1, "Import song", (300, 150))
        self.Bind(wx.EVT_BUTTON, self.OnImportSong, btn1) 
        
        btn2 = wx.Button(self, -1, "Remove song", (300, 210))
        self.Bind(wx.EVT_BUTTON, self.OnRemoveSong, btn2) 
         
        sizer.Add(self.lb1, 0)
        sizer.Add(btn1, 0)
        sizer.Add(btn2, 0)
        
        #self.SetSizer(sizer)
        
        
    def OnRemoveSong(self, evt):
        selection = self.lb1.GetSelection()
        if selection != -1:
            self.lb1.Delete(selection)
        print selection
    
    def OnImportSong(self, evt):
        dlg = wx.FileDialog(
                            self, message="Choose a file",
                            defaultDir=os.getcwd(), 
                            defaultFile="",
                            style=wx.OPEN | wx.CHANGE_DIR
                            )

        # Show the dialog and retrieve the user response. If it is the OK response, 
        # process the data.
        if dlg.ShowModal() == wx.ID_OK:
            # This returns a Python list of files that were selected.
            path = dlg.GetPath()

            self.lb1.Append(os.path.basename(path).split('.')[0])
            
            # TODO: add load file here

        dlg.Destroy()  