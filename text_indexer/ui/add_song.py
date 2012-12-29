'''

@author: Oren
'''
import  wx
import os
from text_indexer.core.file_importer import FileImporter

#---------------------------------------------------------------------------
# Create and set a help provider.  Normally you would do this in
# the app's OnInit as it must be done before any SetHelpText calls.
provider = wx.SimpleHelpProvider()
wx.HelpProvider.Set(provider)

#---------------------------------------------------------------------------

class AddSongDialog(wx.Dialog):
    def __init__(
            self, parent, ID, title, size=wx.DefaultSize, pos=wx.DefaultPosition, 
            style=wx.DEFAULT_DIALOG_STYLE,
            useMetal=False,
            ):
        
        self.name = ""
        self.writer = ""
        self.performer = ""
        self.path = ""
        self.parent = parent

        # Instead of calling wx.Dialog.__init__ we precreate the dialog
        # so we can set an extra style that must be set before
        # creation, and then we create the GUI object using the Create
        # method.
        pre = wx.PreDialog()
        pre.SetExtraStyle(wx.DIALOG_EX_CONTEXTHELP)
        pre.Create(parent, ID, title, pos, size, style)

        # This next step is the most important, it turns this Python
        # object into the real wrapper of the dialog (instead of pre)
        # as far as the wxPython extension is concerned.
        self.PostCreate(pre)

        # This extra style can be set after the UI object has been created.
        if 'wxMac' in wx.PlatformInfo and useMetal:
            self.SetExtraStyle(wx.DIALOG_EX_METAL)


        # Now continue with the normal construction of the dialog
        # contents
        sizer = wx.BoxSizer(wx.VERTICAL)

        label = wx.StaticText(self, -1, "Song Details")
        sizer.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)

        box = wx.BoxSizer(wx.HORIZONTAL)

        label = wx.StaticText(self, -1, "Song Name")
        box.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)

        self.name_text = wx.TextCtrl(self, -1, "", size=(80,-1))
        box.Add(self.name_text, 1, wx.ALIGN_CENTRE|wx.ALL, 5)
        
        btn1 = wx.Button(self, -1, "Choose song", (300, 150))
        self.Bind(wx.EVT_BUTTON, self.chooseFile, btn1)
#        box.Add(btn1, 2, wx.ALIGN_CENTRE|wx.ALL, 5) 

        sizer.Add(box, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
        

        box = wx.BoxSizer(wx.HORIZONTAL)

        label = wx.StaticText(self, -1, "Song Writer")
        box.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)

        self.writer_text = wx.TextCtrl(self, -1, "", size=(80,-1))
        box.Add(self.writer_text, 1, wx.ALIGN_CENTRE|wx.ALL, 5)
        
        label = wx.StaticText(self, -1, "Song Performer")
        box.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)

        self.performer_text = wx.TextCtrl(self, -1, "", size=(80,-1))
        box.Add(self.performer_text, 1, wx.ALIGN_CENTRE|wx.ALL, 5)


        sizer.Add(box, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
        
        sizer.Add(btn1, 2, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)

        line = wx.StaticLine(self, -1, size=(20,-1), style=wx.LI_HORIZONTAL)
        sizer.Add(line, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.RIGHT|wx.TOP, 5)

        btnsizer = wx.StdDialogButtonSizer()
        
        if wx.Platform != "__WXMSW__":
            btn = wx.ContextHelpButton(self)
            btnsizer.AddButton(btn)
        
        btn = wx.Button(self, wx.ID_OK)
        btn.SetHelpText("The OK button completes the dialog")
        btn.SetDefault()
        btnsizer.AddButton(btn)
        self.Bind(wx.EVT_BUTTON, self.addSong, btn)

        btn = wx.Button(self, wx.ID_CANCEL)
        btn.SetHelpText("The Cancel button cancels the dialog. (Cool, huh?)")
        btnsizer.AddButton(btn)
        btnsizer.Realize()

        sizer.Add(btnsizer, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)

        self.SetSizer(sizer)
        sizer.Fit(self)
        
    def addSong(self, evt):
        
        name = self.name_text.Value
        writer = self.writer_text.Value
        performer = self.performer_text.Value
        path = self.path
        
        FileImporter().import_file(name, writer, performer, path)
        self.parent.lb1.Append(name)
        evt.EventObject.Parent.Destroy()

        
        
        
        
        
    def chooseFile(self, evt):
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
            self.path = dlg.GetPath() 
            
            # TODO: add load file here

        dlg.Destroy()  

#---------------------------------------------------------------------------

class TestPanel(wx.Panel):
    def __init__(self, parent, log):
        self.log = log
        wx.Panel.__init__(self, parent, -1)

        b = wx.Button(self, -1, "Create and Show a custom Dialog", (50,50))
        self.Bind(wx.EVT_BUTTON, self.OnButton, b)

        if 'wxMac' in wx.PlatformInfo:
            self.cb = wx.CheckBox(self, -1, "Set Metal appearance", (50,90))
            

    def OnButton(self, evt):
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