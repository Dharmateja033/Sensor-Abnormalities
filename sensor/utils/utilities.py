from sensor.exception import sensor_exception
import os, sys, yaml
import numpy as np
import dill

def read_yaml(file_path:str)-> dict:
    try:
        with open(file_path, 'rb') as yaml_file:
            return yaml.safe_load(yaml_file)
    except Exception as e:
        raise sensor_exception(e, sys)
    
def write_yaml_file(file_path, content: object, replace: bool=False):
    try:
        if replace:
            if os.path.exists(file_path):
                os.remove(file_path)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path,'w') as f:
            yaml.dump(content, f)
    except Exception as e:
        raise sensor_exception(e, sys)
    
def save_numpy_array_data(file_path:str, data:np.array):
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path,exist_ok=True)
        with open(file_path, 'wb') as file_obj:
            np.save(file_obj,data)
    except Exception as e:
        raise sensor_exception(e, sys)
        

def load_numpy_array_data(file_path:str) -> np.array:
    try:
        with open(file_path,'rb') as file_obj:
            return np.load(file_obj)
    except Exception as e:
        raise sensor_exception(e, sys)
    
def save_object(file_path: str, object:object):
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path,exist_ok=True)
        with open(file_path, 'wb') as file_obj:
            dill.dump(object, file_obj)
    except Exception as e:
        raise sensor_exception(e, sys)
    


def load_object(file_path: str, ) -> object:
    try:
        if not os.path.exists(file_path):
            raise Exception(f"The file: {file_path} does not exists")
        with open(file_path, "rb") as file_obj:
            return dill.load(file_obj)
    except Exception as e:
        raise sensor_exception(e, sys) from e