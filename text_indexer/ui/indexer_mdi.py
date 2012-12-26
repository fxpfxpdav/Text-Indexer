
import wx
import wx.aui
import wx.lib.platebtn as pbtn
import pickle
import os
try:
    from agw import pybusyinfo as PBI
except ImportError: # if it's not there locally, try the wxPython lib.
    import wx.lib.agw.pybusyinfo as PBI


#----------------------------------------------------------------------

class ParentFrame(wx.aui.AuiMDIParentFrame):
    def __init__(self, parent):
        wx.aui.AuiMDIParentFrame.__init__(self, parent, -1,
                                          title="Stress",
                                          size=(1400,700),
                                          style=wx.DEFAULT_FRAME_STYLE)
        self.count = 0
        mb = self.MakeMenuBar()
        self.SetMenuBar(mb)
        self.CreateStatusBar()
        #self.Bind(wx.EVT_CLOSE)
        
    def MakeMenuBar(self):
        mb = wx.MenuBar()
        menu = wx.Menu()
        item = menu.Append(-1, "Import file\tCtrl-O")
        self.Bind(wx.EVT_MENU, self.OnImportFile, item)
        
        item = menu.Append(-1, "Text analysis\tCtrl-O")
        self.Bind(wx.EVT_MENU, self.OnTextAnalysis, item)
             
        item = menu.Append(-1, "Close")
        self.Bind(wx.EVT_MENU, self.OnDoClose, item)
        mb.Append(menu, "&File")
        return mb
        
    def OnImportFile(self, evt):

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

            print path
            
            # TODO: add load file here

        dlg.Destroy()    
     
     
    def OnTextAnalysis(self, evt):
        self.count += 1
        child = ChildFrame(self, self.count, "Orders Stress")
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
    def __init__(self, parent, count, title):
        wx.aui.AuiMDIChildFrame.__init__(self, parent, -1,
                                         title=title)
        """
        mb = parent.MakeMenuBar()
        menu = wx.Menu()
        item = menu.Append(-1, "This is child %d's menu" % count)
        mb.Append(menu, title + " menu")
        self.SetMenuBar(mb)
        """
        
        p = OrderStressPanel(self, parent.campus_list)
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
