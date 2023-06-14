import sqlite3
import analyser as sh
import ds_handler as ds_h
from unused.vectoriser import *
# from classes import post

con = sqlite3.connect('dataset.sql')
cur = con.cursor()
cutoff = 0.4

posts = ds_h.get_all_posts(con, -1)
embeddings = vectorize_multiple(posts)

print("MAIN POST:" + posts[801].text)
print("================================")
for i in range(len(posts)):
    sim = compare_vectors(embeddings[801], embeddings[i])
    if sim > cutoff:
        print(posts[i].text)
        print(sim)
        print("================================")
# for post in sh.find_similar_posts(posts[801].lem_text.split(' '), posts, cutoff):
#     print(post.id)
#     print(post.text)

