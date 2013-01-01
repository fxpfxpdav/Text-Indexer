'''

@author: Oren
'''
import  wx
import os
from text_indexer.core.file_importer import FileImporter
from text_indexer.orm.relation import Relation

#---------------------------------------------------------------------------
# Create and set a help provider.  Normally you would do this in
# the app's OnInit as it must be done before any SetHelpText calls.
provider = wx.SimpleHelpProvider()
wx.HelpProvider.Set(provider)

#---------------------------------------------------------------------------

class AddRelationDialog(wx.Dialog):
    def __init__(
            self, parent, ID, title, size=wx.DefaultSize, pos=wx.DefaultPosition, 
            style=wx.DEFAULT_DIALOG_STYLE,
            useMetal=False,
            ):
        
        self.name = ""
        self.first = ""
        self.second = ""
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

        label = wx.StaticText(self, -1, "Relation Details")
        sizer.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)

        box = wx.BoxSizer(wx.HORIZONTAL)

        label = wx.StaticText(self, -1, "Relation Name")
        box.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)

        self.name_text = wx.TextCtrl(self, -1, "", size=(80,-1))
        box.Add(self.name_text, 1, wx.ALIGN_CENTRE|wx.ALL, 5)
        

        sizer.Add(box, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
        

        box = wx.BoxSizer(wx.HORIZONTAL)

        label = wx.StaticText(self, -1, "First word")
        box.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)

        self.first_text = wx.TextCtrl(self, -1, "", size=(80,-1))
        box.Add(self.first_text, 1, wx.ALIGN_CENTRE|wx.ALL, 5)
        
        label = wx.StaticText(self, -1, "Second word")
        box.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)

        self.second_text = wx.TextCtrl(self, -1, "", size=(80,-1))
        box.Add(self.second_text, 1, wx.ALIGN_CENTRE|wx.ALL, 5)


        sizer.Add(box, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
        

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
        self.Bind(wx.EVT_BUTTON, self.addRelation, btn)

        btn = wx.Button(self, wx.ID_CANCEL)
        btn.SetHelpText("The Cancel button cancels the dialog. (Cool, huh?)")
        btnsizer.AddButton(btn)
        btnsizer.Realize()

        sizer.Add(btnsizer, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)

        self.SetSizer(sizer)
        sizer.Fit(self)
        
    def addRelation(self, evt):
        
        name = self.name_text.Value
        first = self.first_text.Value
        second = self.second_text.Value
        grid = self.parent.relations_grid
        grid.InsertRows(grid.NumberRows)
        grid.SetCellValue(grid.NumberRows-1,0, first)
        grid.SetCellValue(grid.NumberRows-1,1, second)
        grid.SetCellValue(grid.NumberRows-1,2, name)
        grid.Refresh()
        
        Relation.add_relation(name, first, second)
        evt.EventObject.Parent.Destroy()
        

        
        
        
        
        

