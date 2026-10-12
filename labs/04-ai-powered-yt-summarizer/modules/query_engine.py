from langchain.chains import LLMChain
from langchain_community.vectorstores import FAISS

from config import TOP_K
from modules.llm_interface import build_embeddings, build_llm
from modules.prompts import QA_PROMPT, SUMMARY_PROMPT
from modules.transcript import chunk_transcript, load_transcript


def summarize(url):
    chain = LLMChain(llm=build_llm(), prompt=SUMMARY_PROMPT, verbose=True)
    return chain.invoke({"transcript": load_transcript(url)})["text"]


def build_index(url):
    # one index per video, so follow-up questions don't embed the transcript again
    return FAISS.from_texts(chunk_transcript(load_transcript(url)), build_embeddings())


def answer(url, question):
    docs = build_index(url).similarity_search(question, k=TOP_K)
    context = "\n".join(doc.page_content for doc in docs)

    chain = LLMChain(llm=build_llm(), prompt=QA_PROMPT, verbose=True)
    return chain.invoke({"context": context, "question": question})["text"]
