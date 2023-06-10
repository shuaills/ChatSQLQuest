import os
import time
from sql_data_loader import SQLDataLoader

class FileListener:
    def __init__(self, folder_path, db_folder_path):
        self.folder_path = folder_path
        self.db_folder_path = db_folder_path
        self.failed_files = set()

    def start(self):
        sql_data_loader = SQLDataLoader()
        while True:
            files = [f for f in os.listdir(self.folder_path) if f not in self.failed_files]
            if files:
                for file in files:
                    file_path = os.path.join(self.folder_path, file)
                    try:
                        sql_data_loader.load_data(file_path, self.db_folder_path, file)  # 处理文件
                        #os.remove(file_path)  # 删除处理完的文件
                    except Exception as e:
                        print(f"Error processing file {file}: {e}")
                        self.failed_files.add(file)
            time.sleep(1)  # 等待1秒
            
# Define the path to the "UploadedFile" folder
folder_path = "../UploadedFile"

# Check if the "UploadedFile" folder exists, if not, create it
if not os.path.exists(folder_path):
    os.mkdir(folder_path)

listener = FileListener(folder_path, "../DB")
listener.start()  # 启动监听器


