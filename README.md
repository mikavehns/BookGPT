<h1 align="center">BookGPT (Beta)</h1>
<p align="center">This program uses the ChatGPT API to generate books based on your specified parameters.
<br><br>
</p>


## Installation
To install this program, simply follow these steps:
1. Clone this repository to your local machine by running the following command in your terminal:
```bash
git clone https://github.com/mikavehns/BookGPT.git
```
2. Navigate to the root directory of the repository using `cd BookGPT`
3. Install the required dependencies by running the following command:
```bash
pip install -r requirements.txt
```


## Prerequisites
In order to use this program, you must have a [ChatGPT API key](https://beta.openai.com/account/api-keys). The API Key must then be inserted into the `src/config.json` file.


## Usage
To use this program, simply run the following command in your terminal:
```bash
python src/run.py
```
You will then be prompted to enter the following information:
- Chapter Amount: The amount of chapters you want the book to have.
- Chapter Length: The amount of words you want each chapter to have.
- Topic: The topic you want the book to be about.
- Category: The type of book you want to generate. (Science, Biography, etc.)

The program will then generate a Title and Chapter Titles + Content. You will get a detailed structure of the book.
The generated books will then be saved as `book.md` in `BookGPT/src`.


## Examples
Here are some examples:
- Generate book with 5 chapters and 300 words per chapter, with quotes as chapter title, with the topic "success":

https://user-images.githubusercontent.com/66560242/210459589-751c82d7-e874-4119-a09a-cc36ea2be73c.mp4

- You can see all examples in the `examples/` directory.


## Notes
- The run.py file is just one example on how to use the book generator. You can also implement it into a website, discord bot, desktop app, etc.
- The program may take some time to run, depending on the specified parameters and the performance of the ChatGPT API. Please be patient while the book is being generated.
- The program may not always generate the wished amount of words for each chapter. This can happen, if there is not enough data available for the specified topic.
- Currently, it is only possible to generate Non-Fiction books.
- Since this is a really early version (v0.8.0), there are many missing features, that will be added by time


## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.


## Contributing
- If you are interested in contributing to BookGPT, I welcome any suggestions or pull requests. Please feel free to open an issue or submit a pull request on the [GitHub repository](https://github.com/mikavehns/BookGPT).
- You can also submit your books, which I will then add to the `examples` folder. Just open a pull request with the book in the `examples` folder.
