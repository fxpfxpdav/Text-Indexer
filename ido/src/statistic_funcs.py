from funcs import *

def youngest_writer():
    cursor.execute("SELECT * FROM writers WHERE date_of_birth = (SELECT MAX(date_of_birth) from writers)")
    return cursor.fetchone()

def oldest_writer():
    cursor.execute("SELECT * FROM writers WHERE date_of_birth = (SELECT MIN(date_of_birth) from writers)")
    return cursor.fetchone()

def best_writer():
    #return only one =/
    cursor.execute("select writers from articles")
    res = cursor.fetchall()
    writers = {}
    for i in res:
        temp_writers = i['writers'].split(',')
        for w in temp_writers:
            if writers.has_key(w):
                writers[w] += 1
            else:
                writers[w] = 1


    maximum = 0
    best = ""
    for wr in writers.keys():
        if writers[wr] > maximum:
            maximum = writers[wr]
            best = wr

    cursor.execute('SELECT * FROM writers WHERE id = "%s"' % best)
    return cursor.fetchone(), maximum

def best_newspaper():
    cursor.execute("SELECT id FROM newspaper")
    ids = cursor.fetchall()
    ids = [i["id"] for i in ids]
    maximum = 0
    best = ""
    for newsId in ids:
        cursor.execute("SELECT COUNT(*) FROM articles WHERE newspaper =%d"%newsId)
        num = cursor.fetchone()["COUNT(*)"]
        if num > maximum:
            maximum = num
            best = newsId

    cursor.execute("SELECT name FROM newspaper WHERE id = %d" %best)
    return cursor.fetchone()['name'], maximum

def longest_word():
    cursor.execute("SELECT * FROM word WHERE length(word) = (SELECT max(length(word)) FROM word WHERE is_phrase = 0) AND is_phrase = 0")
    return cursor.fetchone()

def longest_phrase():
    cursor.execute("SELECT * FROM word WHERE length(word) = (SELECT max(length(word)) FROM word WHERE is_phrase = 1) AND is_phrase = 1")
    return cursor.fetchone()


def word_in_groups():
    cursor.execute("SELECT * FROM word_in_group")
    words_in_groups = cursor.fetchall()
    maximum = 0
    best = []
    for i in words_in_groups:
        word = i['word']
        cursor.execute('SELECT COUNT(*) FROM word WHERE word = "%s" ' % word)
        num = cursor.fetchone()["COUNT(*)"]
        if num > maximum:
            maximum = num
            best = [word]
        elif num == maximum:
            best.append(word)
    return best
    
def best_category():
    cursor.execute("SELECT * FROM category")
    categories = cursor.fetchall()
    maximum = 0
    best = []
    for i in categories:
        id = i['id']
        category = i["name"]
        cursor.execute('SELECT COUNT(*) FROM articles WHERE category = %d ' % id)
        num = cursor.fetchone()["COUNT(*)"]
        if num > maximum:
            maximum = num
            best = [category]
        elif num == maximum:
            best.append(category)
        
    return best

def longest_article():
    cursor.execute("SELECT article_id,COUNT(*) FROM word group by article_id")
    words_in_article = cursor.fetchall()
    maximum = 0
    best = -1
    for i in words_in_article:
        article_id = i['article_id']
        num = i["COUNT(*)"]
        if num > maximum:
            maximum = num
            best = article_id

        
    cursor.execute("SELECT title FROM articles WHERE article_id = %d" %best)
    return cursor.fetchone()['title']

def avg_words_in_article():
    cursor.execute("SELECT COUNT(*) FROM word group by article_id")
    words_in_article = cursor.fetchall()
    sum = 0
    for i in words_in_article:
        sum += i["COUNT(*)"]

    return float(sum) / len(words_in_article)
    
def avg_lines_in_article():
    cursor.execute("SELECT max(row) FROM word group by article_id")
    lines_in_article = cursor.fetchall()
    sum = 0
    for i in lines_in_article:
        sum += i["max(row)"]

    return float(sum) / len(lines_in_article)

def avg_word_in_line():
    return float(avg_words_in_article()) / avg_lines_in_article()
        
def first_article():
    cursor.execute("SELECT * FROM articles WHERE date = (SELECT MIN(date) from articles)")
    return cursor.fetchone()

def last_article():
    cursor.execute("SELECT * FROM articles WHERE date = (SELECT MAX(date) from articles)")
    return cursor.fetchone()

def best_related():
    cursor.execute("SELECT * FROM related_couples")
    relations = cursor.fetchall()
    maximum = 0
    best = []
    for i in relations:
        word1 = i ['word1']
        word2 = i ['word2']
        cursor.execute('SELECT COUNT(*) FROM word WHERE word = "%s" OR word = "%s" ' % (word1, word2))
        num = cursor.fetchone()["COUNT(*)"]
        if num > maximum:
            maximum = num
            best = [(word1,word2)]
        elif num == maximum:
            best.append((word1,word2))
    
    return best

def shortest_article():
    cursor.execute("SELECT article_id,COUNT(*) FROM word group by article_id")
    words_in_article = cursor.fetchall()
    if words_in_article is None or len(words_in_article) ==0 :
        return None
    minimum =  words_in_article[0]["COUNT(*)"]
    best = words_in_article[0]["article_id"]
    for i in words_in_article:
        article_id = i['article_id']
        num = i["COUNT(*)"]
        if num < minimum:
            maximum = num
            best = article_id

        
    cursor.execute("SELECT title FROM articles WHERE article_id = %d" %best)
    return cursor.fetchone()['title']

def shortest_word():
    cursor.execute('SELECT min(length(word)) FROM word WHERE is_phrase = 0')
    length =  cursor.fetchone()['min(length(word))']
    cursor.execute("SELECT * FROM word WHERE length(word) = %d AND is_phrase = 0" %length)
    return cursor.fetchone()['word'], length

def avg_word():
    num_words = cursor.execute('SELECT distinct word FROM word ')
    words = cursor.fetchall()
    sum= 0
    for i in words:
        sum += len(i['word'])
    return float(sum) / float(num_words)
    
def best_word():
    cursor.execute("SELECT word FROM word")
    words = cursor.fetchall()
    d = {}
    max = -1
    for i in words:
        d[i['word']] = d.get(i['word'],0) + 1   
    for k,v in d.iteritems():
        if v>max:
            max = v
            best = k
    return best, max
    
def longest_article_in_category():
    cursor.execute("SELECT * FROM category")
    temp_categories = cursor.fetchall()
    cursor.execute("SELECT article_id, COUNT(*) FROM word group by article_id")
    words_count = cursor.fetchall()
    d = {}
    for i in words_count:
        cursor.execute("SELECT * FROM articles WHERE article_id = %d " % i["article_id"])
        article = cursor.fetchone()
        category = article['category']
        d[category] = d.get(category,[])
        d[category].append(i["COUNT(*)"])

    max = -1
    category_best = None
    for category in d.keys():
        category_sum = sum(d.get(category, [])) / float(len(d[category]))
        if category_sum > max:
            category_best = category
    
    for i in temp_categories:
        if i["id"] == category_best:
            return i["name"], max
        
    return None,None
    
def hofrim_articles():
    cursor.execute("SELECT article_id,COUNT(*) FROM word group by article_id")
    words_in_article = cursor.fetchall()
    HOFRIM = 500
    sum = 0
    for i in words_in_article:
        num = i["COUNT(*)"]
        if num > HOFRIM:
            sum += 1

        
    return sum
    

def short_articles():
    cursor.execute("SELECT article_id,COUNT(*) FROM word group by article_id")
    words_in_article = cursor.fetchall()
    SHORT = 100
    sum = 0
    for i in words_in_article:
        num = i["COUNT(*)"]
        if num < SHORT:
            sum += 1

        
    return sum

def most_words_in_newspaper():
    cursor.execute("SELECT * FROM newspaper")
    newspapers_temp = cursor.fetchall()
    cursor.execute("SELECT article_id, COUNT(*) FROM word group by article_id")
    words_in_article = cursor.fetchall()
    d = {}
    for i in words_in_article:
        cursor.execute("SELECT newspaper FROM articles WHERE article_id = %d" % i['article_id'])
        newspaper = cursor.fetchone()['newspaper']
        d[newspaper] = d.get(newspaper,0) + i['COUNT(*)']
    
    dd = {}
    for i in newspapers_temp:
        dd[i["id"]] = i['name']
    return dd[newspaper]
    
    