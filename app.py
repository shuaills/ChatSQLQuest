from io import StringIO
import gradio as gr
import random
import time
import pandas as pd
from DataLoader.sql_data_loader import *
from DataLoader.gradio_data_loader import *


def process_upload(uploaded_file):
    upload_folder_path = 'UploadedFile'  # This should be your uploaded file folder path
    data_loader = GradioDataLoader(upload_folder_path)
    return data_loader.save_uploaded_file(uploaded_file)

iface = gr.Interface(fn=process_upload, inputs="file", outputs="text")
iface.launch()
