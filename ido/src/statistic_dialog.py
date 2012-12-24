#Boa:Dialog:Dialog1

import wx
from statistic_funcs import *

[wxID_DIALOG1] = [wx.NewId() for _init_ctrls in range(1)]

class Dialog1(wx.Dialog):
    def _init_sizers(self):
        # generated method, don't edit
        col_num = 2
        row_num = (len(self.stats_list) + 1) /  2
        self.gridSizer1 = wx.GridSizer(cols=col_num, hgap=5, rows=row_num, vgap=5)
        for s in self.stats_list:
            bw = wx.StaticText(self, label=s)
            self.gridSizer1.Add(bw, 0, 0)

        self.SetSizer(self.gridSizer1)
        self.Fit()


    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Dialog.__init__(self, id=wxID_DIALOG1, name='', parent=prnt,
              #pos=wx.Point(331, 301), size=wx.Size(400, 250),
			  pos=wx.Point(50, 300), size=wx.Size(400, 250),
              style=wx.DEFAULT_DIALOG_STYLE, title='Concordance Statistics')
        self.SetClientSize(wx.Size(384, 212))
        self._init_sizers()

    def __init__(self, parent):
        self.update_stats_list()
        self._init_ctrls(parent)

    def update_stats_list(self):
        self.stats_list = []

        wr = youngest_writer()
        if wr != None:
            self.stats_list.append("The youngest writer is %s. He was born in %s."\
            % (wr["name"], wr["date_of_birth"]))

        wr = oldest_writer()
        if wr != None:
            self.stats_list.append("The oldest writer is %s. He was born in %s. "\
            % (wr["name"], wr["date_of_birth"]))

        wr, num = best_writer()
        if wr != None:
            self.stats_list.append("The best writer is %s. He wrote %d articles. " % (wr["name"], num))

        np, num = best_newspaper()
        if np != None:
            self.stats_list.append("The best newspaper is %s. It has published %d articles. " % (np, num))

        l_word = longest_word()
        if l_word != None:
            self.stats_list.append("The longest word is %s. " % l_word['word'])
            
        l_phrase = longest_phrase()
        if l_phrase != None:
            self.stats_list.append("The longest phrase is %s. " % l_phrase['word'])
            
        best_words_in_groups = word_in_groups()
        if len(best_words_in_groups) > 1:
            best_words = ",".join(best_words_in_groups)
            self.stats_list.append("The words from groups that appears the most are %s. " % best_words)
        elif len(best_words_in_groups) == 1:
            self.stats_list.append("The word from groups that appears the most is %s. " % best_words_in_groups[0])
            
        b_category = best_category()
        if len(b_category) > 1:
            best_categories = ",".join(b_category)
            self.stats_list.append("The categories that appear the most are %s. " % best_categories)
        elif len(b_category) == 1:
            self.stats_list.append("The category that appear the most is %s. " %  b_category[0])
            
        l_article = longest_article()
        if l_article != None:
            self.stats_list.append("The longest article is %s. " % str(l_article))
            
        avg_words = avg_words_in_article()
        if avg_words != None:
            self.stats_list.append("The average words per article is %s. " % str(avg_words))
            
        avg_lines = avg_lines_in_article()
        if avg_lines != None:
            self.stats_list.append("The average lines per article is %s. " % str(avg_lines))
            
        avg_words_line = avg_word_in_line()
        if avg_words_line != None:
            self.stats_list.append("The average words per line is %s. " %  str(avg_words_line))
            
        oldest_article = first_article()
        if oldest_article != None:
            self.stats_list.append("The oldest article is %s. It was published on %s. " % (str(oldest_article["title"]), str(oldest_article["date"])))
        
        youngest_article = last_article()
        if youngest_article != None:
            self.stats_list.append("The youngest article is %s. It was published on %s. " % (str(youngest_article["title"]), str(youngest_article["date"])))
            
        words_related = best_related()
        if len(words_related) > 1:
            related_words = ", ".join("-".join(i) for i in words_related)
            self.stats_list.append("The related words that appear the most are %s. " % related_words)
        elif len(words_related) == 1:
            related_words = "-".join(words_related[0])
            self.stats_list.append("The related words that appear the most are %s. " % related_words)
        
        s_article = shortest_article()
        if s_article != None:
            self.stats_list.append("The shortest article is %s. " % str(s_article))
        
        s_word,length = shortest_word()
        if s_word != None:
            self.stats_list.append("The shortest word is in length of %d, for ex: %s." %(length, s_word))
        
        a_word = avg_word()
        if a_word != None:
            self.stats_list.append("The average word length is %s." % str(a_word))
            
        b_word,times = best_word()
        if b_word != None:
            self.stats_list.append("The most appear word is %s, it appear %d times." %(b_word, times))
        
        l_cat_article, num = longest_article_in_category()
        if l_cat_article != None:
            self.stats_list.append("The category that has the biggest average words per article  is %s with %d words. " % (l_cat_article, num))
            
        num_of_hofrim = hofrim_articles()
        if num_of_hofrim is not None:
            self.stats_list.append("The number of articles that was over 500 words is %d. " % num_of_hofrim)
        
        num_of_short = short_articles()
        if num_of_short is not None:
            self.stats_list.append("The number of articles that was less than 100 words is %d. " % num_of_short)
        
        newspaper_hofer= most_words_in_newspaper()
        if newspaper_hofer is not None:
            self.stats_list.append("The most hofer newspaper is %s. " % newspaper_hofer)
        