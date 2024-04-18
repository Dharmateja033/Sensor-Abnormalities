from sensor.constants.training_pipeline import SCHEMA_FILE_PATH
from sensor.entity.config_entity import DataValidationConfig
from sensor.entity.artifact_entity import DataIngestionArtifact,DataValidationArtifact
from sensor.exception import sensor_exception
from sensor.logger import logging
from sensor.utils.utilities import read_yaml,write_yaml_file
import os, sys,json
#from evidently.report import Report
#from evidently.metrics import DataDriftTable
#from evidently.metrics import DatasetDriftMetric
from scipy.stats import ks_2samp
#from evidently.test_preset import DataDriftPreset
import pandas as pd

class DataValidation:
    
    def __init__(self, data_ingestion_artifact:DataIngestionArtifact,
                data_validation_config:DataValidationConfig):
        try:
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_validation_config = data_validation_config
            self._schema_config = read_yaml(SCHEMA_FILE_PATH)
        except Exception as e:
            raise sensor_exception(e, sys)
    
       
    def validate_number_of_columns(self, dataframe:pd.DataFrame)-> bool:
        try:
            number_of_columns = len(self._schema_config["columns"])
            if len(dataframe.columns) == number_of_columns:
                return True
            return False
        except Exception as e:
            raise sensor_exception(e, sys)  
        
    #def drop_zero_std_columns(self,dataframe)  :
        #pass
        
    def is_numerical_column_exist(self, dataframe : pd.DataFrame)-> bool:
        try:
            numerical_column_status = True
            numerical_columns = self._schema_config["numerical_columns"]
            dataframe_columns = dataframe.columns
            missing_numerical_columns = []
            for num_column in numerical_columns:
                if num_column not in dataframe_columns:
                    numerical_column_status = False
                    missing_numerical_columns.append(num_column)
            logging.info(f"Missing numerical columns are : {missing_numerical_columns}")
            return numerical_column_status

        except Exception as e:
            raise sensor_exception(e, sys)
    
    @staticmethod
    def read_data(file_path)-> pd.DataFrame:
        try:
            return  pd.read_csv(file_path)
        except Exception as e:
            raise sensor_exception(e, sys)
    
        
    
    def detect_data_drift(self,reference_data, current_data,threshold=0.05) -> bool:
        '''
        This code is using evidently open source
        try:
            data_drift_dataset_report = Report(metrics=[
                DatasetDriftMetric(),DataDriftTable()   
            ])
            #print(reference_data)
            #data_drift_dataset_report = Report(metrics=[DataDriftPreset()])
            html_report = data_drift_dataset_report.run(reference_data=reference_data,current_data=current_data)
            # Save the HTML 
            report_file_path = self.data_validation_config.drift_report_file_path
            report_dir = os.path.dirname(report_file_path)
            os.makedirs(report_dir, exist_ok=True)
            data_drift_dataset_report.save_html(report_file_path)
            logging.info(report_file_path)
            json_string_report = data_drift_dataset_report.json()
            
            # Parse the JSON string
            data = json.loads(json_string_report)
            drift_metrics = data["metrics"][0]["result"]
            drift_status = drift_metrics["dataset_drift"]
            return drift_status'''
        try:
            status=True
            report ={}
            for column in reference_data.columns:
                d1 = reference_data[column]
                d2  = current_data[column]
                is_same_dist = ks_2samp(d1,d2)
                if threshold<=is_same_dist.pvalue:
                    is_found=False
                else:
                    is_found = True 
                    status=False
                report.update({column:{
                    "p_value":float(is_same_dist.pvalue),
                    "drift_status":is_found
                    
                    }})
            
            drift_report_file_path = self.data_validation_config.drift_report_file_path
            
            #Create directory
            dir_path = os.path.dirname(drift_report_file_path)
            os.makedirs(dir_path,exist_ok=True)
            write_yaml_file(file_path=drift_report_file_path,content=report,)
            return status
        except Exception as e:
            raise sensor_exception(e, sys)
    
    def initiate_data_validation(self)-> DataValidationArtifact:     
        try:
            error_message =""
            train_file_path = self.data_ingestion_artifact.trained_file_path
            test_file_path = self.data_ingestion_artifact.test_file_path
            
            #reading data of train and test files
            train_dataframe=DataValidation.read_data(train_file_path)
            test_dataframe = DataValidation.read_data(test_file_path)
            
            #validating no.of columns in train data
            status = self.validate_number_of_columns(dataframe=train_dataframe)
            if not status:
                error_message = f"{error_message}No of columns are mismatching in Train dataframe \n"
            #validating no.of columns in test data
            self.validate_number_of_columns(dataframe=test_dataframe)
            if not status:
                error_message = f"{error_message}No of columns are mismatching in Test dataframe \n" 
                
            #validating numerical columns in train data
            n_status = self.is_numerical_column_exist(dataframe=train_dataframe)
            if not n_status:
                error_message = f"{error_message}No of numerical_columns are mismatching in Train dataframe \n"           
            #validating numerical columns in test data
            n_status = self.is_numerical_column_exist(dataframe=test_dataframe)
            if not n_status:
                error_message = f"{error_message}No of numerical_columns are mismatching in Test dataframe \n"
            
            if len(error_message)>0:
                raise Exception(error_message)
            #checking data drift
            d_status = self.detect_data_drift(reference_data=train_dataframe, current_data=test_dataframe)
            data_validation_artifact = DataValidationArtifact(
                validation_status=d_status,
                valid_train_file_path=self.data_ingestion_artifact.trained_file_path,
                valid_test_file_path=self.data_ingestion_artifact.test_file_path,
                invalid_train_file_path=None,
                invalid_test_file_path=None,
                drift_report_file_path=self.data_validation_config.drift_report_file_path,
            )

            logging.info(f"Data validation artifact: {data_validation_artifact}")
            return data_validation_artifact
        except Exception as e:
            raise sensor_exception(e, sys)