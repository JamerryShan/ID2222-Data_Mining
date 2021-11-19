


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
# get larger_frequent_sets from frequent_items, result contains k+1 items while input_set contains k items
def larger_frequent_sets(frequent_sets, frequent_items):
    new_freq_itemsets = []
    possible_sets = set()

    for itemset in frequent_sets:
        for item in frequent_items:
            # add item that not be included in itemsets to set
            if type(itemset) == list:
                possibleSet = list(itemset)
            else:
                possibleSet = [itemset]
            if item not in possibleSet:
                possibleSet.append(item)
                possibleSet.sort()
                # make sure the new itemsets are unique
                # add new_set to possible_sets to store and compare sets
                new_set = ",".join(map(str, possibleSet))
                if new_set not in possible_sets:
                    possible_sets.add(new_set)
                    # if not add in new sets before
                    new_freq_itemsets.append(possibleSet)

    return new_freq_itemsets

#filter itemsets appears' time more than threshold
def filter(baskets, possibleSets, threshold):
    #initial the counter to count
    occurences = [0 for s in range(len(possibleSets))]

    for one_basket in baskets:
        for index, sets in enumerate(possibleSets):
            sets_not_in_basket = False
            #to ckeck if the item in possiblesets is also in the basket
            for item in sets:
                if item not in one_basket:
                    sets_not_in_basket = True
            # add counter
            if sets_not_in_basket == False:
                occurences[index] += 1
    # filter the occurences >= threshold
    frequent_sets = {}
    for i, v in enumerate(occurences):
        if v >= threshold:
            _str = ",".join(map(str, possibleSets[i]))
            frequent_sets[_str] = v
    return frequent_sets


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

    # use frequent single item to creat frequent k-item_sets
    frequent_item_sets = frequent_item
    while len(frequent_item_sets) > 0:
        print(frequent_item_sets)
        possible_freq_itemsets = larger_frequent_sets(frequent_item_sets, frequent_item)
        frequent_item_sets = []
        for sets, v in filter(baskets, possible_freq_itemsets, threshold).items():
            frequent_item_sets.append(list(map(int, sets.split(","))))

    return frequent_item_sets

item_frequency = A_Prior(data_set[:1500], 15)
# print(len(item_frequency))
# print(item_frequency)


