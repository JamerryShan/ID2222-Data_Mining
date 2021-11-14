# finding textually similar documents based on Jaccard similarity using the shingling, minhashing, and locality-sensitive hashing (LSH) techniques and corresponding algorithms
import itertools
from re import S
from dataset_reader import DatasetReader
from preprocess import Preprocessor
import numpy as np
import math
import time
import hashlib
import random
from scipy import integrate

# A class Shingling that constructs k–shingles of a given length k from given datasets, computes a hash value for each unique shingle, and represents the document in the form of an ordered set of its hashed k-shingles.



class Shingling:
    def __init__(self, k=6):
        self.k = k

    def create_shingling(self, dataset):
        shingling_list = []
        for doc in dataset:
            shingling_list.append(self.create_shingling_from_doc(doc))
        return shingling_list

    def create_shingling_from_doc(self, doc):
        shingling = []
        for i in range(len(doc) - self.k + 1):
            shingling.append(self.hash_shingle(doc[i:i + self.k]))
            # shingling.append(doc[i:i+self.k])
        return set(shingling)

    def hash_shingle(self, shingle):
        return hash(str(shingle))

    # return the shingling list of all documents in the dataset
    def get_shingling_list(self, dataset):
        # shingling_list is a empty set
        shingling_list = set()
        for doc in dataset:
            shingling_list.update(self.create_shingling_from_doc(doc))
        return shingling_list


# A class CompareSets that computes the Jaccard similarity of two sets of integers – two sets of hashed shingles.
class CompareSets:
    def jaccard_similarity(self, set1, set2):
        # set1 = set(set1)
        # set2 = set(set2)
        intersection = len(set1.intersection(set2))
        union = len(set1.union(set2))
        return intersection / union


'''
A class MinHashing that builds a minHash signature of a given n from a set of already hashed shingles which are integers.
using n different hash functions
'''


class MinHashing:
    def __init__(self, n=500):
        self.n = n
        self.hash_prime = 299999627
        # self.n_prime = 739
        self.random_hash = []
        for i in range(self.n):
            self.random_hash.append(self.random_hash_function(i))

    def random_hash_function(self, i):
        return lambda x: abs(hash(str(x) + str(i))) % self.hash_prime

    def create_min_hashing(self, sets_of_hashed_shingles):
        min_hashing_sig = []
        for shingles in sets_of_hashed_shingles:
            min_hashing_sig.append(self.min_hash(shingles))
        return min_hashing_sig

    def min_hash(self, a_set_of_shingles):
        signature = []
        for hash_function in self.random_hash:
            min_hash = float('inf')
            hashed_shi_list = []
            for shingle in a_set_of_shingles:
                # print(shingle)
                hashed_shingle = hash_function(shingle)
                hashed_shi_list.append(hashed_shingle)
                if hashed_shingle < min_hash:
                    min_hash = hashed_shingle
            #print(hashed_shi_list)
            signature.append(min_hash)
        #print(signature)
        return signature


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

    def calculate_lsh_params(self, signature_length, threshold):
        prob = 1
        result = (1, 1)

        for i in range(1, signature_length + 1):
            band_number = i
            rows_number = math.ceil(signature_length / i)

            min = abs(threshold - (1 / band_number) ** (1 / rows_number))
            if prob > min:
                prob = min
                result = (band_number, rows_number)
        return result

    def lsh(self, signature_matrix, threshold, lsh_buckets):

        bands_num, rows_num = self.calculate_lsh_params(self.n, threshold)

        print(bands_num, rows_num)
        signature_matrix = np.array(signature_matrix)
        candidate_pairs = set()

        for i in range(bands_num):
            bucket = {}
            rows_start = rows_num * i
            rows_end = rows_start + rows_num
            bands = signature_matrix[:, rows_start:rows_end]
            for index, band in enumerate(bands):
                hash_r = abs(hash(tuple(band))) % lsh_buckets
                if hash_r in bucket:
                    bucket[hash_r].append(index)
                else:
                    bucket[hash_r] = [index]

            for one_bucket in bucket.values():
                if len(one_bucket) > 1:
                    candidate_pairs.update(list(itertools.combinations(one_bucket, 2)))

        return candidate_pairs


if __name__ == "__main__":
    start = time.time()
    # read the dataset
    dataset_reader = DatasetReader("dataset")
    dataset = dataset_reader.read_dataset()

    # preprocess the dataset
    preprocess = Preprocessor()
    dataset = preprocess.preprocess_dataset(dataset)
    dataset_test = dataset[:10]
    # create a Shingling object
    shingling = Shingling()
    shingling_list = shingling.create_shingling(dataset_test)
    whole_shingling_list = shingling.get_shingling_list(dataset_test)
    # print(len(whole_shingling_list))
    # compute the Jaccard similarity of two sets of integers – two sets of hashed shingles
    compare_sets = CompareSets()
    print(compare_sets.jaccard_similarity(shingling_list[0], shingling_list[1]))

    dataset_test_shingling_size = len(whole_shingling_list)
    # create a MinHashing object
    # print(dataset_test_shingling_size)
    minHashing = MinHashing()
    signature_list = minHashing.create_min_hashing(shingling_list)
    # create a CompareSignatures object
    compareSignatures = CompareSignatures()
    sig_similarity = compareSignatures.signature_similarity(signature_list[0], signature_list[3])
    print(sig_similarity)

    lshashing = LSH()
    candidate_pairs = lshashing.lsh(signature_list, 0.8, 20)
    print(candidate_pairs)

    for pair in candidate_pairs:
        print('Similar Document Pair:' + str(pair))
        print(compare_sets.jaccard_similarity(shingling_list[pair[0]], shingling_list[pair[1]]))
        print(compareSignatures.signature_similarity(signature_list[pair[0]], signature_list[pair[1]]))

    end = time.time()
    print(f"Runtime of was {end - start}")