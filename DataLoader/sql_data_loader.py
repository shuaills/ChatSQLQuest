import os
import pandas as pd
import logging
from sqlalchemy import create_engine
from typing import Union
import sqlite3

class SQLDataLoader: # csv, xlsx to sqlite
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(level=logging.INFO)

    def load_data(self, file_path: str, db_folder_path: str, file_name: str):
        self.file_path = file_path
        self.db_folder_path = db_folder_path
        self.file_name = file_name
        
        file_type = os.path.splitext(self.file_name)[-1].lstrip('.')
        table_name = os.path.splitext(self.file_name)[0]
        db_path = os.path.join(self.db_folder_path, f'{table_name}.db')

        if os.path.exists(db_path):
            self.logger.info(f"Database {db_path} already exists, skipping this file.")
            return None

        try:
            df = self._load_data_from_file(file_type)
            self._store_data_to_sqlite(df, table_name, db_path)
        except FileNotFoundError as e:
            self.logger.error(f"Error occurred: File {self.file_path} not found.")
            return None
        except pd.errors.ParserError as e:
            self.logger.error(f"Error occurred: File {self.file_path} parsing error, possibly due to incorrect file format.")
            return None
        except ValueError as e:
            self.logger.error(f"Error occurred: Unsupported file type or error occurred while trying to read CSV file.")
            return None
        except sqlite3.OperationalError as e:
            self.logger.error(f"Error occurred: Error occurred while trying to store data to SQLite database.")
            return None
        else:
            self.logger.info('Data loaded successfully!')
            self._delete_original_file()
            return df

    def _load_data_from_file(self, file_type):
        if file_type == 'csv':
            df = pd.read_csv(self.file_path)
            # Check if column 'index' or 'Index' exists in DataFrame
            if 'index' in df.columns or 'Index' in df.columns:
                df.set_index('index' if 'index' in df.columns else 'Index', inplace=True)
            return df
        elif file_type == 'xlsx':
            return pd.read_excel(self.file_path)
        else:
            raise ValueError(f'Unsupported file type: {file_type}')

    def _store_data_to_sqlite(self, df, table_name, db_path):
        engine = create_engine(f'sqlite:///{db_path}')
        try:
            df.to_sql(table_name, engine, if_exists='replace', index=True if df.index.name is not None else False)
        except sqlite3.OperationalError as e:
            self.logger.error(f"Error occurred when storing data to SQLite: {e}")
            raise

    def _delete_original_file(self):
        os.remove(self.file_path)
