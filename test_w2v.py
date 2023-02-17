#!/usr/bin/env python
from w2v import Word2Vec


def test_word2vec():
    corpus = [
        ["king", "queen", "man", "woman"],
        ["dog", "cat", "fish", "bird", "snake"],
        ["red", "green", "blue", "yellow"],
        ["car", "bike", "boat", "plane"],
        ["apple", "orange", "banana", "grape"],
    ]
    query_word = 'king'
    # corpus = [["cat", "say", "meow"], ["dog", "say", "woof"]]
    # query_word = "dog"
    model = Word2Vec(corpus, window=2)
    model.train(epochs=50)

    # Test most similar words
    similar_words = model.get_similar_words(query_word, k=3)
    print(f"Most similar words to '%s': {similar_words}" % query_word)
