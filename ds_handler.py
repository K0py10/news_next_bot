import sqlite3 as sql
import csv
from vectoriser import vectorize_multiple
from classes import post_from_ds

channels_list = ["@novosti_voinaa", 
                 "@truexanewsua", 
                 "@rian_ru", 
                 "@readovkanews", 
                 "@bbbreaking", 
                 "@ostorozhno_novosti", 
                 "@voynareal", 
                 "@wargonzo", 
                 "@nexta_live", 
                 "@meduzalive", 
                 "@pravdadirty", 
                 "@varlamov_news"]        

def get_channel_posts(con, channel, batch_size): #batch_size == -1 => no limit 
    cur = con.cursor()
    res = []
    if batch_size > 0: #fetch limited amount of posts
        for row in cur.execute("SELECT * FROM posts WHERE channel = ?", (channel,)).fetchmany(batch_size):
            print(str(row))
            res.append(post_from_ds(row[1], row[2]))
    else: #fetch all posts
        for row in cur.execute("SELECT * FROM posts WHERE channel = ?", (channel,)).fetchall():
            print(str(row))
            res.append(post_from_ds(row[1], row[2]))
    return res

def get_min_batch(con):
    cur = con.cursor()
    min = 100
    for channel in channels_list:
        ch_batch = len(cur.execute("SELECT * FROM posts WHERE channel = ?", (channel,)).fetchall())
        if ch_batch < min:
            min = ch_batch
    return min

def get_one_post(con):
    cur = con.cursor()
    ds_post = cur.execute("SELECT * FROM posts").fetchmany()[0]
    res = post_from_ds(ds_post[1], ds_post[2])
    return res

def get_all_posts(con, exclude):
    cur = con.cursor()
    res = []
    for post in cur.execute("SELECT * FROM posts").fetchall():
        res.append(post_from_ds(post[1], post[2]))
    if exclude != -1:
        for i in range(exclude):
            res.pop(0)
    return res

def vectorise_all(con, destination):
    with open(destination, 'w', newline = '') as file:
        writer = csv.writer(file)
        posts = get_all_posts(con, -1)
        writer.writerows(vectorize_multiple(posts))


def save_vector(vector, writer):
    writer.writerow(vector)

def get_all_vectors(filename):
    with open(filename, 'r', newline = '') as file:
        res = []
        reader = csv.reader(file)
        for row in reader:
            res.append(row)
        return res