import openai
import os
from dotenv import load_dotenv
import streamlit as st
from streamlit import session_state as ss

load_dotenv()

# Configure OpenAI API key
openai.api_key = os.getenv('OPENAI_API_KEY')


def hindi_to_english_translator(hindi_text):
    """
    Translates the given Hindi text to English
    """
    prompt = "I'm sharing a set of words in Hindi, these are the words" + \
        hindi_text+"translate them to English"
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=2048,  # Maximum length of the generated text
        n=1,  # Number of completions to generate
        stop=None,  # Stop condition to end the generated text
        temperature=0.7,  # Controls the randomness of the output
    )
    return response.choices[0].text


def summarizer(input_content):
    """
    Summarises the given text and provides information on the order details
    """
    prompt = "summarise the following text and give information on the order details " + \
        input_content+" do not provide additional information"
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=2048,  # Maximum length of the generated text
        n=1,  # Number of completions to generate
        stop=None,  # Stop condition to end the generated text
        temperature=0.7,  # Controls the randomness of the output
    )

    return response.choices[0].text


# Streamlit app - Multi Lingual AI
st.header("Language Translation with GPT based models")

col1, col2, col3 = st.columns([1, 1, 1])

# Summarizer and data extractor
with col1:
    st.text_area("Paste the input text here",
                 placeholder="Input text", key="Input")
    translator = st.button("Translate", key="Translate")
    if translator:
        hindi_text = ss['Input']
        translated_text = hindi_to_english_translator(hindi_text)
        ss['Output'] = translated_text

# Hindi to English Translator
with col2:
    st.text_area("The translated text is ",
                 placeholder="Translated text is", key="Output")
    summarizer = st.button('Submit')
    if summarizer:
        text = ss['Output']
        summarised_text = summarizer(text)
        ss['summary'] = summarised_text

# Output of the summarizer/Translator
with col3:
    st.text_area("AI's answer", key="summary")
