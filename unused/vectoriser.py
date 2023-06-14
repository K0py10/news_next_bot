import pkgutil
import torch
from transformers import BertTokenizer, BertModel, BertConfig
import matplotlib.pyplot as plt
import sqlite3 as sql
import numpy as np
from numpy.linalg import norm
# from classes import post_from_ds
        

def vectorize_multiple(posts_list):
    # Load the BERT tokenizer and configuration
    tokenizer = BertTokenizer.from_pretrained('bert-base-multilingual-cased')
    config = BertConfig.from_pretrained('bert-base-multilingual-cased')
    config.max_position_embeddings = 2048 # Increase the maximum sequence length
    config.model_max_length = 2048 
    # Load the BERT model with the modified configuration
    model = BertModel.from_pretrained('bert-base-multilingual-cased', config=config, ignore_mismatched_sizes=True)
    res = []
    for post in posts_list:
        res.append(get_bert_embedding(post.text, model, tokenizer))
    return res


def get_bert_embedding(text, model, tokenizer):
    print("Started tokenizing")

    # Tokenize input text
    input_ids = torch.tensor(tokenizer.encode(text)).unsqueeze(0)

    # Generate embedding using BERT model
    with torch.no_grad():
        output = model(input_ids)

    # Extract the embedding vector from BERT's output
    embedding = output[0][0][0].numpy()
    #print(embedding)
    return embedding


def compare_vectors(a, b):
    # Convert inputs to NumPy arrays
    a = np.array(a)
    b = np.array(b)

    # Calculate the Euclidean distance between the two vectors
    # distance = np.linalg.norm(a - b)
    # return distance
    similarity = np.dot(a, b)/(norm(a)*norm(a))
    return similarity

if __name__ == "__main__":
    text = ["A quick brown fox jumped over the lazy dog"]
    res = vectorize_multiple(text)
    # print(res)
    text = ["A quick brown fox jumped over the lazy dog"]
    res2 = vectorize_multiple(text)
    print()
    #print(res)
    print(compare_vectors(res, res2))
