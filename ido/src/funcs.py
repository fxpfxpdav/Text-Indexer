# -*- coding: cp1255 -*-
import MySQLdb as sql
import sys
import os
import re
HOST = 'localhost'
USER = 'root'
PASSWD = '123'
DB = 'MySQL'
line_sep = [".", ";", "?", "!", ":"]
marks = [".", ",", "'", '"', ";", ":", "?", "!", "/", "\\","(", ")", "[", "]", "-","”", "“", "–"]
WORD_SEP = [" ", "-", "/", "\\", "@", "|", "–"]
from db import MAX_NUM_OF_WRITERS_PER_ARTICLE
try:
    con = sql.Connection(host = HOST, user = USER,
                   passwd = PASSWD , db = DB)
except sql.Error, e:
    print "Error %d: %s" % (e.args[0], e.args[1])
    sys.exit(1)

cursor = con.cursor(sql.cursors.DictCursor)

def split_with(s, l):
    '''
    split a string with a list of chars
    @param s: a string to split
    @param l: list of chars
    '''
    output = [s]
    for i in l:
        temp = []
        for word in output:
            temp += word.split(i)
            output = temp
        return output

def pydate_to_sqldate(date):
    '''
    get a python date and change it to sql date
    @param date: python date
    @return: sql date
    '''
    year, month, day = str(date.Year), str(date.Month), str(date.Day)
    if len(month) == 1:
        month = "0" + month
    if len(day) == 1:
        day = "0" + day
    return year + "-" + month + "-" + day

def amount_of_shows(substring, string):
    '''
    return how many shows of substring we have in the string 
    '''
    return len(re.findall(substring, string))

def findall(string, sub):
    '''
    return a list of index of the substring in the string
    '''
    listindex=[]
    offset=0
    i = string.find(sub, offset)
    while i >= 0:
        listindex.append(i)
        i = string.find(sub, i + 1)
    return listindex
    
######################################################################
### Generic functions for checking values in tables
######################################################################
def value_in_table(table, value_name, value):
    '''
    return how many times the value appear in the table
    '''
    return cursor.execute("SELECT * FROM %s WHERE %s = %d"%
                         (table, value_name, value))

def str_value_in_table(table, value_name, value):
    '''
    return how many times the str value appear in the table
    '''
    return cursor.execute('SELECT * FROM %s WHERE %s = "%s"'%
                         (table, value_name, value))


######################################################################
### "Exists" functions
######################################################################
def newspaper_exists(num):
    '''
    does a newspaper exists
    @param num: a newspaper id
    '''
    amount = value_in_table("newspaper", "id", num)
    if 1 == amount:
        return True
    elif 0 == amount:
        return False
    else:
        raise "error"
    
def newspaper_name_exists(name):
    '''
    does a newspaper exists
    @param num: a newspaper name
    '''
    amount = str_value_in_table("newspaper", "name", name)
    if amount == 1:
        return True
    elif amount == 0:
        return False
    else:
        raise "error"
    
def category_exists(num):
    '''
    does a category exists
    @param num: a category id
    '''
    amount = value_in_table("category", "id", num)
    if 1 == amount:
        return True
    elif 0 == amount:
        return False
    else:
        raise "error"

def writer_exists(num):
    '''
    does a writer exists
    @param num: a writer id
    '''
    amount = str_value_in_table("writers", "id", num)
    if 1 == amount:
        return True
    elif 0 == amount:
        return False
    else:
        raise "error"
    
def article_exists(path):
    '''
    does a article exists
    @param num: a article path
    '''
    amount = str_value_in_table("articles", "path", path )
    if amount == 1:
        return True
    elif amount == 0:
        return False
    else:
        raise "article_exists error"
     
def group_name_exists(name):
    '''
    does a group_name_ exists
    @param num: a group name
    '''
    amount = str_value_in_table("groups", "name", name)
    if amount == 1:
        return True
    elif amount == 0:
        return False
    else:
        raise "error"

def relation_name_exists(name):
    '''
    does a relation_name exists
    @param num: a relation name
    '''
    amount = str_value_in_table("relation", "name", name)
    if amount == 1:
        return True
    elif amount == 0:
        return False
    else:
        raise "error"
    
def group_id_exists(group_id):
    '''
    does a group_name_ exists
    @param num: a group_id
    '''
    amount = value_in_table("groups", "id", group_id)
    if amount == 1:
        return True
    elif amount == 0:
        return False
    else:
        raise "error"
    
def relation_id_exists(relation_id):
    '''
    does a relation exists
    @param num: a relation_id_
    '''
    amount = value_in_table("relation", "id", relation_id)
    if amount == 1:
        return True
    elif amount == 0:
        return False
    else:
        raise "error"
def phrase_exists(phrase):
    '''
    does a phrase exists
    @param num: a phrase
    '''
    amount = str_value_in_table("phrases", "phrase", phrase)
    if 1 == amount:
        return True
    elif 0 == amount:
        return False
    else:
        raise "error"
    
######################################################################
### Counter functions
######################################################################
def get_counter_num(name):
    '''
    get counter value by name or create a new one 
    '''
    cursor.execute('SELECT * FROM counter_values WHERE name="%s"'%(name))
    l = cursor.fetchall()
    if len(l)==0:
        cursor.execute("""
            INSERT INTO counter_values (name, value)
            VALUES ("%s", 0)
            """ % (name))
        return 0
    elif len(l)==1:
        return l[0]["value"]
    else:
        raise "Too many counter values of %s"%(name)

def update_counter_num(name):
    '''
    update a counter number
    '''
    cur_num = get_counter_num(name)
    cursor.execute("""
        UPDATE counter_values
        SET value = %d
        WHERE name = '%s'
        """ % (cur_num + 1, name))
    cursor.connection.commit()
                   
######################################################################
### Add functions
######################################################################
def add_a_newspaper(name):
    '''
    add a newspaper
    '''
    name = normalize_uni(name)
    newspaper_counter = get_counter_num("newspaper")
    num = newspaper_counter + 1
    if newspaper_name_exists(name):
        return -1
    cursor.execute("""
        INSERT INTO newspaper (id, name)
        VALUES (%d, "%s")
                """ % (num, name))
    cursor.connection.commit()
    update_counter_num("newspaper")
    return True
    
def add_a_category(name):
    '''
    add_a_category
    '''
    name = normalize_uni(name)
    category_counter = get_counter_num("category")
    num = category_counter + 1
    cursor.execute("""
        INSERT INTO category (id, name)
        VALUES (%d, "%s")
                """ % (num, name))
    cursor.connection.commit()
    update_counter_num("category")
    return True

def add_a_writer(num, name, date):
    '''
    add_a_writer
    '''
    name = normalize_uni(name)
    if writer_exists(num):
        return False
    cursor.execute("""
        INSERT INTO writers (id, name, date_of_birth)
        VALUES ("%s", "%s", "%s")
                """ % (num, name, date))
    cursor.connection.commit()
    return True
    
def add_an_article(title, path, newspaper, page, date, writers, category):
    '''
    add_an_article
    '''
    title = normalize_uni(title)
    cursor.connection.commit()
    article_counter = get_counter_num("article")
    path = os.path.abspath(path).replace("\\", "\\\\")
    if article_exists(path):
        raise "Article with that path already exists"
    if not newspaper_exists(newspaper):
        raise "No such newspaper"
    writers_set = set(writers.split(","))
    writers_list = []
    for i in writers_set:
        try:
            writers_list.append(i)
        except:
            raise "writers_list append error"
    for i in writers_list:
        if not writer_exists(i):
            raise "no such writer: %s"%(i)
    writers_output = ""
    for i in writers_list:
        writers_output = writers_output + i + ","
    if writers_output != "":
        writers_output = writers_output[:-1]
    if not category_exists(category):
        raise "No such category"
                   
    update_counter_num("article")
    article_id = article_counter+1
    cursor.execute("""
        INSERT INTO articles (article_id, path, newspaper, page, date, writers,
        title, category)
        VALUES (%d, "%s", %d, %d, "%s", "%s", "%s", %d)
                """ % (article_id, path, newspaper, page, date,\
                       writers_output, title, category))

    parse_a_file(path, article_id)
    cursor.connection.commit()
    
def add_a_group(name):
    '''
    
    add_a_group    
    '''
    name = normalize_uni(name)
    group_counter = get_counter_num("group")
    if group_name_exists(name):
        return -1
    group_id = group_counter + 1
    update_counter_num("group")
                   
    cursor.execute("""
        INSERT INTO groups (id, name)
        VALUES (%d, "%s")
                """ % (group_id, name))
    cursor.connection.commit()
    return group_id

def add_word_to_DB(word, par_num, line_num, row_num, col_num, article_id, offset, full_word_length, is_phrase = 0):
    '''
    add_word_to_DB
    '''
    word = normalize_uni(word)
    if len(word)>0:
        while len(word)>0 and word[-1] in marks:
            word = word[:-1]
        while len(word)>0 and word[0] in marks:
            word = word[1:]
        if len(word)>0:
            try:
                cursor.execute("""
                INSERT INTO word (word, article_id, paragraph, line, row, col, offset, full_len, is_phrase)
                VALUES ("%s", %d, %d, %d, %d, %d, %d, %d, %d)
                        """ % (word.lower(), article_id, par_num, line_num,
                               row_num, col_num, offset, full_word_length, is_phrase))
            except:
                print word.lower(), article_id, par_num, line_num, row_num, col_num, offset, full_word_length, is_phrase

def add_word_to_group(word, group_id):
    '''
    
    add_word_to_group
    '''
    word = normalize_uni(word)
    if group_id_exists(group_id) == True:
        if (0 == cursor.execute("SELECT * FROM word_in_group WHERE word='%s' AND group_id=%d"%(word, group_id))):
            cursor.execute("""
                INSERT INTO word_in_group (word, group_id)
                VALUES ("%s", %d)
                        """ % (word, group_id))
            cursor.connection.commit()  

def add_a_relation(name):
    '''
    add_a_relation
    '''
    name = normalize_uni(name)
    relation_counter = get_counter_num("relation")
    if relation_name_exists(name):
        return -1
    relation_id = relation_counter + 1
    update_counter_num("relation")
                   
    cursor.execute("""
        INSERT INTO relation (id, name)
        VALUES (%d, "%s")
                """ % (relation_id, name))
    cursor.connection.commit()
    return relation_id

def add_a_related_couple(word1, word2, relation_id):
    '''
    
    add_a_related_couple
    '''
    if relation_id_exists(relation_id) == True:
        if (0 == cursor.execute("SELECT * FROM related_couples WHERE word1='%s' AND word2='%s' AND relation_id=%d"%(word1, word2, relation_id))
            and
            0 == cursor.execute("SELECT * FROM related_couples WHERE word1='%s' AND word2='%s' AND relation_id=%d"%(word2, word1, relation_id))):
            cursor.execute("""
                INSERT INTO related_couples (word1, word2, relation_id)
                VALUES ("%s", "%s", %d)
                        """ % (word1, word2, relation_id))
            cursor.connection.commit()

def add_a_phrase(phrase):
    '''
    
    add_a_phrase
    '''
    phrase = normalize_uni(phrase)
    if phrase_exists(phrase):
        raise "phrase already exists"
    cursor.execute("""
        INSERT INTO phrases (phrase)
        VALUES ("%s")
                """ % (phrase))
    cursor.connection.commit()
    add_phrase_shows(phrase)

def add_phrase_shows(phrase):
    '''
    add_phrase_shows
    '''
    phrase = normalize_uni(phrase)
    phrase = phrase.lower()
    all_articles = get_all_articles()
    for art in all_articles:
        f = file(art["path"], "r")
        text = f.read().lower()
        f.close()
        locations = [i.start() for i in re.finditer(phrase, text)]
        for loc in locations:
            row = amount_of_shows("\n", text[:loc])
            col = len(text[:loc].split("\n")[-1])
            par = amount_of_shows("\n\n", text[:loc])
            last_par = text[:loc].split("\n\n")[-1]
            line = len(split_with(last_par, line_sep)) - 1
            add_word_to_DB(phrase, par, line, row, col, art["article_id"], loc, len(phrase), is_phrase = 1)
    cursor.connection.commit()
            
        
        
######################################################################
### Delete functions
######################################################################  

def delete_group(group_id):
    '''
    delete_group by group id
    '''
    cursor.execute("""
        DELETE FROM word_in_group
        WHERE group_id = %d
        """ % (group_id))
    cursor.execute("""
        DELETE FROM groups
        WHERE id = %d
        """ % (group_id))
    cursor.connection.commit()

   
def delete_word_from_group(word, group_id):
    '''
    delete_word_from_group
    @param word: word to delete
    @param group_id: from which group
    '''
    cursor.execute("""
        DELETE FROM word_in_group
        WHERE word = "%s" AND group_id = %d
        """ % (word, group_id))
    cursor.connection.commit()
        
def delete_relation(relation_id):
    '''
    delete_relation
    '''
    cursor.execute("""
        DELETE FROM related_couples
        WHERE relation_id = %d
                        """ % (relation_id))
    cursor.execute("""
                        DELETE FROM relation
                        WHERE id = %d
                        """ % (relation_id))
    cursor.connection.commit()
        
def delete_related_couple(word1, word2, relation_id):
        '''
        delete_related_couple
        @param word1: first word
        @param word2: second word
        @param relation_id: from which relation
        '''
        cursor.execute("""
                        DELETE FROM related_couples
                        WHERE word1 = "%s" AND word2 = "%s" AND relation_id = %d
                        """ % (word1, word2, relation_id))
        cursor.execute("""
                        DELETE FROM related_couples
                        WHERE word2 = "%s" AND word1 = "%s" AND relation_id = %d
                        """ % (word1, word2, relation_id))
        cursor.connection.commit()

def delete_article(article_id):
    '''
    delete an article and all the world form this article
    '''
    cursor.execute("""
                    DELETE FROM articles
                    WHERE article_id = %d
                        """ % (article_id))
    cursor.execute("""
                    DELETE FROM word
                    WHERE article_id = %d
                        """ % (article_id))
    cursor.connection.commit()

def delete_newspaper(newspaper_id):
    '''
    delete a newspaper and all the articles and words from this newspaper
    '''
    cursor.execute("""
                    DELETE FROM newspaper
                    WHERE id = %d
                        """ % (newspaper_id))
    cursor.execute(""" SELECT article_id FROM articles WHERE newspaper = %d""" %newspaper_id)
    res = cursor.fetchall()
    for i in res:
        article_id = i['article_id']
        delete_article(article_id)
#    cursor.execute("""
#                    DELETE FROM articles
#                    WHERE newspaper = %d
#                        """ % (newspaper_id))
    cursor.connection.commit()
    
def delete_category(category_id):
    '''
    delete a category and all the articles and words from this category
    '''
    cursor.execute("""
                    DELETE FROM category
                    WHERE id = %d
                        """ % (category_id))
    
    cursor.execute(""" SELECT article_id FROM articles WHERE category = %d""" % category_id)
    res = cursor.fetchall()
    for i in res:
        article_id = i['article_id']
        delete_article(article_id)
    cursor.connection.commit()

def delete_writer(writer_id):
    '''
    delete_writer
    '''
    cursor.execute("""
                    DELETE FROM writers
                    WHERE id = "%s"
                        """ % (writer_id))
    
    articles_to_delete = []
    articles = get_all_articles()
    for art in articles:
        if writer_id in art["writers"]:
            articles_to_delete.append(art["article_id"])
    for art in articles_to_delete:
        delete_article(art)
    cursor.connection.commit()

def delete_phrase(phrase):
    '''
    delete_phrase
    '''
    cursor.execute("""
                    DELETE FROM phrases
                    WHERE phrase = "%s"
                        """ % (phrase))
    cursor.execute("""
                    DELETE FROM word
                    WHERE is_phrase = 1 AND word = "%s"
                        """ % (phrase))
    cursor.connection.commit()
######################################################################
### Complex functions
######################################################################  
def parse_a_file(path, article_id):
    '''
    get a file and parse all the words from it and add them to the db
    @param path: a path to the file
    @param article_id: a new article id
    '''
    f = open(path, "r")
    text = f.read()
    f.close()
    
    words = []
    par = text.split("\n\n")
    rows = 0
    offset = 0
    for par_number,paragraph in enumerate(par):
        cur_line = 0
        temp_rows = paragraph.split("\n")
        for row in temp_rows:
            cur_col = 0
            temp_words = split_with(row, WORD_SEP)
            for word in temp_words:
                add_word_to_DB(word, par_number, cur_line, rows, cur_col, article_id, offset, len(word))
                cur_col += len(word) + 1
                if len(word)>0 and word[-1] in line_sep:
                    cur_line += 1
                offset += len(word) + 1
            rows += 1
        rows += 1
        offset += 1
    phrases_list = [x["phrase"] for x in get_all_phrases()]
    for ph in phrases_list:
        add_phrase_shows(ph)
    cursor.connection.commit()

    
    
######################################################################
### Queries
######################################################################

class NoSuchRow(Exception):
    pass

class WrongCol(Exception):
    pass

class WordNotFound(Exception):
    pass

def find_word(row, col):
    '''
    find a word by a row and column
    '''
    if 0 == cursor.execute("SELECT word FROM word WHERE row = %d" % row):
        raise NoSuchRow()
    found = False
    cursor.execute("SELECT max(col) from word where row = %d"%row)
    max_col = cursor.fetchone()['max(col)']
    while not found:
        if col < 0 or col > max_col + 50:
            raise WrongCol()
        if 0 == cursor.execute("SELECT word FROM word WHERE row = %d and col = %d" % (row,col)):
            col -= 1
        else:
            found = True
    return cursor.fetchall()


def get_newspaper_name(num):
        '''
        get_newspaper_name
        '''
        cursor.execute("SELECT name FROM newspaper WHERE id = %d"%(num))
        return cursor.fetchone()["name"]
	
def get_category_name(num):
        '''
        get_category_name
        '''
        cursor.execute("SELECT name FROM category WHERE id = %d"%(num))
        return cursor.fetchone()["name"]
	
def get_writer_name(num):
        '''
        get_writer_name
        '''
        cursor.execute("SELECT name FROM writers WHERE id = %s"%(num))
        return cursor.fetchone()["name"]
    
def get_article_title(num):
    '''
    get_article_title
    '''
    cursor.execute("SELECT title FROM articles WHERE article_id = %s"%(num))
    output = cursor.fetchone()
    if output != None:
        return output["title"]
    
def get_article_path(num):
    '''
    get_article_path
    '''
    cursor.execute("SELECT path FROM articles WHERE article_id = %s"%(num))
    output = cursor.fetchone()
    if output != None:
        return output["path"]
    
def get_article_details(num):
        '''
        get_article_details
        '''
        cursor.execute("SELECT * FROM articles WHERE article_id = %s"%(num))
        return cursor.fetchone()
    
def get_words_in_group(num):
    '''
    get_words_in_group
    '''
    if group_id_exists(num):
        cursor.execute("SELECT word FROM word_in_group WHERE group_id = %d"%(num))
        return cursor.fetchall()

def get_related_couples(num):
    '''
    get_related_couples
     '''
    if relation_id_exists(num):
        cursor.execute("SELECT * FROM related_couples WHERE relation_id = %d"%(num))
        return cursor.fetchall()

def get_words_in_articles(articles_list, get_words = True, get_phrases = False):
    '''
    get_words_in_articles
    @param articles_list: from which articles
    @param get_words:  to get the words or not
    @param get_phrases: to get the phrases or not
    '''
    if False == get_words and False == get_phrases:
        return ()
    t_article_list = tuple(map(int,articles_list))
    if len(t_article_list) == 1:
        t_article_list = "(" + str(t_article_list[0]) + ")"
    else:
        t_article_list = str(t_article_list)
    fil = ""
    if get_words and False == get_phrases:
        cursor.execute("SELECT * from word WHERE article_id IN %s AND is_phrase = FALSE ORDER BY article_id, row, col" % (t_article_list))
    elif False == get_words and get_phrases:
        cursor.execute("SELECT * from word WHERE article_id IN %s AND is_phrase = TRUE ORDER BY article_id, row, col" % (t_article_list))
    else:
        cursor.execute("SELECT * from word WHERE article_id IN %s ORDER BY article_id, row, col" % (t_article_list))
    return cursor.fetchall()

def get_article_dictionary():
    '''
    get and article dict by article_id : article_title
    '''
    articles = get_all_articles()
    output = {}
    for a in articles:
        output[a["article_id"]] = a["title"]
    return output

def get_aritlces_with_filter(where_filter):
    '''
    get an articles with specific filter
    '''
    if "" == where_filter:
        return get_all_articles()
    cursor.execute("SELECT * FROM articles WHERE %s"%(where_filter))
    return cursor.fetchall()

def get_words_in_location(row = None, col = None, line = None, par = None, show_words = True, show_phrases = False, group_id = -1):
    '''
    get_words_in_location by row/col/par/line and if to show words or phrases or both
    '''
    if (row == "" or row == None) and\
       (col == "" or col == None) and\
       (line == "" or line == None) and\
       (par == "" or par == None) and\
       group_id == -1:
        return ()
    fil = ""
    if row != "" and row != None:
        if fil != "":
            fil += " AND "
        fil += "word.row = %d" % (int(row))
    if col != "" and col != None:
        if fil != "":
            fil += " AND "
        fil += "word.col = %d" % (int(col))
    if line != "" and line != None:
        if fil != "":
            fil += " AND "
        fil += "word.line = %d" % (int(line))
    if par != "" and par != None:
        if fil != "":
            fil += " AND "
        fil += "word.paragraph = %d" % (int(par))
    if show_words == True and show_phrases == False:
        if fil != "":
            fil2 = " AND word.is_phrase = False"
        else:
            fil2 = "word.is_phrase = False"
    elif show_words == False and show_phrases == True:
        if fil != "":
            fil2 = " AND word.is_phrase = True"
        else:
            fil2 ="word.is_phrase = True"
    else:
        fil2 = ""

    fil3 = ""
    if group_id != -1:
        fil3 = " AND word_in_group.group_id = %d" % (group_id)
                
    if fil + fil2 + fil3 == "":
        output = ""
    else:
        output = "WHERE %s" % (fil + fil2 + fil3)
    
    if group_id != -1:
        cursor.execute("""
        SELECT word.word, word.article_id, word.paragraph, word.line, word.row, word.col, word.offset, word.full_len, word.is_phrase
        FROM word
        INNER JOIN word_in_group
        ON word.word = word_in_group.word
        %s"""%(output))
    else:
        cursor.execute("SELECT * FROM word %s" % (output))
    return cursor.fetchall()

def is_word_in_article(word, article_id):
    '''
    is_word_in_article
    '''
    return (0 < cursor.execute('SELECT * from word WHERE word = "%s" AND article_id = %d' % (word.lower(), article_id)))

def get_specific_word_in_article(word, article_id):
    '''
    get_specific_word_in_article
    '''
    cursor.execute('SELECT * from word WHERE word = "%s" AND article_id = %d' % (word.lower(), article_id))
    return cursor.fetchall()

def get_words_in_group_for_table(num):
    if group_id_exists(num):
        cursor.execute("""
                        SELECT word.word, word.article_id, word.paragraph, word.line, word.row, word.col, word.offset, word.full_len, word.is_phrase
                        FROM word
                        INNER JOIN word_in_group
                        ON word.word = word_in_group.word
                        WHERE word_in_group.group_id = %d""" % (num))
        return cursor.fetchall()
######################################################################
### "get all" Queries
######################################################################
def get_all_articles():
    '''
    get_all_articles
    '''
    cursor.execute("SELECT * FROM articles")
    return cursor.fetchall()

def get_all_writers():
        '''
        get_all_writers
        '''
        cursor.execute("SELECT * FROM writers")
        return cursor.fetchall()

def get_all_groups():
    '''
    get_all_groups
    '''
    cursor.execute("SELECT * FROM groups")
    return cursor.fetchall()


def get_all_relations():
    '''
    get_all_relations
    '''
    cursor.execute("SELECT * FROM relation")
    return cursor.fetchall()
    
def get_all_related_couples():
    '''
    get_all_related_couples
    '''
    cursor.execute("SELECT * FROM related_couples")
    return cursor.fetchall()

def get_all_newspapers():
    '''
    get_all_newspapers
    '''
    cursor.execute("SELECT * FROM newspaper")
    return cursor.fetchall()
    
def get_all_categories():
    '''
    get_all_categories
    '''
    cursor.execute("SELECT * FROM category")
    return cursor.fetchall()

def get_all_phrases():
    '''
    get_all_phrases
    '''
    cursor.execute("SELECT * FROM phrases")
    return cursor.fetchall()


def edit_article_values(article_id, path, newspaper, page, date, 
                        writers, title, category):
    '''
    edit_article_values
    '''
    path = os.path.abspath(path).replace("\\", "\\\\")
    if article_exists(path):
        raise Exception("Article with that path already exists")
    if not newspaper_exists(newspaper):
        raise "No such newspaper"
    writers_set = set(writers.split(","))
    writers_list = []
    for i in writers_set:
        try:
            writers_list.append(i)
        except:
            raise "writers_list append error"
    for i in writers_list:
        if not writer_exists(i):
            raise "no such writer: %s"%(i)
    writers_output = ""
    for i in writers_list:
        writers_output = writers_output + i + ","
    if writers_output != "":
        writers_output = writers_output[:-1]
    if not category_exists(category):
        raise "No such category"
    cursor.execute("""
                    UPDATE articles
                    SET path="%s", newspaper = %d, page = %d, date = "%s", writers = "%s", title = "%s", category = %d
                    WHERE article_id = %d
                """ % (path, newspaper, page, date,\
                       writers_output, title, category, article_id))

def normalize_uni(word):
    '''
    remove the unicode from the word
    '''
    return word
    tr =  { 0x2018:0x27, 0x2019:0x27, 0x201C:0x22, 0x201D:0x22, ord("’"):ord("'"), ord("“"):ord('"'), ord('”'):ord('"')}
    word = unicode(word)
    return word.translate(tr).encode("ascii", "ignore")
