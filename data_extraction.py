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
    
    def retrieve_pdf_data(self, pdf_path):
        pdf_list = tabula.read_pdf(pdf_path, pages = 'all')
        pdf_to_df = pd.concat(pdf_list, ignore_index=True)
        return pdf_to_df
    
    def list_number_of_stores(self, num_store_link, header):
        r = requests.get(num_store_link, headers = header)
        number_of_stores = json.loads(r.text)
        return number_of_stores['number_stores']
    
    def retrieve_stores_data(self, store_link):
        num_store_link = 'https://aqj7u5id95.execute-api.eu-west-1.amazonaws.com/prod/number_stores'
        header = {'x-api-key': 'yFBQbwXe9J3sd6zWVAMrK6lcxxr0q1lr2PT6DDMX'}
        store_num = self.list_number_of_stores(num_store_link, header)
        store_list = []
        
        for store_number in range(store_num):
            #link = f"https://aqj7u5id95.execute-api.eu-west-1.amazonaws.com/prod/store_details/{i}"
            stores = requests.get(store_link + f'{store_number}', headers = header)
            stores_json = json.loads(stores.text)
            store_list.append(stores_json)
        store_details_df = pd.DataFrame(store_list)
        return store_details_df
    
    def extract_from_s3(self, url):
        path = os.getcwd()
        command = f'aws s3 cp {url} {path}'
        os.system(command)
        product =pd.read_csv('products.csv')
        product = product.set_index(product.columns[0])
        return product
    
    def extract_json_data(self, url):
        date_times_df = pd.read_json(url)
        return date_times_df