#Boa:Frame:Frame1

import wx
import wx.grid
from wx.lib.anchors import LayoutAnchors
from article_editor import article_frame
from preview import instances_dialog
from db2xml import *
from statistic_dialog import Dialog1
from funcs import *
articles = list(get_all_articles())
cur_article_id = -1
groups = list(get_all_groups())
cur_group_num = -1
relations = list(get_all_relations())
cur_relation_num = -1
newspapers = list(get_all_newspapers())
cur_newspaper_num = -1
categories = list(get_all_categories())
cur_category_num = -1
writers = list(get_all_writers())
cur_writer_num = -1
phrases = list(get_all_phrases())

NO = 5104
YES = 5103
        
def question(qu):
    return wx.MessageDialog(None, qu, 'Concordentation', wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION).ShowModal()

def error_msg(msg):
    wx.MessageDialog(None, msg, 'Error', wx.OK | wx.ICON_EXCLAMATION).ShowModal()
def info_msg(msg):
    wx.MessageDialog(None, msg, 'Concordantation', wx.OK | wx.ICON_INFORMATION).ShowModal()


def create(parent):
    return Frame1(parent)

[wxID_FRAME1, wxID_FRAME1ADD_ART_BUTTON, wxID_FRAME1ADD_NEW_RELATED_COUPLE, 
 wxID_FRAME1ADD_PHRASE_BUTTON, wxID_FRAME1APPLY_FILTER_BUTTON, 
 wxID_FRAME1ARTICLES_LIST_BOX, wxID_FRAME1ART_CATEGORY, 
 wxID_FRAME1ART_NEWSPAPER, wxID_FRAME1ART_PUBLISH_DATE, wxID_FRAME1ART_TITLE, 
 wxID_FRAME1BOTH_RADIO, wxID_FRAME1CATEGORY_CHECK, wxID_FRAME1CATEGORY_LIST, 
 wxID_FRAME1COL_TEXT, wxID_FRAME1CONTAINING_CHECK, wxID_FRAME1CONTAINING_TEXT, 
 wxID_FRAME1DELETE_ART_BUTTON, wxID_FRAME1DELETE_GROUP_BUTTON, 
 wxID_FRAME1DELETE_MEMBER_BUTTON, wxID_FRAME1DELETE_PHRASE_BUTTON, 
 wxID_FRAME1DELETE_RELATED_COUPLE, wxID_FRAME1DELETE_RELATION_BUTTON, 
 wxID_FRAME1DESELECT_ALL_BUTTON, wxID_FRAME1EDIT_BUTTON, 
 wxID_FRAME1ENCRYPT_BOX, wxID_FRAME1EXPORT_BROWSE_BUTTON, 
 wxID_FRAME1EXPORT_BUTTON, wxID_FRAME1EXPORT_PATH, wxID_FRAME1GROUPS_FRAME, 
 wxID_FRAME1GROUPS_LIST, wxID_FRAME1GROUP_NAME, 
 wxID_FRAME1IMPORT_BROWSE_BUTTON, wxID_FRAME1IMPORT_BUTTON, 
 wxID_FRAME1IMPORT_PATH, wxID_FRAME1LINE_TEXT, 
 wxID_FRAME1MAX_PAGE_FILTER_TEXT, wxID_FRAME1MAX_PUBLISH_DATE, 
 wxID_FRAME1MIN_PAGE_FILTER_TEXT, wxID_FRAME1MIN_PUBLISH_DATE, 
 wxID_FRAME1NEWSPAPER_FILTER_CHECK, wxID_FRAME1NEWSPAPER_FILTER_LIST, 
 wxID_FRAME1NEW_GROUP_BUTTON, wxID_FRAME1NEW_GROUP_NAME, 
 wxID_FRAME1NEW_MEMBER, wxID_FRAME1NEW_MEMBER_BUTTON, 
 wxID_FRAME1NEW_PHRASE_TEXT, wxID_FRAME1NEW_RELATION_BUTTON, 
 wxID_FRAME1NEW_RELATION_NAME, wxID_FRAME1PAGE_FILTER_CHECK, 
 wxID_FRAME1PAGE_NUM, wxID_FRAME1PANEL1, wxID_FRAME1PAR_TEXT, 
 wxID_FRAME1PASS_TEXT, wxID_FRAME1PHRASES_RADIO, wxID_FRAME1PHRASE_LIST, 
 wxID_FRAME1PUBLISH_DATE_CHECK, wxID_FRAME1RELATED_COUPLES_LIST, 
 wxID_FRAME1RELATIONS_FRAME, wxID_FRAME1RELATIONS_LIST, 
 wxID_FRAME1RELATION_WORD_1, wxID_FRAME1RELATION_WORD_2, 
 wxID_FRAME1RESET_BUTTON, wxID_FRAME1ROW_TEXT, wxID_FRAME1SELECTED_GROUP_BOX, 
 wxID_FRAME1SELECT_ALL_BUTTON, wxID_FRAME1SHOW_BUTTON, 
 wxID_FRAME1SHOW_STATISTIC_BUTTONS, wxID_FRAME1STATICBOX1, 
 wxID_FRAME1STATICBOX2, wxID_FRAME1STATICBOX3, wxID_FRAME1STATICBOX4, 
 wxID_FRAME1STATICBOX5, wxID_FRAME1STATICBOX6, wxID_FRAME1STATICLINE1, 
 wxID_FRAME1STATICLINE2, wxID_FRAME1STATICTEXT1, wxID_FRAME1STATICTEXT10, 
 wxID_FRAME1STATICTEXT11, wxID_FRAME1STATICTEXT12, wxID_FRAME1STATICTEXT13, 
 wxID_FRAME1STATICTEXT14, wxID_FRAME1STATICTEXT15, wxID_FRAME1STATICTEXT16, 
 wxID_FRAME1STATICTEXT18, wxID_FRAME1STATICTEXT2, wxID_FRAME1STATICTEXT3, 
 wxID_FRAME1STATICTEXT4, wxID_FRAME1STATICTEXT5, wxID_FRAME1STATICTEXT6, 
 wxID_FRAME1STATICTEXT7, wxID_FRAME1STATICTEXT8, wxID_FRAME1STATICTEXT9, 
 wxID_FRAME1TITLE_FILTER_CHECK, wxID_FRAME1TITLE_FILTER_TEXT, 
 wxID_FRAME1UPDATE_WORDS_BUTTON, wxID_FRAME1WORDS_GRID, 
 wxID_FRAME1WORDS_IN_GROUP_LIST, wxID_FRAME1WORDS_RADIO, 
 wxID_FRAME1WRITERS_CHECK, wxID_FRAME1WRITERS_FILTER_LIST, 
 wxID_FRAME1WRITERS_LIST, 
] = [wx.NewId() for _init_ctrls in range(101)]

class Frame1(wx.Frame):
    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Frame.__init__(self, id=wxID_FRAME1, name='', parent=prnt,
              pos=wx.Point(9, 7), size=wx.Size(1037, 760),
              style=wx.DEFAULT_FRAME_STYLE, title='Concordance')
        self.SetClientSize(wx.Size(1021, 722))

        self.panel1 = wx.Panel(id=wxID_FRAME1PANEL1, name='panel1', parent=self,
              pos=wx.Point(0, 0), size=wx.Size(1021, 722),
              style=wx.TAB_TRAVERSAL)
        self.panel1.SetToolTipString('')

        self.staticBox1 = wx.StaticBox(id=wxID_FRAME1STATICBOX1,
              label='articles', name='staticBox1', parent=self.panel1,
              pos=wx.Point(24, 16), size=wx.Size(320, 704), style=0)

        self.articles_list_box = wx.CheckListBox(choices=[],
              id=wxID_FRAME1ARTICLES_LIST_BOX, name='articles_list_box',
              parent=self.panel1, pos=wx.Point(32, 32), size=wx.Size(184, 176),
              style=0)
        self.articles_list_box.Bind(wx.EVT_LISTBOX,
              self.OnArticles_list_boxListbox, id=wxID_FRAME1ARTICLES_LIST_BOX)

        self.update_words_button = wx.Button(id=wxID_FRAME1UPDATE_WORDS_BUTTON,
              label='update words', name='update_words_button',
              parent=self.panel1, pos=wx.Point(232, 32), size=wx.Size(75, 23),
              style=0)
        self.update_words_button.Bind(wx.EVT_BUTTON,
              self.OnUpdate_words_buttonButton,
              id=wxID_FRAME1UPDATE_WORDS_BUTTON)

        self.select_all_button = wx.Button(id=wxID_FRAME1SELECT_ALL_BUTTON,
              label='select all', name='select_all_button', parent=self.panel1,
              pos=wx.Point(232, 64), size=wx.Size(75, 23), style=0)
        self.select_all_button.Bind(wx.EVT_BUTTON,
              self.OnSelect_all_buttonButton, id=wxID_FRAME1SELECT_ALL_BUTTON)

        self.deselect_all_button = wx.Button(id=wxID_FRAME1DESELECT_ALL_BUTTON,
              label='deselect all', name='deselect_all_button',
              parent=self.panel1, pos=wx.Point(232, 96), size=wx.Size(75, 23),
              style=0)
        self.deselect_all_button.Bind(wx.EVT_BUTTON,
              self.OnDeselect_all_buttonButton,
              id=wxID_FRAME1DESELECT_ALL_BUTTON)

        self.edit_button = wx.Button(id=wxID_FRAME1EDIT_BUTTON, label='edit',
              name='edit_button', parent=self.panel1, pos=wx.Point(232, 128),
              size=wx.Size(75, 23), style=0)
        self.edit_button.Bind(wx.EVT_BUTTON, self.OnEdit_buttonButton,
              id=wxID_FRAME1EDIT_BUTTON)

        self.delete_art_button = wx.Button(id=wxID_FRAME1DELETE_ART_BUTTON,
              label='delete', name='delete_art_button', parent=self.panel1,
              pos=wx.Point(232, 160), size=wx.Size(75, 23), style=0)
        self.delete_art_button.Bind(wx.EVT_BUTTON,
              self.OnDelete_art_buttonButton, id=wxID_FRAME1DELETE_ART_BUTTON)

        self.add_art_button = wx.Button(id=wxID_FRAME1ADD_ART_BUTTON,
              label='add', name='add_art_button', parent=self.panel1,
              pos=wx.Point(232, 192), size=wx.Size(75, 23), style=0)
        self.add_art_button.Bind(wx.EVT_BUTTON, self.OnAdd_art_buttonButton,
              id=wxID_FRAME1ADD_ART_BUTTON)

        self.staticText1 = wx.StaticText(id=wxID_FRAME1STATICTEXT1,
              label='Article Title:', name='staticText1', parent=self.panel1,
              pos=wx.Point(32, 216), size=wx.Size(58, 13), style=0)

        self.art_title = wx.StaticText(id=wxID_FRAME1ART_TITLE, label='',
              name='art_title', parent=self.panel1, pos=wx.Point(96, 216),
              size=wx.Size(112, 16), style=0)
        self.art_title.SetMaxSize(wx.Size(120, 32))

        self.staticText3 = wx.StaticText(id=wxID_FRAME1STATICTEXT3,
              label='Newspaper:', name='staticText3', parent=self.panel1,
              pos=wx.Point(32, 232), size=wx.Size(59, 13), style=0)

        self.art_newspaper = wx.StaticText(id=wxID_FRAME1ART_NEWSPAPER,
              label='', name='art_newspaper', parent=self.panel1,
              pos=wx.Point(96, 232), size=wx.Size(88, 16), style=0)

        self.staticText5 = wx.StaticText(id=wxID_FRAME1STATICTEXT5,
              label='Page Number:', name='staticText5', parent=self.panel1,
              pos=wx.Point(32, 248), size=wx.Size(69, 13), style=0)

        self.page_num = wx.StaticText(id=wxID_FRAME1PAGE_NUM, label='',
              name='page_num', parent=self.panel1, pos=wx.Point(104, 248),
              size=wx.Size(32, 13), style=0)

        self.staticText2 = wx.StaticText(id=wxID_FRAME1STATICTEXT2,
              label='Publish Date:', name='staticText2', parent=self.panel1,
              pos=wx.Point(32, 264), size=wx.Size(64, 13), style=0)

        self.art_publish_date = wx.StaticText(id=wxID_FRAME1ART_PUBLISH_DATE,
              label='', name='art_publish_date', parent=self.panel1,
              pos=wx.Point(96, 264), size=wx.Size(64, 13), style=0)

        self.staticText4 = wx.StaticText(id=wxID_FRAME1STATICTEXT4,
              label='Category:', name='staticText4', parent=self.panel1,
              pos=wx.Point(32, 280), size=wx.Size(50, 13), style=0)

        self.writers_list = wx.ListBox(choices=[], id=wxID_FRAME1WRITERS_LIST,
              name='writers_list', parent=self.panel1, pos=wx.Point(88, 296),
              size=wx.Size(128, 32), style=0)

        self.staticText6 = wx.StaticText(id=wxID_FRAME1STATICTEXT6,
              label='Writers:', name='staticText6', parent=self.panel1,
              pos=wx.Point(32, 296), size=wx.Size(40, 13), style=0)

        self.art_category = wx.StaticText(id=wxID_FRAME1ART_CATEGORY, label='',
              name='art_category', parent=self.panel1, pos=wx.Point(88, 280),
              size=wx.Size(104, 16), style=0)

        self.staticBox2 = wx.StaticBox(id=wxID_FRAME1STATICBOX2, label='filter',
              name='staticBox2', parent=self.panel1, pos=wx.Point(40, 344),
              size=wx.Size(296, 368), style=0)

        self.title_filter_check = wx.CheckBox(id=wxID_FRAME1TITLE_FILTER_CHECK,
              label='Title contains:', name='title_filter_check',
              parent=self.panel1, pos=wx.Point(48, 368), size=wx.Size(88, 13),
              style=0)
        self.title_filter_check.SetValue(False)

        self.title_filter_text = wx.TextCtrl(id=wxID_FRAME1TITLE_FILTER_TEXT,
              name='title_filter_text', parent=self.panel1, pos=wx.Point(136,
              368), size=wx.Size(192, 24), style=0, value='')

        self.newspaper_filter_check = wx.CheckBox(id=wxID_FRAME1NEWSPAPER_FILTER_CHECK,
              label='Newspaper:', name='newspaper_filter_check',
              parent=self.panel1, pos=wx.Point(48, 400), size=wx.Size(72, 13),
              style=0)
        self.newspaper_filter_check.SetValue(False)

        self.newspaper_filter_list = wx.ListBox(choices=[],
              id=wxID_FRAME1NEWSPAPER_FILTER_LIST, name='newspaper_filter_list',
              parent=self.panel1, pos=wx.Point(136, 400), size=wx.Size(192, 40),
              style=0)
        self.newspaper_filter_list.Bind(wx.EVT_LISTBOX,
              self.OnNewspaper_filter_listListbox,
              id=wxID_FRAME1NEWSPAPER_FILTER_LIST)

        self.page_filter_check = wx.CheckBox(id=wxID_FRAME1PAGE_FILTER_CHECK,
              label='Page number between:', name='page_filter_check',
              parent=self.panel1, pos=wx.Point(48, 448), size=wx.Size(128, 13),
              style=0)
        self.page_filter_check.SetValue(False)

        self.min_page_filter_text = wx.TextCtrl(id=wxID_FRAME1MIN_PAGE_FILTER_TEXT,
              name='min_page_filter_text', parent=self.panel1, pos=wx.Point(184,
              448), size=wx.Size(32, 16), style=0, value='')

        self.staticText8 = wx.StaticText(id=wxID_FRAME1STATICTEXT8, label='and',
              name='staticText8', parent=self.panel1, pos=wx.Point(224, 448),
              size=wx.Size(19, 13), style=0)

        self.max_page_filter_text = wx.TextCtrl(id=wxID_FRAME1MAX_PAGE_FILTER_TEXT,
              name='max_page_filter_text', parent=self.panel1, pos=wx.Point(256,
              448), size=wx.Size(32, 16), style=0, value='')

        self.publish_date_check = wx.CheckBox(id=wxID_FRAME1PUBLISH_DATE_CHECK,
              label='Publish date between:', name='publish_date_check',
              parent=self.panel1, pos=wx.Point(48, 472), size=wx.Size(128, 13),
              style=0)
        self.publish_date_check.SetValue(False)

        self.min_publish_date = wx.DatePickerCtrl(id=wxID_FRAME1MIN_PUBLISH_DATE,
              name='min_publish_date', parent=self.panel1, pos=wx.Point(176,
              472), size=wx.Size(96, 21), style=wx.DP_SHOWCENTURY)
        self.min_publish_date.SetLabel('2010/07/10')
        self.min_publish_date.SetValue(wx.DateTimeFromDMY(10, 6, 2010, 0, 0, 0))

        self.staticText9 = wx.StaticText(id=wxID_FRAME1STATICTEXT9, label='and',
              name='staticText9', parent=self.panel1, pos=wx.Point(152, 496),
              size=wx.Size(19, 13), style=0)

        self.max_publish_date = wx.DatePickerCtrl(id=wxID_FRAME1MAX_PUBLISH_DATE,
              name='max_publish_date', parent=self.panel1, pos=wx.Point(176,
              496), size=wx.Size(96, 21), style=wx.DP_SHOWCENTURY)

        self.category_check = wx.CheckBox(id=wxID_FRAME1CATEGORY_CHECK,
              label='Category:', name='category_check', parent=self.panel1,
              pos=wx.Point(48, 520), size=wx.Size(70, 13), style=0)
        self.category_check.SetValue(False)

        self.category_list = wx.ListBox(choices=[], id=wxID_FRAME1CATEGORY_LIST,
              name='category_list', parent=self.panel1, pos=wx.Point(120, 520),
              size=wx.Size(208, 48), style=0)
        self.category_list.Bind(wx.EVT_LISTBOX, self.OnCategory_listListbox,
              id=wxID_FRAME1CATEGORY_LIST)

        self.writers_check = wx.CheckBox(id=wxID_FRAME1WRITERS_CHECK,
              label='Writers:', name='writers_check', parent=self.panel1,
              pos=wx.Point(48, 576), size=wx.Size(70, 13), style=0)
        self.writers_check.SetValue(False)

        self.writers_filter_list = wx.CheckListBox(choices=[],
              id=wxID_FRAME1WRITERS_FILTER_LIST, name='writers_filter_list',
              parent=self.panel1, pos=wx.Point(120, 576), size=wx.Size(208, 48),
              style=0)

        self.containing_check = wx.CheckBox(id=wxID_FRAME1CONTAINING_CHECK,
              label='Containing the words:', name='containing_check',
              parent=self.panel1, pos=wx.Point(48, 632), size=wx.Size(128, 16),
              style=0)
        self.containing_check.SetValue(False)

        self.staticText13 = wx.StaticText(id=wxID_FRAME1STATICTEXT13,
              label='(seperate with ,)', name='staticText13',
              parent=self.panel1, pos=wx.Point(64, 648), size=wx.Size(81, 13),
              style=0)

        self.containing_text = wx.TextCtrl(id=wxID_FRAME1CONTAINING_TEXT,
              name='containing_text', parent=self.panel1, pos=wx.Point(176,
              632), size=wx.Size(152, 40), style=0, value='')

        self.apply_filter_button = wx.Button(id=wxID_FRAME1APPLY_FILTER_BUTTON,
              label='apply', name='apply_filter_button', parent=self.panel1,
              pos=wx.Point(248, 680), size=wx.Size(75, 23), style=0)
        self.apply_filter_button.Bind(wx.EVT_BUTTON,
              self.OnApply_filter_buttonButton,
              id=wxID_FRAME1APPLY_FILTER_BUTTON)

        self.staticText10 = wx.StaticText(id=wxID_FRAME1STATICTEXT10,
              label='show:', name='staticText10', parent=self.panel1,
              pos=wx.Point(352, 24), size=wx.Size(30, 13), style=0)

        self.words_radio = wx.RadioButton(id=wxID_FRAME1WORDS_RADIO,
              label='words', name='words_radio', parent=self.panel1,
              pos=wx.Point(392, 24), size=wx.Size(56, 13), style=0)
        self.words_radio.SetValue(True)
        self.words_radio.Bind(wx.EVT_RADIOBUTTON, self.OnWords_radioRadiobutton,
              id=wxID_FRAME1WORDS_RADIO)

        self.phrases_radio = wx.RadioButton(id=wxID_FRAME1PHRASES_RADIO,
              label='phrases', name='phrases_radio', parent=self.panel1,
              pos=wx.Point(392, 40), size=wx.Size(56, 13), style=0)
        self.phrases_radio.Bind(wx.EVT_RADIOBUTTON,
              self.OnPhrases_buttonRadiobutton, id=wxID_FRAME1PHRASES_RADIO)

        self.both_radio = wx.RadioButton(id=wxID_FRAME1BOTH_RADIO, label='both',
              name='both_radio', parent=self.panel1, pos=wx.Point(392, 56),
              size=wx.Size(48, 13), style=0)
        self.both_radio.Bind(wx.EVT_RADIOBUTTON, self.OnBoth_radioRadiobutton,
              id=wxID_FRAME1BOTH_RADIO)

        self.staticBox5 = wx.StaticBox(id=wxID_FRAME1STATICBOX5,
              label='find by location and group', name='staticBox5',
              parent=self.panel1, pos=wx.Point(456, 16), size=wx.Size(320, 64),
              style=0)

        self.staticText7 = wx.StaticText(id=wxID_FRAME1STATICTEXT7,
              label='row:', name='staticText7', parent=self.panel1,
              pos=wx.Point(464, 32), size=wx.Size(23, 13), style=0)

        self.row_text = wx.TextCtrl(id=wxID_FRAME1ROW_TEXT, name='row_text',
              parent=self.panel1, pos=wx.Point(488, 32), size=wx.Size(24, 16),
              style=0, value='')

        self.staticText14 = wx.StaticText(id=wxID_FRAME1STATICTEXT14,
              label='col:', name='staticText14', parent=self.panel1,
              pos=wx.Point(464, 56), size=wx.Size(18, 13), style=0)

        self.col_text = wx.TextCtrl(id=wxID_FRAME1COL_TEXT, name='col_text',
              parent=self.panel1, pos=wx.Point(488, 56), size=wx.Size(24, 16),
              style=0, value='')

        self.staticText15 = wx.StaticText(id=wxID_FRAME1STATICTEXT15,
              label='sentence:', name='staticText15', parent=self.panel1,
              pos=wx.Point(520, 32), size=wx.Size(49, 13), style=0)

        self.line_text = wx.TextCtrl(id=wxID_FRAME1LINE_TEXT, name='line_text',
              parent=self.panel1, pos=wx.Point(568, 32), size=wx.Size(24, 16),
              style=0, value='')

        self.staticText16 = wx.StaticText(id=wxID_FRAME1STATICTEXT16,
              label='paragraph:', name='staticText16', parent=self.panel1,
              pos=wx.Point(520, 56), size=wx.Size(55, 13), style=0)

        self.par_text = wx.TextCtrl(id=wxID_FRAME1PAR_TEXT, name='par_text',
              parent=self.panel1, pos=wx.Point(576, 56), size=wx.Size(24, 16),
              style=0, value='')

        self.selected_group_box = wx.CheckBox(id=wxID_FRAME1SELECTED_GROUP_BOX,
              label='only from\n', name='selected_group_box',
              parent=self.panel1, pos=wx.Point(616, 32), size=wx.Size(88, 16),
              style=0)
        self.selected_group_box.SetValue(False)

        self.staticText18 = wx.StaticText(id=wxID_FRAME1STATICTEXT18,
              label='selected group', name='staticText18', parent=self.panel1,
              pos=wx.Point(632, 48), size=wx.Size(72, 13), style=0)

        self.show_button = wx.Button(id=wxID_FRAME1SHOW_BUTTON, label='show',
              name='show_button', parent=self.panel1, pos=wx.Point(712, 32),
              size=wx.Size(48, 16), style=0)
        self.show_button.Bind(wx.EVT_BUTTON, self.OnShow_buttonButton,
              id=wxID_FRAME1SHOW_BUTTON)

        self.reset_button = wx.Button(id=wxID_FRAME1RESET_BUTTON, label='reset',
              name='reset_button', parent=self.panel1, pos=wx.Point(712, 56),
              size=wx.Size(48, 16), style=0)
        self.reset_button.Bind(wx.EVT_BUTTON, self.OnReset_buttonButton,
              id=wxID_FRAME1RESET_BUTTON)

        self.groups_frame = wx.StaticBox(id=wxID_FRAME1GROUPS_FRAME,
              label='groups', name='groups_frame', parent=self.panel1,
              pos=wx.Point(784, 16), size=wx.Size(224, 224), style=0)

        self.groups_list = wx.ListBox(choices=[], id=wxID_FRAME1GROUPS_LIST,
              name='groups_list', parent=self.panel1, pos=wx.Point(792, 40),
              size=wx.Size(112, 56), style=0)
        self.groups_list.Bind(wx.EVT_LISTBOX, self.OnGroups_listListbox,
              id=wxID_FRAME1GROUPS_LIST)

        self.staticLine1 = wx.StaticLine(id=wxID_FRAME1STATICLINE1,
              name='staticLine1', parent=self.panel1, pos=wx.Point(792, 136),
              size=wx.Size(200, 2), style=0)
        self.staticLine1.SetToolTipString('')

        self.delete_group_button = wx.Button(id=wxID_FRAME1DELETE_GROUP_BUTTON,
              label='delete', name='delete_group_button', parent=self.panel1,
              pos=wx.Point(912, 72), size=wx.Size(72, 23), style=0)
        self.delete_group_button.SetToolTipString('Delete selected group')
        self.delete_group_button.Bind(wx.EVT_BUTTON,
              self.OnDelete_group_buttonButton,
              id=wxID_FRAME1DELETE_GROUP_BUTTON)

        self.new_group_name = wx.TextCtrl(id=wxID_FRAME1NEW_GROUP_NAME,
              name='new_group_name', parent=self.panel1, pos=wx.Point(792, 104),
              size=wx.Size(112, 21), style=0, value='<enter name here>')

        self.new_group_button = wx.Button(id=wxID_FRAME1NEW_GROUP_BUTTON,
              label='add new', name='new_group_button', parent=self.panel1,
              pos=wx.Point(912, 104), size=wx.Size(72, 23), style=0)
        self.new_group_button.SetToolTipString('Add new group')
        self.new_group_button.Bind(wx.EVT_BUTTON, self.OnNew_group_buttonButton,
              id=wxID_FRAME1NEW_GROUP_BUTTON)

        self.words_in_group_list = wx.ListBox(choices=[],
              id=wxID_FRAME1WORDS_IN_GROUP_LIST, name='words_in_group_list',
              parent=self.panel1, pos=wx.Point(792, 144), size=wx.Size(112, 56),
              style=0)
        self.words_in_group_list.SetToolTipString('Words in group')
        self.words_in_group_list.Bind(wx.EVT_LISTBOX,
              self.OnWords_in_group_listListbox,
              id=wxID_FRAME1WORDS_IN_GROUP_LIST)

        self.delete_member_button = wx.Button(id=wxID_FRAME1DELETE_MEMBER_BUTTON,
              label='delete', name='delete_member_button', parent=self.panel1,
              pos=wx.Point(912, 176), size=wx.Size(72, 23), style=0)
        self.delete_member_button.SetToolTipString('Delete selected word from group')
        self.delete_member_button.Bind(wx.EVT_BUTTON,
              self.OnDelete_member_buttonButton,
              id=wxID_FRAME1DELETE_MEMBER_BUTTON)

        self.new_member = wx.TextCtrl(id=wxID_FRAME1NEW_MEMBER,
              name='new_member', parent=self.panel1, pos=wx.Point(792, 208),
              size=wx.Size(112, 16), style=0, value='<enter word here>')
        self.new_member.SetToolTipString('The new group member')

        self.new_member_button = wx.Button(id=wxID_FRAME1NEW_MEMBER_BUTTON,
              label='add new', name='new_member_button', parent=self.panel1,
              pos=wx.Point(912, 208), size=wx.Size(72, 23), style=0)
        self.new_member_button.SetToolTipString('Add new word to group')
        self.new_member_button.Bind(wx.EVT_BUTTON,
              self.OnNew_member_buttonButton, id=wxID_FRAME1NEW_MEMBER_BUTTON)

        self.group_name = wx.StaticText(id=wxID_FRAME1GROUP_NAME, label='',
              name='group_name', parent=self.panel1, pos=wx.Point(824, 144),
              size=wx.Size(0, 13), style=0)

        self.relations_frame = wx.StaticBox(id=wxID_FRAME1RELATIONS_FRAME,
              label='relations', name='relations_frame', parent=self.panel1,
              pos=wx.Point(784, 248), size=wx.Size(224, 264), style=0)

        self.relations_list = wx.ListBox(choices=[],
              id=wxID_FRAME1RELATIONS_LIST, name='relations_list',
              parent=self.panel1, pos=wx.Point(800, 272), size=wx.Size(112, 56),
              style=0)
        self.relations_list.Bind(wx.EVT_LISTBOX, self.OnRelations_listListbox,
              id=wxID_FRAME1RELATIONS_LIST)

        self.delete_relation_button = wx.Button(id=wxID_FRAME1DELETE_RELATION_BUTTON,
              label='delete', name='delete_relation_button', parent=self.panel1,
              pos=wx.Point(920, 304), size=wx.Size(75, 23), style=0)
        self.delete_relation_button.Bind(wx.EVT_BUTTON,
              self.OnDelete_relation_buttonButton,
              id=wxID_FRAME1DELETE_RELATION_BUTTON)

        self.new_relation_name = wx.TextCtrl(id=wxID_FRAME1NEW_RELATION_NAME,
              name='new_relation_name', parent=self.panel1, pos=wx.Point(800,
              336), size=wx.Size(112, 21), style=0, value='<enter name here>')

        self.new_relation_button = wx.Button(id=wxID_FRAME1NEW_RELATION_BUTTON,
              label='add new', name='new_relation_button', parent=self.panel1,
              pos=wx.Point(920, 336), size=wx.Size(75, 23), style=0)
        self.new_relation_button.Bind(wx.EVT_BUTTON,
              self.OnNew_relation_buttonButton,
              id=wxID_FRAME1NEW_RELATION_BUTTON)

        self.staticLine2 = wx.StaticLine(id=wxID_FRAME1STATICLINE2,
              name='staticLine2', parent=self.panel1, pos=wx.Point(793, 368),
              size=wx.Size(199, 2), style=0)

        self.related_couples_list = wx.ListBox(choices=[],
              id=wxID_FRAME1RELATED_COUPLES_LIST, name='related_couples_list',
              parent=self.panel1, pos=wx.Point(800, 376), size=wx.Size(192, 56),
              style=0)

        self.relation_word_1 = wx.TextCtrl(id=wxID_FRAME1RELATION_WORD_1,
              name='relation_word_1', parent=self.panel1, pos=wx.Point(800,
              440), size=wx.Size(112, 21), style=0, value='<enter word here>')

        self.delete_related_couple = wx.Button(id=wxID_FRAME1DELETE_RELATED_COUPLE,
              label='delete', name='delete_related_couple', parent=self.panel1,
              pos=wx.Point(920, 440), size=wx.Size(75, 23), style=0)
        self.delete_related_couple.Bind(wx.EVT_BUTTON,
              self.OnDelete_related_coupleButton,
              id=wxID_FRAME1DELETE_RELATED_COUPLE)

        self.relation_word_2 = wx.TextCtrl(id=wxID_FRAME1RELATION_WORD_2,
              name='relation_word_2', parent=self.panel1, pos=wx.Point(800,
              472), size=wx.Size(112, 21), style=0, value='<enter word here>')

        self.add_new_related_couple = wx.Button(id=wxID_FRAME1ADD_NEW_RELATED_COUPLE,
              label='add new', name='add_new_related_couple',
              parent=self.panel1, pos=wx.Point(920, 472), size=wx.Size(75, 23),
              style=0)
        self.add_new_related_couple.Bind(wx.EVT_BUTTON,
              self.OnAdd_new_related_coupleButton,
              id=wxID_FRAME1ADD_NEW_RELATED_COUPLE)

        self.staticBox3 = wx.StaticBox(id=wxID_FRAME1STATICBOX3,
              label='phrases', name='staticBox3', parent=self.panel1,
              pos=wx.Point(784, 520), size=wx.Size(224, 128), style=0)

        self.phrase_list = wx.ListBox(choices=[], id=wxID_FRAME1PHRASE_LIST,
              name='phrase_list', parent=self.panel1, pos=wx.Point(800, 544),
              size=wx.Size(192, 40), style=0)

        self.delete_phrase_button = wx.Button(id=wxID_FRAME1DELETE_PHRASE_BUTTON,
              label='delete', name='delete_phrase_button', parent=self.panel1,
              pos=wx.Point(800, 592), size=wx.Size(75, 23), style=0)
        self.delete_phrase_button.Bind(wx.EVT_BUTTON,
              self.OnDelete_phrase_buttonButton,
              id=wxID_FRAME1DELETE_PHRASE_BUTTON)

        self.add_phrase_button = wx.Button(id=wxID_FRAME1ADD_PHRASE_BUTTON,
              label='add new', name='add_phrase_button', parent=self.panel1,
              pos=wx.Point(912, 592), size=wx.Size(75, 23), style=0)
        self.add_phrase_button.Bind(wx.EVT_BUTTON,
              self.OnAdd_phrase_buttonButton, id=wxID_FRAME1ADD_PHRASE_BUTTON)

        self.new_phrase_text = wx.TextCtrl(id=wxID_FRAME1NEW_PHRASE_TEXT,
              name='new_phrase_text', parent=self.panel1, pos=wx.Point(792,
              624), size=wx.Size(192, 21), style=0,
              value='<enter phrase here>')

        self.staticBox4 = wx.StaticBox(id=wxID_FRAME1STATICBOX4,
              label='import/export DB', name='staticBox4', parent=self.panel1,
              pos=wx.Point(352, 608), size=wx.Size(384, 104), style=0)

        self.import_path = wx.TextCtrl(id=wxID_FRAME1IMPORT_PATH,
              name='import_path', parent=self.panel1, pos=wx.Point(400, 632),
              size=wx.Size(168, 21), style=0, value='')

        self.staticText11 = wx.StaticText(id=wxID_FRAME1STATICTEXT11,
              label='import:', name='staticText11', parent=self.panel1,
              pos=wx.Point(360, 632), size=wx.Size(35, 13), style=0)

        self.import_browse_button = wx.Button(id=wxID_FRAME1IMPORT_BROWSE_BUTTON,
              label='Browse', name='import_browse_button', parent=self.panel1,
              pos=wx.Point(576, 632), size=wx.Size(75, 23), style=0)
        self.import_browse_button.Bind(wx.EVT_BUTTON,
              self.OnImport_browse_buttonButton,
              id=wxID_FRAME1IMPORT_BROWSE_BUTTON)

        self.import_button = wx.Button(id=wxID_FRAME1IMPORT_BUTTON,
              label='import', name='import_button', parent=self.panel1,
              pos=wx.Point(656, 632), size=wx.Size(75, 23), style=0)
        self.import_button.Bind(wx.EVT_BUTTON, self.OnImport_buttonButton,
              id=wxID_FRAME1IMPORT_BUTTON)

        self.staticText12 = wx.StaticText(id=wxID_FRAME1STATICTEXT12,
              label='export:', name='staticText12', parent=self.panel1,
              pos=wx.Point(360, 656), size=wx.Size(37, 13), style=0)

        self.export_path = wx.TextCtrl(id=wxID_FRAME1EXPORT_PATH,
              name='export_path', parent=self.panel1, pos=wx.Point(400, 656),
              size=wx.Size(168, 21), style=0, value='')

        self.export_browse_button = wx.Button(id=wxID_FRAME1EXPORT_BROWSE_BUTTON,
              label='Browse', name='export_browse_button', parent=self.panel1,
              pos=wx.Point(576, 656), size=wx.Size(75, 23), style=0)
        self.export_browse_button.Bind(wx.EVT_BUTTON,
              self.OnExport_browse_buttonButton,
              id=wxID_FRAME1EXPORT_BROWSE_BUTTON)

        self.export_button = wx.Button(id=wxID_FRAME1EXPORT_BUTTON,
              label='export', name='export_button', parent=self.panel1,
              pos=wx.Point(656, 656), size=wx.Size(75, 23), style=0)
        self.export_button.Bind(wx.EVT_BUTTON, self.OnExport_buttonButton,
              id=wxID_FRAME1EXPORT_BUTTON)

        self.staticBox6 = wx.StaticBox(id=wxID_FRAME1STATICBOX6,
              label='statistics', name='staticBox6', parent=self.panel1,
              pos=wx.Point(744, 648), size=wx.Size(264, 64), style=0)

        self.show_statistic_buttons = wx.Button(id=wxID_FRAME1SHOW_STATISTIC_BUTTONS,
              label='show statistics', name='show_statistic_buttons',
              parent=self.panel1, pos=wx.Point(800, 672), size=wx.Size(192, 24),
              style=0)
        self.show_statistic_buttons.Bind(wx.EVT_BUTTON,
              self.OnShow_statistic_buttonsButton,
              id=wxID_FRAME1SHOW_STATISTIC_BUTTONS)

        self.encrypt_box = wx.CheckBox(id=wxID_FRAME1ENCRYPT_BOX,
              label='Encrypt/Decrypt using password:', name='encrypt_box',
              parent=self.panel1, pos=wx.Point(360, 688), size=wx.Size(184, 13),
              style=0)
        self.encrypt_box.SetValue(False)

        self.pass_text = wx.TextCtrl(id=wxID_FRAME1PASS_TEXT, name='pass_text',
              parent=self.panel1, pos=wx.Point(544, 688), size=wx.Size(184, 16),
              style=wx.TE_PASSWORD, value='')

        self.words_grid = wx.grid.Grid(id=wxID_FRAME1WORDS_GRID,
              name='words_grid', parent=self.panel1, pos=wx.Point(352, 88),
              size=wx.Size(424, 512), style=0)
        self.words_grid.SetHelpText('')
        self.words_grid.EnableEditing(False)
        self.words_grid.Bind(wx.grid.EVT_GRID_CELL_LEFT_CLICK,
              self.OnWords_GridGrid, id=wxID_FRAME1WORDS_GRID)

    def __init__(self, parent):
        self._init_ctrls(parent)
        self.words_grid.CreateGrid(0, 6)
        self.update_all()

    def update_all(self):
        self.update_articles_list()
        self.update_groups_list()
        self.update_relations_list()
        self.update_categories_list()
        self.update_writers_list()
        self.update_newspapers_list()
        self.update_phrases_list()
        
    ##################################################
    ##  Groups handling
    ##################################################
        
    def update_groups_list(self):
        global groups
        global cur_group_num
        groups = list(get_all_groups())
        self.groups_list.Clear()
        for gr in groups:
            self.groups_list.Append(gr["name"])
        self.new_group_name.Value = "<enter name here>"
        cur_group_num = -1

    def update_members_list(self):
        global cur_group_num
        if -1 == cur_group_num:
            raise Exception("-1 == cur_group_num error")
        l = get_words_in_group(cur_group_num)
        if l != None:
            words_in_group = [x["word"] for x in l]
            self.words_in_group_list.Clear()
            self.words_in_group_list.AppendItems(words_in_group)
            self.new_member.Value = "<enter word here>"
            
    def OnNew_group_buttonButton(self, event):
        global groups
        if "<enter name here>" == self.new_group_name.Value or "" == self.new_group_name.Value:
            error_msg("You must select a group name")
            return
        return_val = add_a_group(self.new_group_name.Value)
        if return_val!=-1:
            self.update_groups_list()
        #    self.groups_list.Append(self.new_group_name.Value)
        #    new_mem = {"id": return_val, "name": self.new_group_name.Value}
        #    groups.append(new_mem)
        

    def OnDelete_group_buttonButton(self, event):
        global cur_group_num
        if cur_group_num == -1:
            error_msg("No group is selected")
            return
        if question("Are you sure you want to delete this group?") == YES:
            delete_group(cur_group_num)
            self.update_groups_list()
            self.words_in_group_list.Clear()
        


    def OnGroups_listListbox(self, event):
        global groups
        global cur_group_num
        sel = event.GetSelection()
        group_name = self.groups_list.Items[sel]
        group_num = None
        for grp in groups:
            if grp["name"] == group_name:
                group_num = grp["id"]
        if group_num == None:
            raise Exception("no such group")
        cur_group_num = group_num
        self.update_members_list()
        
        
    def OnNew_member_buttonButton(self, event):
        global cur_group_num
        if cur_group_num == -1:
            error_msg("No group is selected")
            return
        if "<enter word here>" == self.new_member.Value or "" == self.new_member.Value:
            error_msg("You must enter a new member name")
            return
        add_word_to_group(self.new_member.Value, cur_group_num)
        self.update_members_list()
        

    def OnDelete_member_buttonButton(self, event):
        global cur_group_num
        if cur_group_num == -1:
            error_msg("No member is selected")
            return
        if YES == question("Are you sure you want to delete this member?"):
            sel = self.words_in_group_list.Selection
            member_name = self.words_in_group_list.Items[sel]
            delete_word_from_group(member_name, cur_group_num)
            self.update_members_list()
            
    def OnWords_GridGrid(self, event):
        if event.GetCol() == 0:
            word = self.words_list[event.GetRow()]
            dlg = instances_dialog(None)
            dlg.init_text(word["article_id"], word["word"])
            try:
               dlg.ShowModal()
            finally:
               dlg.Destroy()
        

        
    ##################################################
    ##  Relations handling
    ##################################################

    def update_relations_list(self):
        global relations
        global cur_relation_num
        relations = list(get_all_relations())
        self.relations_list.Clear()
        for rl in relations:
            self.relations_list.Append(rl["name"])
        self.new_relation_name.Value = "<enter name here>"
        cur_relation_num = -1
        
    def update_related_couples_list(self):
        global cur_relation_num
        if -1 == cur_relation_num:
            raise Exception("-1 == cur_relation_num error")
        l = get_related_couples(cur_relation_num)
        if l != None:
            related_couples = [x["word1"] + " | " + x["word2"] for x in l]
            self.related_couples_list.Clear()
            self.related_couples_list.AppendItems(related_couples)
            self.relation_word_1.Value = "<enter word here>"
            self.relation_word_2.Value = "<enter word here>"
            
    def OnNew_relation_buttonButton(self, event):
        global relations
        if "<enter name here>" == self.new_relation_name.Value or "" == self.new_relation_name.Value:
            error_msg("You must enter a new relation name")
            return
        return_val = add_a_relation(self.new_relation_name.Value)
        if return_val != -1:
            self.update_relations_list()
        #    self.groups_list.Append(self.new_group_name.Value)
        #    new_mem = {"id": return_val, "name": self.new_group_name.Value}
        #    groups.append(new_mem)
        

    def OnRelations_listListbox(self, event):
        global relations
        global cur_relation_num
        sel = event.GetSelection()
        relation_name = self.relations_list.Items[sel]
        relation_num = None
        for rl in relations:
            if rl["name"] == relation_name:
                relation_num = rl["id"]
        if relation_num == None:
            raise Exception("no such relation")
        cur_relation_num = relation_num
        self.update_related_couples_list()
        

    def OnDelete_relation_buttonButton(self, event):
        global cur_relation_num
        if cur_relation_num == -1:
            error_msg("No relation is selected")
            return
        if question("Are you sure you want to delete this relation?") == YES:
            delete_relation(cur_relation_num)
            self.update_relations_list()
            self.related_couples_list.Clear()
        

    def OnAdd_new_related_coupleButton(self, event):
        global cur_relation_num
        if cur_relation_num == -1:
            error_msg("No group is selected")
            return
        if "<enter word here>" == self.relation_word_1.Value or "" == self.relation_word_1.Value:
            error_msg("You must enter a new relation member name")
            return
        if "<enter word here>" == self.relation_word_2.Value or "" == self.relation_word_2.Value:
            error_msg("You must enter a new relation member name")
            return
        add_a_related_couple(self.relation_word_1.Value, self.relation_word_2.Value, cur_relation_num)
        self.update_related_couples_list()
        

    def OnDelete_related_coupleButton(self, event):
        global cur_relation_num
        if cur_relation_num == -1:
            error_msg("No relation is selected")
            return
        if question("Are you sure you want to delete this related couple?") == YES:
            sel = self.related_couples_list.Selection
            word1, word2 = self.related_couples_list.Items[sel].split(" | ")
            delete_related_couple(word1, word2, cur_relation_num)
            self.update_related_couples_list()
        
        
    ##################################################
    ##  Words list handling
    ##################################################
    def update_words_list(self):
        if 0 != self.words_grid.GetNumberRows():
            self.words_grid.DeleteRows(0, self.words_grid.GetNumberRows())
        
        global articles
        selected_articles = [articles[i]["article_id"] for i in self.articles_list_box.Checked]
        if len(selected_articles) == 0:
            return
        if self.words_radio.Value == True:
            words = get_words_in_articles(selected_articles, True, False)
        elif self.phrases_radio.Value == True:
            words = get_words_in_articles(selected_articles, False, True)
        else:
            words = get_words_in_articles(selected_articles, True, True)
        column_labels = ["word", "par", "sen", "row", "col", "article"]
        self.words_grid.InsertRows(numRows = len(words))
        art_dict = get_article_dictionary()
        for col in xrange(len(column_labels)):
            self.words_grid.SetColLabelValue(col, column_labels[col])
            for i in xrange(len(words)):
                self.words_grid.SetCellValue(i, 0, str(words[i]["word"]))
                self.words_grid.SetCellValue(i, 1, str(words[i]["paragraph"]))
                self.words_grid.SetCellValue(i, 2, str(words[i]["line"]))                          
                self.words_grid.SetCellValue(i, 3, str(words[i]["row"]))
                self.words_grid.SetCellValue(i, 4, str(words[i]["col"]))
                self.words_grid.SetCellValue(i, 5, str(art_dict[words[i]["article_id"]]))
                self.words_list = words
        self.words_grid.ForceRefresh()
        self.words_grid.AutoSizeColumns()
                
    
    def OnWords_in_group_listListbox(self, event):
        event.skip()


    ##################################################
    ##  Articles handling
    ##################################################

    def update_articles_list(self):
        global articles
        articles = list(get_all_articles())
        self.articles_list_box.Clear()
        for art in articles:
            self.articles_list_box.Append(art["title"])
        self.select_all_articles()
        self.update_words_list()
        
    def OnArticles_list_boxListbox(self, event):
        global articles
        global cur_article_id
        """sel = event.GetSelection()
        article_name = self.article_list.Items[sel]
        article_id = None
        for art in article:
            if art["title"] == article_name:
                article_id = art["article_id"]
        if article_id == None:
            raise Exception("no such article")
        cur_article_id = article_id"""
        sel = event.GetSelection()
        title = self.articles_list_box.Items[sel]
        num = None
        for i,art in enumerate(articles):
            if art["title"] == title:
                num = i
        if num == None:
            raise Exception("num problem")
        cur_article_id = articles[num]["article_id"]
        date = articles[num]["date"]
        writers_l = articles[num]["writers"].split(",")
        writers_names = []
        for i in writers_l:
            writers_names.append(get_writer_name(i))
        self.art_title.Label = articles[num]["title"]
        self.art_newspaper.Label = get_newspaper_name(articles[num]["newspaper"])
        self.art_category.Label = get_category_name(articles[num]["category"])
        self.page_num.Label = str(articles[num]["page"])
        self.art_publish_date.Label = str(date.day) + "/" + str(date.month) + "/" + str(date.year)
        self.writers_list.Clear()
        self.writers_list.AppendItems(writers_names)
        
        
    def OnSelect_all_buttonButton(self, event):
        self.select_all_articles()
        

    def OnDeselect_all_buttonButton(self, event):
        self.articles_list_box.SetChecked(())
        

    def OnUpdate_words_buttonButton(self, event):
        self.update_words_list()
        
        
    def select_all_articles(self):
        self.articles_list_box.SetChecked(range(self.articles_list_box.Count))

    def OnAdd_art_buttonButton(self, event):
        dlg = article_frame(None)
        retval = dlg.ShowModal()
        values = dlg.get_values()
        if len(values) != 0:
            add_an_article(*values)
        self.update_articles_list()
        dlg.Destroy() 

    def OnDelete_art_buttonButton(self, event):
        global cur_article_id
        if cur_article_id == -1:
            error_msg("No article is selected")
            return
        if question("Are you sure you want to delete this article?") == YES:
            delete_article(cur_article_id)
            self.update_articles_list()
            self.update_words_list()

    def OnEdit_buttonButton(self, event):
        global cur_article_id
        if cur_article_id == -1:
            error_msg("No article is selected")
            return
        details = get_article_details(cur_article_id)
        # values = (title, newspaper, page, date, writers, path)
        values = (details["title"], details["newspaper"], details["page"], details["date"],
                  details["category"], details["writers"].split(","), details["path"], details["article_id"])
        dlg = article_frame(None, values)
        retval = dlg.ShowModal()
        values = dlg.get_values()
        if len(values) != 0:
            add_an_article(*values)
        self.update_articles_list()
        dlg.Destroy() 

    def OnNewspaper_filter_listListbox(self, event):
        global newspapers
        global cur_newspaper_num
        sel = event.GetSelection()
        newspaper_name = self.newspaper_filter_list.Items[sel]
        newspaper_num = None
        for np in newspapers:
            if np["name"] == newspaper_name:
                newspaper_num = np["id"]
        if newspaper_num == None:
            raise Exception("no such newspaper")
        cur_newspaper_num = newspaper_num

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
            raise Exception("no such category")
        cur_category_num = category_num
        
    def update_categories_list(self):
        global categories
        categories = list(get_all_categories())
        self.category_list.Clear()
        for ct in categories:
            self.category_list.Append(ct["name"])

    def update_writers_list(self):
        global writers
        writers = list(get_all_writers())
        self.writers_list.Clear()
        for wr in writers:
            self.writers_filter_list.Append(wr["name"])

    def update_newspapers_list(self):
        global newspapers
        newspapers = list(get_all_newspapers())
        self.newspaper_filter_list.Clear()
        for np in newspapers:
            self.newspaper_filter_list.Append(np["name"])

    def OnApply_filter_buttonButton(self, event):
            filter_output = ""
            if frame.title_filter_check.Value == True:
                if "" != filter_output:
                    filter_output += " AND "
                filter_output += 'title LIKE "%%%s%%"' % (self.title_filter_text.Value)
                
            if frame.newspaper_filter_check.Value == True and cur_newspaper_num != -1:
                if "" != filter_output:
                    filter_output += " AND "
                filter_output += 'newspaper = %d' % (cur_newspaper_num)
                
            if frame.page_filter_check.Value == True:
                if "" != filter_output:
                    filter_output += " AND "
                min_p = self.min_page_filter_text.Value
                max_p = self.max_page_filter_text.Value
                filter_output += 'page >= %s AND page <= %s' % (min_p, max_p)
                
            if frame.publish_date_check.Value == True:
                if "" != filter_output:
                    filter_output += " AND "
                min_d = pydate_to_sqldate(self.min_publish_date.Value)
                max_d = pydate_to_sqldate(self.max_publish_date.Value)
                filter_output += 'date >= "%s" AND date <= "%s"' % (min_d, max_d)
                
            if frame.category_check.Value == True and cur_category_num != -1:
                if "" != filter_output:
                    filter_output += " AND "
                filter_output += 'category = %d' % (cur_category_num)

            selected_writers = [writers[i]["id"] for i in self.writers_filter_list.Checked]
            
            to_be_checked_articles = []
            if filter_output == "":
                fil_articles = get_all_articles()
            else:
                fil_articles = get_aritlces_with_filter(filter_output)
            selected_writers = [writers[i]["id"] for i in self.writers_filter_list.Checked]
            if self.writers_check.Value == False or len(selected_writers) == 0:
                for i in fil_articles:
                    to_be_checked_articles.append(i["article_id"])
            else:
                for art in fil_articles:
                    flag = True
                    for wr in selected_writers:
                        if (wr in art["writers"].split(",")) == False:
                            flag = False
                    if flag:
                        to_be_checked_articles.append(art["article_id"])
                        
            to_be_checked_articles2 = []
            if self.containing_check.Value == False or self.containing_text.Value == "":
                to_be_checked_articles2 = to_be_checked_articles
            else:
                word_list = self.containing_text.Value.split(",")
                word_list = map(str.lstrip, word_list)
                for art in to_be_checked_articles:
                    ok = True
                    for w in word_list:
                        if is_word_in_article(w, art) == False:
                            ok = False
                            break
                    if ok == True:
                        to_be_checked_articles2.append(art)
            art_loc_dict = {}
            for i in xrange(len(articles)):
                art_loc_dict[articles[i]["article_id"]] = i
            art_selections = []
            for i in to_be_checked_articles2:
                art_selections.append(art_loc_dict[i])
            self.articles_list_box.Checked = tuple(art_selections)
            self.update_words_list()

    def nothing_checked():
        if self.title_filter_check.Value == False and\
           (self.newspaper_filter_check.Value == False or cur_newspaper_num == -1) and\
           self.page_filter_check.Value == False and\
           self.publish_date_check.Value == False and\
           (self.category_check.Value == False or cur_category_num == -1) and\
           (self.writers_check.Value == False or self.writers_list.Checked == ()):
            return True
        else:
            return False
        
    def only_writers_checked():
        if self.title_filter_check.Value == False and\
           (self.newspaper_filter_check.Value == False or cur_newspaper_num == -1) and\
           self.page_filter_check.Value == False and\
           self.publish_date_check.Value == False and\
           (self.category_check.Value == False or cur_category_num == -1) and\
           (self.writers_check.Value == True and self.writers_list.Checked != ()):
            return True
        else:
            return False

        
    ##################################################
    ##  Phrases handling
    ##################################################
        
    def update_phrases_list(self):
        global phrases
        phrases = list(get_all_phrases())
        self.phrase_list.Clear()
        for ph in phrases:
            self.phrase_list.Append(ph["phrase"])
        self.new_phrase_text.Value = "<enter phrase here>"
        
    def OnDelete_phrase_buttonButton(self, event):
        if self.phrase_list.StringSelection == "":
            error_msg("No phrase is selected")
            return
        if question("Are you sure you want to delete this phrase?") == YES:
            delete_phrase(self.phrase_list.StringSelection)
            self.update_phrases_list()
            self.update_words_list()
            #TODO: if "phrase" or "both", update words_list

    def OnAdd_phrase_buttonButton(self, event):
        global phrases
        if "<enter phrase here>" == self.new_phrase_text.Value or "" == self.new_phrase_text.Value:
            error_msg("You must select a phrase")
            return
        if len(split_with(self.new_phrase_text.Value, WORD_SEP)) == 1:
            error_msg("You have selected a word, not a phrase")
            return
        try:
            add_a_phrase(self.new_phrase_text.Value)
        except:
            error_msg("The phrase you've entered already exists")
            return
        self.update_phrases_list()
        self.update_words_list()

    def OnWords_radioRadiobutton(self, event):
        self.update_words_list()

    def OnBoth_radioRadiobutton(self, event):
        self.update_words_list()

    def OnPhrases_buttonRadiobutton(self, event):
        self.update_words_list()

    def OnImport_browse_buttonButton(self, event):
        dlg = wx.FileDialog(self, message="Select a file...", style=wx.OPEN, wildcard = "Concordentation files (.con)|*.con")
        if dlg.ShowModal() == wx.ID_OK:
            self.import_path.Value = dlg.GetPath()

    def OnImport_buttonButton(self, event):
        import_path = self.import_path.Value
        enc = self.encrypt_box.Value
        pas = self.pass_text.Value
        if import_path == "":
            error_msg("You must select a concordentation DB file")
            return
        if False == os.access(import_path, os.F_OK):
            error_msg("Concordentation DB file doesn't exists")
            return
        if NO == question("Are you sure you want to delete the entire DB\nand replace it by the new one?"):
            return
        try:
            s = file(import_path, "rb").read()
        except Exception:
            error_msg("Error opening file")
            return
        if enc and self.pass_text.Value == "":
            error_msg("Please select a password")
            return
        if False == import_xml_to_db(s, cursor, enc, pas):
            error_msg("Error importing. This could occur\nbecause of a wrong file or a wrong password.")
            return
        self.import_path.Value = ""
        self.pass_text.Value = ""
        self.encrypt_box.Value = False
        self.update_all()
        info_msg("DB was successfully imported")
        
    def OnExport_browse_buttonButton(self, event):
        dlg = wx.FileDialog(self, message="Select a file...", style=wx.SAVE, wildcard = "Concordentation files (.con)|*.con")
        if dlg.ShowModal() == wx.ID_OK:
            self.export_path.Value = dlg.GetPath()

    def OnExport_buttonButton(self, event):
        export_path = self.export_path.Value
        enc = self.encrypt_box.Value
        pas = self.pass_text.Value
        if export_path == "":
            error_msg("You must select a concordentation DB file")
            return
        if True == os.access(export_path, os.F_OK):
            if NO == question("File already exists. Overwrite?"):
                return
        if enc and self.pass_text.Value == "":
            error_msg("Please select a password")
            return
        export_db_to_xml(export_path, cursor, enc, pas)
        self.export_path.Value = ""
        self.pass_text.Value = ""
        self.encrypt_box.Value = False
        info_msg("DB was successfully exported")

    def OnShow_buttonButton(self, event):
        wanted_group = cur_group_num
        if self.selected_group_box.Value == False or cur_group_num == -1:
            wanted_group = -1
            if self.row_text.Value != "" and self.row_text.Value.isdigit() == False or\
               self.col_text.Value != "" and self.col_text.Value.isdigit() == False or\
               self.line_text.Value != "" and self.line_text.Value.isdigit() == False or\
               self.par_text.Value != "" and self.par_text.Value.isdigit() == False:
                error_msg("You must enter numeric values or select a group")
                return
            if self.row_text.Value == "" and\
               self.col_text.Value == "" and\
               self.line_text.Value == "" and\
               self.par_text.Value == "":
                self.update_words_list()
                return
                
        if self.words_radio.Value == True:
            words = get_words_in_location(self.row_text.Value, self.col_text.Value,
                                          self.line_text.Value, self.par_text.Value, True, False, wanted_group)
        elif self.phrases_radio.Value == True:
            words = get_words_in_location(self.row_text.Value, self.col_text.Value,
                                          self.line_text.Value, self.par_text.Value, False, True, wanted_group)
        else:
            words = get_words_in_location(self.row_text.Value, self.col_text.Value,
                                          self.line_text.Value, self.par_text.Value, True, True, wanted_group)
                                          
        if 0 != self.words_grid.GetNumberRows():
            self.words_grid.DeleteRows(0, self.words_grid.GetNumberRows())
            
        column_labels = ["word", "par", "line", "row", "col", "article"]
        self.words_grid.InsertRows(numRows = len(words))
        art_dict = get_article_dictionary()
        for col in xrange(len(column_labels)):
            self.words_grid.SetColLabelValue(col, column_labels[col])
            for i in xrange(len(words)):
                self.words_grid.SetCellValue(i, 0, str(words[i]["word"]))
                self.words_grid.SetCellValue(i, 1, str(words[i]["paragraph"]))
                self.words_grid.SetCellValue(i, 2, str(words[i]["line"]))                          
                self.words_grid.SetCellValue(i, 3, str(words[i]["row"]))
                self.words_grid.SetCellValue(i, 4, str(words[i]["col"]))
                self.words_grid.SetCellValue(i, 5, str(art_dict[words[i]["article_id"]]))
                self.words_list = words
        self.words_grid.ForceRefresh()
        self.words_grid.AutoSizeColumns()
        
           

    def OnReset_buttonButton(self, event):
        self.row_text.Value = ""
        self.col_text.Value = ""
        self.line_text.Value = ""
        self.par_text.Value = ""
        self.selected_group_box.Value = False
        self.update_words_list()

    def OnShow_statistic_buttonsButton(self, event):
        dlg = Dialog1(None)
        try:
            dlg.ShowModal()
        finally:
            dlg.Destroy()



if __name__ == '__main__':
    app = wx.PySimpleApp()
    frame = create(None)
    frame.Show();app.MainLoop()
