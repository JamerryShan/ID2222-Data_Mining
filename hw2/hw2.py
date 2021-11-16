


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

# def A_Prior(buckets, threshold):

