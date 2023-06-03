import sqlite3
import classes

def restart_db(cur):
    cur.execute("DROP TABLE IF EXISTS channels")
    cur.execute("CREATE TABLE channels(id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, last_message INTEGER NOT NULL)")
    cur.execute("DROP TABLE IF EXISTS subs")
    cur.execute("CREATE TABLE subs(chat_id INTEGER NOT NULL, channel INTEGER NOT NULL REFERENCES channels(id))")
    cur.execute("DROP TABLE IF EXISTS posts")
    cur.execute("CREATE TABLE posts (id INTEGER PRIMARY KEY AUTOINCREMENT, channel INTEGER NOT NULL REFERENCES channels(id), text TEXT NOT NULL, lem_text TEXT NOT NULL)")
    cur.execute("DROP TABLE IF EXISTS chat_posts")
    cur.execute("CREATE TABLE chat_posts (chat_id INTEGER NOT NULL, post INTEGER NOT NULL REFERENCES posts(chat_id))")
    cur.connection.commit()

def save_channel(cur, name, last_message, chat_id):
    channel_id = cur.execute("SELECT id FROM channels WHERE name = ? LIMIT 1", (name,)).fetchmany() 
    if channel_id == []: #adding channel to channels table if it doesn't exist
        channel = {'name' : name, 'last_message' : last_message}
        cur.execute("INSERT INTO channels (name, last_message) VALUES (:name, :last_message)", channel)
        channel_id = cur.execute("SELECT id FROM channels ORDER BY id DESC LIMIT 1").fetchmany()
    
    cur.execute("INSERT INTO subs (chat_id, channel) VALUES (:chat_id, :channel)", {'chat_id': chat_id, 'channel': channel_id[0][0]}) #adding subscription
    cur.connection.commit()

def get_all_channels(cur):
    res = []
    for row in cur.execute("SELECT * FROM channels"):
        res.append(classes.channel(row[0], row[1], row[2]))
        #print(row)
    return res

def update_last_message(cur, id, last_message):
    cur.execute("UPDATE channels SET last_message = ? WHERE id = ?", (last_message, id))
    cur.connection.commit()

def get_channel_subs(cur, channel_id):
    res = []
    for row in cur.execute("SELECT chat_id FROM channels INNER JOIN subs ON channels.id = subs.channel WHERE channel_id = ?", (channel_id,)):
        res.append(row[0])
    return res


def save_post(cur, channel_id, text, lem_text):
    cur.execute("INSERT INTO posts (channel_id, text, lem_text) VALUES (:channel_id, :text, :lem_lext)", {"channel_id": channel_id, "text": text, "lem_text": lem_text})
    cur.connection.commit()
    return cur.execute("SELECT id FROM POSTS ORDER BY id DESC LIMIT 1").fetchmany()[0][0]

def add_post_to_chat(cur, chat_id, post_id):
    cur.execute("INSERT INTO chat_posts (chat_id, post) VALUES (:chat_id, :post)", {"chat_id": chat_id, "post": post_id})
    cur.connection.commit()