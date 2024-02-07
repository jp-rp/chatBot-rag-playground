import os

from langchain_community.document_loaders import PyPDFLoader, PyPDFDirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv('OPENAI_API_KEY')
DATA_PATH = 'data/'
DB_PATH = 'vector_stores/chromadb'


def load_pdf_docs():
    pdf_loader = PyPDFDirectoryLoader(DATA_PATH, glob='*.pdf')
    docs = pdf_loader.load()
    return docs


def split_docs(docs):
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    texts = splitter.split_documents(docs)
    return texts


def load_vector_db(texts):
    embeddings = OpenAIEmbeddings(openai_api_key=API_KEY)

    vector_db = Chroma.from_documents(documents=texts,
                                      embedding=embeddings,
                                      persist_directory=DB_PATH)
    vector_db.persist()
    vector_db = None


if __name__ == '__main__':
    docs = load_pdf_docs()
    texts = split_docs(docs)
    load_vector_db(texts)
