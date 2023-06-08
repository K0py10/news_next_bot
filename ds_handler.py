import sqlite3 as sql
import csv
#from unused.vectoriser import vectorize_multiple
from classes import ds_post
from simularity_handler import prepare_text

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
            res.append(ds_post(row[0], row[1], row[2]))
    else: #fetch all posts
        for row in cur.execute("SELECT * FROM posts WHERE channel = ?", (channel,)).fetchall():
            print(str(row))
            res.append(ds_post(row[0], row[1], row[2]))
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
    res = ds_post(ds_post[0], ds_post[1], ds_post[2], ds_post[3])
    return res

def get_all_posts(con, exclude):
    cur = con.cursor()
    res = []
    for dspost in cur.execute("SELECT * FROM posts").fetchall():
        res.append(ds_post(dspost[0], dspost[1], dspost[2], dspost[3]))
    if exclude != -1:
        for i in range(exclude):
            res.pop(0)
    return res

# def vectorise_all(con, destination):
#     with open(destination, 'w', newline = '') as file:
#         writer = csv.writer(file)
#         posts = get_all_posts(con, -1)
#         writer.writerows(vectorize_multiple(posts))


# def save_vector(vector, writer):
#     writer.writerow(vector)

# def get_all_vectors(filename):
#     with open(filename, 'r', newline = '') as file:
#         res = []
#         reader = csv.reader(file)
#         for row in reader:
#             res.append(row)
#         return res


# con = sql.connect("dataset.sql")
# cur = con.cursor()

# cur.execute("DROP TABLE IF EXISTS posts2")
# con.commit()

# cur.execute("DROP TABLE IF EXISTS posts")
# cur.execute("CREATE TABLE posts (id INTEGER PRIMARY KEY AUTOINCREMENT, channel VARCHAR(16), text VARCHAR(4096), lem_text VARCHAR(4096))")
# for row in cur.execute('SELECT * FROM posts2').fetchall():
#     cur.execute("INSERT INTO posts (channel, text, lem_text) VALUES (:channel, :text, :lem_text)", {"channel": row[1], "text": row[2], "lem_text" : row[3]})

# for row in cur.execute("SELECT * FROM posts2").fetchall():
#     for data in row:    
#         print(data)
# con.commit()

# cur.execute("DROP TABLE IF EXISTS posts2")
# cur.execute("CREATE TABLE posts2 (id INTEGER PRIMARY KEY AUTOINCREMENT, channel VARCHAR(16), text VARCHAR(4096), lem_text VARCHAR(4096))")
# for row in cur.execute("SELECT * FROM posts").fetchall():
#     # print(row)
#     lem_text = ' '.join(prepare_text(row[2]))
#     cur.execute("INSERT INTO posts2 (id, channel, text, lem_text) VALUES (:id, :channel, :text, :lem_text)", {'id': row[0], 'channel': row[1], 'text': row[2], 'lem_text' : lem_text})
# for row in cur.execute("SELECT * FROM posts2").fetchall():
#     for data in row:
#         print(data)
# con.commit()
