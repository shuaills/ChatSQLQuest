import gradio as gr
import pandas as pd
from DataLoader.sql_data_loader import *
from DataLoader.gradio_data_loader import *
from shutil import copyfile



def process_uploads(uploaded_files):
    root_dir = os.path.dirname(os.path.abspath(__file__))  # Get the root directory of your project
    local_folder_path = os.path.join(root_dir, 'UploadedFile')  # Construct the path to the "UploadedFile" folder

    # Check if the "UploadedFile" folder exists, if not, create it
    if not os.path.exists(local_folder_path):
        os.mkdir(local_folder_path)

    data_loader = GradioDataLoader(local_folder_path)
    processed_files = []

    for uploaded_file in uploaded_files:
        local_file = os.path.basename(uploaded_file.name)
        temp_filename = uploaded_file.name
        data_loader.save_uploaded_file(temp_filename, local_file)
        processed_files.append(local_file + " has been processed. /n")

    return processed_files

def inject_SQL(inputs):
    folder_path = "UploadedFile"
    db_folder_path = "DB"
    failed_files = set()
    sql_data_loader = SQLDataLoader()
    files = [f for f in os.listdir(folder_path) if f not in failed_files]
    if files:
        for file in files:
            file_path = os.path.join(folder_path, file)
            try:
                df = sql_data_loader.load_data(file_path, db_folder_path, file)  # 处理文件
                if df is not None:
                    os.remove(file_path)  # 删除处理完的文件
            except Exception as e:
                print(f"Error processing file {file}: {e}")
                failed_files.add(file)
        return "Files processed successfully!"
    else:
        return "No files to process."





# Create a Gradio interface
Upload_button = gr.Interface(
    fn=process_uploads,
    inputs = gr.Files(file_types=[".csv", ".sql", ".xlsx"], label="Upload CSV, SQL, XLSX file"),
    outputs="text"
)

# Create a Gradio interface
SQL_injection_button = gr.Interface(
    fn=inject_SQL,
    inputs=gr.Button("SQL injection"),
    outputs="text"
)


demo = gr.TabbedInterface([Upload_button, SQL_injection_button], ["Upload file", "SQL injection"])

if __name__ == "__main__":
    demo.launch()
