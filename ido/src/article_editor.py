#Boa:Frame:article_frame
NO = 5104
YES = 5103

import wx
from funcs import *
from db import MAX_NUM_OF_WRITERS_PER_ARTICLE
import os
newspapers = list(get_all_newspapers())
categoriess = list(get_all_categories())
writers = list(get_all_writers())
cur_newspaper_num = -1
cur_category_num = -1
cur_writer_num = -1

[wxID_ARTICLE_FRAME, wxID_ARTICLE_FRAMEADD_CATEGORY_BUTTON, 
 wxID_ARTICLE_FRAMEADD_NEWSPAPER_BUTTON, wxID_ARTICLE_FRAMEADD_WRITER_BUTTON, 
 wxID_ARTICLE_FRAMEARTICLE_PATH_TEXT, wxID_ARTICLE_FRAMEARTICLE_TITLE_TEXT, 
 wxID_ARTICLE_FRAMEBROWSE_BUTTON, wxID_ARTICLE_FRAMECANCEL_BUTTON, 
 wxID_ARTICLE_FRAMECATEGORY_LIST, wxID_ARTICLE_FRAMEDATEPICKERCTRL1, 
 wxID_ARTICLE_FRAMEDELETE_CATEGORY_BUTTON, 
 wxID_ARTICLE_FRAMEDELETE_NEWSPAPER_BUTTON, 
 wxID_ARTICLE_FRAMEDELETE_WRITER_BUTTON, wxID_ARTICLE_FRAMENEWSPAPERS_LIST, 
 wxID_ARTICLE_FRAMENEWS_WRITER_ID_TEXT, wxID_ARTICLE_FRAMENEW_CATEGORY_TEXT, 
 wxID_ARTICLE_FRAMENEW_NEWSPAPER_TEXT, wxID_ARTICLE_FRAMEOK_BUTTON, 
 wxID_ARTICLE_FRAMEPAGE_NUMBER_TEXT, wxID_ARTICLE_FRAMEPANEL1, 
 wxID_ARTICLE_FRAMEPUBLISH_DATE, wxID_ARTICLE_FRAMESTATICTEXT1, 
 wxID_ARTICLE_FRAMESTATICTEXT10, wxID_ARTICLE_FRAMESTATICTEXT2, 
 wxID_ARTICLE_FRAMESTATICTEXT3, wxID_ARTICLE_FRAMESTATICTEXT4, 
 wxID_ARTICLE_FRAMESTATICTEXT5, wxID_ARTICLE_FRAMESTATICTEXT6, 
 wxID_ARTICLE_FRAMESTATICTEXT7, wxID_ARTICLE_FRAMESTATICTEXT8, 
 wxID_ARTICLE_FRAMESTATICTEXT9, wxID_ARTICLE_FRAMEWRITERS_LIST, 
 wxID_ARTICLE_FRAMEWRITER_NAME_TEXT, 
] = [wx.NewId() for _init_ctrls in range(33)]



def question(qu):
    return wx.MessageDialog(None, qu, 'Concordentation', wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION).ShowModal()

def error_msg(msg):
    wx.MessageDialog(None, msg, 'Error', wx.OK | wx.ICON_EXCLAMATION).ShowModal()
    
class article_frame(wx.Dialog):
    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Dialog.__init__(self, id=wxID_ARTICLE_FRAME, name='article_frame',
              parent=prnt, pos=wx.Point(410, 186), size=wx.Size(401, 632),
              style=wx.DEFAULT_FRAME_STYLE, title='Article')
        self.SetClientSize(wx.Size(385, 594))

        self.panel1 = wx.Panel(id=wxID_ARTICLE_FRAMEPANEL1, name='panel1',
              parent=self, pos=wx.Point(0, 0), size=wx.Size(385, 594),
              style=wx.TAB_TRAVERSAL)

        self.staticText1 = wx.StaticText(id=wxID_ARTICLE_FRAMESTATICTEXT1,
              label='Article title:', name='staticText1', parent=self.panel1,
              pos=wx.Point(16, 16), size=wx.Size(56, 13), style=0)

        self.article_title_text = wx.TextCtrl(id=wxID_ARTICLE_FRAMEARTICLE_TITLE_TEXT,
              name='article_title_text', parent=self.panel1, pos=wx.Point(88,
              16), size=wx.Size(280, 21), style=0, value='')

        self.staticText2 = wx.StaticText(id=wxID_ARTICLE_FRAMESTATICTEXT2,
              label='Newspaper:', name='staticText2', parent=self.panel1,
              pos=wx.Point(16, 48), size=wx.Size(59, 13), style=0)

        self.newspapers_list = wx.ListBox(choices=[],
              id=wxID_ARTICLE_FRAMENEWSPAPERS_LIST, name='newspapers_list',
              parent=self.panel1, pos=wx.Point(88, 48), size=wx.Size(200, 63),
              style=0)
        self.newspapers_list.Bind(wx.EVT_LISTBOX, self.OnNewspapers_listListbox,
              id=wxID_ARTICLE_FRAMENEWSPAPERS_LIST)

        self.delete_newspaper_button = wx.Button(id=wxID_ARTICLE_FRAMEDELETE_NEWSPAPER_BUTTON,
              label='delete', name='delete_newspaper_button',
              parent=self.panel1, pos=wx.Point(296, 88), size=wx.Size(75, 23),
              style=0)
        self.delete_newspaper_button.Bind(wx.EVT_BUTTON,
              self.OnDelete_newspaper_buttonButton,
              id=wxID_ARTICLE_FRAMEDELETE_NEWSPAPER_BUTTON)

        self.new_newspaper_text = wx.TextCtrl(id=wxID_ARTICLE_FRAMENEW_NEWSPAPER_TEXT,
              name='new_newspaper_text', parent=self.panel1, pos=wx.Point(120,
              120), size=wx.Size(168, 21), style=0, value='')

        self.add_newspaper_button = wx.Button(id=wxID_ARTICLE_FRAMEADD_NEWSPAPER_BUTTON,
              label='add', name='add_newspaper_button', parent=self.panel1,
              pos=wx.Point(296, 120), size=wx.Size(75, 23), style=0)
        self.add_newspaper_button.Bind(wx.EVT_BUTTON,
              self.OnAdd_newspaper_buttonButton,
              id=wxID_ARTICLE_FRAMEADD_NEWSPAPER_BUTTON)

        self.staticText10 = wx.StaticText(id=wxID_ARTICLE_FRAMESTATICTEXT10,
              label='Page number:', name='staticText10', parent=self.panel1,
              pos=wx.Point(16, 152), size=wx.Size(68, 13), style=0)

        self.page_number_text = wx.TextCtrl(id=wxID_ARTICLE_FRAMEPAGE_NUMBER_TEXT,
              name='page_number_text', parent=self.panel1, pos=wx.Point(88,
              152), size=wx.Size(40, 21), style=0, value='')
        
        self.staticText3 = wx.StaticText(id=wxID_ARTICLE_FRAMESTATICTEXT3,
              label='Publish date:', name='staticText3', parent=self.panel1,
              pos=wx.Point(16, 176), size=wx.Size(63, 13), style=0)

        self.publish_date = wx.DatePickerCtrl(id=wxID_ARTICLE_FRAMEPUBLISH_DATE,
              name='publish_date', parent=self.panel1, pos=wx.Point(88, 176),
              size=wx.Size(96, 21), style=wx.DP_SHOWCENTURY)

        self.staticText4 = wx.StaticText(id=wxID_ARTICLE_FRAMESTATICTEXT4,
              label='Category:', name='staticText4', parent=self.panel1,
              pos=wx.Point(16, 200), size=wx.Size(50, 13), style=0)

        self.category_list = wx.ListBox(choices=[],
              id=wxID_ARTICLE_FRAMECATEGORY_LIST, name='category_list',
              parent=self.panel1, pos=wx.Point(88, 200), size=wx.Size(200, 63),
              style=0)
        self.category_list.Bind(wx.EVT_LISTBOX, self.OnCategory_listListbox,
              id=wxID_ARTICLE_FRAMECATEGORY_LIST)

        self.delete_category_button = wx.Button(id=wxID_ARTICLE_FRAMEDELETE_CATEGORY_BUTTON,
              label='delete', name='delete_category_button', parent=self.panel1,
              pos=wx.Point(296, 240), size=wx.Size(75, 23), style=0)
        self.delete_category_button.Bind(wx.EVT_BUTTON,
              self.OnDelete_category_buttonButton,
              id=wxID_ARTICLE_FRAMEDELETE_CATEGORY_BUTTON)

        self.new_category_text = wx.TextCtrl(id=wxID_ARTICLE_FRAMECATEGORY_LIST,
              name='new_category_text', parent=self.panel1, pos=wx.Point(128,
              272), size=wx.Size(160, 21), style=0, value='')

        self.add_category_button = wx.Button(id=wxID_ARTICLE_FRAMEADD_CATEGORY_BUTTON,
              label='add', name='add_category_button', parent=self.panel1,
              pos=wx.Point(296, 272), size=wx.Size(75, 23), style=0)
        self.add_category_button.Bind(wx.EVT_BUTTON,
              self.OnAdd_category_buttonButton,
              id=wxID_ARTICLE_FRAMEADD_CATEGORY_BUTTON)

        self.staticText5 = wx.StaticText(id=wxID_ARTICLE_FRAMESTATICTEXT5,
              label='Writers:', name='staticText5', parent=self.panel1,
              pos=wx.Point(16, 304), size=wx.Size(40, 13), style=0)

        self.writers_list = wx.CheckListBox(choices=[],
              id=wxID_ARTICLE_FRAMEWRITERS_LIST, name='writers_list',
              parent=self.panel1, pos=wx.Point(88, 304), size=wx.Size(200, 96),
              style=0)
        self.writers_list.Bind(wx.EVT_LISTBOX, self.OnWriters_listListbox,
              id=wxID_ARTICLE_FRAMEWRITERS_LIST)

        self.delete_writer_button = wx.Button(id=wxID_ARTICLE_FRAMEDELETE_WRITER_BUTTON,
              label='delete', name='delete_writer_button', parent=self.panel1,
              pos=wx.Point(296, 384), size=wx.Size(75, 23), style=0)
        self.delete_writer_button.Bind(wx.EVT_BUTTON,
              self.OnDelete_writer_buttonButton,
              id=wxID_ARTICLE_FRAMEDELETE_WRITER_BUTTON)

        self.staticText8 = wx.StaticText(id=wxID_ARTICLE_FRAMESTATICTEXT8,
              label='id:', name='staticText8', parent=self.panel1,
              pos=wx.Point(88, 424), size=wx.Size(13, 13), style=0)

        self.news_writer_id_text = wx.TextCtrl(id=wxID_ARTICLE_FRAMENEWS_WRITER_ID_TEXT,
              name='news_writer_id_text', parent=self.panel1, pos=wx.Point(128,
              416), size=wx.Size(160, 21), style=0, value='')

        self.staticText6 = wx.StaticText(id=wxID_ARTICLE_FRAMESTATICTEXT6,
              label='name:', name='staticText6', parent=self.panel1,
              pos=wx.Point(88, 440), size=wx.Size(31, 13), style=0)

        self.writer_name_text = wx.TextCtrl(id=wxID_ARTICLE_FRAMEWRITER_NAME_TEXT,
              name='writer_name_text', parent=self.panel1, pos=wx.Point(128,
              440), size=wx.Size(160, 21), style=0, value='')

        self.staticText7 = wx.StaticText(id=wxID_ARTICLE_FRAMESTATICTEXT7,
              label='date of birth:', name='staticText7', parent=self.panel1,
              pos=wx.Point(88, 472), size=wx.Size(65, 13), style=0)

        self.datePickerCtrl1 = wx.DatePickerCtrl(id=wxID_ARTICLE_FRAMEDATEPICKERCTRL1,
              name='datePickerCtrl1', parent=self.panel1, pos=wx.Point(160,
              472), size=wx.Size(96, 21), style=wx.DP_SHOWCENTURY)

        self.add_writer_button = wx.Button(id=wxID_ARTICLE_FRAMEADD_WRITER_BUTTON,
              label='add', name='add_writer_button', parent=self.panel1,
              pos=wx.Point(296, 472), size=wx.Size(75, 23), style=0)
        self.add_writer_button.Bind(wx.EVT_BUTTON,
              self.OnAdd_writer_buttonButton,
              id=wxID_ARTICLE_FRAMEADD_WRITER_BUTTON)

        self.staticText9 = wx.StaticText(id=wxID_ARTICLE_FRAMESTATICTEXT9,
              label='Article path:', name='staticText9', parent=self.panel1,
              pos=wx.Point(16, 504), size=wx.Size(60, 13), style=0)
        self.staticText9.SetToolTipString('staticText9')

        self.article_path_text = wx.TextCtrl(id=wxID_ARTICLE_FRAMEARTICLE_PATH_TEXT,
              name='article_path_text', parent=self.panel1, pos=wx.Point(80,
              496), size=wx.Size(208, 21), style=0, value='')

        self.browse_button = wx.Button(id=wxID_ARTICLE_FRAMEBROWSE_BUTTON,
              label='Browse', name='browse_button', parent=self.panel1,
              pos=wx.Point(296, 496), size=wx.Size(75, 23), style=0)
        self.browse_button.Bind(wx.EVT_BUTTON, self.OnBrowse_buttonButton,
              id=wxID_ARTICLE_FRAMEBROWSE_BUTTON)
        
        self.ok_button = wx.Button(id=wxID_ARTICLE_FRAMEOK_BUTTON, label='OK',
              name='ok_button', parent=self.panel1, pos=wx.Point(200, 552),
              size=wx.Size(75, 23), style=0)
        self.ok_button.Bind(wx.EVT_BUTTON, self.OnOk_buttonButton,
              id=wxID_ARTICLE_FRAMEOK_BUTTON)

        self.cancel_button = wx.Button(id=wxID_ARTICLE_FRAMECANCEL_BUTTON,
              label='Cancel', name='cancel_button', parent=self.panel1,
              pos=wx.Point(296, 552), size=wx.Size(75, 23), style=0)
        self.cancel_button.Bind(wx.EVT_BUTTON, self.OnCancel_buttonButton,
              id=wxID_ARTICLE_FRAMECANCEL_BUTTON)

        

        

        

        
        
# values = (title, newspaper, page, date, writers, path)
    def __init__(self, parent, values = None):
        global cur_newspaper_num
        global cur_category_num
        global cur_writer_num
        cur_newspaper_num = -1
        cur_category_num = -1
        cur_writer_num = -1
        self._init_ctrls(parent)
        self.update_newspapers_list()
        self.update_categories_list()
        self.update_writers_list()
        self.values = ()
        if values != None:
            self.set_title(values[0])
            self.set_newspaper(values[1])
            self.set_page(values[2])
            self.set_publish_date(values[3])
            self.set_category(values[4])
            self.set_writers(values[5])
            self.set_path(values[6])
            self.article_id = values[7]
            self.in_edit = True
        else:
            self.in_edit = False
            
    def get_values(self):
        return self.values


###################### newspaper #####################
    def OnAdd_newspaper_buttonButton(self, event):
        global cur_newspaper_num
        if self.new_newspaper_text.Value == "":
            error_msg("You must select a newspaper name")
            return
        return_val = add_a_newspaper(self.new_newspaper_text.Value)
        if return_val != -1:
            self.update_newspapers_list()
            self.new_newspaper_text.Value = ""
            cur_newspaper_num = -1
        
    def OnDelete_newspaper_buttonButton(self, event):
        global cur_newspaper_num
        if cur_newspaper_num == -1:
            error_msg("No newspaper is selected")
            return
        if question("Are you sure you want to delete this newspaper and all its articles?") == YES:
            delete_newspaper(cur_newspaper_num)
            cur_newspaper_num = -1
            self.update_newspapers_list()
   

    def OnNewspapers_listListbox(self, event):
        global newspapers
        global cur_newspaper_num
        sel = event.GetSelection()
        newspaper_name = self.newspapers_list.Items[sel]
        newspaper_num = None
        for np in newspapers:
            if np["name"] == newspaper_name:
                newspaper_num = np["id"]
        if newspaper_num == None:
            raise "no such newspaper"
        cur_newspaper_num = newspaper_num


    def update_newspapers_list(self):
        global newspapers
        newspapers = list(get_all_newspapers())
        self.newspapers_list.Clear()
        for np in newspapers:
            self.newspapers_list.Append(np["name"])

        
###################### category #####################
    def OnAdd_category_buttonButton(self, event):
        global cur_category_num
        if self.new_category_text.Value == "":
            error_msg("You must select a category name")
            return
        return_val = add_a_category(self.new_category_text.Value)
        if return_val!=-1:
            self.update_categories_list()
            self.new_category_text.Value = ""
            cur_category_num = -1
        
    def OnDelete_category_buttonButton(self, event):
        global cur_category_num
        if cur_category_num == -1:
            error_msg("No category is selected")
            return
        if question("Are you sure you want to delete this category and all its articles?") == YES:
            delete_category(cur_category_num)
            cur_category_num = -1
            self.update_categories_list()


    def OnCategory_listListbox(self, event):
        global categories
        global cur_category_num
        sel = event.GetSelection()
        category_name = self.category_list.Items[sel]
        category_num = None
        for ct in categories:
            if ct["name"] == category_name:
                category_num = ct["id"]
        if category_num == None:
            raise "no such category"
        cur_category_num = category_num
        
    def update_categories_list(self):
        global categories
        categories = list(get_all_categories())
        self.category_list.Clear()
        for ct in categories:
            self.category_list.Append(ct["name"])
            
###################### writers #####################
    def OnAdd_writer_buttonButton(self, event):
        if self.news_writer_id_text.Value == "":
            error_msg("You must select a valid writer id")
            return
        if self.writer_name_text.Value == "":
            error_msg("You must select a writer name")
            return

        date = self.datePickerCtrl1.Value
        output_date = pydate_to_sqldate(date)
        return_val = add_a_writer(  self.news_writer_id_text.Value,
                                    self.writer_name_text.Value, output_date)
        if return_val == False:
            error_msg("A writer with that id already exists")
            return
        else:
            self.update_writers_list()
            self.writer_name_text.Value = ""
            self.news_writer_id_text.Value = ""
            cur_writer_num = -1
        
        
    def OnDelete_writer_buttonButton(self, event):
        global cur_writer_num
        global writers
        if cur_writer_num == -1:
            error_msg("No writer is selected")
            return
        if question("Are you sure you want to delete this writer and all his articles?") == YES:
            delete_writer(cur_writer_num)
            cur_writer_num = -1
            self.update_writers_list()        
        
    def OnWriters_listListbox(self, event):
        global writers
        global cur_writer_num
        sel = event.GetSelection()
        writer_name = self.writers_list.Items[sel]
        writer_num = None
        for wr in writers:
            if wr["name"] == writer_name:
                writer_num = wr["id"]
        if writer_num == None:
            raise "no such writer"
        cur_writer_num = writer_num

    def update_writers_list(self):
        global writers
        writers = list(get_all_writers())
        self.writers_list.Clear()
        for wr in writers:
            self.writers_list.Append(wr["name"])


    def OnOk_buttonButton(self, event):
        global MAX_NUM_OF_WRITERS_PER_ARTICLE
        global writers
        selected_writers = self.writers_list.GetChecked()
        selected_path = self.article_path_text.Value
        article_title = self.article_title_text.Value
        
        if article_title == "":
            error_msg("You must select an article title")
            return
        if cur_newspaper_num == -1:
            error_msg("You must select a newspaper")
            return
        if self.page_number_text.Value == "":
            error_msg("You must enter a page number")
            return
        if self.page_number_text.Value.isdigit() == False:
            error_msg("You must enter a numeric page number")
            return
        if len(selected_writers) > MAX_NUM_OF_WRITERS_PER_ARTICLE:
            error_msg("You can select %d maximum writers" % (MAX_NUM_OF_WRITERS_PER_ARTICLE))
            return
        if cur_category_num == -1:
            error_msg("You must select a category")
            return
        if len(selected_writers) == 0:
            error_msg("You must select at least one writer")
            return
        if selected_path == "":
            error_msg("You must select the article's file")
            return
        if False == os.access(selected_path, os.F_OK):
            error_msg("Article file doesn't exists")
            return
        
        publish_date = pydate_to_sqldate(self.publish_date.Value)
    
        writers_output = ""
        for wr in selected_writers:
            if writers_output != "":
                writers_output += ","
            writers_output += writers[wr]["id"]
        self.values = (article_title, selected_path, cur_newspaper_num,
                       int(self.page_number_text.Value), publish_date,
                       writers_output, cur_category_num)
        if self.in_edit:
            delete_article(self.article_id)
        self.Close()

    def OnCancel_buttonButton(self, event):
        self.Close()

    def OnBrowse_buttonButton(self, event):
        dlgs = wx.FileDialog(self, message="Select an article...", style=wx.OPEN)
        if dlgs.ShowModal() == wx.ID_OK:
            self.article_path_text.Value = dlgs.GetPath()
            
    def set_title(self, title):
        self.article_title_text.Value = title
            
    def set_newspaper(self, np):
        global cur_newspaper_num
        cur_newspaper_num = np
        for i in xrange(len(newspapers)):
            if newspapers[i]["id"] == np:
                cur_newspaper = np
                self.newspapers_list.Selection = i
                return True
        return False

    def set_page(self, num):
        self.page_number_text.Value = str(num)

    def set_publish_date(self, date_str):
        l = str(date_str).split("-")
        date = wx.DateTimeFromDMY(int(l[2]), int(l[1]) - 1, int(l[0]))
        self.publish_date.SetValue(date)
        
    def set_category(self, ct):
        global cur_category_num
        cur_category_num = ct
        for i in xrange(len(categories)):
            if categories[i]["id"] == ct:
                cur_category = ct
                self.category_list.Selection = i
                return True
        return False

    def set_writers(self, writers_list):
        sel_writers = []
        for i in xrange(len(writers)):
            if writers[i]["id"] in writers_list:
                sel_writers.append(i)
        self.writers_list.SetChecked(tuple(sel_writers))

    def set_path(self, path):
        self.article_path_text.SetValue(path)
