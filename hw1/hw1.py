# finding textually similar documents based on Jaccard similarity using the shingling, minhashing, and locality-sensitive hashing (LSH) techniques and corresponding algorithms

from dataset_reader import DatasetReader
from preprocess import Preprocessor

import itertools
import numpy as np
import math
import time



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
        intersection = len(set1.intersection(set2))
        union = len(set1.union(set2))
        return intersection / union


'''
A class MinHashing that builds a minHash signature of a given n from a set of already hashed shingles which are integers.
using n different hash functions
'''


class MinHashing:
    def __init__(self, k=500):
        self.k = k
        self.prime = 1000000007
        # generate random numbers lists a and b, where a and b both have k elements
        self.a = np.random.randint(1, self.prime, self.k)
        self.b = np.random.randint(1, self.prime, self.k)

    # universal hash function ((a*x + b) % p) , a and b are random numbers, p is a large prime number, n is the number of unique shingles
    def universal_hash(self, x, a, b, p):
        return ((a * x + b) % p)


    # compute the minhash signatures using universal hash function above
    def compute_minhash_signatures(self, dataset, n):
        minhash_signatures = []
        for docs in dataset:
            minhash_signatures.append(self.compute_minhash_signature(docs, n))
        return minhash_signatures

    # compute the minhash signature of a document
    def compute_minhash_signature(self, docs, n):
        signature = [math.inf] * self.k
        for doc in docs:
            for i in range(self.k):
                if (self.universal_hash(doc, self.a[i], self.b[i], self.prime) < signature[i]):
                    signature[i] = self.universal_hash(doc, self.a[i], self.b[i], self.prime)
        return signature


# A class CompareSignatures that estimates similarity of two integer vectors – minhash signatures – as a fraction of components, in which they agree.
class CompareSignatures:
    def signature_similarity(self, signature1, signature2):
        agree = 0
        for i in range(len(signature1)):
            if signature1[i] == signature2[i]:
                agree += 1
        return agree / len(signature1)


# A class LSH that implements the LSH technique: given a collection of minhash signatures (integer vectors) and a similarity threshold t, the LSH class (using banding and hashing) finds candidate pairs of signatures agreeing on at least fraction t of their components.
# Locality-Sensitive Hashing
class LSH:
    def __init__(self, signature_length=500, threshold=0.5):
        self.signature_length = signature_length  # k is signature length
        self.threshold = threshold  # between 0 and 1

    # calculate the band number and rows number of each band using given signature length and threshold
    # band number * rows number = signature length
    # (1/band number) ** (1/rows number) = threshold
    def calculate_lsh_params(self, signature_length, threshold):
        prob = 1
        result = (1, 1)

        for i in range(1, signature_length + 1):
            band_number = i
            rows_number = math.ceil(signature_length / i)
            # (1/band number) ** (1/rows number) ≈ threshold
            min = abs(threshold - (1 / band_number) ** (1 / rows_number))
            if prob > min:
                prob = min
                result = (band_number, rows_number)
        return result

    def lsh(self, signature_matrix, threshold, lsh_buckets):

        bands_num, rows_num = self.calculate_lsh_params(self.signature_length, threshold)

        signature_matrix = np.array(signature_matrix)
        candidate_pairs = set()
        # find the columns that have same hash value(in the same bucket) in each band
        for i in range(bands_num):
            bucket = {}
            rows_start = rows_num * i
            rows_end = rows_start + rows_num
            # divide the signature matrix
            bands = signature_matrix[:, rows_start:rows_end]
            # index: the index of text's signature
            for index, band in enumerate(bands):
                hash_r = abs(hash(tuple(band))) % lsh_buckets
                # if the bucket has the same hash value
                if hash_r in bucket:
                    bucket[hash_r].append(index)
                else:
                    bucket[hash_r] = [index]
            # to get the pairs from the bucket that contains more than one value
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
    # pprint(shingling_list[0])
    whole_shingling_list = shingling.get_shingling_list(dataset_test)
    # print(len(whole_shingling_list))
    # compute the Jaccard similarity of two sets of integers – two sets of hashed shingles
    compare_sets = CompareSets()
    jaccard_similarity_matrix = np.zeros((len(dataset_test), len(dataset_test)))
    for i in range(len(dataset_test)):
        for j in range(len(dataset_test)):
            jaccard_similarity_matrix[i][j] = compare_sets.jaccard_similarity(shingling_list[i], shingling_list[j])
    for i in range(len(jaccard_similarity_matrix)):
        jaccard_similarity_matrix[i] = ['%.3f' % elem for elem in jaccard_similarity_matrix[i]]
    print('Jaccard Similarity Matrix of Dataset')
    print(jaccard_similarity_matrix)
    # print(compare_sets.jaccard_similarity(shingling_list[0], shingling_list[1]))

    dataset_test_shingling_size = len(whole_shingling_list)
    # create a MinHashing object
    # print(dataset_test_shingling_size)
    minhashing = MinHashing()
    minhash_signatures = minhashing.compute_minhash_signatures(shingling_list, dataset_test_shingling_size)
    # pprint(minhash_signatures[0])
    # create a CompareSignatures object
    compare_signatures = CompareSignatures()
    signatures_similarity_matrix = np.zeros((len(dataset_test), len(dataset_test)))
    for i in range(len(dataset_test)):
        for j in range(len(dataset_test)):
            signatures_similarity_matrix[i][j] = compare_signatures.signature_similarity(minhash_signatures[i], minhash_signatures[j])
    for i in range(len(signatures_similarity_matrix)):
        signatures_similarity_matrix[i] = ['%.3f' % elem for elem in signatures_similarity_matrix[i]]
    print('Signature Similarity Matrix of Dataset')
    print(signatures_similarity_matrix)
    # print(compare_signatures.signature_similarity(minhash_signatures[0], minhash_signatures[1]))

    # create a LSH object
    # lsh = LSH()
    # lsh_signatures = lsh.compute_LSH_signatures(shingling_list, dataset_test_shingling_size)
    # print(compare_signatures.signature_similarity(lsh_signatures[0], lsh_signatures[1]))
    lshashing = LSH()
    threshold = 0.4
    candidate_pairs = lshashing.lsh(minhash_signatures, threshold, 300)
    #print(candidate_pairs)

    for pair in candidate_pairs:
        if (compare_sets.jaccard_similarity(shingling_list[pair[0]], shingling_list[pair[1]])) > threshold:
            print('Candidate pair' + str(pair))
            print(compare_sets.jaccard_similarity(shingling_list[pair[0]], shingling_list[pair[1]]))
            print(compare_signatures.signature_similarity(minhash_signatures[pair[0]], minhash_signatures[pair[1]]))

    end = time.time()
    print(f"Runtime of was {end - start}")
