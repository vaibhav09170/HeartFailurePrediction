import os,sys

from sklearn.linear_model import LogisticRegression
from sklearn.metrics import r2_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import AdaBoostClassifier,GradientBoostingClassifier,RandomForestClassifier

from heartfailure.exception.exception import heartfailureException
from heartfailure.logging.logger import logging
from heartfailure.entity.artifact_entity import DataTransformationArtifact,ModelTrainerArtifact
from heartfailure.entity.config_entity import ModeTrainerConfig
from heartfailure.utils.ml_utils.model.estimator import HeartModel
from heartfailure.utils.main_utils.utils import save_object,load_object
from heartfailure.utils.main_utils.utils import load_numpy_array_object,evaluate_models
from heartfailure.utils.ml_utils.metric.classifaction_metric import get_classification_score


class ModelTrainer:
    def __init__(self,model_trainer_config:ModeTrainerConfig, data_transformation_artifact:DataTransformationArtifact):
        try:
            self.model_trainer_config = model_trainer_config
            self.data_transformation_artifact = data_transformation_artifact
            
        except Exception as e:
            raise heartfailureException(e,sys)
    
    def train_model(self,x_train,y_train,x_test,y_test):
        try:
             models = {
                "Decision Tree":DecisionTreeClassifier(),
                "Random Forest":RandomForestClassifier(verbose=1),
                "Gradient Boosting":GradientBoostingClassifier(verbose=1),
                "Logistic Regression":LogisticRegression(verbose=1),
                "AdaBoost":AdaBoostClassifier()
            }
             params={
            "Decision Tree": {
                'criterion':['gini', 'entropy', 'log_loss'],
                # 'splitter':['best','random'],
                # 'max_features':['sqrt','log2'],
            },
            "Random Forest": {
                # 'criterion':['gini', 'entropy', 'log_loss'],
                
                # 'max_features':['sqrt','log2',None],
                'n_estimators': [8,16,32,128,256]
                },
            "Gradient Boosting" : {
                # 'loss':['log_loss', 'exponential'],
                'learning_rate':[.1,.01,.05,.001],
                'subsample':[0.6,0.7,0.75,0.85,0.9],
                # 'criterion':['squared_error', 'friedman_mse'],
                # 'max_features':['auto','sqrt','log2'],
                'n_estimators': [8,16,32,64,128,256]
                 },
            "Logistic Regression" : {},
            "AdaBoost" : {
                'learning_rate':[.1,.01,.001],
                'n_estimators': [8,16,32,64,128,256]
                 }
            
            }
             
             model_report:dict=evaluate_models(X_train = x_train, y_train=y_train, X_test = x_test, y_test = y_test,models=models,param=params)
             print(f"model_report : {model_report}")
             best_model_score = max(sorted(model_report.values()))
            
             best_model_name = list(model_report.keys())[list(model_report.values()).index(best_model_score)]
             print(f"model score : {best_model_score}, Model Name : {best_model_name}")
            
             best_model = models[best_model_name]
             y_train_pred = best_model.predict(x_train)
             
             classification_train_metric = get_classification_score(y_true=y_train,y_pred=y_train_pred)
             
             # track the MLFlow
             
             y_test_pred = best_model.predict(x_test)
             classification_test_metric = get_classification_score(y_true=y_test,y_pred=y_test_pred)
             
             preprocessor = load_object(file_path=self.data_transformation_artifact.transformed_object_file_path)
            
             model_dir_path = os.path.dirname(self.model_trainer_config.trained_model_file_path)
             os.makedirs(model_dir_path,exist_ok=True)
             
             
             heart_model = HeartModel(preprocessor=preprocessor, model=best_model)
             save_object(self.model_trainer_config.trained_model_file_path,obj=HeartModel)
             save_object("final_model/mode.pkl",best_model)
             
             model_trainer_artifact=ModelTrainerArtifact(
                                trained_model_file_path=self.model_trainer_config.trained_model_file_path,
                                 train_metric_artifact=classification_train_metric,
                                 test_metric_artifact=classification_test_metric
                                 )
        
             logging.info(f"Model trainer artifact {model_trainer_artifact}")
             return model_trainer_artifact   
             
            
        except Exception as e:
            raise heartfailureException(e,sys)
        
    def initiate_model_trainer(self) -> ModelTrainerArtifact:
        try:
            train_file_path = self.data_transformation_artifact.transformed_train_file_path
            test_file_path = self.data_transformation_artifact.transformed_test_file_path
            logging.info("load the numpy transformation file to array")
            train_arr = load_numpy_array_object(train_file_path)
            test_arr = load_numpy_array_object(test_file_path)
            
            x_train, y_train, x_test, y_test = (
                train_arr[:,:-1],
                train_arr[:,-1],
                test_arr[:,:-1],
                test_arr[:,-1]
            )
            
            model_trainer_artifact = self.train_model(x_train,y_train,x_test,y_test)
            return model_trainer_artifact
        except Exception as e:
            raise heartfailureException(e,sys)