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
    
    def init_db_engine(self):
        self.creds = self.read_db_creds()
        engine = create_engine(f"{'postgresql'}+{'psycopg2'}://{self.creds['RDS_USER']}:{self.creds['RDS_PASSWORD']}@{self.creds['RDS_HOST']}:{self.creds['RDS_PORT']}/{self.creds['RDS_DATABASE']}")
        engine.connect()
        return engine
    
    def list_db_tables(self):
        engine = self.init_db_engine()
        inspector = inspect(engine)
        table_list = inspector.get_table_names()
        return table_list
    
    def upload_to_db(self, table, table_name):
        self.engine = create_engine(f"{'postgresql'}+{'psycopg2'}://{self.creds['USER']}:{self.creds['PASSWORD']}@{self.creds['HOST']}:{self.creds['PORT']}/{self.creds['DATABASE']}")
        self.engine.connect()
        if table_name == 'user_table_clean':
            db_table_name = 'dim_users'
        elif table_name == 'pdf_table_clean':
            db_table_name = 'dim_card_details'
        elif table_name == 'store_table_clean':
            db_table_name = 'dim_store_details'
        elif table_name == 'product_table_clean':
            db_table_name = 'dim_products'
        elif  table_name == 'order_table_clean':
            db_table_name = 'orders_table'
        else:
            db_table_name = 'dim_date_times'
        table.to_sql(db_table_name, self.engine, if_exists='replace')
        
conn = DatabaseConnector()
data_extract = de.DataExtractor()
data_clean = dc.DataCleaning()

yaml_data = conn.read_db_creds()
engine = conn.init_db_engine()
table_list = conn.list_db_tables()
start_time = time.time()
pdf_path = "https://data-handling-public.s3.eu-west-1.amazonaws.com/card_details.pdf"
store_link = f'https://aqj7u5id95.execute-api.eu-west-1.amazonaws.com/prod/store_details/'
user_table = data_extract.read_rds_table(engine, table_list[1])
pdf_to_df = data_extract.retrieve_pdf_data(pdf_path)
store_details_table = data_extract.retrieve_stores_data(store_link)
aws_url = 's3://data-handling-public/products.csv'
product_table = data_extract.extract_from_s3(aws_url)
order_table = data_extract.read_rds_table(engine, table_list[2])
json_url = 'https://data-handling-public.s3.eu-west-1.amazonaws.com/date_details.json'
dates_table = data_extract.extract_json_data(json_url)

user_table_clean = data_clean.clean_user_data(user_table)
pdf_table_clean = data_clean.clean_card_data(pdf_to_df)
store_table_clean = data_clean.clean_store_data(store_details_table)
product_table_clean = data_clean.clean_products_data(product_table)
order_table_clean = data_clean.clean_orders_data(order_table)
dates_table_clean = data_clean.clean_datetimes_data(dates_table)

user_table_upload = conn.upload_to_db(user_table_clean, 'user_table_clean')
pdf_table_upload = conn.upload_to_db(pdf_table_clean, 'pdf_table_clean')
store_table_upload = conn.upload_to_db(store_table_clean, 'store_table_clean')
product_table_upload = conn.upload_to_db(product_table_clean, 'product_table_clean')
order_table_upload = conn.upload_to_db(order_table_clean, 'order_table_clean')
dates_table_upload = conn.upload_to_db(dates_table_clean, 'dates_table_clean')
mins, secs = divmod(round((time.time() - start_time)), 60)
print(f'time taken - {mins}:{secs} seconds')