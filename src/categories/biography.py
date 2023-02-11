import openai
import retrying
from typing import List, Dict

class Biography:
    """
    This class is used to generate a self-help book.
    """

    def __init__(self, chapter_amount: int, words_per_chapter: int, topic: str, language: str):
        """
        Initialize the class.
        :param chapter_amount: The amount of chapters in the book.
        :param words_per_chapter: The amount of words per chapter.
        :param topic: The topic of the book.
        """

        self.chapter_amount = chapter_amount
        self.words_per_chapter = words_per_chapter
        self.topic = topic
        self.language = language

    @staticmethod
    @retrying.retry(stop_max_attempt_number=5, wait_fixed=1000, retry_on_exception=lambda e: isinstance(e, openai.error.ServiceUnavailableError or openai.error.RateLimitError))
    def get_response(prompt: str):
        """
        Gets a response from the API.
        :param prompt: The prompt to send to the API.
        :return: The response from the API.
        """

        return openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            temperature=0.7,
            max_tokens=1500,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        ).choices[0].text

    def get_title(self):
        """
        Gets the title of the book.
        :return: The title of the book.
        """

        return self.get_response(
            f"Generate a title for a biography book on {self.topic} in {self.language}. "
            f"The title should be compelling and memorable, and should accurately reflect the content and purpose of the book. "
            f"The book will contain the life story and accomplishments of the person being featured. "
            f"The title should be inspiring and informative, and should encourage readers to learn about the subject's life and contributions.")

    def get_chapters(self, title: str):
        """
        Gets the chapters of the book.
        :param title: The title of the book.
        :return: The chapters of the book.
        """

        return self.get_response(
            f"Generate a list of the size {self.chapter_amount} of chapter titles for a biography book called {title}. "
            f"Each chapter should cover a specific period in the subject's life and should be structured as a series of "
            f"lessons or steps that the reader can follow to understand the events and experiences that shaped the subject's life. "
            f"The chapter titles should be descriptive and should clearly convey the main focus of each chapter. "
            f"The chapters should be engaging and informative, and should encourage the reader to learn about the subject's life and accomplishments and should be written in {self.language}.")

    def get_structure(self, title: str, chapters: List[str]):
        """
        Gets the structure of the book.
        :param title: The title of the book.
        :param chapters: The chapters of the book.
        :return: The structure of the book.
        """

        return self.get_response(
            f"Generate a structure plan for a biography book called {title} in {self.language}. "
            f"The book should contain {self.chapter_amount} chapters, with the following titles: {','.join(chapters)} "
            f"Each chapter should be structured as a chronology of the subject's life, including significant events, achievements, and challenges. "
            f"The chapters should include quotes, photographs, and personal anecdotes to help the reader understand and relate to the subject. "
            f"The book should be inspiring and engaging, and should offer insight into the subject's character and legacy. "
            f"\n\nFor each chapter, create a list of paragraph titles and corresponding recommended word counts in the following format: "
            f"'paragraph_title---word_amount.' The paragraph titles should not include the word 'paragraph' or a number. "
            f"The total recommended word count for all paragraphs in each chapter should add up to {self.words_per_chapter} words. "
            f"In order to prevent any individual paragraph from being too long, "
            f"try to divide the content into multiple paragraphs, each with a recommended word count.")

    def get_paragraph(self, title: str, chapters: list[str], paragraphs: List[List[Dict[str, str]]],
                      paragraph_index: int, chapter_index: int):
        """
        Gets a paragraph of the book.
        :param title: The title of the book.
        :param chapters: The chapters of the book.
        :param paragraphs: The paragraphs of the book.
        :param paragraph_index: The index of the paragraph.
        :param chapter_index: The index of the chapter.
        :return: The paragraph of the book.
        """

        paragraphs = paragraphs[chapter_index]
        titles = '\n'.join([paragraph["title"] + ' - ' + paragraph["word_count"] for paragraph in paragraphs])
        paragraph = paragraphs[paragraph_index]
        return self.get_response(
            f"Write the content for Chapter {chapter_index + 1} in {self.language} of a biography called {title}. The chapter is called {chapters[chapter_index]}, "
            f"and should focus on discussing a significant period in the subject's life, including their experiences, achievements, and challenges. "
            f"The chapter should include a clear explanation of the historical context and background, as well as supporting evidence and examples to illustrate the subject's life and accomplishments. "
            f"The chapter should also provide analysis and interpretation of the events and trends discussed, and may include primary sources for readers to examine. "
            f"The chapter should be written in a clear and engaging style, and should be well-organized and easy to follow. "
            f"\n\nThe chapter contains the following paragraphs:\n{titles}\nWrite the content for paragraph {paragraph_index + 1}, "
            f"with the title '{paragraph['title']}.' The paragraph should have the recommended word count of {paragraph['word_count']} words. "
            f"In order to effectively convey the main ideas and concepts of the paragraph, be sure to include relevant historical information, "
            f"anecdotes, and other sources. Use a clear and engaging writing style that will keep the reader interested and informed. "
            f"The paragraph should be well-structured and coherent, with a clear introduction, body, and conclusion. Do not write a title.")
