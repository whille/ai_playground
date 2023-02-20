#!/usr/bin/env python

import numpy as np

# implement Locality-Sensitive Hashing (LSH) for approximate nearest neighbor search
# write codes bellow
# 1. generate random hyperplanes
# 2. hash data points to buckets
# 3. find candidate neighbors
# 4. verify candidate neighbors
class LSHash:
    def __init__(self, hash_size, input_dim, num_hashtables=3):
        self.hash_size = hash_size
        self.input_dim = input_dim
        self.num_hashtables = num_hashtables
        self.hash_tables = [{} for _ in range(num_hashtables)]
        # generate random projection matrices
        self.projection_matrices = np.random.randn(num_hashtables, input_dim, hash_size)

    def _hash(self, table_index, vector):
        # project the vector onto the random projection matrix
        projection = np.dot(vector, self.projection_matrices[table_index])
        # apply sign function to get the hash value
        hash_value = tuple([bool(x > 0) for x in projection])
        return hash_value

    def index(self, vector):
        for i in range(self.num_hashtables):
            hash_value = self._hash(i, vector)
            self.hash_tables[i].setdefault(hash_value, [])
            self.hash_tables[i][hash_value].append(vector)

    def query(self, query_vector, num_results=10):
        candidates = set()
        for i in range(self.num_hashtables):
            hash_value = self._hash(i, query_vector)
            if hash_value in self.hash_tables[i]:
                for v in self.hash_tables[i][hash_value]:
                    candidates.update(v)
        # calculate distances from query to candidate vectors
        distances = [np.linalg.norm(np.array(candidate)-np.array(query_vector))
                     for candidate in candidates]

        # sort candidates by distance and return top num_results
        results = [candidate for _, candidate in sorted(zip(distances, candidates))]
        return results[:num_results]


#from py_lsh import LSHash
def test_lsh():
    lsh = LSHash(hash_size=6, input_dim=10)
    # insert some vectors into the LSH table
    lsh.index([1,2,3,4,5,6,7,8,9,10])
    lsh.index([2,4,6,8,10,12,14,16,18,20])
    lsh.index([3,6,9,12,15,18,21,24,27,30])
    lsh.index([4,8,12,16,20,24,28,32,36,40])
    print(lsh.hash_tables)

    # query the LSH table for similar vectors
    query = [1,3,5,7,9,11,13,15,17,19]
    result = lsh.query(query, num_results=2)
    print(result)
