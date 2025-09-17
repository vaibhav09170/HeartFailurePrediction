import yaml
import os,sys
import numpy as np
import pickle

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