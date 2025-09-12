from heartfailure.components.data_ingestion import DataIngestion
from heartfailure.entity.config_entity import DataIngestionConfig, TrainingPipelineConfig

from heartfailure.exception.exception import heartfailureException
from heartfailure.logging.logger import logging

if __name__ == "__main__":
    try:
        trainingpipelineconfig=TrainingPipelineConfig()
        dataingestionconfig = DataIngestionConfig(trainingpipelineconfig)
        data_ingestion = DataIngestion(dataingestionconfig)
        logging.info("initiate data ingestion")
        dataingestionaritifact = data_ingestion.initiate_data_ingestion()
        print(dataingestionaritifact)
    
    except Exception as e:
        raise heartfailureException(e,sys)