import os
import pandas as pd
import logging
from sqlalchemy import create_engine
from typing import Union

class SQLDataLoader: # csv, xlsx to sqlite
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(level=logging.INFO)

    def load_data(self, file_path: str, db_folder_path: str, file_name: str):
        self.file_path = file_path
        self.db_folder_path = db_folder_path
        self.file_name = file_name
        
        print(f"filename: {self.file_name}")
        file_type = os.path.splitext(self.file_name)[-1].lstrip('.')
        print(f"file_type: {file_type}")
        table_name = os.path.splitext(self.file_name)[0]
        print(f"table_name: {table_name}")
        db_path = os.path.join(self.db_folder_path, f'{table_name}.db')
        print(f"db_path: {db_path}")

        try:
            df = self._load_data_from_file(file_type)
            self._store_data_to_sqlite(df, table_name, db_path)
            #self._delete_original_file()
        except (FileNotFoundError, pd.errors.ParserError, ValueError) as e:
            self.logger.error(f"Error occurred: {e}")
            return None
        else:
            self.logger.info('Data loaded successfully!')
            return df

    def _load_data_from_file(self, file_type):
        if file_type == 'csv':
            return pd.read_csv(self.file_path)
        elif file_type == 'xlsx':
            return pd.read_excel(self.file_path)
        else:
            raise ValueError(f'Unsupported file type: {file_type}')

    def _store_data_to_sqlite(self, df, table_name, db_path):
        engine = create_engine(f'sqlite:///{db_path}')
        df.to_sql(table_name, engine, if_exists='replace')

    def _delete_original_file(self):
        os.remove(self.file_path)
