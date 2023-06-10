import os
import gradio as gr

class GradioDataLoader:
    def __init__(self, upload_folder_path: str):
        self.upload_folder_path = upload_folder_path

    def save_uploaded_file(self, uploaded_file):
        # Get file metadata
        filename = uploaded_file.name
        file_type = os.path.splitext(filename)[-1].lstrip('.').lower()

        if file_type not in ["csv", "xlsx", "sql"]:
            return f"Unsupported file type: {file_type}"

        try:
            # Define destination file path
            dest_file_path = os.path.join(self.upload_folder_path, filename)

            # Save the uploaded file to the destination file path
            with open(dest_file_path, 'wb') as f:
                f.write(uploaded_file.read())

            return f"File saved successfully to {dest_file_path}"
        except Exception as e:
            return f"Error occurred: {e}"

def process_upload(uploaded_file):
    upload_folder_path = 'UploadedFile'  # This should be your uploaded file folder path
    data_loader = GradioDataLoader(upload_folder_path)
    return data_loader.save_uploaded_file(uploaded_file)

iface = gr.Interface(fn=process_upload, inputs="file", outputs="text")
iface.launch()
