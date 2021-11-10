# finding textually similar documents based on Jaccard similarity using the shingling, minhashing, and locality-sensitive hashing (LSH) techniques and corresponding algorithms
import dataset_reader
import preprocess
import numpy as np
import math
import time

# A class Shingling that constructs k–shingles of a given length k from given datasets, computes a hash value for each unique shingle, and represents the document in the form of an ordered set of its hashed k-shingles.
class Shingling:
    def __init__(self, k=10):
        self.k = k
    
    def create_shingling(self, dataset):
        shingling_list = []
        for doc in dataset:
            shingling_list.append(self.create_shingling_from_doc(doc))
        return shingling_list
    
    def create_shingling_from_doc(self, doc):
        shingling = []
        for i in range(len(doc) - self.k + 1):
            shingling.append(self.hash_shingle(doc[i:i+self.k]))
        return shingling
    
    def hash_shingle(self, shingle):
        return hash(str(shingle))
    
# A class CompareSets that computes the Jaccard similarity of two sets of integers – two sets of hashed shingles.
class CompareSets:
    def jaccard_similarity(self, set1, set2):
        intersection = len(set1.intersection(set2))
        union = len(set1.union(set2))
        return intersection / union
    
# A class MinHashing that builds a minHash signature (in the form of a vector or a set) of a given length n from a given set of integers (a set of hashed shingles).
class MinHashing:
    def __init__(self, n=500):
        self.n = n
    
    def create_min_hashing(self, set_of_hashed_shingles):
        min_hashing = []
        for i in range(self.n):
            min_hashing.append(self.min_hash(set_of_hashed_shingles))
        return min_hashing
    
    def min_hash(self, set_of_hashed_shingles):
        min_hash = float('inf')
        for shingle in set_of_hashed_shingles:
            if shingle < min_hash:
                min_hash = shingle
        return min_hash
    
# A class CompareSignatures that estimates similarity of two integer vectors – minhash signatures – as a fraction of components, in which they agree.
class CompareSignatures:
    def signature_similarity(self, signature1, signature2):
        agree = 0
        for i in range(len(signature1)):
            if signature1[i] == signature2[i]:
                agree += 1
        return agree / len(signature1)

# A class LSH that constructs a table of size n × m of LSH signatures (in the form of a vector or a set) of a given length n from a given set of integers (a set of hashed shingles).
class LSH:
    def __init__(self, n=500, m=10):
        self.n = n
        self.m = m
    