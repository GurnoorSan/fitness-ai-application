from flask import Flask, render_template, jsonify, request
from src.helpers import download_hugging_face_embeddings
from langchain_pinecone import PineconeVectorStore 
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_openai import OpenAI
from dotenv import load_dotenv
from src.prompt import *
import os

app = Flask(__name__)

load_dotenv()


PINECONE_API_KEY="pcsk_m2CNC_7Wd4hkQFNDxiNWxxQryG2J7PmmdRuUkB6wU6zWqZvSsbwSqAyMSKB32rrRKhPrc"
OPENAI_API_KEY="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"

os.environ["PINECONE_API_KEY"] = PINECONE_API_KEY
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY



embeddings = download_hugging_face_embeddings()

index_name = "fitbot"

docsearch = PineconeVectorStore.from_existing_index(index_name=index_name, embedding= embeddings)

retriever = docsearch.as_retriever(search_type = "similarity", search_kwargs = {"k": 3})

llm = OpenAI(temperature=0.4, max_tokens=500)
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        ("human", "{input}"),
    ]
)

question_answer_chain = create_stuff_documents_chain(llm, prompt)
rag_chain = create_retrieval_chain(retriever, question_answer_chain)

@app.route('/')
def index():
    return render_template('chat.html')

@app.route('/get', methods=['GET','POST'])
def chat():
    msg = request.form['msg']
    input_text = msg
    print(input_text)
    response = rag_chain.invoke({"input": msg})
    print("Response: ", response["answer"])
    return str(response["answer"])

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080, debug=True)