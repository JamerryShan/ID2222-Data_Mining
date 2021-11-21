# Discovery of Frequent Itemsets and Association Rules

# read dataset from T10I4D100K.dat
# read intergers sets from dataset line by line
def read_dataset(filename):
    dataset = []
    with open(filename, 'r') as f:
        for line in f:
            lines = list(map(int, line.strip().split()))
            lines.sort()
            dataset.append(lines)
    dataset.sort()
    return dataset

dataset = read_dataset('./T10I4D100K.dat')
# length of dataset
print('length of dataset:', len(dataset))

# get the apporopriate support threshold
# typicallly, support threshold is the length of dataset / 100
def get_support_threshold(dataset):
    return len(dataset) * 0.01

print('support threshold:', int(get_support_threshold(dataset)))

s = get_support_threshold(dataset)

# finding frequent itemsets of integers with support at least s in the dataset
import numpy as np
import pandas as pd
import itertools
class Apriori:
    def __init__(self, dataset, support_threshold):
        self.dataset = dataset
        self.support_threshold = support_threshold
        self.frequent_itemsets = []
        self.frequent_item = []
        self.possible_freq_itemsets = []
        self.item_frequency = {}
        self.frequent_item_sets = []
        
   # compute the support of given itemset
    def support(self, itemset):
        support = 0
        for transaction in self.dataset:
            if set(itemset).issubset(set(transaction)):
                support += 1
        return support
    
    # filter generated possible itemset
    def filter_itemset(self, itemset):
        return (self.support(itemset) >= self.support_threshold)

    # get 1-item_set
    def get_1_item_set(self):
        for transaction in self.dataset:
            for item in transaction:
                if item not in self.item_frequency:
                    self.item_frequency[item] = 1
                else:
                    self.item_frequency[item] += 1
        for item in self.item_frequency:
            if self.item_frequency[item] >= self.support_threshold:
                self.frequent_item.append(item)
        self.frequent_item.sort()
        return self.frequent_item

    # update the dataset
    def update_dataset(self, itemset):
        new_dataset = []
        for transaction in self.dataset:
            for item in transaction:
                if item in itemset:
                    new_dataset.append(transaction)
                    break
        new_dataset.sort()
        self.dataset = new_dataset
        return self.dataset
    
    # get canadiate k-item_set
    # compute the support using the support function
    def get_k_item_set(self, _k_1_itemsets, k):
        k_itemsets = []
        possible_itemsets = list(itertools.combinations(_k_1_itemsets, k))
        possible_itemsets.sort()
        for itemset in possible_itemsets:
            if self.filter_itemset(itemset):
                k_itemsets.append(itemset)
                print('2-itemset:', itemset, 'support:', self.support(itemset))
        return k_itemsets

# test
apriori = Apriori(dataset, s)
frequent_item = apriori.get_1_item_set()
# print('frequent_item:', frequent_item)
# print('len(frequent_item):', len(frequent_item))
print('len(apriori.dataset):', len(apriori.dataset))
apriori.update_dataset(frequent_item)
print('len(apriori.dataset):', len(apriori.dataset))
a = apriori.get_k_item_set(frequent_item, 2)
print('a:', len(a))



