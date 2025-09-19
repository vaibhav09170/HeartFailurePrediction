import os,sys
import pandas as pd
import numpy as np

from sklearn.impute import KNNImputer,SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from heartfailure.exception.exception import heartfailureException
from heartfailure.logging.logger import logging
from heartfailure.constant.training_pipeline import TARGET_COLUMN
from heartfailure.constant.training_pipeline import DATA_TRANSFORMATION_IMPUTER_PARAMS
from heartfailure.entity.artifact_entity import DataTransformationArtifact,DataValidationArtifact
from heartfailure.entity.config_entity import DataTransformationConfig
from heartfailure.utils.main_utils.utils import save_numpy_array_data, save_object


class DataTransformation:
    def __init__(self,data_validation_artifact:DataValidationArtifact, data_transformation_config:DataTransformationConfig):
        try:
            self.data_validation_artifact = data_validation_artifact
            self.data_transformation_config = data_transformation_config
            
        except Exception as e:
            raise heartfailureException(e,sys)
        
    @staticmethod
    def read_data(file_path) -> pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise heartfailureException(e,sys)
    
    def get_data_transformer_object(cls)-> Pipeline:
        
        logging.info("fectching transformation object")
        try:
            numerical_Feature = ['Age', 'RestingBP', 'Cholesterol', 'FastingBS', 'MaxHR', 'Oldpeak'] 
            categorical_Feature = ['Sex', 'ChestPainType', 'RestingECG', 'ExerciseAngina', 'ST_Slope'] 
            
            #imputer:KNNImputer = KNNImputer(**DATA_TRANSFORMATION_IMPUTER_PARAMS)
            #logging.info(f"initialise KNNImputer with {DATA_TRANSFORMATION_IMPUTER_PARAMS}")
            
            num_pipeline = Pipeline(
                steps=[
                    ('imputer',SimpleImputer(strategy="median")),
                    ("scaler", StandardScaler())
                ]
                
            )
            logging.info("Numerical column scalling completed")
            
            cat_pipeline = Pipeline(
                steps=[
                    ("imputer", SimpleImputer(strategy="most_frequent")),
                    ("one_hot_encoder", OneHotEncoder()),
                    ("scaler", StandardScaler(with_mean=False))
                    
                ]
            )
            
            logging.info("Categorical column enconding completed")
            
            processor=ColumnTransformer(
                [
                    ("num_pipeline",num_pipeline,numerical_Feature),
                    ("cat_pipeline", cat_pipeline, categorical_Feature)
                ]
            )
            
            return processor
        
        except Exception as e:
            raise heartfailureException(e,sys)
    
    def initiate_data_transformation(self) -> DataTransformationArtifact:
        logging.info("initiating data transformation ")
        try:
            train_df = DataTransformation.read_data(self.data_validation_artifact.valid_train_file_path)
            test_df = DataTransformation.read_data(self.data_validation_artifact.valid_test_file_path)
            
            input_feature_train_df = train_df.drop(columns=[TARGET_COLUMN], axis=1)
            target_feature_train_df = train_df[TARGET_COLUMN]
            
            input_feature_test_df = test_df.drop(columns=[TARGET_COLUMN],axis=1)
            target_feature_test_df = test_df[TARGET_COLUMN]
            
            preprocessor_object = self.get_data_transformer_object()
            #preprocessor_object = processor.fit(input_feature_train_df)
            transformed_input_train_feature = preprocessor_object.fit_transform(input_feature_train_df)
            transformed_input_test_feature = preprocessor_object.transform(input_feature_test_df)
            
            train_arr = np.c_[transformed_input_train_feature,np.array(target_feature_train_df)]
            test_arr = np.c_[transformed_input_test_feature,np.array(target_feature_test_df)]
            
            save_numpy_array_data(self.data_transformation_config.transformed_train_file_path,array=train_arr)
            save_numpy_array_data(self.data_transformation_config.transformed_test_file_path,array=test_arr)
            save_object(self.data_transformation_config.transformed_object_file_path, preprocessor_object)
            
            data_transformation_artifact=DataTransformationArtifact(
                transformed_object_file_path=self.data_transformation_config.transformed_object_file_path,
                transformed_train_file_path=self.data_transformation_config.transformed_train_file_path,
                transformed_test_file_path=self.data_transformation_config.transformed_test_file_path
            )
            return data_transformation_artifact
            
        except Exception as e:
            raise heartfailureException(e,sys)