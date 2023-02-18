#!/usr/bin/env python
from w2v import Word2Vec
import sys
sys.path.append('../poem')
from t_poem import gen_sentence


def test_simple():
    corpus = [
        ["king", "queen", "man", "woman"],
        ["dog", "cat", "fish", "bird", "snake"],
        ["red", "green", "blue", "yellow"],
        ["car", "bike", "boat", "plane"],
        ["apple", "orange", "banana", "grape"],
    ]
    model = Word2Vec(corpus, window=2, min_count=1)
    model.train(epochs=500)
    for query_word in ('man', 'car', 'grape', 'dog'):
        similar_words = model.get_similar_words(query_word, k=3)
        print(f"Most similar words to '%s': {similar_words}" % query_word)


def test_poem():
    fname = '../poem/data/全唐诗.txt'
    corpus = []
    for s in gen_sentence(fname):
        corpus.append(list(s))
    model = Word2Vec(corpus, window=3, min_count=5)
    model.train(epochs=1)
    for query_word in (list(s)):
        similar_words = model.get_similar_words(query_word, k=3)
        print(f"Most similar words to '%s': {similar_words}" % query_word)
