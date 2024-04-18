from sensor.configuration.mongo_db_connection import MongoDBClient
from sensor.exception import sensor_exception
from sensor.logger import logging
import sys
from sensor.entity.config_entity import TrainingPipelineConfig, DataIngestionConfig
from sensor.pipeline.training_pipeline import TrainPipeline
if __name__ == "__main__":
    try:
       train_pipeline = TrainPipeline()
       train_pipeline.run_pipeline()
       
    except Exception as e:
        raise sensor_exception(e, sys)
