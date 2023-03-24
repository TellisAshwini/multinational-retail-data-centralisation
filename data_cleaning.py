import pandas as pd
import numpy as np

class DataCleaning:
    def  clean_user_data(self, table):
        #drops the rows with wrong data
        table = table.drop(table[table['country_code'].str.len() > 3].index.tolist())
        #replaces mis-spelled country codes
        table['country_code'] = table['country_code'].replace('GGB', 'GB')
        #converts the date strings to ISO date format
        date_columns = ['date_of_birth', 'join_date']
        for column in date_columns:
            if column in table.columns:
                table[column] = table[column].apply(lambda x: pd.to_datetime(x, errors='coerce', infer_datetime_format= True))
        return table
    
    def clean_card_data(self, table):
        #drops the rows with wrong data
        table = table.drop(table[table['expiry_date'].apply(lambda x: (len(x) > 5) or len(x) == 4)].index.tolist())
        # removes '?' from card_number
        table['card_number'] = table['card_number'].apply(lambda x: str(x) )
        table['card_number'] = table['card_number'].apply(lambda x: x.strip('?') if '?' in x else x)
        #converts the date strings to ISO date format
        table['date_payment_confirmed'] = table['date_payment_confirmed'].apply(lambda x: pd.to_datetime(x, errors='coerce', infer_datetime_format= True))
        return table
    
    def clean_store_data(self, table):
        #setting 'index' column as index
        table =table.set_index('index')
        #drops the rows with wrong data and NULL values and deleting column 'lat' which has no useful data
        table = table.drop(table[table['country_code'].str.len() > 3].index.tolist())
        del table['lat']
        #replacing mis-spelled words in the columns with correct values
        mapping = {'eeEurope': 'Europe', 'eeAmerica': 'America', '30e': '30', '80R': "80", 'A97': "97", '3n9': "39", 'J78':'78', 'N/A': np.nan, None: np.nan}
        for column in ['staff_numbers', 'continent', 'latitude', 'longitude']:
            table[column] = table[column].replace(mapping)
       #converts the date strings to ISO date format
        table['opening_date'] = table['opening_date'].apply(lambda x: pd.to_datetime(x, errors='coerce', infer_datetime_format= True))
        return table

    def convert_product_weights(self, table):
        table = table.drop(table[table['weight'].apply(lambda x: (type(x) != str or len(x) == 10))].index.tolist())
        table['weight'] = table['weight'].apply(lambda x:x.strip('kg') if x[-2:] == 'kg' else x)
        table['weight'] = table['weight'].apply(lambda x: str(int(x[:-2])/1000) if x.endswith('ml') else x)
        table['weight'] = table['weight'].apply(lambda x :str(int(x[:x.index('x')-1]) * int(x[x.index('x')+2:-1])/1000) if 'x' in x else x)
        table['weight'] = table['weight'].apply(lambda x: str(float(x[:-1])/1000) if x.endswith('g') else x)
        table['weight'] = table['weight'].apply(lambda x: str(int(x[:-3])/1000) if x.endswith('g .') else x)
        table['weight'] = table['weight'].apply(lambda x: str(int(x[:-2])*0.028) if x.endswith('oz') else x)
        table['weight'] = table['weight'].astype('float64')
        return table
        
    def clean_products_data(self, table):
        table = self.convert_product_weights(table)
        table['product_price'] = table['product_price'].apply(lambda x: x.strip('£'))
        #table['product_price'] = table['product_price'].astype('float64')
        #table['removed'] = table['removed'].astype('category')
        #table['category'] = table['category'].astype('category')
        table['date_added'] = table['date_added'].apply(lambda x: pd.to_datetime(x, errors='coerce', infer_datetime_format= True))
        return table

    def clean_orders_data(self, table):
        table = table.set_index('level_0')
        del table['first_name']
        del table['last_name']
        del table ['1']
        return table
    
    def clean_datetimes_data(self, table):
        table = table.drop(table[table['month'].apply(lambda x: len(x) > 2)].index.tolist())
        return table