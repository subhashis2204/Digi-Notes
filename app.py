from flask import Flask, jsonify, request
from dotenv import load_dotenv
import uuid
from utils.azure_blob_utils import ComputerVisionProcessor
from azure.storage.blob import ContainerClient, ContentSettings
from utils.azure_openai_utils import FlashCardGenerator
import os

import time

load_dotenv()


connection_string =  os.environ['STORAGE_ENDPOINT']

key = os.environ['VISION_KEY']
endpoint = os.environ['VISION_ENDPOINT']

gpt_key = os.environ['AZURE_OPENAI_KEY']
gpt_endpoint = os.environ['AZURE_OPENAI_ENDPOINT']
gpt_deployment_name = os.environ['AZURE_OPENAI_DEPLOYMENT_NAME']

container = ContainerClient.from_connection_string(conn_str=connection_string, container_name='imgdata')

app = Flask(__name__)


@app.route('/')
def index():
    return jsonify({'message': 'Hello, World!'})

file_extensions = ['image/png', 'image/jpg', 'image/jpeg']


@app.route('/uploads/api/v1', methods=['POST'])
def upload_image():
    response = request.files.getlist('files')

    visionClient = ComputerVisionProcessor(key, endpoint)
    gptClient = FlashCardGenerator(gpt_key, gpt_endpoint, gpt_deployment_name)

    file_urls = []

    for file in response:
        try : 
            file_extension = file.filename.rsplit('.', 1)[1].lower()
            
            if file.mimetype not in file_extensions:
                pass
            else :
                print(file)
                content_type = ""
                if file_extension == 'jpg' or file_extension == '.jpeg':
                    print('jpg')
                    content_type = "image/jpeg"
                elif file_extension == 'png':
                    print('png')
                    content_type = "image/png"
                else:
                    content_type = "application/octet-stream"

                content_settings = ContentSettings(content_type)

                filename = str(uuid.uuid4()) + '.' + file_extension
                blob =  container.upload_blob(name = filename, data = file, content_settings=content_settings)
                file_urls.append(blob.url)

                print(blob.url)

        except Exception as e:
            print(e)
            return jsonify({'message': 'Error uploading files'}), 500
    
    for url in file_urls : 
        visionClient.read_file_remote(url)

    time.sleep(1)

    answer = gptClient.generate_flashcards()

    return answer

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000, debug=True)
