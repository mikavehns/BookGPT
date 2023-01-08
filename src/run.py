# Imports
from pyfiglet import Figlet
from book import Book
from utils import *
import json
import openai
import os


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

    # Print the book parameters
    print(f'Generating a book with {chapters} chapters, {words} words per chapter, topic "{topic}" and category "{category}".')

    # Create a new book
    book = Book(chapters, words, topic, category)

    # Print title
    print(f'Title: {book.title}')

    # Print chapter titles
    print('Chapter titles:')
    for i, title in enumerate(book.chapter_titles):
        print(f'[{i + 1}] {title}')

    # Print the structure
    print('\nStructure:')
    print(book.structure)

    # Print Information
    print('\nGenerating content...')

    # Generate the book
    book.save_md()

    # Print that the process is done
    print('Done.')


# Run the main function
if __name__ == "__main__":
    main()
