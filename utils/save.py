from book import Book


class Save:
    def __init__(self, book: Book):
        self.book = book

    def save_txt(self):
        print('Saving as txt.')
        with open('books/' + self.book.title.lower().replace(' ', '_') + '.txt', 'w') as f:
            f.write(str(self.book))
