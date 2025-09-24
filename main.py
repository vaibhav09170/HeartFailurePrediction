from heartfailure.components.data_ingestion import DataIngestion
from heartfailure.components.data_validation import DataValidation
from heartfailure.components.data_transformation import DataTransformation
from heartfailure.components.model_trainer import ModelTrainer

from heartfailure.entity.config_entity import DataIngestionConfig, TrainingPipelineConfig, DataValidationConfig,DataTransformationConfig,ModeTrainerConfig

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
        
        
        data_transformation_config=DataTransformationConfig(trainingpipelineconfig)
        logging.info(f"Initiate Data transformation")
        data_transformation = DataTransformation(data_validation_artifact=data_validation_artifact, data_transformation_config=data_transformation_config)
        data_transformation_artifact = data_transformation.initiate_data_transformation()
        logging.info(f"Data transformation completed")
        print(data_transformation_artifact)
        
        
        logging.info("Model Training started ")
        model_trainer_config = ModeTrainerConfig(training_pipeline_config=trainingpipelineconfig)
        model_trainer = ModelTrainer(model_trainer_config=model_trainer_config, data_transformation_artifact=data_transformation_artifact)
        model_trainer_artifact = model_trainer.initiate_model_trainer()
        logging.info("Model training artifact created")
        print(model_trainer_artifact)
    
    except Exception as e:
        raise heartfailureException(e,sys)