import os
import sys
import fitz
import openai
from dotenv import load_dotenv
import streamlit as st
from langchain import OpenAI, PromptTemplate, LLMChain
from langchain.text_splitter import CharacterTextSplitter
from langchain.chains.mapreduce import MapReduceChain
from langchain.prompts import PromptTemplate
from langchain.document_loaders import PyMuPDFLoader
from langchain.docstore.document import Document
from langchain.chains.summarize import load_summarize_chain

load_dotenv()

# Set the title of the app
st.header("Document Summarisation using OpenAI GPT3")

# Configure OpenAI API key
openai.api_key = os.getenv('OPENAI_API_KEY')

# Load the model
llm = OpenAI(temperature=0, openai_api_key=openai.api_key)

# Upload the file
pdf_file = st.file_uploader("Upload the file here")

if pdf_file is not None:
    # Convert the pdf file to text
    doc = fitz.open("pdf", pdf_file.getvalue())
    out = open("file"+".txt", "wb")

    # Write the text to a file
    for page in doc:
        text = page.get_text().encode("utf8")
        out.write(text)
        out.write(bytes((12,)))
    out.close()

    # Split the text into sentences
    text_splitter = CharacterTextSplitter()
    with open("file.txt") as f:
        state_of_the_union = f.read()
    texts = text_splitter.split_text(state_of_the_union)

    # Create a document object
    docs = [Document(page_content=t) for t in texts[:1]]

    # Create a prompt template
    prompt_template = """Write a detailed summary of the following in 1000 words:{text} DETAILED SUMMARY IN English:"""
    PROMPT = PromptTemplate(template=prompt_template, input_variables=["text"])

    # Create a summarization chain
    chain = load_summarize_chain(
        llm, 
        chain_type="map_reduce",
        return_intermediate_steps=False, 
        map_prompt=PROMPT, 
        combine_prompt=PROMPT
    )
    result = chain({"input_documents": docs}, return_only_outputs=True)
    st.write(result['output_text'])
