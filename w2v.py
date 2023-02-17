#!/usr/bin/env python
import numpy as np
from collections import defaultdict


class Word2Vec:
    def __init__(self, sentences, embedding_size=10, window=5, negative_samples=5, learning_rate=0.025):
        self.sentences = sentences
        self.embedding_size = embedding_size
        self.window_size = window
        self.negative_samples = negative_samples
        self.learning_rate = learning_rate
        self.init()

    def init(self):
        self.vocab = self.build_vocab()
        print(f"vocab size: {len(self.vocab)}")
        self.word2idx, self.idx2word = self.build_index()
        # word_vectors
        self.W1 = np.random.uniform(-0.8, 0.8, (len(self.vocab), self.embedding_size))
        self.W2 = np.random.uniform(-0.8, 0.8, (self.embedding_size, len(self.vocab)))

    def train(self, epochs):
        for epoch in range(epochs):
            self.loss = 0
            for sentence in self.sentences:
                for i, w in enumerate(sentence):
                    w_idx = self.word2idx[w]
                    context = sentence[max(0, i-self.window_size):i] + sentence[i+1:min(len(sentence), i+self.window_size+1)]
                    for c in context:
                        c_idx = self.word2idx[c]
                        neg_samples = self.get_negative_samples(w_idx, c_idx)
                        self.update_weights(w_idx, c_idx, neg_samples)
            if epoch % 10 == 0:
                print(f"Epoch {epoch} Loss: {self.loss}")

    def build_vocab(self):
        word_freq = defaultdict(int)
        for sentence in self.sentences:
            for w in sentence:
                word_freq[w] += 1
        vocab = set(word_freq.keys())
        return vocab

    def build_index(self):
        word2idx = {}
        idx2word = {}
        for i, w in enumerate(self.vocab):
            word2idx[w] = i
            idx2word[i] = w
        return word2idx, idx2word

    def get_negative_samples(self, w_idx, c_idx):
        neg_samples = []
        while len(neg_samples) < self.negative_samples:
            sample = np.random.choice(list(self.vocab))
            if sample != self.idx2word[c_idx]:
                neg_samples.append(self.word2idx[sample])
        return neg_samples

    def forward(self, x):
        h = self.W1[x]
        u = np.dot(self.W2.T, h)
        y_pred = self.softmax(u)
        return y_pred

    def backward(self, w_idx, c_idx, neg_samples, y):
        d2 = np.copy(y)
        d2[c_idx] -= 1
        for n in neg_samples:
            d2[n] -= 1
        d1 = np.dot(self.W2, d2)
        self.W2 -= self.learning_rate * np.outer(self.W1[w_idx], d2)
        self.W1[w_idx] -= self.learning_rate * d1

    def softmax(self, x):
        e_x = np.exp(x - np.max(x))
        return e_x / e_x.sum(axis=0)

    def update_weights(self, w_idx, c_idx, neg_samples):
        y = self.forward(w_idx)
        self.loss -= np.log(y[c_idx])
        self.backward(w_idx, c_idx, neg_samples, y)

    def get_similar_words(self, word, k=10):
        if word not in self.vocab:
            return None
        word_idx = self.word2idx[word]
        word_vec = self.W1[word_idx]
        similarities = np.dot(self.W1, word_vec)
        top_k = similarities.argsort()[::-1][:k]
        return [self.idx2word[idx] for idx in top_k]
