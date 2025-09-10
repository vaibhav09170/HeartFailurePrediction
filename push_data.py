import os
import sys
import json
import certifi
ca=certifi.where()
import pandas as pd
import numpy as np
import pymongo


from dotenv import load_dotenv
load_dotenv()

from heartfailure.exception.exception import heartfailureException
from heartfailure.logging.logger import logging


MONGO_DB_URL = os.getenv("MONGO_DB_URL")
print(MONGO_DB_URL)

class HeartDataExtract():
    def __init__(self):
        try:
            pass
        except Exception as e:
            raise heartfailureException(e,sys)
    
    def cv_to_json_convert(self,file_path):
        try:
            data = pd.read_csv(file_path)
            data.reset_index(drop=True,inplace=True)
            records = list(json.loads(data.T.to_json()).values())
            return records
        except Exception as e:
            raise heartfailureException(e,sys)
    
    def insert_data_mongodb(self,records,database,collection):
        try:
            self.database = database
            self.collection = collection
            self.records = records
            
            self.mongo_client= pymongo.MongoClient(MONGO_DB_URL)
            self.database = self.mongo_client[self.database]
        
            self.collection = self.database[self.collection]
            self.collection.insert_many(self.records)
            
            return (len(self.records))
        
        except Exception as e:
            raise heartfailureException(e,sys)
        
if __name__ == "__main__":
    FILE_PATH = "dataset\heart.csv"
    DATABASE="vaibhav09170"
    COLLECTION = "HeartFailureData"
    
    heartdataobj = HeartDataExtract()
    records = heartdataobj.cv_to_json_convert(file_path=FILE_PATH)
    print(records)
    no_of_records = heartdataobj.insert_data_mongodb(records=records,database=DATABASE,collection=COLLECTION)
    print(no_of_records)        