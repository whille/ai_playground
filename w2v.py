#!/usr/bin/env python
import numpy as np
from collections import defaultdict

# https://nathanrooy.github.io/posts/2018-03-22/word2vec-from-scratch-with-python-and-numpy/

class Word2Vec:
    def __init__(self, sentences, window=5, min_count=5, negative_samples=5, learning_rate=0.025):
        self.sentences = sentences
        self.window_size = window
        self.negative_samples = negative_samples
        self.learning_rate = learning_rate
        self.min_count = min_count
        self.init()

    def init(self):
        self.vocab = self.build_vocab()
        self.embedding_size = int(len(self.vocab) ** 0.5)
        print(f"vocab size: {len(self.vocab)}, embedding_size: {self.embedding_size}")
        self.word2idx, self.idx2word = self.build_index()

    def train(self, epochs):
        self.W1 = np.random.uniform(-0.8, 0.8, (len(self.vocab), self.embedding_size))
        self.W2 = np.random.uniform(-0.8, 0.8, (self.embedding_size, len(self.vocab)))
        for epoch in range(epochs):
            self.loss = 0
            for sentence in self.sentences:
                for i, w in enumerate(sentence):
                    if w not in self.word2idx:
                        continue
                    w_idx = self.word2idx[w]
                    context = sentence[max(0, i-self.window_size):i] + sentence[i+1:min(len(sentence), i+self.window_size+1)]
                    c_idxs = [self.word2idx[c] for c in context if c in self.word2idx]
                    self.update_weights(w_idx, c_idxs)
            if epoch % 10 == 0:
                print(f"Epoch {epoch} Loss: {self.loss}")

    def build_vocab(self):
        word_freq = defaultdict(int)
        print(f"len(sentences): {len(self.sentences)}")
        for sentence in self.sentences:
            for w in sentence:
                word_freq[w] += 1
        vocab = set()
        for w, c in word_freq.items():
            if c >= self.min_count:
                vocab.add(w)
        return vocab

    def build_index(self):
        word2idx = {}
        idx2word = {}
        for i, w in enumerate(self.vocab):
            word2idx[w] = i
            idx2word[i] = w
        return word2idx, idx2word

    def negtive_sampling(self, w_idx, c_idxs):
        neg_samples = []
        while len(neg_samples) < self.negative_samples:
            i = np.random.choice(len(self.vocab))
            if i not in c_idxs:
                neg_samples.append(i)
        return neg_samples

    def softmax(self, x):
        e_x = np.exp(x - np.max(x))
        return e_x / e_x.sum(axis=0)

    def forward(self, x):
        # Since x is a one-hot encoded vector, ℎ is simply the k_th row of matrix W1
        h = self.W1[x]
        u = np.dot(self.W2.T, h)
        y_pred = self.softmax(u)
        return y_pred, h

    def backward(self, w_idx, c_idxs, neg_idxs, y_pred, h):
        e = np.copy(y_pred)
        e[c_idxs] -= 1
        self.loss = e[c_idxs].sum()
        e[neg_idxs] += 1
        d2 = np.outer(h, e)
        d1 = np.dot(self.W2, e.T)
        self.W2 -= self.learning_rate * d2
        self.W1[w_idx] -= self.learning_rate * d1

    def update_weights(self, w_idx, c_idxs):
        neg_idxs = self.negtive_sampling(w_idx, c_idxs)
        y_pred, h = self.forward(w_idx)
        self.backward(w_idx, c_idxs, neg_idxs, y_pred, h)

    def get_similar_words(self, word, k=5):
        if word not in self.vocab:
            return None
        w_idx = self.word2idx[word]
        y_pred, h = self.forward(w_idx)
        top_k = y_pred.argsort()[::-1][:k]
        return [self.idx2word[idx] for idx in top_k]
