import os
import fitz
import openai
import streamlit as st
from langchain.chains import RetrievalQA
from langchain.llms import OpenAI
from langchain.indexes import VectorstoreIndexCreator
from langchain.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.document_loaders import PyMuPDFLoader
from langchain.vectorstores import Chroma
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.docstore.document import Document
from langchain import OpenAI, VectorDBQA
from dotenv import load_dotenv
from typing import Any, List, Optional


load_dotenv()


# Configure OpenAI API key
openai.api_key = os.getenv('OPENAI_API_KEY')

# Streamlit app - Q&A Chat Bot using GPT3
st.title("Q&A Chat Bot using GPT3")


def load_pdf(self, **kwargs: Optional[Any]) -> List[Document]:
    """
    Load a PDF file into a list of documents.
    """

    # Load the PDF file
    doc = fitz.open("pdf", self.getvalue())

    return [
        Document(
            page_content=page.get_text(**kwargs).encode("utf-8"),
            metadata=dict(
                {
                    "source": "Uploaded",
                    "file_path": "N/A",
                    "page_number": page.number + 1,
                    "total_pages": len(doc),
                },
                **{
                    k: doc.metadata[k]
                    for k in doc.metadata
                    if type(doc.metadata[k]) in [str, int]
                }
            ),
        )
        for page in doc
    ]


def extract_pdf_content(pdf_filepath, question):
    """
    Extract the content from a PDF file.
    """

    # Load the PDF file
    documents = load_pdf(pdf_filepath)

    # Process the documents
    text_splitter = CharacterTextSplitter(chunk_overlap=0, chunk_size=1000)
    texts = text_splitter.split_documents(documents)
    # print(texts)

    # Configure the LLM
    llm = OpenAI(
        model_name="text-davinci-003",
        temperature=0.7,
        openai_api_key=openai.api_key
    )
    embeddings = OpenAIEmbeddings(openai_api_key=openai.api_key)
    docsearch = Chroma.from_documents(texts, embeddings)
    QA_bot = RetrievalQA.from_chain_type(
        llm=llm, chain_type="stuff", retriever=docsearch.as_retriever(search_kwargs={"k": 1}), )
    answer = QA_bot.run(question)
    return answer


# Upload the file
pdf_file = st.file_uploader("Give the file here")

# Ask the question
if pdf_file is not None:
    with st.form('Q&A Form'):
        question = st.text_input(
            "Ask your question", placeholder="You question ...")
        ask = st.form_submit_button("Ask")
        if ask:
            st.text_area("**AI's** Answer is ",
                         value=extract_pdf_content(pdf_file, question))
