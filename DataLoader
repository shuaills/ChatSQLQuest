import os
import pandas as pd
from sqlalchemy import create_engine
from typing import Union

class DataLoader:
    def __init__(self, folder_path: str, db_folder_path: str):
        self.folder_path = folder_path
        self.db_folder_path = db_folder_path

    def load_data(self):
        for filename in os.listdir(self.folder_path):
            file_path = os.path.join(self.folder_path, filename)
            file_type = os.path.splitext(filename)[-1].lstrip('.')
            table_name = os.path.splitext(filename)[0]
            db_path = os.path.join(self.db_folder_path, f'{table_name}.db')
            self.engine = create_engine(f'sqlite:///{db_path}')

            # 根据文件类型读取数据
            if file_type == 'csv':
                df = pd.read_csv(file_path)
            elif file_type == 'xlsx':
                df = pd.read_excel(file_path)
            else:
                raise ValueError(f'Unsupported file type: {file_type}')

            # 将数据存储到SQLite数据库中
            df.to_sql(table_name, self.engine, if_exists='replace')
            print('good!')

            # 删除原始文件
            os.remove(file_path)
