import json
from langchain.chains.question_answering import load_qa_chain
from langchain.chat_models import AzureChatOpenAI
from langchain.document_loaders import TextLoader


class FlashCardGenerator:

    def __init__(self, subscription_key, endpoint, deployment_name):
        self.llm = AzureChatOpenAI(
            openai_api_base=endpoint,
            openai_api_key=subscription_key,
            deployment_name=deployment_name,
            openai_api_type='azure',
            openai_api_version='2023-05-15'
        )

    def generate_flashcards(self):
        loader = TextLoader("output.txt").load()

        print(loader)

        chain = load_qa_chain(llm=self.llm, chain_type="map_reduce")
        query = 'output : 2 questions and their answers in [{"question" : "question 1", "answer" : "answer to question 1"}, {...}] format'

        response = chain.run(input_documents=loader, question=query)

        answer = json.loads(response)

        return answer
