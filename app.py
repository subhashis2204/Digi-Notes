from flask import Flask, jsonify, request
from dotenv import load_dotenv
import uuid
from utils.azure_blob_utils import ComputerVisionProcessor
from azure.storage.blob import ContainerClient, ContentSettings
from utils.azure_openai_utils import FlashCardGenerator
from utils.file_utils import file_mimetype_allowed, find_content_type
import os
import codecs
import time
from pymongo import MongoClient, ReturnDocument
from datetime import datetime
from bson import ObjectId
import concurrent.futures


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

client = MongoClient("mongodb://localhost:27017")
db = client.users
collection = db.users


@app.route('/')
def home_route():
    response = collection.find({}, {"image_url" : 1, "timestamp" : 1, "last_updated" : 1})

    documents = []
    for document in response:
        document['_id'] = str(document['_id'])
        documents.append(document)

    return jsonify({'message': documents})

@app.route('/uploads', methods=['POST'])
def upload_route():
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

        # content = ''

        # with codecs.open('output.txt', 'r', encoding='utf-8', errors='ignore') as f:
        #     content = f.read()

        # gptClient.generate_vector_db()


        with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
            # Submit the tasks to the executor
            flashcards_future = executor.submit(gptClient.generate_flashcards)
            summary_future = executor.submit(gptClient.generate_summary)

            # Wait for both tasks to complete
            flashcards_result = flashcards_future.result()
            summary_result = summary_future.result()

        # summary = gptClient.generate_summary()

        # print("summary\n\n")
        # print(summary)

        # print("\n\n")


        # flashCards = gptClient.generate_flashcards()

        # print("flashcards\n\n")
        # print(flashCards)

        print("\n\n")

        print(flashcards_result)

        print("\n\n")

        print(summary_result)

        print("\n\n")

        sample_data = {
            'image_urls': file_urls,
            'summary': summary_result,
            'flashcards': flashcards_result,
            'timestamp': datetime.utcnow(),
            'last_updated': datetime.utcnow()
        }

        response = collection.insert_one(sample_data)

        print(response)

        return jsonify({'message': 'Files uploaded successfully'})

    except Exception as e:

        # for url in file_urls:
        #     container.delete_blob(url.split('/')[-1])

        return jsonify({'message': 'Error uploading files'}), 500


@app.route('/uploads/<string:id>', methods=['GET'])
def get_document_id(id):
    object_id = ObjectId(id)

    response = collection.find_one_and_update(
        {"_id" : object_id}, 
        {"$set" : {"last_updated" : datetime.utcnow()}},
        # {"_id" : 1, "last_updated" : 1}, 
        return_document=ReturnDocument.AFTER
    )

    response["_id"] = str(response["_id"])

    return jsonify({"answer": response})


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
