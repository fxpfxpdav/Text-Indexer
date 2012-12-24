#Boa:Dialog:instances_dialog

import wx
import wx.stc
from funcs import *

[wxID_INSTANCES_DIALOG, wxID_INSTANCES_DIALOGAPPEAR_NUM_LABEL, 
 wxID_INSTANCES_DIALOGCLOSE_BUTTON, wxID_INSTANCES_DIALOGCOL_LABEL, 
 wxID_INSTANCES_DIALOGNEXT_BUTTON, wxID_INSTANCES_DIALOGOPEN_ARTICLE_BUTTON, 
 wxID_INSTANCES_DIALOGPREV_BUTTON, wxID_INSTANCES_DIALOGROW_LABEL, 
 wxID_INSTANCES_DIALOGTEXTCTRL1, 
] = [wx.NewId() for _init_ctrls in range(9)]

class instances_dialog(wx.Dialog):
    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Dialog.__init__(self, id=wxID_INSTANCES_DIALOG,
              name='instances_dialog', parent=prnt, pos=wx.Point(589, 341),
              size=wx.Size(352, 148), style=wx.DEFAULT_DIALOG_STYLE,
              title='Instances')
        self.SetClientSize(wx.Size(336, 110))

        self.textCtrl1 = wx.TextCtrl(id=wxID_INSTANCES_DIALOGTEXTCTRL1,
              name='textCtrl1', parent=self, pos=wx.Point(16, 8),
              size=wx.Size(248, 64), style=wx.TE_MULTILINE|wx.TE_RICH2,
              value='')
        self.textCtrl1.SetEditable(False)

        self.prev_button = wx.Button(id=wxID_INSTANCES_DIALOGPREV_BUTTON,
              label='previous', name='prev_button', parent=self,
              pos=wx.Point(16, 80), size=wx.Size(72, 23), style=0)
        self.prev_button.Bind(wx.EVT_BUTTON, self.OnPrev_buttonButton,
              id=wxID_INSTANCES_DIALOGPREV_BUTTON)

        self.next_button = wx.Button(id=wxID_INSTANCES_DIALOGNEXT_BUTTON,
              label='next', name='next_button', parent=self, pos=wx.Point(96,
              80), size=wx.Size(72, 23), style=0)
        self.next_button.Bind(wx.EVT_BUTTON, self.OnNext_buttonButton,
              id=wxID_INSTANCES_DIALOGNEXT_BUTTON)

        self.open_article_button = wx.Button(id=wxID_INSTANCES_DIALOGOPEN_ARTICLE_BUTTON,
              label='open article', name='open_article_button', parent=self,
              pos=wx.Point(176, 80), size=wx.Size(72, 23), style=0)
        self.open_article_button.Bind(wx.EVT_BUTTON,
              self.OnOpen_article_buttonButton,
              id=wxID_INSTANCES_DIALOGOPEN_ARTICLE_BUTTON)

        self.close_button = wx.Button(id=wxID_INSTANCES_DIALOGCLOSE_BUTTON,
              label='close', name='close_button', parent=self, pos=wx.Point(256,
              80), size=wx.Size(72, 23), style=0)
        self.close_button.Bind(wx.EVT_BUTTON, self.OnClose_buttonButton,
              id=wxID_INSTANCES_DIALOGCLOSE_BUTTON)

        self.row_label = wx.StaticText(id=wxID_INSTANCES_DIALOGROW_LABEL,
              label='row:', name='row_label', parent=self, pos=wx.Point(272, 8),
              size=wx.Size(23, 13), style=0)

        self.col_label = wx.StaticText(id=wxID_INSTANCES_DIALOGCOL_LABEL,
              label='col:', name='col_label', parent=self, pos=wx.Point(272,
              24), size=wx.Size(18, 13), style=0)

        self.appear_num_label = wx.StaticText(id=wxID_INSTANCES_DIALOGAPPEAR_NUM_LABEL,
              label='', name='appear_num_label', parent=self, pos=wx.Point(272,
              56), size=wx.Size(0, 13), style=0)

    def __init__(self, parent):
        self._init_ctrls(parent)

    def OnPrev_buttonButton(self, event):
        self.cur_appear = (self.cur_appear - 1) % len(self.appear_list)
        self.update_fields()

    def OnNext_buttonButton(self, event):
        self.cur_appear = (self.cur_appear + 1) % len(self.appear_list)
        self.update_fields()

    def OnClose_buttonButton(self, event):
        self.Close()
        
    def set_text(self, text, start, end):
        self.textCtrl1.SetValue(text)
        points = self.textCtrl1.GetFont().GetPointSize()
        f = wx.Font(points + 3, wx.ROMAN, wx.ITALIC, wx.BOLD, True)
        if start < end and start >= 0 and end < len(text):
            self.textCtrl1.SetStyle(start, end, wx.TextAttr("blue", wx.NullColour, f))
            self.textCtrl1.SetSelection(0,1)
            self.textCtrl1.SetSelection(0,0)
        
    def OnOpen_article_buttonButton(self, event):
        os.system("notepad " + self.article_path)
    
    def init_text(self, article_id, word):
        article_path = get_article_path(article_id)
        RANGE = 100
        appears = get_specific_word_in_article(word, article_id)
        self.appear_list = []
        self.article_path = article_path
        article_text = open(article_path, "r").read()
        for a in appears:
            start = max(a["offset"] - RANGE, 0)
            end = min(a["offset"] + RANGE, len(article_text) - 1)
            text = "..." + article_text[start:end] + "..."
            mark_start = a["offset"] - start + 3
            self.appear_list.append((text, mark_start, mark_start + a["full_len"], a["row"], a["col"]))
        if len(self.appear_list) == 0:
            raise Exception("update text error")
        if len(self.appear_list) == 1:
            self.next_button.Disable()
            self.prev_button.Disable()
            self.cur_appear = 0
            self.update_fields()
        else:
            self.next_button.Enable()
            self.prev_button.Enable()
            self.cur_appear = 0
            self.update_fields()
            
    def update_fields(self):
        (text, mark_start, mark_end, row_num, col_num) = self.appear_list[self.cur_appear]
        self.set_text(text, mark_start, mark_end)
        self.row_label.SetLabel("row: " + str(row_num))
        self.col_label.SetLabel("col: " + str(col_num))    
        self.appear_num_label.SetLabel("%d/%d" % (self.cur_appear + 1, len(self.appear_list)))

