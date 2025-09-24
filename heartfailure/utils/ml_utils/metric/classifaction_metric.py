from sklearn.metrics import f1_score,precision_score,recall_score
import sys

from heartfailure.entity.artifact_entity import ClassificationMetricArtifact
from heartfailure.exception.exception import heartfailureException
from heartfailure.logging.logger import logging


def get_classification_score(y_true,y_pred) -> ClassificationMetricArtifact:
    try:
        logging.info("performing classification score")
        model_f1_score = f1_score(y_true,y_pred)
        model_recall_score = recall_score(y_true,y_pred)
        model_precision_score = precision_score(y_true,y_pred)
        
        classification_metric = ClassificationMetricArtifact(f1_score=model_f1_score,precision_score=model_precision_score,recall_score=model_recall_score)
        logging.info(f"Classification completed with {classification_metric}")
        
        return classification_metric
    
    except Exception as e:
        raise heartfailureException(e,sys)