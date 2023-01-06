import openai


class Science:
    """
    This class is used to generate a self-help book.
    """

    def __init__(self, chapter_amount: int, words_per_chapter: int, topic: str):
        """
        Initialize the class.
        :param chapter_amount: The amount of chapters in the book.
        :param words_per_chapter: The amount of words per chapter.
        :param topic: The topic of the book.
        """

        self.chapter_amount = chapter_amount
        self.words_per_chapter = words_per_chapter
        self.topic = topic

    @staticmethod
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

        return self.get_response(f"Generate a title for a science book on {self.topic}. "
                                 f"The title should be engaging and memorable, and should "
                                 f"accurately reflect the content and purpose of the book. "
                                 f"The book will contain scientific information, experiments, "
                                 f"and research to help readers understand and learn about the topic. "
                                 f"The title should be informative and educational, and should inspire "
                                 f"readers to further explore the subject.")

    def get_chapters(self, title: str):
        """
        Gets the chapters of the book.
        :param title: The title of the book.
        :return: The chapters of the book.
        """

        return self.get_response(
            f"Generate a list of the size {self.chapter_amount} of chapter titles for a science book on the topic {self.topic}, called {title}. "
            f"Each chapter should cover a specific aspect of the topic and should be structured as a "
            f"series of lessons or explanations that the reader can follow to gain a deeper understanding of the subject. "
            f"The chapter titles should be descriptive and should clearly convey the main focus of each chapter. "
            f"The chapters should be informative and educational, and should encourage the reader to think critically about the topic.")

    def get_structure(self, title: str, chapters: list[str]):
        """
        Gets the structure of the book.
        :param title: The title of the book.
        :param chapters: The chapters of the book.
        :return: The structure of the book.
        """

        return self.get_response(f"Generate a structure plan for a science book called {title}. "
                                 f"The book should contain {self.chapter_amount} chapters, with the following titles: "
                                 f"{','.join(chapters)}. Each chapter should cover a specific topic in science and "
                                 f"be structured as a series of lessons or sections that explain the key concepts and ideas. "
                                 f"The chapters should include examples, illustrations, and case studies to help the reader "
                                 f"understand and apply the concepts. The book should be informative and accurate, "
                                 f"and should encourage the reader to think critically about the topic."
                                 f"\n\nFor each chapter, create a list of paragraph titles and corresponding recommended"
                                 f" word counts in the following format: 'paragraph_title---word_amount.' "
                                 f"The section titles should not include the word 'paragraph' or a number. "
                                 f"The total recommended word count for all sections in each chapter should add up to {self.words_per_chapter} words. "
                                 f"In order to prevent any individual section from being too long, try to divide the "
                                 f"content into multiple sections, each with a recommended word count.")

    def get_paragraph(self, title: str, chapters: list[str], paragraphs: list[list[dict[str, str]]],
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
            f"Write the content for Chapter {chapter_index + 1} of a science book called {title}. The chapter is called {chapters[chapter_index]}, "
            f"and should focus on discussing scientific theories, principles, and research findings related to the topic. "
            f"The chapter should include a clear explanation of the key concepts, as well as supporting evidence and examples to illustrate their importance. "
            f"The chapter should also provide practical applications of the concepts, and may include hands-on activities or exercises for readers to try. "
            f"The chapter should be written in a clear and concise style, and should be well-organized and easy to follow. "
            f"\n\nThe chapter contains the following paragraphs:\n{titles}\nWrite the content for paragraph {paragraph_index + 1}, "
            f"with the title '{paragraph['title']}.' The paragraph should have the recommended word count of {paragraph['word_count']} words. "
            f"In order to effectively convey the main ideas and concepts of the paragraph, be sure to include relevant data, "
            f"experiments, and other scientific evidence. Use a logical and scientific writing style that will keep the reader engaged and informed. "
            f"The paragraph should be well-structured and coherent, with a clear introduction, body, and conclusion. Do not write a title.")
