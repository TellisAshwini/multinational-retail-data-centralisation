import pandas as pd
from sqlalchemy import create_engine, text 
import tabula
import requests
import json
import os

class DataExtractor:
    def read_rds_table(self, engine, table_name):
        #engine is the instance of DatabaseConnector and table_name for 1st one is user table from the list
        table = pd.DataFrame(engine.connect().execute(text(f'''select * from {table_name}'''))).set_index('index')
        return table