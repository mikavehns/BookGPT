from src.book import Book


def convert_to_markdown(book: Book):
    print('Converting to markdown.')
    markdown = '# ' + book.title + '\n'
    for chapter in range(0, book.chapter_amount):
        markdown += '## ' + book.chapter_titles[chapter] + '\n'
        markdown += book.content[chapter] + '\n'
    return markdown


def draw_data_structure(data, indent=0):
    for key, value in data.items() if isinstance(data, dict) else enumerate(data):
        if isinstance(value, (dict, list)):
            print(' ' * indent + '\n' + str(key))
            draw_data_structure(value, indent + 2)
        else:
            print(' ' * (indent + 2) + str(value))
