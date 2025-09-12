import os
import sys
import numpy as np
import pandas as pd

"""
defining common variable for pipeline 
"""
### start

TARGET_COLUMN = "HeartDisease"
PIPELINE_NAME: str = "HeartDisease"
ARTIFACT_DIR: str = "Artifacts"
FILE_NAME: str = "HeartDisease.csv"

TRAIN_FILE_NAME: str = "train.csv"
TEST_FILE_NAME: str = "test.csv"


""" 
Data Ingestion related constant 
"""
### start

DATA_INGESTION_COLLECTION_NAME: str = "HeartFailureData"
DATA_INGESTION_DATABASE_NAME: str = "vaibhav09170"
DATA_INGESTION_DIR_NAME: str = "data_ingestion"
DATA_INGESTION_FEATURE_STORE_DIR: str = "feature_store"
DATA_INGESTION_INGESTED_DIR: str  = "ingested"
DATA_INGESTION_TRAIN_TEST_SPLIT_RATION: float = 0.2

### END 