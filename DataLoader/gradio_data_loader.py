import os
import gradio as gr
from shutil import copyfile

class GradioDataLoader:
    def __init__(self, local_folder_path: str):
        self.local_folder_path = local_folder_path

    def save_uploaded_file(self, temp_file, local_file):
        # Get file metadata
        file_type = os.path.splitext(temp_file)[-1].lstrip('.').lower()

        if file_type not in ["csv", "xlsx", "sql"]:
            return f"Unsupported file type: {file_type}"

        try:
            # Define destination file path
            #dest_file_path = os.path.join(self.local_folder_path, temp_file)

            # Copy the temp_file to the destination file path
            des_file = os.path.join(self.local_folder_path, local_file)
            copyfile(temp_file, des_file)
            #copyfile(temp_file, dest_file_path)

            return f"File saved successfully to {des_file}"
        except Exception as e:
            return f"Error occurred: {e}"
