import yaml
import os,sys
import numpy as np
import pickle

from sklearn.metrics import r2_score
from sklearn.model_selection import GridSearchCV


from heartfailure.exception.exception import heartfailureException
from heartfailure.logging.logger import logging


def read_yaml_file(file_path:str) -> dict:
    try:
        with open(file_path,'rb') as yaml_file:
            return yaml.safe_load(yaml_file)
    except Exception as e:
        raise heartfailureException(e,sys)
    
def write_yaml_file(file_path:str, content:object, replace:bool=False) -> None:
    try:
        if replace:
            if os.path.exists(file_path):
                os.remove(file_path)
        
        os.makedirs(os.path.dirname(file_path),exist_ok=True)
        with open(file_path, "w") as yaml_file:
            yaml.dump(content,yaml_file)
            
    except Exception as e:
        raise heartfailureException(e,sys)
    

def save_numpy_array_data(file_path:str, array : np.array):
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path,exist_ok=True)
        with open(file_path,"wb") as file_obj:
            np.save(file_obj,array)
            
    except Exception as e:
        raise heartfailureException(e,sys)
    
def save_object(file_path:str, obj:object) -> None:
    try:
        logging.info("save object triggerd ")
        os.makedirs(os.path.dirname(file_path),exist_ok=True)
        with open(file_path,"wb") as file_obj:
            pickle.dump(obj,file_obj)
        logging.info("Object has been saved ")
    
    except Exception as e:
        raise heartfailureException(e,sys)
    
def load_object(file_path:str, ) ->object:
    try:
        logging.info("Loading Object in progress")
        if not os.path.exists(file_path):
            raise Exception(f"The file : {file_path} is not exists")
        with open(file_path,"rb") as file_obj:
            print(file_obj)
            return pickle.load(file_obj)
        logging.info("Loading completed")
        
    except Exception as e:
        raise heartfailureException(e,sys)

def load_numpy_array_object(file_path:str)-> np.array:
    try:
        logging.info("Loading numpy array : ")
        with open(file_path,"rb") as file_obj:
            return np.load(file_obj)
        
    except Exception as e:
        raise heartfailureException(e,sys)
    
def evaluate_models(X_train, y_train,X_test,y_test,models,param):
    try:
        report = {}

        for i in range(len(list(models))):
            model = list(models.values())[i]
            print(model)
            para=param[list(models.keys())[i]]
            print(para)

            gs = GridSearchCV(model,para,cv=3)
            gs.fit(X_train,y_train)

            model.set_params(**gs.best_params_)
            model.fit(X_train,y_train)

            #model.fit(X_train, y_train)  # Train model

            y_train_pred = model.predict(X_train)

            y_test_pred = model.predict(X_test)

            train_model_score = r2_score(y_train, y_train_pred)

            test_model_score = r2_score(y_test, y_test_pred)

            report[list(models.keys())[i]] = test_model_score

        return report

    except Exception as e:
        raise heartfailureException(e,sys)
