# Imports
import pandas as pd
from pyfiglet import Figlet
from book import Book
from utils.utils import draw_data_structure
import json
import openai


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


# Get the type of the book
def get_type():
    # Load the types list
    types = pd.read_csv('types.csv')

    # Get the type of the book
    selection = get_option(types['name'].values)

    # Return the type
    return types.iloc[selection - 1, 1::].values


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

    # Get the type of the book
    book_type, type = get_type()

    # Get the topic of the book
    print('What is the topic of the book?')
    topic = input('> ')

    # Print the book parameters
    print(f'Generating a {book_type} book about {topic} with {chapters} chapters and {words} words per chapter...')

    # Create a new book
    book = Book(chapters, words, type, topic, book_type)

    # Print that the book is done
    print('Book generated.\nShow structure')

    # Check if the user wants to show the structure
    if not get_option(['Yes', 'No']) - 1:
        # Draw the book structure
        draw_data_structure(book.get_structure())

    # Check if the user wants to run the correction
    print('Correct book')
    if not get_option(['Yes', 'No']) - 1:

        # Print that the book is being checked
        print('Checking for errors...')

        # Correct the book
        book.correct()
    else:

        # Print that the correction is skipped
        print('Skipping correction...')

    # Check if the user wants to save the book
    print('Save book')
    if not get_option(['Yes', 'No']) - 1:

        # Save the book
        book.save_txt()
    else:

        # Print that the book is not saved
        print('Skipping save.')

    # Print that the process is done
    print('Done.')


# Run the main function
if __name__ == "__main__":
    main()
