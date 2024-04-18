from sensor.entity.config_entity import DataIngestionConfig, TrainingPipelineConfig,DataValidationConfig,DataTransformationConfig,ModelTrainerConfig
from sensor.exception import sensor_exception
from sensor.logger import logging
from sensor.components.data_ingestion import DataIngestion
from sensor.components.data_validation import DataValidation
from sensor.components.data_transformation import DataTransformation
from sensor.components.model_training import ModelTrainer
from sensor.entity.artifact_entity import DataIngestionArtifact,DataValidationArtifact,DataTransformationArtifact, ModelTrainerArtifact
import os,sys




class TrainPipeline:
    def __init__(self) :
        self.training_pipeline_config = TrainingPipelineConfig()
        #data_ingestion_config = DataIngestionConfig(training_pipeline_config)
        
        
    def execute_data_ingestion(self)->DataIngestionArtifact:
        try:
            self.data_ingestion_config = DataIngestionConfig(self.training_pipeline_config)
            logging.info("*"*10 + "DATA INGESTION STARTED" + "*"*10)
            data_ingestion = DataIngestion(self.data_ingestion_config)
            data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
            logging.info(f"DATA SUCCESSFULLY INGESTED / check here : {data_ingestion_artifact}")
            return data_ingestion_artifact
            
        except Exception as e:
            raise sensor_exception(e,sys)
    
    def execute_data_validation(self, data_ingestion_artifact:DataIngestionArtifact)-> DataValidationArtifact:
        try:
            data_validation_config = DataValidationConfig(self.training_pipeline_config)
            data_validation = DataValidation(data_ingestion_artifact,
                                             data_validation_config)
            logging.info("*"*10 + "DATA VALIDATION STARTED" + "*"*10)
            data_validation_artifact = data_validation.initiate_data_validation()
            logging.info(f"DATA SUCCESSFULLY VALIDATED / check here : {data_ingestion_artifact}")
            return data_validation_artifact
        except  Exception as e:
            raise  sensor_exception(e,sys)
    
    def execute_data_transformation(self,data_validation_artifact:DataValidationArtifact)-> DataTransformationArtifact:
        try:
            data_transformation_config = DataTransformationConfig(self.training_pipeline_config)
            data_transformation = DataTransformation(data_validation_artifact,data_transformation_config)
            logging.info("*"*10 + "DATA TRANSFORMATION STARTED" + "*"*10)
            data_transformation_artifact = data_transformation.initiate_data_transformation()
            logging.info(f"DATA SUCCESSFULLY TRANSFORMED / check here : {data_transformation_artifact}")
            return data_transformation_artifact
        except  Exception as e:
            raise  sensor_exception(e,sys)
    
    
    def execute_model_training(self,data_transformation_artifact:DataTransformationArtifact)-> ModelTrainerArtifact:
        try:
            model_trainer_config = ModelTrainerConfig(self.training_pipeline_config)
            model_trainer = ModelTrainer(model_trainer_config,data_transformation_artifact )
            logging.info("*"*10 + "MODEL TRAINING STARTED" + "*"*10)
            model_trainer_artifact = model_trainer.initiate_model_training()
            logging.info(f"MODEL SUCCESSFULLY TRAINED / check here : {model_trainer_artifact}")
            return model_trainer_artifact
        except  Exception as e:
            raise  sensor_exception(e,sys)
    
    
    def run_pipeline(self):
        try:
            
            data_ingestion_artifact: DataIngestionArtifact = self.execute_data_ingestion()
            data_validation_artifact = self.execute_data_validation(data_ingestion_artifact)
            data_transformation_artifact: DataTransformationArtifact = self.execute_data_transformation(data_validation_artifact)
            model_training_artifact: ModelTrainerArtifact = self.execute_model_training(data_transformation_artifact)
        except Exception as e:
            raise sensor_exception(e,sys)