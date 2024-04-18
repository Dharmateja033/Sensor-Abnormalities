from sensor.entity.config_entity import DataIngestionConfig
from sensor.entity.artifact_entity import DataIngestionArtifact
from sensor.exception import sensor_exception
from sensor.logger import logging
import os,sys
from sensor.utils.utilities import read_yaml,write_yaml_file
from sensor.constants.training_pipeline import SCHEMA_FILE_PATH
from pandas import DataFrame
from sensor.data_retrieval.sensor_data import SensorData
from sklearn.model_selection import train_test_split




class DataIngestion:
    
    def __init__(self, data_ingestion_config:DataIngestionConfig):
        try:
            self.data_ingestion_config = data_ingestion_config
            self._schema_config = read_yaml(SCHEMA_FILE_PATH)
        except Exception as e:
            raise sensor_exception(e,sys)
    
    def export_data_into_feature_store(self)->DataFrame:
        """
        exports mongoDB collection records as DataFrame into feature_store
        """
        try:
            logging.info("Exporting data from database to feature store")
            sensor_data = SensorData()
            dataframe:DataFrame = sensor_data.export_collection_as_dataframe(collection_name=self.data_ingestion_config.collection_name)
            
            feature_store_filepath = self.data_ingestion_config.feature_store_file_path
            
            # creating feature store directory if not exist
            dir_name = os.path.dirname(feature_store_filepath)
            os.makedirs(dir_name, exist_ok=True)
            
            dataframe.to_csv(feature_store_filepath, index=False, header=True )
            logging.info("Successfully exported data from database to feature store")
            return dataframe

        except Exception as e:
            raise sensor_exception(e,sys)
    
        
        
    def split_data_into_train_test(self, dataframe:DataFrame)->None:
        """
        Feature store dataset will be splitted into Train abd Test data files     
        """
        
        try:
            logging.info("Splitting feature store data into Train and Test dataframes")
            
            train_set, test_set = train_test_split(
                dataframe, test_size=self.data_ingestion_config.train_test_split_ratio
            )

            #logging.info("Performing Train_Test split on the dataframe")

            logging.info("Splitting finished successfully")

            dir_path = os.path.dirname(self.data_ingestion_config.training_file_path)
            os.makedirs(dir_path, exist_ok=True)
            logging.info(f"Exporting train and test files to {dir_path}")

            train_set.to_csv(
                self.data_ingestion_config.training_file_path, index=False, header=True
            )

            test_set.to_csv(
                self.data_ingestion_config.testing_file_path, index=False, header=True
            )

            logging.info("Exported train and test file successfully")
        except Exception as e:
            raise sensor_exception(e,sys)
    
        
    
    
    def initiate_data_ingestion(self)-> DataIngestionArtifact:
        try:
            dataframe = self.export_data_into_feature_store()
            dataframe = dataframe.drop(self._schema_config['drop_columns'],axis=1)
            self.split_data_into_train_test(dataframe)
            data_ingestion_artifact = DataIngestionArtifact(
                trained_file_path=self.data_ingestion_config.training_file_path,
                test_file_path=self.data_ingestion_config.testing_file_path
            )
            return data_ingestion_artifact
            
        except Exception as e:
            raise sensor_exception(e,sys)