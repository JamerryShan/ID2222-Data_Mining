# data preprocessor
from dataset_reader import DatasetReader
import unicodedata
import re
import os
import string

class Preprocessor:
    def __init__(self, lowercase=True, remove_punctuation = True):
        pass
    
    def preprocess(self, text):
        # lowercase
        text = text.lower()
        # remove punctuation
        text = re.sub(r'[^\w\s]', '', text)
        # remove non-ascii characters
        text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8', 'ignore')
        # remove extra spaces
        # text = re.sub(' +', ' ', text)
        return text
    
    def preprocess_dataset(self, dataset):
        for i in range(len(dataset)):
            dataset[i] = self.preprocess(dataset[i])
        return dataset

if __name__ == '__main__':
    # test
    preprocessor = Preprocessor()
    datasetReader = DatasetReader('dataset')
    dataset = datasetReader.read_dataset()
    dataset = preprocessor.preprocess_dataset(dataset)
    print(dataset[0])