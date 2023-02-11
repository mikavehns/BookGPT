import streamlit as st
import openai
from book import Book
from utils import *

valid = False
content = ''

# Center the title
st.title('BookGPT')
st.markdown('---')


def initialize():
    global valid
    # Get the API key and check if it is valid
    api_key = st.text_input('OpenAI API Key', type='password')
    if api_key:
        openai.api_key = api_key

        # Check if the API key is valid
        try:
            openai.Engine.list()
            valid = True
            st.success('API key is valid!')

        # API key is not valid
        except openai.error.AuthenticationError:
            valid = False
            st.error('API key is not valid!')


def generate_book(chapters, words, category, topic, language):
    book = Book(chapters, words, topic, category, language)

    content = book.get_md()
    st.markdown(content)


def show_form():
    # Create form for user input
    with st.form('BookGPT'):

        # Get the number of chapters
        chapters = st.number_input('How many chapters should the book have?', min_value=3, max_value=100, value=5)

        # Get the number of words per chapter
        words = st.number_input('How many words should each chapter have?', min_value=100, max_value=3500, value=1000,
                                step=50)

        # Get the category of the book
        category = st.selectbox('What is the category of the book?',
                                get_categories())

        # Get the topic of the book
        topic = st.text_input('What is the topic of the book?', placeholder='e.g. "Finance"')

        # Get the language of the book
        language = st.text_input('What is the language of the book?', placeholder='e.g. "English"')

        # Submit button
        submit = st.form_submit_button('Generate')

        # Check if the api key was valid
        if submit and not valid:
            st.error('The API key is not valid!')

        # Check if all fields are filled
        elif submit and not (chapters and words and category and topic and language):
            st.error('Please fill in all fields!')

        # Generate the book
        elif submit:
            # Generate the book outside the form
            generate_book(chapters, words, category, topic, language)


initialize()
show_form()
