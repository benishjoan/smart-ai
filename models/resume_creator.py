import os
import openai
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

# Configure OpenAI API key
openai.api_key = os.getenv('OPENAI_API_KEY')


def resume_generator(data):
    """
    Generates a resume based on the information given
    """

    prompt = "I'm sharing information about me and the contents are "+data + \
        "\n I want you to build a comprehensive and professional resume with these information. Include Projects relevant to the skillsets."

    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=2048,  # Maximum length of the generated text
        n=1,  # Number of completions to generate
        stop=None,  # Stop condition to end the generated text
        temperature=0.7,  # Controls the randomness of the output
    )
    return response.choices[0].text

# Streamlit app - Resume Creator
st.title("Resume Creator")

with st.form("Resume Creator", clear_on_submit=False):
    st.header("Resume Creator using GPT3")
    st.write("Provide basic details required for resume and let GPT3 create one for you")
    name = st.text_input("Enter your name", placeholder="Name")
    email = st.text_input("Enter your email address",placeholder="someone@gmail.com")
    st.write("---")

    # Education
    degree = st.text_input("Provide the name of your degree")
    st.write("---")

    # Skills
    Skills = st.text_area("Please list your skills here",placeholder="Your skillset")
    st.write("---")

    # Projects
    Projects = st.text_area("Please list your projects here",placeholder="Your project experiences")
    st.write("---")

    # Experience
    exp = st.text_area("Please provide information on your previous experiences (if any) here", placeholder='Your experiences')
    st.write("---")

    # submit button
    submitted = st.form_submit_button("Submit")
    if submitted:
        st.write("Your info has been successfully submitted")
        st.write(resume_generator(name+"\n"+email+"\n"+degree +
                 "\n"+Skills+"\n"+Projects+"\n"+exp))
