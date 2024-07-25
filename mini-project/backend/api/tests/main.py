import requests
import logging

# Setup logging to print the logs to the console
console_handler = logging.StreamHandler()
console_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))

# General logger
general_logger = logging.getLogger('general')
general_logger.setLevel(logging.INFO)
general_logger.addHandler(console_handler)

# Error logger
error_logger = logging.getLogger('error')
error_logger.setLevel(logging.ERROR)
error_logger.addHandler(console_handler)

# URLs for testing
UPLOAD_URL = 'http://127.0.0.1:5000/files/upload'
DOWNLOAD_URL = 'http://127.0.0.1:5000/files/download/'

# Local file to upload
local_file_path = 'data.xlsx'

# Upload a file
def upload_file(file_path):
    with open(file_path, 'rb') as f:
        files = {'file': f}
        response = requests.post(UPLOAD_URL, files=files)
    print("Upload Response:", response.json())
    return response.json().get('processed_file')

# Download the processed file
def download_file(processed_filename):
    response = requests.get(DOWNLOAD_URL + processed_filename)
    if response.status_code == 200:
        with open(processed_filename, 'wb') as f:
            f.write(response.content)
        print(f"File {processed_filename} downloaded successfully.")
    else:
        print("Download Response:", response.json())

def main():
    # Upload file and get the processed filename
    processed_filename = upload_file(local_file_path)
    
    # Download the processed file
    if processed_filename:
        download_file(processed_filename)

if __name__ == "__main__":
    main()
