from flask import Flask, jsonify, request
from dotenv import load_dotenv
import uuid
from utils.azure_blob_utils import ComputerVisionProcessor
from azure.storage.blob import ContainerClient, ContentSettings
from utils.azure_openai_utils import FlashCardGenerator
import os
import codecs
import time
from pymongo import MongoClient
from datetime import datetime

load_dotenv()

connection_string =  os.environ['STORAGE_ENDPOINT']

key = os.environ['VISION_KEY']
endpoint = os.environ['VISION_ENDPOINT']

gpt_key = os.environ['AZURE_OPENAI_KEY']
gpt_endpoint = os.environ['AZURE_OPENAI_ENDPOINT']
gpt_deployment_name = os.environ['AZURE_OPENAI_DEPLOYMENT_NAME']

container = ContainerClient.from_connection_string(conn_str=connection_string, container_name='imgdata')
gptClient = FlashCardGenerator(gpt_key, gpt_endpoint, gpt_deployment_name)

app = Flask(__name__)

client = MongoClient('localhost', 27017)
db = client.users
collection = db.users


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

@app.route('/uploads/api/v1/uploads', methods=['POST'])
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

        print(file_urls)
        
        lines = []
        for url in file_urls:
            visionClient.read_file_remote(url, lines)

        print('OCR completed')

        print(lines)

        with codecs.open('output.txt', 'w', encoding='utf-8', errors='ignore') as f:
            f.writelines(lines)

        f.close()

        content = ''

        with codecs.open('output.txt', 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()

        # gptClient.generate_vector_db()

        sample_data = {
            'image_urls': file_urls,
            'content': content,
            'timestamp': datetime.utcnow(),
            'last_updated': datetime.utcnow()
        }

        collection.insert_one(sample_data)

        return jsonify({'message':content})

    except Exception as e:

        for url in file_urls:
            container.delete_blob(url.split('/')[-1])

        return jsonify({'message': 'Error uploading files'}), 500


@app.route('/uploads/api/v1/uploads/summary', methods=['GET'])
def generate_summary():
    answer = gptClient.generate_summary()

    return answer

@app.route('/uploads/api/v1/uploads/flashcards', methods=['GET'])
def generate_flashcards():
    answer = gptClient.generate_flashcards()

    return answer

@app.route('/uploads/api/v1/uploads/questions', methods=['GET'])
def questions_and_answers():
    query = request.args.get('query')
    answer = gptClient.questions_and_answers(query)

    return answer

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000, debug=True)
