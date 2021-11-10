# data preprocessor
import dataset_reader
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
            dataset[i]['text'] = self.preprocess(dataset[i]['text'])
        return dataset