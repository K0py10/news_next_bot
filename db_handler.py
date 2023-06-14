import sqlite3
import classes

con = sqlite3.connect('db.sql')
cur = con.cursor()

def restart_db():
    cur.execute("DROP TABLE IF EXISTS channels")
    cur.execute("CREATE TABLE channels(id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, last_message INTEGER NOT NULL)")
    cur.execute("DROP TABLE IF EXISTS subs")
    cur.execute("CREATE TABLE subs(user INTEGER NOT NULL REFERENCES users(chat), channel INTEGER NOT NULL REFERENCES channels(id))")
    cur.execute("DROP TABLE IF EXISTS posts")
    cur.execute("CREATE TABLE posts (id INTEGER PRIMARY KEY AUTOINCREMENT, channel INTEGER NOT NULL REFERENCES channels(id), lem_text TEXT NOT NULL)")
    cur.execute("DROP TABLE IF EXISTS user_posts")
    cur.execute("CREATE TABLE user_posts (user INTEGER NOT NULL REFERENCES users(chat), id INTEGER NOT NULL, text TEXT NOT NULL, post INTEGER NOT NULL REFERENCES posts(chat_id))")
    cur.execute("DROP TABLE IF EXISTS users")
    cur.execute("CREATE TABLE users (chat INTEGER PRIMARY KEY, lang VARCHAR(4) NOT NULL, shorten_msgs INTEGER NOT NULL, del_sim INTEGER NOT NULL)")
    cur.connection.commit()

def save_channel(name, last_message, chat_id):
    channel_id = cur.execute("SELECT id FROM channels WHERE name = ? LIMIT 1", (name,)).fetchmany() 
    if channel_id == []: #adding channel to channels table if it doesn't exist
        channel = {'name' : name, 'last_message' : last_message}
        cur.execute("INSERT INTO channels (name, last_message) VALUES (:name, :last_message)", channel)
        channel_id = cur.execute("SELECT id FROM channels ORDER BY id DESC LIMIT 1").fetchmany()
    if cur.execute("SELECT * FROM subs WHERE user = :chat AND channel = :channel_id", {'chat' : chat_id, "channel_id" : channel_id[0][0]}).fetchmany() == []: #checking if user is already subscribed
        cur.execute("INSERT INTO subs (user, channel) VALUES (:chat_id, :channel)", {'chat_id': chat_id, 'channel': channel_id[0][0]}) #adding subscription
        cur.connection.commit()
        return True
    else:
        cur.connection.commit()
        return False
def unsubscribe(channel, chat):
    channel_id = cur.execute("SELECT id FROM channels WHERE name = ?", (channel,)).fetchmany()
    if channel_id != []:
        if cur.execute("SELECT * FROM subs WHERE user = :chat AND channel = :channel", {'chat': chat, 'channel': channel_id[0][0]}).fetchmany() != []: #checking if user is already subscribed
            cur.execute("DELETE FROM subs WHERE user = :chat AND channel = :channel", {'chat': chat, 'channel': channel_id[0][0]})
            con.commit()
            return True
        else:
            return False
    else:
        return False
def get_all_channels():
    res = []
    for row in cur.execute("SELECT * FROM channels"):
        res.append(classes.channel(row[0], row[1], row[2]))
        #print(row)
    
    return res
def update_last_message(id, last_message):
    cur.execute("UPDATE channels SET last_message = ? WHERE id = ?", (last_message, id))
    cur.connection.commit()
def get_channel_subs(channel_id):
    res = []
    for row in cur.execute("SELECT subs.user FROM channels INNER JOIN subs ON channels.id = subs.channel WHERE channel = ?", (channel_id,)):
        res.append(row[0])
    return res
def save_post(channel_id, lem_text):
    same_post_id = cur.execute("SELECT id FROM posts WHERE lem_text = ?", (lem_text,)).fetchmany()
    if same_post_id == []:
        cur.execute("INSERT INTO posts (channel, lem_text) VALUES (:channel_id, :lem_lext)", {"channel_id": channel_id, "lem_lext": lem_text})
        cur.connection.commit()
        return cur.execute("SELECT id FROM POSTS ORDER BY id DESC LIMIT 1").fetchmany()[0][0]
    else:
        return same_post_id[0][0]
def get_all_posts():
    res = []
    for row in cur.execute("SELECT * FROM posts"):
        res.append(classes.post(row[0], row[1], row[2]))
    return res
def add_post_to_chat(chat, id, text, posts_id):
    cur.execute("INSERT INTO user_posts (user, id, text, post) VALUES (:chat, :id, :text, :post)", {"chat": chat, "id": id, "text": text, "post": posts_id})
    cur.connection.commit()
def get_chat_post_ids(chat_id):
    res = []
    for row in cur.execute("SELECT post FROM user_posts WHERE user = ?", (chat_id,)).fetchall():
        res.append(row[0])
    return res
def get_chats_posts(chats):
    res = []
    check_ids = []
    ch_chats = '(' + str(chats[0])
    for i in range(1, len(chats)):
        ch_chats += ', ' + str(chats[i])
    ch_chats += ' )'
    for row in cur.execute(f"SELECT posts.id, posts.channel, posts.lem_text FROM user_posts INNER JOIN posts ON user_posts.post = posts.id WHERE user_posts.user IN {ch_chats}"):
        if row[0] not in check_ids:
            res.append(classes.post(row[0], row[1], row[2]))
            check_ids.append(row[0])
    return res
def get_chat_post(chat, post_id):
    for row in cur.execute("SELECT id, text FROM user_posts WHERE user = ? AND post = ?", (chat, post_id)):
        res = classes.message(chat, row[0], row[1])
    return res
def get_user_channels(user):
    res = []
    for row in cur.execute("SELECT channels.name FROM subs INNER JOIN channels ON channels.id = subs.channel WHERE subs.user = ?", (user,)):
        res.append(row[0])
    return res
def update_chat_message(message, text):
    cur.execute("UPDATE user_posts SET text = :text WHERE user = :chat AND id = :id", {"text": text, "chat": message.chat, "id": message.id})
    con.commit()
def delete_chat_message(id):
    cur.execute("DELETE * FROM user_posts WHERE id = ?", (id,))
    con.commit()
def delete_user_messages(chat):
    cur.execute("DELETE * FROM user_posts WHERE user = ?", (chat,))
    con.commit()
def add_user(chat):
    if cur.execute("SELECT * FROM users WHERE chat = ?", (chat,)).fetchall() == []:
        cur.execute("INSERT INTO users (chat, lang, shorten_msgs, del_sim) VALUES (:chat, :lang, :shorten_msgs, :del_sim)", {"chat": chat, "lang": 'null', "shorten_msgs": 1, 'del_sim' : 1})
        con.commit()
def get_user(chat):
    res = 0
    for row in cur.execute("SELECT chat, lang, shorten_msgs, del_sim FROM users WHERE chat = ?", (chat,)).fetchall():
        res = classes.user(row[0], row[1], row[2], row[3])
    if res != 0:
        return res
    else:
        add_user(chat)
        return classes.user(0, 'null', 1, 1)
def get_all_users():
    res = []
    for row in cur.execute("SELECT user FROM subs").fetchall():
        if row[0] not in res:
            res.append(row[0])
    return res
def change_user_lang(chat, lang):
    cur.execute("UPDATE users SET lang = :lang WHERE chat = :chat", {'chat': chat, 'lang': lang})
    con.commit()
def change_user_del_sim(chat):
    if cur.execute("SELECT del_sim FROM users WHERE chat = ?", (chat,)).fetchmany()[0][0] == 1:
        cur.execute("UPDATE users SET del_sim = 0 WHERE chat = ?", (chat,))
    else:
        cur.execute("UPDATE users SET del_sim = 1 WHERE chat = ?", (chat,))
    con.commit()
def change_shorten_msgs(chat, set):
    cur.execute("UPDATE users SET shorten_msgs = :set WHERE chat = :chat",  {'chat': chat, 'set': set})
    con.commit()
def delete_user(chat):
    cur.execute("DELETE FROM user_posts WHERE user = ?", (chat,))