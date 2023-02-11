import os
import markdown
from gtts import gTTS


def draw_data_structure(data, indent=0):
    for key, value in data.items() if isinstance(data, dict) else enumerate(data):
        if isinstance(value, (dict, list)):
            print(' ' * indent + '\n' + str(key))
            draw_data_structure(value, indent + 2)
        else:
            print(' ' * (indent + 2) + str(value))


def get_html(markdown_file):
    return markdown.markdown(markdown_file)


def get_mp3(markdown_file, language):
    return gTTS(markdown_file, lang=language)


def get_python_files(path):
    return [file[:-3] for file in os.listdir(path) if not file.startswith('__') and file.endswith('.py')]


def get_categories():
    # Get all the files in the directory 'categories'
    categories = get_python_files('categories')

    # Check if the category is in the directory
    special_names = {'selfimprovement': 'SelfImprovement'}

    # Return all categories with the first letter capitalized, except for the special names, which are returned, how they are defined in special_names
    return [category.capitalize() if category not in special_names else special_names[category] for category in
            categories]
