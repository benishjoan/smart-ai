import openai
import os
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

# Configure OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")


def resume_validator(resume, job_description):
    """
    Validates a resume based on the job description given
    """
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant who compares a resume and Job Description. Please give a score out of 10 for this Resume for the given Job Description",
            },
            {
                "role": "user",
                "content": "This is a resume\n "
                + resume
                + " \n and this is a Job Description \n"
                + job_description,
            },
        ],
    )
    return response["choices"][0]["message"]["content"]


# Streamlit app - Resume Validator
st.title("Resume validator")

with st.form("Resume Form"):
    st.header("Resume Validator using GPT3")
    # Resume and Job Description inputs
    resume = st.text_area(
        "Paste the contents of your resume here", placeholder="Your resume")
    job_description = st.text_area(
        "Paste the contents of the Job Description here", placeholder="Job description")

    submitted = st.form_submit_button("Submit")
    if submitted:
        st.write(resume_validator(resume, job_description))
