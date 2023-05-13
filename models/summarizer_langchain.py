import os
import sys
import fitz
from langchain import OpenAI, PromptTemplate, LLMChain
from langchain.text_splitter import CharacterTextSplitter
from langchain.chains.mapreduce import MapReduceChain
from langchain.prompts import PromptTemplate
from langchain.document_loaders import PyMuPDFLoader
from langchain.chains.summarize import load_summarize_chain
from langchain.docstore.document import Document

# Configure LLM
llm = OpenAI(temperature=0)


def summarize_pdf(pdf_path):
    """
    Summarize a PDF file using OpenAI's LLM.
    """

    # Convert the pdf file to text
    doc = fitz.open(pdf_path)
    out = open("file" + ".txt", "wb")
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
    docs = [Document(page_content=t) for t in texts[:3]]
    chain = load_summarize_chain(llm, chain_type="map_reduce")

    return chain.run(docs)


if __name__ == "__main__":
    pdf_path = sys.argv[1]
    result = summarize_pdf(pdf_path)
    print(result)
