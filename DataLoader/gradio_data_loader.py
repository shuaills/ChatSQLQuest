import os
import gradio as gr
from shutil import copyfile


class GradioDataLoader:
    def __init__(self, upload_folder_path: str):
        self.upload_folder_path = upload_folder_path

    def save_uploaded_file(self, uploaded_file, original_filename):
        # Get file metadata
        file_type = os.path.splitext(original_filename)[-1].lstrip('.').lower()

        if file_type not in ["csv", "xlsx", "sql"]:
            return f"Unsupported file type: {file_type}"

        try:
            # Define destination file path
            dest_file_path = os.path.join(self.upload_folder_path, original_filename)

            # Save the uploaded file to the destination file path
            with open(dest_file_path, 'wb') as f:
                f.write(uploaded_file.read())
                

            return f"File saved successfully to {dest_file_path}"
        except Exception as e:
            return f"Error occurred: {e}"