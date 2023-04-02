# Imports
from pyfiglet import Figlet
from book import Book
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
    # Check if it is below 1200
    words = int(input('> '))
    if words <= 1200:
        words = 1200
        print('The number of words per chapter has been set to 1200. (The max number of words per chapter)')

    # Get the category of the book
    print('What is the category of the book?')
    category = input('> ')

    # Get the topic of the book
    print('What is the topic of the book?')
    topic = input('> ')

    # What is the tolerance of the book?
    print('What is the tolerance of the book? (0.8 means that 80% of the words will be written 100%)')
    tolerance = float(input('> '))
    if tolerance < 0 or tolerance > 1:
        tolerance = 0.8

    # Do you want to add any additional parameters?
    print('Do you want to add any additional parameters?')
    if get_option(['No', 'Yes']) - 1:
        print(
            'Please enter the additional parameters in the following format: "parameter1=value1, parameter2=value2, ..."')
        additional_parameters = input('> ')
        additional_parameters = additional_parameters.split(', ')
        for i in range(len(additional_parameters)):
            additional_parameters[i] = additional_parameters[i].split('=')
        additional_parameters = dict(additional_parameters)
    else:
        additional_parameters = {}

    # Initialize the Book
    book = Book(chapters=chapters, words_per_chapter=words, topic=topic, category=category, tolerance=tolerance,
                **additional_parameters)

    # Print the title
    print(f'Title: {book.get_title()}')

    # Ask if he wants to change the title until he is satisfied
    while True:
        print('Do you want to generate a new title?')
        if get_option(['No', 'Yes']) - 1:
            print(f'Title: {book.get_title()}')
        else:
            break

    # Print the structure of the book
    print('Structure of the book:')
    structure, _ = book.get_structure()
    print(structure)

    # Ask if he wants to change the structure until he is satisfied
    while True:
        print('Do you want to generate a new structure?')
        if get_option(['No', 'Yes']) - 1:
            print('Structure of the book:')
            structure, _ = book.get_structure()
            print(structure)
        else:
            break

    print('Generating book...')

    # Initialize the book generation
    book.finish_base()

    content = book.get_content()

    # Save the book
    book.save_book()
    print('Book saved as book.md.')


# Run the main function
if __name__ == "__main__":
    main()
