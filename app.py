from flask import Flask, jsonify, request
from dotenv import load_dotenv
import uuid
from utils.azure_blob_utils import ComputerVisionProcessor
from azure.storage.blob import ContainerClient, ContentSettings, BlobServiceClient
from utils.azure_openai_utils import FlashCardGenerator
import os
import json
from pysondb import getDb
import randomname
import codecs
from langdetect import detect_langs


db = getDb('db.json')

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

def file_mimetype_allowed(file):
    allowed_mimetypes = ['image/png', 'image/jpg', 'image/jpeg']

    if file.mimetype not in allowed_mimetypes:
        return False

    return True

def get_file_extension(file):
    return file.filename.rsplit('.', 1)[1].lower()

def find_content_type(file):
    file_extension = get_file_extension(file)

    content_type = ""
    if file_extension == 'jpg' or file_extension == '.jpeg':
        content_type = "image/jpeg"
    elif file_extension == 'png':
        content_type = "image/png"
    else:
        content_type = "application/octet-stream"

    return content_type


@app.route('/uploads/api/v1', methods=['POST'])
def upload_image():
    response = request.files.getlist('files')

    output_file = open('output.txt', 'w')

    visionClient = ComputerVisionProcessor(output_file, key, endpoint)
    gptClient = FlashCardGenerator(gpt_key, gpt_endpoint, gpt_deployment_name)

    file_urls = []

    for file in response:
        try :             
            if not file_mimetype_allowed(file):
                pass
            else :
                content_type = find_content_type(file)
                content_settings = ContentSettings(content_type)

                filename = str(uuid.uuid4()) + '.' + file.filename
                blob =  container.upload_blob(name = filename, data = file, content_settings=content_settings)
                file_urls.append(blob.url)

        except Exception as e:
            print(e)
            return jsonify({'message': 'Error uploading files'}), 500
    

    if len(file_urls) == 0:
        return jsonify({'message': 'No files to process'}), 400
    
    for url in file_urls : 
        visionClient.read_file_remote(url)

    output_file.close()

    time.sleep(1)
    answer = ''
    # answer = await gptClient.generate_flashcards_doctran()
    answer = gptClient.generate_flashcards()

    return answer

@app.route('/uploads/api/v1/summary', methods=['GET'])
def generate_summary():
    gptClient = FlashCardGenerator(gpt_key, gpt_endpoint, gpt_deployment_name)
    answer = gptClient.generate_summary()

    return answer

@app.route('/uploads/api/v1/upload', methods=['POST'])
def upload_file():
    image_files = request.files.getlist('files')
    visionClient = ComputerVisionProcessor(key, endpoint)
    file_urls = []

    try:
        for image in image_files:
            if not file_mimetype_allowed(image):
                continue

            content_type = find_content_type(image)
            content_settings = ContentSettings(content_type)

            filename = str(uuid.uuid4()) + image.filename
            blob = container.upload_blob(name=filename, data=image, content_settings=content_settings)
            file_urls.append(blob.url)

        if len(file_urls) == 0:
            return jsonify({'message': 'No files to process'}), 400

        # Upload an empty text file to Azure Blob Storage
        # file_name = str(uuid.uuid4()) + randomname.get_name() + '.txt'
        # blob_client = container.upload_blob(name=file_name, data=b'', content_settings=ContentSettings(content_type='text/plain', content_encoding='utf-8'))

        print(file_urls)
        
        lines = []
        for url in file_urls:
            visionClient.read_file_remote(url, lines)

        print('OCR completed')

        print(lines)

        with codecs.open('output.txt', 'w', encoding='utf-8', errors='ignore') as f:
            f.writelines(lines)

        f.close()

        # output_file = open('output.txt', 'w')

        # output_file.writelines(lines)

        # output_file.close()


        # with codecs.open('output.txt', 'r', encoding='utf-8', errors='ignore') as f:
        #     content = f.read()

        # print(content)

        # f.close()


        # Write the OCR results to the file in Azure Blob Storage
        # blob_client.upload_blob(data=''.join(lines), overwrite=True, content_settings=ContentSettings(content_type='text/plain', content_encoding='utf-8'))

        # new_session = {
        #     'file': blob_client.url,
        #     'created_at': time.time(),
        #     'img_urls': file_urls,
        # }

        # Save the new session details to your database
        # Replace the 'db.add(new_session)' with your actual database code
        # db.add(new_session)

        return jsonify({'message': 'Output File updated successfully'})

    except Exception as e:
        print(e)

        # If an error occurs, delete the uploaded blobs
        for url in file_urls:
            container.delete_blob(url.split('/')[-1])

        return jsonify({'message': 'Error uploading files'}), 500

@app.route('/uploads/api/v1/uploads/flashcards', methods=['GET'])
def generate_flashcards():
    # docId = request.args.get('docId')
    # blob_nf7ame = db.getById(id)['file']

    # blob_client = container.get_blob_client(blob=blob_name)
    # blob_content = blob_client.download_blob()
    # data = blob_content.decode('utf-8')

    # return blob_content.readall().decode('utf-8')
    # with open('output.txt', 'w') as file:
    #     file.write(blob_content.readall().decode('utf-8'))
    
    # file.close()
    
    gptClient = FlashCardGenerator(gpt_key, gpt_endpoint, gpt_deployment_name)
    answer = gptClient.generate_flashcards()

    return answer
    # return jsonify({'message': answer})

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000, debug=True)
