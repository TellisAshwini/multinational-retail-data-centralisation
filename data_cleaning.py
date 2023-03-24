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
