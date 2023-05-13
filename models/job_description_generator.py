import os
import openai
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

# Configure OpenAI API key
openai.api_key = os.getenv('OPENAI_API_KEY')


def job_description_generator(requirements):
    """
    Generates a job description based on the requirements given
    """
    prompt = "I'm sharing information related to a job description :\n" + requirements + \
        "\n prepare a comprehensive job description for this skillset. It should be formal and professional with required skillsets, knowledge, qualification, etc"
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=2048,  # Maximum length of the generated text
        n=1,  # Number of completions to generate
        stop=None,  # Stop condition to end the generated text
        temperature=0.7,  # Controls the randomness of the output
    )
    return response.choices[0].text


# Streamlit app - Job Description Generator
st.title("Job Description Creator")
with st.form("JD_Creator"):
    requirements = st.text_area(
        "Please provide the necessary skills and requirements need for the job", placeholder="JD to be given here")
    submitted = st.form_submit_button("Submit")
    if submitted:
        st.write(job_description_generator(requirements))
