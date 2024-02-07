import os

from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA
import chainlit as cl
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv('OPENAI_API_KEY')
VECTOR_STORE_PATH = 'vector_stores/chromadb'

prompt_template = PromptTemplate(template=""""
Use the provided context to answer questions about Machine Learning. If you don't know the answer reply with "The answer is not clear from the context" instead of making it up.

Context: {context}
Question: {question}
""", input_variables=['context', 'question'])


def retrieval_qa_chain(llm, prompt, vector_db):
  qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type='stuff',
    retriever=vector_db.as_retriever(search_kwargs={'k': 3}),
    return_source_documents=True,
    chain_type_kwargs={'prompt': prompt}
  )
  return qa_chain


def bot():
  embeddings = OpenAIEmbeddings(open_ai_key=API_KEY)
  vector_db = Chroma(persist_directory=VECTOR_STORE_PATH,
                     embedding_function=embeddings)
  llm = ChatOpenAI(openai_api_key=API_KEY)
  qa = retrieval_qa_chain(llm, prompt_template, vector_db)
  return qa


def answer(query):
  qa_result = bot()
  response = qa_result({'query': query})
  return response


@cl.on_chat_start
async def start():
    chain = bot()
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
