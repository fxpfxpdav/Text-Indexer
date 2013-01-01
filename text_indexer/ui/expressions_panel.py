import wx
import os
from text_indexer.orm.expression import Expression
from text_indexer.core.db import delete_expression, delete_group, session
from text_indexer.orm.group import Group
from text_indexer.orm.word import Word
from text_indexer.orm.word_group_association import WordGroupAssocaition

class GroupAndExpressionsPanel(wx.Panel):
    
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, -1)
        
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        exp_sizer = wx.BoxSizer(wx.VERTICAL)
        
        relation_sizer = wx.BoxSizer(wx.HORIZONTAL)
        relation_grid_sizer = wx.BoxSizer(wx.VERTICAL)
        relation_buttons_sizer = wx.BoxSizer(wx.VERTICAL)
        
        word_list_sizer = wx.BoxSizer(wx.VERTICAL)
        
        
        group_sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        select_group_sizer = wx.BoxSizer(wx.VERTICAL)
        
        buttons_group_sizer = wx.BoxSizer(wx.VERTICAL)
        
        
        self.groups_list = [g.name for g in Group.get_groups()]
        
        self.select_group = wx.ComboBox(self, 500, "", (90, 50), 
                                        (160, -1), self.groups_list, wx.CB_DROPDOWN)
        self.Bind(wx.EVT_COMBOBOX, self.onGroupChosen, self.select_group)
        
        group_text = wx.StaticText(self, -1, "Manage Group", (20, 20)) 
        
        self.group_words = wx.ListBox(self, 60, (100, 100), (150, 200), [], wx.LB_SINGLE)
        
        self.create_group_button = wx.Button(self, -1, "Create New Group", (300, 150))
        self.Bind(wx.EVT_BUTTON, self.onCreateGroup, self.create_group_button) 
        
        self.add_word_to_group_button = wx.Button(self, -1, "Add Word", (300, 150))
        self.Bind(wx.EVT_BUTTON, self.onAddWordToGroup, self.add_word_to_group_button)
        
        self.add_word_to_group_from_list_button = wx.Button(self, -1, "Add Words From List", (300, 150))
        self.Bind(wx.EVT_BUTTON, self.OnAddWordToGroupFromList, self.add_word_to_group_from_list_button)

        self.remove_word_button = wx.Button(self, -1, "Remove Word", (300, 150))
        self.Bind(wx.EVT_BUTTON, self.onRemoveWordFromGroup, self.remove_word_button)
        
        self.remove_group_button = wx.Button(self, -1, "Remove Group", (300, 150))
        self.Bind(wx.EVT_BUTTON, self.onRemoveGroup, self.remove_group_button)
        
        
        
        select_group_sizer.Add(group_text)
        select_group_sizer.Add(self.select_group)
        select_group_sizer.Add(self.group_words)
        
        buttons_group_sizer.AddSpacer(100)
        buttons_group_sizer.Add(self.create_group_button)
        buttons_group_sizer.Add(self.add_word_to_group_button)
        buttons_group_sizer.Add(self.add_word_to_group_from_list_button)
        buttons_group_sizer.Add(self.remove_word_button)
        buttons_group_sizer.Add(self.remove_group_button)
        
        group_sizer.Add(select_group_sizer)
        group_sizer.Add(buttons_group_sizer)
        
        
        expressions_sizer = wx.BoxSizer(wx.HORIZONTAL)
        buttons_expressions_sizer = wx.BoxSizer(wx.VERTICAL)
        select_expressions_sizer = wx.BoxSizer(wx.VERTICAL)
        
        expression_text = wx.StaticText(self, -1, "Manage Expressions", (20, 20))
        self.expressions_list = [e.name for e in Expression.get_expressions()] 
        
        self.expressions = wx.ListBox(self, 60, (100, 100), (150, 200), self.expressions_list, wx.LB_EXTENDED)
        
        self.add_expression_button = wx.Button(self, -1, "Add Expression", (300, 150))
        self.Bind(wx.EVT_BUTTON, self.onAddExpression, self.add_expression_button) 

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
        
        
        
        expression_text = wx.StaticText(self, -1, "Manage relations", (20, 20))
        
        
        self.relations_grid = wx.grid.Grid(self, -1)
        
        self.relations_grid.CreateGrid(0, 3)
        
        self.relations_grid.SetColSize(0, 100)
        self.relations_grid.SetColSize(1, 100)
        self.relations_grid.SetColSize(2, 100)

        
        self.relations_grid.SetColLabelValue(0, "Word 1")
        self.relations_grid.SetColLabelValue(1, "Word 2")
        self.relations_grid.SetColLabelValue(2, "Relation Name")
        
        
        relation_grid_sizer.AddSpacer(50)
        relation_grid_sizer.Add(expression_text)
        relation_grid_sizer.AddSpacer(10)
        relation_grid_sizer.Add(self.relations_grid)
        
        
        self.add_relation_button = wx.Button(self, -1, "Add Relation", (300, 150))
        self.Bind(wx.EVT_BUTTON, self.onAddRelation, self.add_relation_button) 

        self.remove_relation_button = wx.Button(self, -1, "Remove Relation", (300, 150))
        self.Bind(wx.EVT_BUTTON, self.onRemoveRelation, self.remove_relation_button) 
        
        relation_buttons_sizer.AddSpacer(100)
        relation_buttons_sizer.Add(self.add_relation_button)
        relation_buttons_sizer.Add(self.remove_relation_button)
        
        relation_sizer.Add(relation_grid_sizer)
        relation_sizer.AddSpacer(20)
        relation_sizer.Add(relation_buttons_sizer)
        
        word_list_text = wx.StaticText(self, -1, "Words List", (20, 20)) 
        word_list = [w.word for w in Word.get_words()]
        self.lb1 = wx.ListBox(self, 60, (100, 50), (200, 400), word_list, wx.LB_EXTENDED)
        
        word_list_sizer.AddSpacer(100)
        word_list_sizer.Add(word_list_text)
        word_list_sizer.Add(self.lb1)
        
        
        sizer.AddSpacer(50)
        sizer.Add(exp_sizer)
        sizer.AddSpacer(50)
        sizer.Add(relation_sizer)        
        sizer.AddSpacer(100)        
        sizer.Add(word_list_sizer)
        
        self.SetSizer(sizer)
        
    
    def onCreateGroup(self, evt):
        dlg = wx.TextEntryDialog(
                self, 'Please insert the group name:')


        if dlg.ShowModal() == wx.ID_OK:
            name = dlg.GetValue()
            Group.add_group(name)
            self.select_group.Append(name)
            self.groups_list.append(name)
            

        dlg.Destroy()
    
    
    def onAddWordToGroup(self, evt):
        name = self.select_group.Items[self.select_group.Selection]
        group = Group.get_groups(name)[0]
        dlg = wx.TextEntryDialog(
                self, 'Please enter the word to add:')


        if dlg.ShowModal() == wx.ID_OK:
            word = dlg.GetValue()
            db_word = Word.add_word(word)
            word_group = WordGroupAssocaition(word_id=db_word.id, group_id=group.id)
            session.add(word_group)
            session.commit()
            self.group_words.Append(word)
        dlg.Destroy()
    
    def OnAddWordToGroupFromList(self, evt):
        selections = self.lb1.GetSelections()
        db_group = Group.get_groups(self.select_group.Items[self.select_group.Selection])[0]
        for selection in selections: 
            db_word = Word.get_words(word=self.lb1.Items[selection])[0]
            word_group = WordGroupAssocaition(word_id=db_word.id, group_id=db_group.id)
            session.add(word_group)
            session.commit()
            self.group_words.Append(db_word.word)

    def onRemoveWordFromGroup(self, evt):
        selection = self.group_words.GetSelection()
        word = self.group_words.Items[selection]
        db_word = Word.get_words(word)[0]
        db_group = Group.get_groups(self.select_group.Items[self.select_group.Selection])[0]
        self.group_words.Delete(selection)
        db_wga = session.query(WordGroupAssocaition).filter_by(group_id=db_group.id, word_id=db_word.id).first()
        session.delete(db_wga)
        session.commit()
        
    
    def onRemoveGroup(self, evt):
        selection = self.select_group.GetSelection()
        group = Group.get_groups(name=self.select_group.Items[selection])[0]
        self.select_group.Delete(selection)
        delete_group(group)
        pass

    def onAddExpression(self, evt):
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
                
    def onGroupChosen(self, evt):
        name = self.select_group.Items[evt.GetSelection()]
        group = Group.get_groups(name)[0]
        self.group_words.Clear()
        for word in group.words:
            self.group_words.Append(word.word)
            
    def onAddRelation(self, evt):
        pass
    
    def onRemoveRelation(selfself, evt):
        pass
    
        
        
    
    
    
    
        
        