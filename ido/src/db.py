import MySQLdb as sql
import sys
HOST = 'localhost'
USER = 'root'
PASSWD = '123'
DB = 'MySQL'
MAX_NUM_OF_WRITERS_PER_ARTICLE = 4
cursor = None
def get_cursor():
    global cursor
    if cursor is None:
        try:
            con = sql.Connection(host = HOST, user = USER, 
                           passwd = PASSWD , db = DB)
        except sql.Error, e:
            print "Error %d: %s" % (e.args[0], e.args[1])
            sys.exit (1)
    
        cursor = con.cursor(sql.cursors.DictCursor)
    
    return cursor

def init_db():
    cursor = get_cursor()
    try:
        cursor.execute(""" DROP TABLE   articles,
                                    newspaper,
                                    writers,
                                    category,
                                    word,
                                    groups,
                                    word_in_group,
                                    relation,
                                    related_couples,
                                    counter_values,
                                    phrases""")
    except:
        pass


    cursor.execute("""
                CREATE TABLE counter_values
                (
                name CHAR(80) NOT NULL,
                value INT
                )
                """
                   )

    cursor.execute("""
                CREATE TABLE articles
                (
                article_id INT,
                path CHAR(80) NOT NULL,
                newspaper INT,
                page INT,
                date DATE,
                writers CHAR(%d),
                title CHAR(128),
                category INT
                )
                """ % (MAX_NUM_OF_WRITERS_PER_ARTICLE * 11)
                   )

    cursor.execute("""
                CREATE TABLE newspaper
                (
                id INT NOT NULL,
                name CHAR(40)
                )
                """
                   )

    cursor.execute("""
                CREATE TABLE writers
                (
                id CHAR(10) NOT NULL,
                name CHAR(40),
                date_of_birth DATE
                )
                """
                   )

    cursor.execute("""
                CREATE TABLE category
                (
                id INT NOT NULL,
                name CHAR(40)
                )
                """
                   )

    cursor.execute("""
                CREATE TABLE word
                (
                word CHAR(60) NOT NULL,
                article_id INT,
                
                paragraph INT,
                line INT,
                
                row INT,
                col INT,

                offset INT,
				full_len INT,

                is_phrase BOOL
                )
                """
                   )


    cursor.execute("""
                CREATE TABLE groups
                (
                id INT NOT NULL,
                name CHAR(40)
                )
                """
                   )

    cursor.execute("""
                CREATE TABLE word_in_group
                (
                word CHAR(40) NOT NULL,
                group_id INT NOT NULL
                )
                """
                   )

    cursor.execute("""
                CREATE TABLE relation
                (
                id INT NOT NULL,
                name CHAR(40)
                )
                """
                   )

    cursor.execute("""
                CREATE TABLE related_couples
                (
                word1 CHAR(40) NOT NULL,
                word2 CHAR(40) NOT NULL,
                relation_id INT NOT NULL
                )
                """
                   )
    
    cursor.execute("""
                CREATE TABLE phrases
                (
                phrase CHAR(80) NOT NULL
                )
                """
                   )

if __name__ == '__main__':
    init_db()
