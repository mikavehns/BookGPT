from categories.nonfiction import NonFiction
import openai
from openai.error import InvalidRequestError as ire, APIConnectionError as ace
import retrying
import re
import os


class Book:
    """
    This class represents a book.

    Attributes:
        chapter_amount: The amount of chapters the book has.
        words_per_chapter: The amount of words per chapter.
        category: The category of the book.
        topic: The topic of the book.
        title: The title of the book.
        chapter_titles: The titles of the chapters.
        structure: The structure of the book.
        content: The content of the book.
    """

    def __init__(self, chapter_amount: int, words_per_chapter: int, type: str, topic: str, category: str):
        """
        This is the constructor for the Book class. It initializes the object with the given parameters.
        :param chapter_amount: The number of chapters in the book (int).
        :param words_per_chapter: The number of words per chapter (int).
        :param type: The type of book (fiction, non-fiction, etc) (str).
        :param topic: The topic of the book (str).
        :param category: The category of the book (fiction, non-fiction, etc) (str).
        """

        # Define the amount of chapters
        self.chapter_amount = chapter_amount

        # Define the amount of words per chapter
        self.words_per_chapter = words_per_chapter

        # Define the category of the book
        self.category = category

        # Define the topic of the book
        self.topic = topic

        # Check what category of book it is
        if category == 'non-fiction':

            # If it is non-fiction, create a non-fiction book
            content = NonFiction(chapter_amount, words_per_chapter, type, topic, category)

        else:

            # If the book category is not supported, raise an error
            raise ValueError('This book type is not supported yet.')

        # Define the title of the book
        self.title = content.title

        # Define the chapter titles
        self.chapter_titles = content.chapter_titles

        # Define the structure of the book
        self.structure = content.structure

        # Define the content of the book
        self.content = content.content

    def __str__(self):
        """
        This method returns a string representation of the book object.
        """

        # Remove all expressions that begin with "Paragraph" and return the book as a string
        return re.sub(r"Paragraph \d+: ", "", self.combine_chapters())

    def get_structure(self):
        """
        This method returns a dictionary containing the title, chapters, and structure of the book.
        """

        # Create a dictionary to store the structure
        return {'Title': self.title, 'Chapters': dict(zip(self.chapter_titles, self.structure))}

    @staticmethod
    def __get_edit(input_text, instruction, temperature: float = 0):
        """
        This is a private, static method for getting an edited version of the given input text.
        :param input_text: The text to be edited.
        :param instruction: The instructions for the edit.
        :param temperature: The temperature of the edit (defaults to 0).
        :return: The edited text.
        """

        # Define the engine to use and returning the edited version
        return openai.Edit.create(
            model="text-davinci-edit-001",
            input=input_text,
            instruction=instruction,
            temperature=temperature).choices[0].text

    def combine_chapters(self):
        """
        This method combines all the chapters of the book into one string.
        :return: The book as a single string.
        """

        # Define the book variable as the title with three empty lines below it
        book = self.title + (3*"\n")

        # Loop through all the chapters
        for chapter in range(0, self.chapter_amount):

            # Add the chapter title and the content of the chapter to the book
            book += self.chapter_titles[chapter] + "\n"
            book += self.content[chapter] + "\n"

        # Return the book
        return book

    @retrying.retry(stop_max_attempt_number=2, wait_fixed=1000, retry_on_exception=lambda e: isinstance(e, ire) or isinstance(e, ace))
    def correct_chapter(self, input_text):
        """
        This method corrects the grammar and punctuation of a given chapter.
        :param input_text: The text of the chapter to be corrected.
        :return: The corrected text of the chapter.
        """

        # Define the instruction for the edit and return the edited version
        return self.__get_edit(input_text, "Remove all Titles. Correct Grammar mistakes. Correct punctuation mistakes. Remove \"Paragraph\" and other expression in front of the paragraphs.", temperature=0.7)

    def correct(self):
        """
        This method corrects the grammar and punctuation of all chapters in the book.
        """

        # Loop through all the chapters
        for chapter in range(0, self.chapter_amount):

            try:

                # Correct the grammar and punctuation of the chapter
                self.content[chapter] = self.correct_chapter(self.content[chapter])

            except ire or ace:

                print(f'Could not correct chapter {chapter + 1}.')

    def save_txt(self):
        """
        This method saves the book as a text file.
        """

        # Check if the directory to save the book in exists
        if not os.path.exists('books'):

            # If it does not exist, create the directory
            os.mkdir('books')

        # Define the variable for the file name as the title of the book with all spaces replaced by underscores
        file_name = (self.title + '.txt').replace(' ', '_').replace('"', '').replace('?', '')

        # Checking the file name has a colon
        if ':' in file_name:

            # If it does, split the file name at the colon and set the file name as the first part
            file_name = file_name.split(':')[0]

        # Define the file path as the file name plus the directory to save the book in
        path = 'books/' + file_name + '.txt'

        # Open the file
        with open(path, 'w') as f:

            # Write the book to the file
            f.write(str(self))
