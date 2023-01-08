# Imports
from pyfiglet import Figlet
from book import Book
import json
import openai
from utils import *


# Get the OpenAI API key from the config file
def get_api_key():
    # Read the config file
    with open('config.json', 'r') as f:
        # Return the OpenAI key
        return json.load(f)['OpenAI_key']


# Draw the given text in a figlet
def draw(text):
    # Create a new figlet object
    f = Figlet()

    # Print the figlet
    print(f.renderText(text))


# Get a selection from a list of options
def get_option(options):
    # Print the available options
    print('Please select an option:')
    for i, option in enumerate(options):
        print(f'[{i + 1}] {option}')

    # While the user input is not valid
    while True:
        try:

            # Get the selection
            selection = int(input('> '))

            # Check if the selection is valid
            if selection < 1 or selection > len(options):
                raise ValueError

            # Return the selection
            return selection

        # User input was not valid
        except ValueError:
            print('Invalid option. Please try again.')


# Main function
def main():
    # Set the OpenAI API key
    openai.api_key = get_api_key()

    # Draw the title
    draw('BookGPT')

    # Check if the user wants to generate a new book or not
    if get_option(['Generate a book', 'Exit']) - 1:
        return

    # Get the number of chapters
    print('How many chapters should the book have?')
    chapters = int(input('> '))

    # Get the number of words per chapter
    print('How many words should each chapter have?')
    words = int(input('> '))

    # Get the category of the book
    print('What is the category of the book?')

    # Get all files in categories folder
    categories = get_categories()

    # Get the category
    category = categories[get_option(categories) - 1]

    # Get the topic of the book
    print('What is the topic of the book?')
    topic = input('> ')

    # Get the topic of the book
    print('What is the language of the book?')
    language = input('> ')

    # Print the book parameters
    print(f'Generating a book with {chapters} chapters, {words} words per chapter, topic "{topic}" and category "{category}" in {language}.')

    # Create a new book
    book = Book(chapters, words, topic, category, language)

    # Print title
    print(f'Title: {book.title}')

    # Print information
    print('Generate book..')

    # Generate the book
    book.generate()

    # Print the saving instruction
    saving_option = get_option(['Markdown', 'HTML'])
    if saving_option == 1:
        print('Saving to markdown...')
        with open('book.md', 'w', encoding='utf-8') as f:
            f.write(book.get_md())

    elif saving_option == 2:
        print('Saving to HTML...')
        with open('book.html', 'w', encoding='utf-8') as f:
            f.write(book.get_html())

    print('Done.')


# Run the main function
if __name__ == "__main__":
    main()
