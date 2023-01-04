# Imports
import openai
from num2words import num2words


class NonFiction:
    """
    A class to generate a non-fiction book on the given topic, type and category.
    It will return a book with the given number of chapters and words per chapter.

    Attributes:
        chapter_amount (int): The number of chapters in the book.
        words_per_chapter (int): The number of words per chapter.
        type (str): The type of book, e.g. "novel" or "textbook".
        topic (str): The topic the book should be about.
        category (str): The category the book should be in, e.g. "children's fiction" or "non-fiction".
        title (str): The title of the book.
        chapter_titles (list): A list of strings containing the titles of each chapter.
        structure (list): A list of lists of strings, each inner list containing the structure of each chapter.
        content (list): A list of strings, each containing the content of each chapter.
    """

    def __init__(self, chapter_amount: int, words_per_chapter: int, type: str, topic: str, category: str):
        """
        The constructor for the NonFiction class.

        :param chapter_amount (int): The number of chapters the book should have.
        :param words_per_chapter (int): The number of words the book should have.
        :param type (str): The type of the book (e.g. novel, essay, etc.).
        :param topic (str): The topic of the book (e.g. history, politics, etc.).
        :param category (str): The category of the book (e.g. non-fiction, fiction, etc.).
        """

        # Define the amount of chapters
        self.chapter_amount = chapter_amount

        #  Define the number of words per chapter
        self.words_per_chapter = words_per_chapter

        # Define the category of the book
        self.category = category

        # Define the topic of the book
        self.topic = topic

        # Define the type of the book
        self.type = type

        # Get the title of the book
        self.title = self.__get_title()

        # Get the chapter titles for the book
        self.chapter_titles = self.__get_chapter_names()

        # Generate the structure of the book
        self.structure = self.__get_structure()

        # Generate the content of the book
        self.content = self.__get_content()

    @staticmethod
    def get_response(input_text: str, max_tokens: int = 1000, temperature: float = 0.7, top_p: float = 1,
                     best_of: int = 1, frequency_penalty: float = 0.6, presence_penalty: float = 0.6):
        """
        A static method to get a response from the OpenAI engine.

        :param input_text: The input text to feed to the OpenAI engine (str).
        :param max_tokens: The maximum number of tokens to generate (int).
        :param temperature: The temperature for the OpenAI engine (float).
        :param top_p: The top-p for the OpenAI engine (float).
        :param best_of: The best-of for the OpenAI engine (int).
        :param frequency_penalty: The frequency penalty for the OpenAI engine (float).
        :param presence_penalty: The presence penalty for the OpenAI engine (float).
        :return (str): The response from the OpenAI engine.
        """

        # Create a completion object using the OpenAI engine
        completion = openai.Completion.create(
            engine="text-davinci-003",
            prompt=input_text,
            max_tokens=max_tokens,
            temperature=temperature,
            top_p=top_p,
            best_of=best_of,
            frequency_penalty=frequency_penalty,
            presence_penalty=presence_penalty
        )

        # Return the response from the OpenAI engine
        return completion.choices[0].text

    def __get_title(self):
        """
        A private method to get the title of the book.

        :return (str): The title of the book.
        """

        # Return the title of the book
        return self.get_response('Choose a title for a book about '
                                 + self.topic + '. The book should be a '
                                 + self.category + ' book. The book should be written in a '
                                 + self.type + '.', best_of=5).replace("\n", "")

    def __get_structure(self):
        """
        A private method to generate the structure of the book.

        :return (list): A list of the structure of the chapters.
        """

        # Create an empty list for the chapter structures
        structures = []

        # For each chapter, get the content structure
        for chapter in range(1, self.chapter_amount + 1):
            structures.append(self.__get_content_structure(chapter))

        # Return the chapter structures
        return structures

    def __get_content_structure(self, chapter: int):
        """
        A private method that uses the get_response() method to generate the content structure for a given chapter.

        :param chapter: Integer - The chapter number for which the content structure is generated.

        :return: List of strings - A list with the content structure for the given chapter.
        """

        # Generate the content structure
        structure = self.get_response(f'Imagine a '
                                      f'{self.category} '
                                      f'{self.topic} book, called '
                                      f'{self.title}. '
                                      f'{self.type} The book has '
                                      f'{self.chapter_amount} chapters, which are: '
                                      + "\n".join(self.chapter_titles)
                                      + f'\nYour task is to write a content structure for the '
                                        f'{num2words(chapter, to="ordinal")} chapter, which is naming different paragraphs it should contain, so the chapter could reach 750 words. '
                                        f'List the different paragraphs in the format "Paragraph n:" (n is the number of the paragraph).',
                                      max_tokens=500).split("\n")

        # Remove empty elements from the structure
        structure = [chapter for chapter in structure if chapter != "" and chapter != " "]

        # Return the chapter structure
        return structure

    def __get_chapter_names(self):
        """
        A private method that uses the get_response() method to generate the chapter titles for the book.

        :return: List of strings - A list with the chapter titles for the book.
        """

        # Get the chapter titles
        chapters = self.get_response(f"I am writing a "
                                     f"{self.chapter_amount} chapter book about "
                                     f"{self.topic}. "
                                     f"{self.type}. The book's title is "
                                     f"{self.title} and is "
                                     f"{self.category}. Create fitting and creative titles for each chapter, that build up on each other and list them below in the format \"Chapter n:\" (n is the number of the chapter).",
                                     best_of=5).split("\n")

        # Remove empty elements from the chapter titles
        chapters = [chapter for chapter in chapters if chapter != "" and chapter != " "]

        # Return the chapter titles
        return chapters

    def __get_chapter_content(self, chapter_number: int):
        """
        A private method that uses the get_response() method to generate the content of a given chapter.

        :param chapter_number: Integer - The chapter number for which the content is generated.

        :return: String - The content of the given chapter.
        """

        # Get the content of the chapter
        content = self.get_response(f'Imagine a '
                                    f'{self.category} '
                                    f'{self.topic} book, called '
                                    f'{self.title}. '
                                    f'{self.type} The book has '
                                    f'{self.chapter_amount} chapters, one of which is '
                                    f'{self.chapter_titles[chapter_number - 1]}. The content structure of this chapter is:'
                                    + "\n".join(self.structure[chapter_number - 1])
                                    + '\nYour task is to write the chapter using the content structure. '
                                      'The chapter should contain every paragraph listed above. '
                                      'The paragraphs should be built on top of each other, totalling to about '
                                      f'{self.chapter_amount} words.', max_tokens=3000)

        # Return the content of the chapter
        return content

    def __get_content(self):
        """
        A private method that uses the __get_chapter_content() method to generate the content of each chapter.

        :return: List of strings - A list with the content of each chapter.
        """

        # Create an empty list for the chapter contents
        content = []

        # For each chapter, get the content
        for chapter in range(1, self.chapter_amount + 1):
            content.append(self.__get_chapter_content(chapter))

        # Return the contents of the chapters
        return content
