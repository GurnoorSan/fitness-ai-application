from src.helpers import load_pdf_file, text_split, download_hugging_face_embeddings
from pinecone import  ServerlessSpec
from langchain_pinecone import PineconeVectorStore
from pinecone.grpc import PineconeGRPC as Pinecone
from dotenv import load_dotenv
import os
import time

load_dotenv()

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
os.environ["PINECONE_API_KEY"] = PINECONE_API_KEY

extracted_data = load_pdf_file("data/") 
text_chunks = text_split(extracted_data)
embeddings = download_hugging_face_embeddings()



pc = Pinecone(api_key= PINECONE_API_KEY)


index_name = "fitbot"


for chunk in text_chunks:
    docsearch = PineconeVectorStore.from_documents(
        documents=[chunk],
        index_name=index_name,
        embedding=embeddings,
    )
