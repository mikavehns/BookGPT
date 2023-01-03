# Imports
import pandas as pd
from pyfiglet import Figlet
from book import Book
from utils.utils import draw_data_structure
import json
import openai


def get_api_key():
    with open('config.json', 'r') as f:
        return json.load(f)['OpenAI_key']


def draw(text):
    # Drawing an ascii art
    f = Figlet()
    print(f.renderText(text))


def get_option(options):
    print('Please select an option:')
    for i, option in enumerate(options):
        print(f'[{i + 1}] {option}')
    while True:
        try:
            selection = int(input('> '))
            if selection < 1 or selection > len(options):
                raise ValueError
            return selection
        except ValueError:
            print('Invalid option. Please try again.')


def get_characteristics():
    characteristics = pd.read_csv('characteristics.csv')
    selection = get_option(characteristics['name'].values)
    return characteristics.iloc[selection - 1, 1::].values


def main():
    openai.api_key = get_api_key()
    draw('BookGPT')
    if get_option(['Generate a book', 'Exit']) - 1:
        return

    print('How many chapters should the book have?')
    chapters = int(input('> '))

    print('How many words should each chapter have?')
    words = int(input('> '))

    book_type, characteristics = get_characteristics()

    print('What is the topic of the book?')
    topic = input('> ')

    print(f'Generating a {book_type} book about {topic} with {chapters} chapters and {words} words per chapter...')

    book = Book(chapters, words, characteristics, topic, book_type)

    print('Book generated.\nShow structure')
    if not get_option(['Yes', 'No']) - 1:
        draw_data_structure(book.get_structure())

    print('Correct book')
    if not get_option(['Yes', 'No']) - 1:
        print('Checking for errors...')
        book.correct()
    else:
        print('Skipping correction...')

    print('Save book')
    if not get_option(['Yes', 'No']) - 1:
        book.save_txt()
    else:
        print('Skipping save.')

    print('Done.')


if __name__ == "__main__":
    main()
