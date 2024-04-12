from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

DATA_PATH = "data/"
DB_PATH = "vector_stores/chromadb"


def load_pdf_docs():
    pdf_loader = PyPDFDirectoryLoader(DATA_PATH, glob="*.pdf")
    docs = pdf_loader.load()
    return docs


def split_docs(docs):
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    texts = splitter.split_documents(docs)
    return texts


def load_vector_db(texts):
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        model_kwargs={"device": "cpu"},
    )

    vector_db = Chroma.from_documents(
        documents=texts, embedding=embeddings, persist_directory=DB_PATH
    )
    vector_db.persist()


docs = load_pdf_docs()
texts = split_docs(docs)
load_vector_db(texts)
