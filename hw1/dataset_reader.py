#dataset reader for the dataset
#read all json files from dataset folder
import os
import json

class DatasetReader:
    def __init__(self, dataset_path):
        self.dataset_path = dataset_path
    
    def read_dataset(self):
        """
        read all json files from dataset folder
        return area with text lable
        """
        dataset = []
        for file in os.listdir(self.dataset_path):
            if file.endswith(".json"):
                with open(os.path.join(self.dataset_path, file), 'rb') as json_file:
                    #load json file with utf-8 encoding
                    data = json.load(json_file, encoding='utf-8')
                    dataset.append(data['text'])
        return dataset


if __name__ == "__main__":
    dataset_reader = DatasetReader("dataset")
    print(dataset_reader.read_dataset()[0])