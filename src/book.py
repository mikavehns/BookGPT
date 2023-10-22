import openai
from tqdm import tqdm
import prompts
import random
from datetime import datetime, timezone, timedelta

class Book:
    def __str__(self):
        book_structure = "Structure of the book:\n"
        for chapter_index, chapter_info in enumerate(self.chapters, start=1):
            chapter_title = chapter_info['title']
            chapter_paragraphs = chapter_info['paragraphs']
            book_structure += f"Chapter {chapter_index} ({len(chapter_paragraphs)} paragraphs): {chapter_title}\n"
            for paragraph_index, paragraph_info in enumerate(chapter_paragraphs, start=1):
                paragraph_title = paragraph_info['title']
                paragraph_words = paragraph_info['words']
                book_structure += f"\tParagraph {paragraph_index} ({paragraph_words} words): {paragraph_title}\n"

        return book_structure
      
    def __init__(self, **kwargs):
        # Joining the keyword arguments into a single string
        self.arguments = '; '.join([f'{key}: {value}' for key, value in kwargs.items() if key != 'tolerance'])

        # Get 'tolerance' attribute from kwargs
        self.tolerance = kwargs.get('tolerance', 0.9)

        # Assign a status variable
        self.status = 0

        # Setting up the base prompt
        self.base_prompt = [
            self.get_message('system', prompts.INITIAL_INSTRUCTIONS),
            self.get_message('user', self.arguments),
            self.get_message('assistant', 'Ready')
        ]

        # Setting up the title prompt
        self.title_prompt = [
            self.get_message('system', prompts.TITLE_INSTRUCTIONS),
            self.get_message('assistant', 'Ready'),
            self.get_message('user', self.arguments)
        ]

        # Setting up the structure prompt
        self.structure_prompt = [
            self.get_message('system', prompts.STRUCTURE_INSTRUCTIONS),
            self.get_message('assistant', 'Ready'),
        ]

        self.output('Prompts set up. Ready to generate book.')

    def get_title(self):
        self.title = self.get_response(self.title_prompt)
        return self.title

    def get_structure(self):
        if not hasattr(self, 'title'):
            self.output('Title not generated. Please generate title first.')
            return
        else:
            structure_arguments = self.arguments + f'; title: {self.title}'
            self.structure_prompt.append(self.get_message('user', structure_arguments))
            self.structure = self.get_response(self.structure_prompt)
            self.chapters = self.convert_structure(self.structure)

            # Ensure self.chapters contains the actual chapter information before assigning paragraph amounts and words.
        if isinstance(self.chapters, list):
            self.paragraph_amounts = self.get_paragraph_amounts(self.chapters)  # updated line
            self.paragraph_words = self.get_paragraph_words(self.chapters)  # updated line
            return str(self.structure), self.chapters
        else:
            self.output('Error in converting the book structure.')

    def finish_base(self):
        if not hasattr(self, 'title'):
            self.output('Title not generated. Please generate title first.')
            return
        elif not hasattr(self, 'structure'):
            self.output('Structure not generated. Please generate structure first.')
            return
        else:
            self.base_prompt.append(self.get_message('user', '!t'))
            self.base_prompt.append(self.get_message('assistant', self.title))

            self.base_prompt.append(self.get_message('user', '!s'))
            self.base_prompt.append(self.get_message('assistant', self.structure))
            return self.base_prompt

    def calculate_max_status(self):
        if not hasattr(self, 'chapters'):
            self.output('Structure not generated. Please generate structure first.')
            return
        else:
            self.max_status = sum(self.get_paragraph_amounts(self.chapters))
            return self.max_status

    def get_content(self):
        chapters = []
        for i in tqdm(range(len(self.chapters))):
            prompt = self.base_prompt.copy()
            chapter = self.get_chapter(i, prompt.copy())
            chapters.append(chapter)
        self.content = chapters
        return self.content

    def save_book(self):
        # Save the book in md format
        # Corrected saving the book with the specified time
        desired_time = datetime.now(timezone(timedelta(hours=-5)))  # EST timezone
        # Use the desired time as a seed for the random number generator
        random.seed(desired_time)
        # Generate a random 4-digit number
        random_number = random.randint(1000009, 9999999)
        # Ensure it's 4 digits long
        random_number = str(random_number).zfill(random.randint(7, 10))
        with open(f'book{random_number}.md', 'w') as file:
            file.write(f'# {self.title}\n\n')
            for chapter in self.content:
                file.write(f'## {self.chapters[self.content.index(chapter)]["title"]}\n\n')
                for paragraph in chapter:
                    file.write(
                        f'### {self.chapters[self.content.index(chapter)]["paragraphs"][chapter.index(paragraph)]["title"]}\n\n'
                              )
                    file.write(paragraph + '\n\n')

    def get_chapter(self, chapter_index, prompt):
        if len(self.base_prompt) <= 9:
            self.finish_base()

        paragraphs = []
        for i in range(self.paragraph_amounts[chapter_index]):
            paragraph = self.get_paragraph(prompt.copy(), chapter_index, i)
            prompt.append(self.get_message('user', f'!w {chapter_index + 1} {i + 1}'))
            prompt.append(self.get_message('assistant', paragraph))
            self.status += 1
            paragraphs.append(paragraph)
        return paragraphs

    def get_paragraph(self, prompt, chapter_index, paragraph_index):
        prompt.append(self.get_message('user', f'!w {chapter_index + 1} {paragraph_index + 1}'))
        paragraph = self.get_response(prompt)
        prompt.append(self.get_message('assistant', paragraph))

        while len(paragraph.split(' ')) < int(self.paragraph_words[chapter_index][paragraph_index] * self.tolerance):
            prompt.append(self.get_message('system', '!c'))
            response = self.get_response(prompt)
            paragraph += response
            prompt.append(self.get_message('assistant', response))

        return paragraph

    @staticmethod
    def get_message(role, content):
        return {"role": role, "content": content}

    @staticmethod
    def convert_structure(structure):
        chapters = structure.split("Chapter")
        chapters = [x for x in chapters if x != '']
        chapter_information = []

        for chapter in chapters:
            for line in chapter.split("\n"):
                if 'paragraphs' in line.lower():
                    chapter_information.append(
                      {'title': line.split('): ')[1], 'paragraphs': []}
                                              )
                if 'paragraph' in line.lower():
                    chapter_information[-1]['paragraphs'].append(
                    {'title': line.split('): ')[1], 'words': line.split(
                      '(')[1].split(')'
                                                                       )[0].split(
                      ' '
                                                                                 )[0]}
                                                                )
                elif chapter_information == []:
                  ## I can't figure out the code for this
                  chapter_information[0]['paragraphs'].append(
                    {'title': line.split('): ')[1], 'words': line.split(
                      '(')[1].split(')'
                                                                       )[0].split(
                      ' '
                                                                                 )[0]}
                                                                )
                  
        return chapter_information

    @staticmethod
    def get_paragraph_amounts(structure):
        amounts = []
        for chapter in structure:
            amounts.append(len(chapter['paragraphs']))
        return amounts

    @staticmethod
    def get_paragraph_words(structure):
        words = []
        for chapter in structure:
            words.append([int(x['words']) for x in chapter['paragraphs']])
        return words

    @staticmethod
    def get_response(prompt):
        return openai.ChatCompletion.create(
            model="gpt-3.5-turbo-16k-0613",
            messages=prompt
        )["choices"][0]["message"]["content"]

    @staticmethod
    def output(message):
        print(message)
