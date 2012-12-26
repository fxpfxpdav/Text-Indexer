import wx
import os
from text_indexer.ui.add_song import AddSongDialog
from text_indexer.core.db import delete_song
from text_indexer.orm.song import Song

class ManageSongsPanel(wx.Panel):
    
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, -1)
        
    
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        text = "Songs List"
        text = wx.StaticText(self, -1, text, (20, 20))
        font = wx.Font(18, wx.SWISS, wx.NORMAL, wx.NORMAL, underline=True)
        text.SetFont(font)
        
        song_list = [s.name for s in Song.get_songs()]
        
        self.lb1 = wx.ListBox(self, 60, (100, 100), (150, 200), song_list, wx.LB_SINGLE)
        
        btn1 = wx.Button(self, -1, "Import song", (300, 150))
        self.Bind(wx.EVT_BUTTON, self.OnAddSong, btn1) 
        
        btn2 = wx.Button(self, -1, "Remove song", (300, 210))
        self.Bind(wx.EVT_BUTTON, self.OnRemoveSong, btn2) 
         
        sizer.Add(self.lb1, 0)
        sizer.Add(btn1, 0)
        sizer.Add(btn2, 0)
        
        #self.SetSizer(sizer)
        
        
    def OnRemoveSong(self, evt):
        selection = self.lb1.GetSelection()
        if selection != -1:
            song = Song.get_songs(name=self.lb1.Items[selection])[0]
            self.lb1.Delete(selection)
            delete_song(song)
        
    def OnAddSong(self, evt):
        useMetal = False
        if 'wxMac' in wx.PlatformInfo:
            useMetal = self.cb.IsChecked()
            
        dlg = AddSongDialog(self, -1, "Import Song", size=(350, 200),
                         #style=wx.CAPTION | wx.SYSTEM_MENU | wx.THICK_FRAME,
                         style=wx.DEFAULT_DIALOG_STYLE, # & ~wx.CLOSE_BOX,
                         useMetal=useMetal,
                         )
        dlg.CenterOnScreen()

        # this does not return until the dialog is closed.
        val = dlg.ShowModal()
    
        if val == wx.ID_OK:
            self.log.WriteText("You pressed OK\n")
        else:
            self.log.WriteText("You pressed Cancel\n")

        dlg.Destroy()
    
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