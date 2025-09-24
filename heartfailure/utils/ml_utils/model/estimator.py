import os,sys

from heartfailure.constant.training_pipeline import SAVED_MODEL_DIR,MODEL_FILE_NAME
from heartfailure.exception.exception import heartfailureException
from heartfailure.logging.logger import logging

class HeartModel:
    def __init__(self,preprocessor,model):
        try:
            self.preprocessor= preprocessor
            self.model = model
        except Exception as e:
            raise heartfailureException(e,sys)
    
    def predict(self, x):
        try:
            logging.info("Starting prediction")
            x_transform = self.preprocessor.transform(x)
            y_hat = self.model.predict(x_transform)
            logging.info("Prediction completed")
            
            return y_hat
        except Exception as e:
            raise heartfailureException(e,sys)