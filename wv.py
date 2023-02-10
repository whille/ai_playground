#!/usr/bin/env python

import numpy as np

class Word2Vec:
    def __init__(self, vocab_size, embedding_size, window_size=2):
        self.vocab_size = vocab_size
        self.embedding_size = embedding_size
        self.window_size = window_size
        self.word_embeddings = np.random.randn(vocab_size, embedding_size)
        self.word_context_vectors = np.random.randn(vocab_size, embedding_size)

    def softmax(self, x):
        e_x = np.exp(x - np.max(x))
        return e_x / e_x.sum(axis=0)

    def forward(self, x):
        out = np.dot(self.word_embeddings[x], self.word_context_vectors.T)
        return self.softmax(out)

    def backward(self, x, y, learning_rate):
        y_pred = self.forward(x)
        y_pred[y] -= 1
        dL_dW_embeddings = np.outer(y_pred, self.word_embeddings[x])
        dL_dW_context = np.outer(y_pred, self.word_context_vectors[y])
        self.word_embeddings[x] -= learning_rate * dL_dW_embeddings
        self.word_context_vectors[y] -= learning_rate * dL_dW_context

    def train(self, X, epochs, learning_rate):
        for epoch in range(epochs):
            total_loss = 0
            for x, y in self.generate_batch(X):
                print(f"x:{x}, y:{y}")
                loss = -np.log(self.forward(x)[y])
                total_loss += loss
                self.backward(x, y, learning_rate)
            if epoch % 10 == 0:
                print(f"Epoch {epoch} Loss: {total_loss}")

    def generate_batch(self, X):
        for i, x in enumerate(X):
            context_start = max(0, i - self.window_size)
            context_end = min(len(X), i + self.window_size + 1)
            for j in range(context_start, context_end):
                if j != i:
                    yield x, X[j]


# Example usage:
corpus = [1, 2, 3, 4, 5, 1, 2, 3, 6, 7, 1, 2, 3, 8, 9]
w2v = Word2Vec(vocab_size=9, embedding_size=3)
w2v.train(corpus, epochs=100, learning_rate=0.05)
