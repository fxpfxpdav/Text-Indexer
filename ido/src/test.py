execfile("db.py")
execfile("funcs.py")
ART_PATH = "c:\\\\project\\\\articles\\\\"

add_a_newspaper("Yediot Aharonot")
add_a_newspaper("Maariv")
add_a_newspaper("Jerusalem Post")
add_a_newspaper("Haaretz")


add_a_category("Sports")
add_a_category("Internal news")
add_a_category("Foreign news")
add_a_category("Opinions")


add_a_writer("820082008", "Roee Nahmias", "1978-12-05")
add_a_writer("12344321", "Eli Senyor", "1983-04-07")
add_a_writer("015336027", "Allon Sinai", "1957-06-23")
add_a_writer("345665432", "Michelle Keren", "1973-02-26")
add_a_writer("987667895", "Doron Rosenblum", "1947-03-16")


add_an_article("Damascus summit: Assad, Ahmadinejad, Nasrallah",\
               ART_PATH + "damascus_summit.txt", 1, 2, "2010-02-26", "820082008", 3)
             
add_an_article("Man gets marijuana surprise",\
               ART_PATH + "marijuana.txt", 1, 18, "2010-02-25", "12344321", 2)

add_an_article("Yoni/Andy reunited ahead of Davis Cup", ART_PATH + "andy.txt",\
               3, 17, "2010-02-24", "015336027,345665432", 1)

add_an_article("Every day is Purim", ART_PATH + "purim.txt",\
               4, 16, "2010-02-25", "987667895", 4)


a = add_a_group("countries")
b = add_a_group("location descriptors")
add_word_to_group("israel", a)
add_word_to_group("iran", a)
add_word_to_group("on", b)
add_word_to_group("in", b)
add_word_to_group("at", b)
add_word_to_group("under", b)

c = add_a_relation("opposites")
d = add_a_relation("synonyms")
add_a_related_couple("short", "tall", c)
add_a_related_couple("happy", "sad", c)
add_a_related_couple("fat", "overweight", d)
add_a_phrase("at the")


con.commit()

