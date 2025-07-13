from langchain.chains.retrieval_qa.base import RetrievalQA
from langchain_community.vectorstores import FAISS
from langchain_huggingface.embeddings import HuggingFaceEmbeddings
from transformers import pipeline
from langchain_huggingface.llms import HuggingFacePipeline

from rag.prompts import get_prompt_template


def load_vectorstore():
    # initialize the sentence transformer model
    embedding = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    # loads vector index from local directory
    return FAISS.load_local("vector_index", embedding, allow_dangerous_deserialization=True)


def answer_question(question: str, persona: str = "friendly") -> str:
    retriever = load_vectorstore().as_retriever()
    # Hugging Face LLM
    hf_pipeline = pipeline(
        "text2text-generation",
        model="google/flan-t5-base",
        max_new_tokens=300,
        temperature=0.7,
        top_p=0.95,
        do_sample=True,
        device=0
    )
    llm = HuggingFacePipeline(pipeline=hf_pipeline)

    # Prompt setup
    prompt = get_prompt_template(persona)

    # QA Chain with custom prompt
    chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",  # uses the full context
        retriever=retriever,
        chain_type_kwargs={"prompt": prompt}
    )

    # return response from model
    return chain.invoke(question)
