import openai
from num2words import num2words


class NonFiction:
    def __init__(self, chapter_amount: int, words_per_chapter: int, characteristics: str, topic: str, book_type: str):
        self.chapter_amount = chapter_amount
        self.words_per_chapter = words_per_chapter
        self.book_type = book_type
        self.topic = topic
        self.characteristics = characteristics

        self.title = self.__get_title()
        self.chapter_titles = self.__get_chapter_names()
        self.structure = self.__get_structure()
        self.content = self.__get_content()

    @staticmethod
    def get_response(input_text: str, max_tokens: int = 1000, temperature: float = 0.7, top_p: float = 1,
                     best_of: int = 1, frequency_penalty: float = 0.6, presence_penalty: float = 0.6):
        return openai.Completion.create(
            engine="text-davinci-003",
            prompt=input_text,
            max_tokens=max_tokens,
            temperature=temperature,
            top_p=top_p,
            best_of=best_of,
            frequency_penalty=frequency_penalty,
            presence_penalty=presence_penalty
        ).choices[0].text

    def __get_title(self):
        return self.get_response('Choose a title for a book about '
                                 + self.topic + '. The book should be a '
                                 + self.book_type + ' book. The book should be written in a '
                                 + self.characteristics + '.', best_of=5).replace("\n", "")

    def __get_structure(self):
        structures = []
        for chapter in range(1, self.chapter_amount + 1):
            structures.append(self.__get_content_structure(chapter))
        return structures

    def __get_content_structure(self, chapter: int):
        structure = self.get_response(f'Imagine a '
                                      f'{self.book_type} '
                                      f'{self.topic} book, called '
                                      f'{self.title}. '
                                      f'{self.characteristics} The book has '
                                      f'{self.chapter_amount} chapters, which are: '
                                      + "\n".join(self.chapter_titles)
                                      + f'\nYour task is to write a content structure for the '
                                        f'{num2words(chapter, to="ordinal")} chapter, which is naming different paragraphs it should contain, so the chapter could reach 750 words. '
                                        f'List the different paragraphs in the format "Paragraph n:" (n is the number of the paragraph).',
                                      max_tokens=500).split("\n")

        structure = [chapter for chapter in structure if chapter != "" and chapter != " "]

        return structure

    def __get_chapter_names(self):
        chapters = self.get_response(f"I am writing a "
                                     f"{self.chapter_amount} chapter book about "
                                     f"{self.topic}. "
                                     f"{self.characteristics}. The book's title is "
                                     f"{self.title} and is "
                                     f"{self.book_type}. Create fitting and creative titles for each chapter, that build up on each other and list them below in the format \"Chapter n:\" (n is the number of the chapter).",
                                     best_of=5).split("\n")

        chapters = [chapter for chapter in chapters if chapter != "" and chapter != " "]

        return chapters

    def __get_chapter_content(self, chapter_number: int):
        content = self.get_response(f'Imagine a '
                                    f'{self.book_type} '
                                    f'{self.topic} book, called '
                                    f'{self.title}. '
                                    f'{self.characteristics} The book has '
                                    f'{self.chapter_amount} chapters, one of which is '
                                    f'{self.chapter_titles[chapter_number - 1]}. The content structure of this chapter is:'
                                    + "\n".join(self.structure[chapter_number - 1])
                                    + '\nYour task is to write the chapter using the content structure. '
                                    'The chapter should contain every paragraph listed above. '
                                    'The paragraphs should be built on top of each other, totalling to about '
                                    f'{self.chapter_amount} words.', max_tokens=3000)

        return content

    def __get_content(self):
        content = []
        for chapter in range(1, self.chapter_amount + 1):
            content.append(self.__get_chapter_content(chapter))
        return content
