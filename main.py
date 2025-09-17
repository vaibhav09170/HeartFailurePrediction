from heartfailure.components.data_ingestion import DataIngestion
from heartfailure.components.data_validation import DataValidation
from heartfailure.entity.config_entity import DataIngestionConfig, TrainingPipelineConfig, DataValidationConfig

from heartfailure.exception.exception import heartfailureException
from heartfailure.logging.logger import logging

import sys

if __name__ == "__main__":
    try:
        trainingpipelineconfig=TrainingPipelineConfig()
        dataingestionconfig = DataIngestionConfig(trainingpipelineconfig)
        data_ingestion = DataIngestion(dataingestionconfig)
        logging.info("initiate data ingestion")
        dataingestionaritifact = data_ingestion.initiate_data_ingestion()
        logging.info("Data initiation completed")
        print(dataingestionaritifact)
        
        data_validation_config=DataValidationConfig(trainingpipelineconfig)
        data_validation = DataValidation(data_ingestion_artifact=dataingestionaritifact,
                                         data_validation_config=data_validation_config)
        logging.info("Initiate Data Validation")
        data_validation_artifact = data_validation.initiate_data_validation()
        logging.info("Data Validation Completed ")
        print(data_validation_artifact)
    
    except Exception as e:
        raise heartfailureException(e,sys)