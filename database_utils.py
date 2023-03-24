import yaml
from sqlalchemy import create_engine, text
from sqlalchemy import inspect
import data_extraction as de
import data_cleaning as dc
import time

class DatabaseConnector:
    def __init__(self):
        self.creds = {}
    
    def read_db_creds(self):
        with open('db_creds.yaml') as yaml_file:
            self.creds = yaml.safe_load(yaml_file)
        return self.creds