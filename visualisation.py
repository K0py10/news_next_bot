import matplotlib.pyplot as plt
from classes import post, post_from_ds
from vectoriser import vectorize_multiple, compare_vectors
from ds_handler import *
import numpy as np
import sqlite3

con = sqlite3.connect("dataset.sql")

vectorise_all(con, 'vectors.csv')
vectors_list = get_all_vectors("vectors.csv")

base_post = get_one_post(con)
base_post = post(base_post.channel, base_post.text, vectors_list[0])
print(base_post.vector)

compare_posts = get_all_posts(con, 1)
# compare_posts_embed = vectorize_multiple(compare_posts)
for i in range(len(compare_posts)):
     compare_posts[i] = post(compare_posts[i].channel, compare_posts[i].text, vectors_list[i + 1])

diffs = []
for pt in compare_posts:
    diffs.append(compare_vectors(base_post.vector, pt.vector))
    print(diffs[-1])

print(base_post.text)
print(compare_posts[min(diffs.astype(int))].text)

plt.style.use('_mpl-gallery')

# plot
fig, ax = plt.subplots()
ax.bar(float(len(diffs)), diffs, width=1, edgecolor="white")
ax.bar([i for i in range(len(diffs))], diffs)
# ax.set(xlim=(0, 8), xticks=np.arange(1, 8),
#        ylim=(0, 8), yticks=np.arange(1, 8))

plt.show()