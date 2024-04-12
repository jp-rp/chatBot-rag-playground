import os

import chainlit as cl
from dotenv import load_dotenv
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_openai import ChatOpenAI

load_dotenv()
VECTOR_STORE_PATH = "vector_stores/chromadb"

prompt_template = PromptTemplate(
    template=""""
Utiliza el siguiente contexto para responder preguntas sobre un reporte.

Contexto: {context}
Pregunta: {question}
""",
    input_variables=["context", "question"],
)


def retrieval_qa_chain(llm, prompt, vector_db):
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=vector_db.as_retriever(search_kwargs={"k": 3}),  # play with fetch_k
        return_source_documents=True,
        chain_type_kwargs={"prompt": prompt},
    )
    return qa_chain


def chat():
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        model_kwargs={"device": "cpu"},
    )
    vector_db = Chroma(
        persist_directory=VECTOR_STORE_PATH, embedding_function=embeddings
    )
    llm = ChatOpenAI()
    qa = retrieval_qa_chain(llm, prompt_template, vector_db)
    return qa


def answer(query):
    qa_result = chat()
    response = qa_result({"query": query})
    return response


@cl.on_chat_start
async def start():
    chain = chat()
    msg = cl.Message(content="Starting...")
    await msg.send()
    msg.content = "Ask me anything"
    await msg.update()
    cl.user_session.set("chain", chain)


@cl.on_message
async def main(message: cl.Message):
    chain = cl.user_session.get("chain")
    call_back = cl.AsyncLangchainCallbackHandler(
        stream_final_answer=True, answer_prefix_tokens=["FINAL", "ANSWER"]
    )
    call_back.answer_reached = True
    res = await chain.acall(message.content, callbacks=[call_back])
    answer = res["result"]
    sources = res["source_documents"]

    if sources:
        answer += f"\nSources: " + str(sources)
    else:
        answer += "\nNo sources found"

    await cl.Message(content=answer).send()
