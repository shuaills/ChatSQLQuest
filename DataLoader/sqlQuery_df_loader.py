'''
sql_query = SQLQuery('example.db')

# 获取 DataFrame
df = sql_query.execute_query("SELECT * FROM tablename")
print(df)

# 保存为 CSV 文件
sql_query.query_to_csv("SELECT * FROM tablename", 'output.csv')

'''

import sqlite3
import pandas as pd

class SQLiteQueryExecutor:
    def __init__(self, db_path):
        self.db_path = db_path

    def execute_query(self, query):
        # 创建一个到 SQLite 数据库文件的连接
        conn = sqlite3.connect(self.db_path)

        # 使用 pandas 的 read_sql_query 函数执行 SQL 查询并获取结果
        df = pd.read_sql_query(query, conn)

        # 确保在完成查询后关闭连接
        conn.close()

        # 返回 DataFrame
        return df

    def query_to_csv(self, query, csv_path, index=False):
        # 执行查询并获取 DataFrame
        df = self.execute_query(query)

        # 将 DataFrame 保存为 CSV 文件
        df.to_csv(csv_path, index=index)
