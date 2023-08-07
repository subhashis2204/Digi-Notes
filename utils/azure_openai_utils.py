import json
from langchain.chains.question_answering import load_qa_chain
from langchain.chat_models import AzureChatOpenAI
from langchain.document_loaders import TextLoader
from langchain.chains.summarize import load_summarize_chain
import openai
from langdetect import detect_langs
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
from langchain.chains import ConversationalRetrievalChain
from transformers import GPT2TokenizerFast
from flask import jsonify

db = None
qa = None
chat_history = []

class FlashCardGenerator:
    llm = None
    embedder = None
    def __init__(self, subscription_key, endpoint, deployment_name):
        self.llm = AzureChatOpenAI(
            openai_api_base=endpoint,
            openai_api_key=subscription_key,
            deployment_name=deployment_name,
            openai_api_type='azure',
            openai_api_version='2023-05-15'
        )
        self.embedder = OpenAIEmbeddings(
            deployment='openaiembedding2204', 
            openai_api_key=subscription_key, 
            openai_api_base=endpoint, 
            openai_api_type='azure', 
            openai_api_version='2023-05-15'
        )
        
        self.openai_api_key = subscription_key
        self.openai_api_base = endpoint
        self.openai_api_type = 'azure'
        self.openai_api_version = '2023-05-15'
        self.deployment_chat = deployment_name
        self.deployment_embedding = 'openaiembedding2204'

    def generate_flashcards(self):
        loader = TextLoader("output.txt", encoding='utf-8').load()
        answer = None

        print(loader)

        try:
            chain = load_qa_chain(llm=self.llm, chain_type="map_reduce")
            query = 'output : short questions and short answers in [{"question" : "question 1", "answer" : "answer to question 1"}, {...}] format'
            response = chain.run(input_documents=loader, question=query)

            print(response)
            answer = { "message": json.loads(response), "error" : False }

        except Exception as e:
            print(e)
            answer = { "message" : [], "error" : True}


        return answer
    

    def generate_flashcards_openai(self):
        
        content = ''
        with open('output.txt', 'r', encoding='utf-8') as f:
            content = f.read()

        print(content)

        languages = detect_langs(content)
        l = [lang.lang for lang in languages]
        print(l)
        t = ''
        for lang in l:
            t = t + lang + ' '

        content = [
            {
                "role" : "system",
                "content" : "You are a teacher"
            },
            {
                "role" : "user",
                "content" : f"Text contains these ${t} languages. Input : " + content + " Output : short questions and answers on the given text"
            }
        ]

        try:
            response = openai.ChatCompletion.create(
                engine=self.deployment_name,
                messages=content
            )            

            print(response)
            answer = { "message": json.loads(response), "error" : False }

        except Exception as e:
            print(e)
            answer = { "message" : [], "error" : True}
        return answer
    
    def generate_summary(self):
        answer = None

        try:
            loader = TextLoader("output.txt")
            docs = loader.load_and_split()

            chain = load_summarize_chain(llm=self.llm, chain_type="map_reduce")
            summary = chain.run(docs)

            answer = { "message": summary, "error" : False }
        except Exception as e:
            print(e)

            answer = { "message" : [], "error" : True}

        return answer
    
    def generate_vector_db(self):
        global db
        global qa

        text = ''
        with open('output.txt', 'r', encoding='utf-8') as f:
            text = f.read()

        tokenizer = GPT2TokenizerFast.from_pretrained("gpt2")

        def count_tokens(text):
            return len(tokenizer.encode(text))
        
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=512,
            chunk_overlap=24,
            length_function=count_tokens
        )

        documents = text_splitter.create_documents([text])
    
        db = FAISS.from_documents(documents, self.embedder)

        qa = ConversationalRetrievalChain.from_llm(self.llm, db.as_retriever())

        return 

    
    def questions_and_answers(self, query):
        global qa 
        global chat_history

        result = qa({"question" : query, "chat_history" : chat_history})

        if result and result['answer']:
            return jsonify({"response" : result["answer"]}), 200
        else :
            return jsonify({"response" : "Sorry, I don't know the answer to that question"}), 500
        
        