import json
from langchain.chains.question_answering import load_qa_chain
from langchain.chat_models import AzureChatOpenAI
from langchain.document_loaders import TextLoader
from langchain.chains.summarize import load_summarize_chain
# from doctran import Doctran
import openai
from langdetect import detect_langs

class FlashCardGenerator:

    def __init__(self, subscription_key, endpoint, deployment_name):
        self.llm = AzureChatOpenAI(
            openai_api_base=endpoint,
            openai_api_key=subscription_key,
            deployment_name=deployment_name,
            openai_api_type='azure',
            openai_api_version='2023-05-15'
        )
        openai.api_key = subscription_key
        openai.api_base = endpoint
        openai.api_type = 'azure'
        openai.api_version = '2023-05-15'
        self.deployment_name = deployment_name

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

    # async def generate_flashcards_doctran(self):
        
    #     try:
    #         doctran = Doctran(openai_api_key='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', openai_model = 'gpt-3.5-turbo-0613')

    #         with open('output.txt', 'r') as f:
    #             content = f.read()

    #         document = doctran.parse(content=content)

    #         response = await document.interrogate().execute()
    #         results = response.extracted_properties

    #     except Exception as e:
    #         print(e)
    #         results = []

    #     return results
    
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
    

            


