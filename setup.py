from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.6.2.1'
DESCRIPTION = 'Generating books using OpenAI\'s GPT-3 API.'
# Set README as long description
with codecs.open('README.md', 'r', 'utf-8') as f:
    LONG_DESCRIPTION = f.read()

# Setting up
setup(
    name="src",
    version=VERSION,
    author="Mika Vehns",
    author_email="<mika.vehns@outlook.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['openai', 'markdown', 'retrying'],
    keywords=['python', 'gpt-3', 'openai', 'book', 'generator', "writer"],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent"
    ]
)
