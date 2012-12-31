import wx
import os
from text_indexer.orm.expression import Expression
from text_indexer.core.db import delete_expression

class GroupAndExpressionsPanel(wx.Panel):
    
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, -1)
        
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        exp_sizer = wx.BoxSizer(wx.VERTICAL)
        
        word_list_sizer = wx.BoxSizer(wx.VERTICAL)
        
        
        group_sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        select_group_sizer = wx.BoxSizer(wx.VERTICAL)
        
        buttons_group_sizer = wx.BoxSizer(wx.VERTICAL)
        
        
        groups_list = [] # DODO: add groups from DB
        
        self.select_group = wx.ComboBox(self, 500, "", (90, 50), 
                                        (160, -1), groups_list, wx.CB_DROPDOWN)
        
        group_text = wx.StaticText(self, -1, "Manage Group", (20, 20)) 
        
        self.group_words = wx.ListBox(self, 60, (100, 100), (150, 200), [], wx.LB_SINGLE)
        
        self.create_group_button = wx.Button(self, -1, "Create New Group", (300, 150))
        self.Bind(wx.EVT_BUTTON, self.OnCreateGroup, self.create_group_button) 
        
        self.add_word_to_group_button = wx.Button(self, -1, "Add Word", (300, 150))
        self.Bind(wx.EVT_BUTTON, self.OnAddWordToGroup, self.add_word_to_group_button)
        
        self.add_word_to_group_from_list_button = wx.Button(self, -1, "Add Word From List", (300, 150))
        self.Bind(wx.EVT_BUTTON, self.OnAddWordToGroupFromList, self.add_word_to_group_button)

        self.remove_word_button = wx.Button(self, -1, "Remove Word", (300, 150))
        self.Bind(wx.EVT_BUTTON, self.OnRemoveWordFromGroup, self.remove_word_button)
        
        
        
        select_group_sizer.Add(group_text)
        select_group_sizer.Add(self.select_group)
        select_group_sizer.Add(self.group_words)
        
        buttons_group_sizer.AddSpacer(100)
        buttons_group_sizer.Add(self.create_group_button)
        buttons_group_sizer.Add(self.add_word_to_group_button)
        buttons_group_sizer.Add(self.add_word_to_group_from_list_button)
        buttons_group_sizer.Add(self.remove_word_button)
        
        group_sizer.Add(select_group_sizer)
        group_sizer.Add(buttons_group_sizer)
        
        
        expressions_sizer = wx.BoxSizer(wx.HORIZONTAL)
        buttons_expressions_sizer = wx.BoxSizer(wx.VERTICAL)
        select_expressions_sizer = wx.BoxSizer(wx.VERTICAL)
        
        expression_text = wx.StaticText(self, -1, "Manage Expressions", (20, 20))
        self.expressions_list = [e.name for e in Expression.get_expressions()] 
        
        self.expressions = wx.ListBox(self, 60, (100, 100), (150, 200), self.expressions_list, wx.LB_EXTENDED)
        
        self.add_expression_button = wx.Button(self, -1, "Add Expression", (300, 150))
        self.Bind(wx.EVT_BUTTON, self.OnAddWordToExpressions, self.add_expression_button) 

        self.remove_expressions_button = wx.Button(self, -1, "Remove Expressions", (300, 150))
        self.Bind(wx.EVT_BUTTON, self.onRemoveExpressions, self.remove_expressions_button) 
        
        select_expressions_sizer.Add(expression_text)
        select_expressions_sizer.Add(self.expressions)
        
        buttons_expressions_sizer.AddSpacer(100)
        buttons_expressions_sizer.Add(self.add_expression_button)
        buttons_expressions_sizer.Add(self.remove_expressions_button)
        
        
        expressions_sizer.Add(select_expressions_sizer)
        expressions_sizer.Add(buttons_expressions_sizer)
        
        exp_sizer.AddSpacer(50)
        exp_sizer.Add(group_sizer)
        exp_sizer.AddSpacer(50)
        exp_sizer.Add(expressions_sizer)
        
        
        word_list_text = wx.StaticText(self, -1, "Words List", (20, 20)) 
        word_list = ["a", "b", "c"]
        self.lb1 = wx.ListBox(self, 60, (100, 50), (200, 400), word_list, wx.LB_EXTENDED)
        
        word_list_sizer.AddSpacer(100)
        word_list_sizer.Add(word_list_text)
        word_list_sizer.Add(self.lb1)
        
        
        sizer.AddSpacer(50)
        sizer.Add(exp_sizer)
        sizer.AddSpacer(200)        
        sizer.Add(word_list_sizer)
        
        self.SetSizer(sizer)
        
    
    def OnCreateGroup(self, evt):
        pass
    
    def OnAddWordToGroup(self, evt):
        pass
    
    def OnAddWordToGroupFromList(self, evt):
        pass

    def OnRemoveWordFromGroup(self, evt):
        pass

    def OnAddWordToExpressions(self, evt):
        dlg = wx.TextEntryDialog(
                self, 'Please insert the expression:')


        if dlg.ShowModal() == wx.ID_OK:
            expression = dlg.GetValue()
            Expression.add_expression(expression)
            self.expressions.Append(expression)
            self.expressions_list.append(expression)

        dlg.Destroy()
    
    def onRemoveExpressions(self, evt):
        selections = self.expressions.GetSelections()
        for selection in selections:
            if selection != -1:
                expression = Expression.get_expressions(expression=self.expressions.Items[selection])[0]
                self.expressions.Delete(selection)
                delete_expression(expression)
    
    
    
    
        
        