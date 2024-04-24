from sensor.utils.utilities import load_numpy_array_data, save_object , load_object
from sensor.exception import sensor_exception
from sensor.logger import logging
from sensor.entity.artifact_entity import DataTransformationArtifact,ModelTrainerArtifact
from sensor.entity.config_entity import ModelTrainerConfig
import os,sys
from sensor.ml.model_metrics.classification_metrics import get_classification_score
from sensor.ml.model.predictor import SensorModel
from xgboost import XGBClassifier

class ModelTrainer:
    
    def __init__(self, model_trainer_config:ModelTrainerConfig,
                 data_transformation_artifact:DataTransformationArtifact):
        try:
            self.model_trainer_config = model_trainer_config
            self.data_transformation_artifact = data_transformation_artifact   
        except Exception as e:
            raise sensor_exception(e,sys)
     
     
    def train_model(self,x_train,y_train):
        try:
           xgb_classifier = XGBClassifier()
           xgb_classifier.fit(x_train,y_train)
           return xgb_classifier
        except Exception as e:
            raise sensor_exception(e,sys)
        
    def initiate_model_training(self)->ModelTrainerArtifact:
        try:
            train_file_path = self.data_transformation_artifact.transformed_train_file_path
            test_file_path = self.data_transformation_artifact.transformed_test_file_path
            
            #loading training array and testing array
            train_array = load_numpy_array_data(train_file_path)
            test_array = load_numpy_array_data(test_file_path)
            
            x_train, y_train, x_test, y_test = (
                train_array[: , :-1],
                train_array[: , -1],
                test_array[:, :-1],
                test_array[:, -1],
            )
            
            model = self.train_model(x_train,y_train)
            y_train_prediction = model.predict(x_train)
            classification_train_metric =  get_classification_score(y_true=y_train, y_pred=y_train_prediction)
            
            if classification_train_metric.f1_score<=self.model_trainer_config.expected_accuracy:
                raise Exception("Trained model's accuracy is lower than expected accuracy")
            
            y_test_prediction = model.predict(x_test)
            classification_test_metric = get_classification_score(y_true=y_test, y_pred=y_test_prediction)
            
            #Checking Overfitting and Underfitting 
            fitting_difference = abs(classification_train_metric.f1_score-classification_test_metric.f1_score)
            if fitting_difference > self.model_trainer_config.fitting_threshold:
                raise Exception("Model is not good try to do more experimentation.")
            
            #load preprocessor
            preprocessor = load_object(file_path=self.data_transformation_artifact.transformed_object_file_path)
            
            #model saving
            model_dir_path = os.path.dirname(self.model_trainer_config.trained_model_file_path)
            os.makedirs(model_dir_path,exist_ok=True)
            sensor_model = SensorModel(preprocessor=preprocessor,model=model)
            save_object(self.model_trainer_config.trained_model_file_path, object=sensor_model)
            
            #model trainer artifact

            model_trainer_artifact = ModelTrainerArtifact(trained_model_file_path=self.model_trainer_config.trained_model_file_path, 
                                        train_metric_artifact=classification_train_metric,
                                        test_metric_artifact=classification_test_metric)
            logging.info(f"Model trainer artifact: {model_trainer_artifact}")
            return model_trainer_artifact
            
            
        except Exception as e:
            raise sensor_exception(e,sys)
        