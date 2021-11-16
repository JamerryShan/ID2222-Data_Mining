


# import dataset
data_set = []
for line in open("./T10I4D100K.dat").readlines():
    line = line.strip().split()
    line_int = []
    for data in line:
        line_int.append(int(data))
    data_set.append(line_int)
# print(data_set)
print(len(data_set))

# Finding frequent itemsets with support at least s
# implement the A-Priori algorithm

def A_Prior(baskets, threshold):
    frequent_item = []
    # find the frequency of each item in all buckets
    item_frequency = {}
    for basket in baskets:
        for item in basket:
            # if this item didn't exist in previous baskets
            if item not in item_frequency:
                item_frequency[item] = 1
            else:
                item_frequency[item] += 1
    # get items whose support >= threshold
    for item, support in item_frequency.items():
        if support >= threshold:
            frequent_item.append(item)

    return frequent_item

item_frequency = A_Prior(data_set, 20)
print(len(item_frequency))
print(item_frequency)

# get larger_frequent_sets from frequent_items, result contains k+1 items while input_set contains k items
def larger_frequent_sets(frequent_sets, frequent_items):

    for itemset in frequent_sets:
        for item in frequent_items:
            # add item that not be included in itemsets to set
            itemset