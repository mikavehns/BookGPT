from book_types.nonfiction import NonFiction
import openai
from openai.error import InvalidRequestError as ire, APIConnectionError as ace
import retrying
import re


class Book:
    def __init__(self, chapter_amount: int, words_per_chapter: int, characteristics: str, topic: str, book_type: str):
        self.chapter_amount = chapter_amount
        self.words_per_chapter = words_per_chapter
        self.book_type = book_type
        self.topic = topic

        if book_type == 'non-fiction':
            content = NonFiction(chapter_amount, words_per_chapter, characteristics, topic, book_type)
        else:
            raise ValueError('This book type is not supported yet.')

        self.title = content.title
        self.chapter_titles = content.chapter_titles
        self.structure = content.structure
        self.content = content.content

    def __str__(self):
        return re.sub(r"Paragraph \d+: ", "", self.combine_chapters())

    def get_structure(self):
        return {'Title': self.title, 'Chapters': dict(zip(self.chapter_titles, self.structure))}

    @staticmethod
    def __get_edit(input_text, instruction, temperature: float = 0):
        return openai.Edit.create(
            model="text-davinci-edit-001",
            input=input_text,
            instruction=instruction,
            temperature=temperature).choices[0].text

    def combine_chapters(self):
        book = self.title + (3*"\n")
        for chapter in range(0, self.chapter_amount):
            book += self.chapter_titles[chapter] + "\n"
            book += self.content[chapter] + "\n"
        return book

    @retrying.retry(stop_max_attempt_number=2, wait_fixed=1000, retry_on_exception=lambda e: isinstance(e, ire) or isinstance(e, ace))
    def correct_chapter(self, input_text):
        print('Removing chapter titles.')
        return self.__get_edit(input_text, "Remove all Titles. Correct Grammar mistakes. Correct punctuation mistakes. Remove \"Paragraph\" and other expression in front of the paragraphs.", temperature=0.7)

    def correct(self):
        for chapter in range(0, self.chapter_amount):
            print(f'Correcting chapter {chapter + 1}.')
            try:
                self.content[chapter] = self.correct_chapter(self.content[chapter])
            except ire or ace:
                print('Could not correct chapter.')

    def save_txt(self):
        file_name = (self.title + '.txt').replace(' ', '_').replace('"', '').replace('?', '')
        if ':' in file_name:
            file_name = file_name.split(':')[0]
        path = 'books/' + file_name + '.txt'
        print(f'Saving as txt to {path}.')
        with open(path, 'w') as f:
            f.write(str(self))
