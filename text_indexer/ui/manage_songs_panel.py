import wx
import os
from text_indexer.ui.add_song import AddSongDialog
from text_indexer.core.db import delete_song, export_db, import_db, session
from text_indexer.orm.song import Song
from text_indexer.orm import song

class ManageSongsPanel(wx.Panel):
    
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, -1)
        
    
        full_sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        text = "Songs List"
        text = wx.StaticText(self, -1, text, (20, 20))
        font = wx.Font(18, wx.SWISS, wx.NORMAL, wx.NORMAL, underline=True)
        text.SetFont(font)
        
        song_list = [s.name for s in Song.get_songs()]
        
        self.lb1 = wx.ListBox(self, 60, (50, 100), (150, 200), song_list, wx.LB_SINGLE)
        self.Bind(wx.EVT_LISTBOX, self.EvtListBox, self.lb1)
        if len(self.lb1.Items) > 0:
            self.lb1.SetSelection(0)
            
        text = wx.StaticText(self, -1, "Song Writer", (250, 120))    
        self.song_writer_text = wx.TextCtrl(self, -1, "", (250, 150), style=wx.TE_READONLY)
        
        text = wx.StaticText(self, -1, "Song Performer", (250, 220))
        self.song_performer_text = wx.TextCtrl(self, -1, "", (250, 250), style=wx.TE_READONLY)
        
        btn1 = wx.Button(self, -1, "Import song", (400, 150))
        self.Bind(wx.EVT_BUTTON, self.OnAddSong, btn1) 
        
        btn2 = wx.Button(self, -1, "Remove song", (400, 210))
        self.Bind(wx.EVT_BUTTON, self.OnRemoveSong, btn2)
        
        btn3 = wx.Button(self, -1, "Show song", (400, 270))
        self.Bind(wx.EVT_BUTTON, self.showSong, btn3)  
         
        sizer.Add(self.lb1, 0)
        sizer.Add(btn1, 1)
        sizer.Add(btn2, 2)
        sizer.Add(btn3, 3)
        
        btn4 = wx.Button(self, -1, "Export DB", (50, 400))
        self.Bind(wx.EVT_BUTTON, self.onExportDB, btn4)
        
        btn5 = wx.Button(self, -1, "Import DB", (150, 400))
        self.Bind(wx.EVT_BUTTON, self.onImportDB, btn5)    
        
        self.song_text_headline = wx.StaticText(self, -1, "The Song", (600, 50))
        font = wx.Font(12, wx.SWISS, wx.NORMAL, wx.NORMAL)
        self.song_text_headline.SetFont(font)
        self.t3 = wx.TextCtrl(self, -1, "", (600, 100), size=(500, 400), style=wx.TE_MULTILINE|wx.TE_READONLY)
        full_sizer.Add(sizer,0, wx.ALIGN_LEFT)
        full_sizer.Add(self.song_text_headline,1, wx.ALIGN_RIGHT)
        
        #self.SetSizer(sizer)
        
        
    def OnRemoveSong(self, evt):
        selection = self.lb1.GetSelection()
        if selection != -1:
            song = Song.get_songs(name=self.lb1.Items[selection])[0]
            self.lb1.Delete(selection)
            delete_song(song)
            
    def showSong(self, evt):
        selection = self.lb1.GetSelection()
        if selection != -1:
            song = Song.get_songs(name=self.lb1.Items[selection])[0]
            self.t3.SetValue(song.get_text())
            self.t3.SetScrollPos(1,1)
            #self.song_text = wx.StaticText(self, -1, song.get_text(), (500, 50))

        
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
    

        dlg.Destroy()
    
        
    def onImportDB(self, evt):

        # Create the dialog. In this case the current directory is forced as the starting
        # directory for the dialog, and no default file name is forced. This can easilly
        # be changed in your program. This is an 'open' dialog, and allows multitple
        # file selections as well.
        #
        # Finally, if the directory is changed in the process of getting files, this
        # dialog is set up to change the current working directory to the path chosen.
        dlg = wx.FileDialog(
            self, message="Choose a file",
            defaultDir=os.getcwd(), 
            defaultFile="",
            wildcard='*.xml',
            style=wx.OPEN | wx.CHANGE_DIR
            )

        # Show the dialog and retrieve the user response. If it is the OK response, 
        # process the data.
        if dlg.ShowModal() == wx.ID_OK:
            # This returns a Python list of files that were selected.
            path = dlg.GetPath()
            import_db(path)
            
            session.close_all()
            song_list = [s.name for s in Song.get_songs()]
            for s in song_list:
                self.lb1.Append(s)
            
        dlg.Destroy()
            
            

    def onExportDB(self, evt):

        # Create the dialog. In this case the current directory is forced as the starting
        # directory for the dialog, and no default file name is forced. This can easilly
        # be changed in your program. This is an 'save' dialog.
        #
        # Unlike the 'open dialog' example found elsewhere, this example does NOT
        # force the current working directory to change if the user chooses a different
        # directory than the one initially set.
        dlg = wx.FileDialog(
            self, message="Save file as ...", defaultDir=os.getcwd(), 
            defaultFile="", wildcard='*.xml', style=wx.SAVE
            )

        # This sets the default filter that the user will initially see. Otherwise,
        # the first filter in the list will be used by default.
        dlg.SetFilterIndex(2)

        # Show the dialog and retrieve the user response. If it is the OK response, 
        # process the data.
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            export_db(path)

            # Normally, at this point you would save your data using the file and path
            # data that the user provided to you, but since we didn't actually start
            # with any data to work with, that would be difficult.
            # 
            # The code to do so would be similar to this, assuming 'data' contains
            # the data you want to save:
            #
            # fp = file(path, 'w') # Create file anew
            # fp.write(data)
            # fp.close()
            #
            # You might want to add some error checking :-)
            #

        # Note that the current working dir didn't change. This is good since
        # that's the way we set it up.

        # Destroy the dialog. Don't do this until you are done with it!
        # BAD things can happen otherwise!
        dlg.Destroy()
            
    
    def EvtListBox(self, event):
        name = event.GetString()
        song = Song.get_songs(name=name)[0]
        self.song_writer_text.SetValue(song.writer)
        
        self.song_performer_text.SetValue(song.performer)
        
        
        

