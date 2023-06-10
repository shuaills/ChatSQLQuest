import gradio as gr
import pandas as pd
from DataLoader.sql_data_loader import *
from DataLoader.gradio_data_loader import *
from shutil import copyfile



def process_uploads(uploaded_files):
    root_dir = os.path.dirname(os.path.abspath(__file__))  # Get the root directory of your project
    upload_folder_path = os.path.join(root_dir, 'UploadedFile')  # Construct the path to the "UploadedFile" folder
    print(upload_folder_path)

    # Check if the "UploadedFile" folder exists, if not, create it
    if not os.path.exists(upload_folder_path):
        os.mkdir(upload_folder_path)

    data_loader = GradioDataLoader(upload_folder_path)
    processed_files = []

    for uploaded_file in uploaded_files:
        original_filename = os.path.basename(uploaded_file.name)
        print(original_filename)
        data_loader.save_uploaded_file(uploaded_file, original_filename)
        processed_files.append(original_filename + " has been processed. /n")

    return processed_files



# Create a Gradio interface
iface = gr.Interface(
    fn=process_uploads,
    inputs = gr.Files(file_types=[".csv", ".sql", ".xlsx"], label="Upload CSV, SQL, XLSX file"),
    outputs="text"
)

# Launch the Gradio interface
iface.launch()
