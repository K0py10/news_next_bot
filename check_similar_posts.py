import sqlite3
import simularity_handler as sh
import ds_handler as ds_h
# from classes import post

con = sqlite3.connect('dataset.sql')
cur = con.cursor()
cutoff = 0.4

posts = ds_h.get_all_posts(con, -1)
print("MAIN POST:" + posts[1].text)
print("================================")
for post in sh.find_similar_posts(posts[1].lem_text, posts, cutoff):
    print(post.id)
    print(post.text)


# for post in posts:
#     print("MAIN POST:" + post.text)
#     print("================================")
#     res = sh.compare_post_to_posts(post, posts, cutoff)
#     for post in res:
#         print(post.text)