Library Assistant
  A small chatbot for browsing a library collection, built with Python and Tkinter. Ask it something like "Who wrote 1984?" or "Is The Hobbit available?" and it answers in a simple chat window.

What it can do :
  It can list all books, available books, or the ones currently issued. You can search by title even if you don't type it exactly, look up books by author or genre, and check details like price, ISBN, publication year, and description. The sidebar has quick buttons for the common requests and shows how many books are in the collection and how many are available. Each book shows up as a card with all its details.

Requirements :
  You need Python 3.8 or newer. There are no extra packages to install, since it only uses the standard library (tkinter, difflib, and re). Tkinter comes with most Python installers. On Linux you may need to install it separately, for example with sudo apt install python3-tk.

Getting started
bash
git clone <your-repo-url>
cd <your-repo-folder>
python assistant.py
Things to try
Show me all books
Show available books
Show programming books
Who wrote 1984?
Is The Hobbit available?
Tell me about Clean Code
What is the price of Atomic Habits?
What is the ISBN of 1984?
When was The Great Gatsby published?
Show me books by Jane Austen

Type help in the app to see everything it understands.

How it works

The whole app is in assistant.py. The sample books are stored in a BOOKS list, where each book has a title, author, genre, year, ISBN, price in ₹, availability, and description.

The LibraryBot class handles the questions. It cleans up the text, then works through a set of rules in order: greetings, help, book lists, genres, authors, and then details about a specific book. For titles, it tries an exact match first, then a partial match, then matching on shared words, and finally a fuzzy match to catch typos. If nothing fits, it says so and suggests some questions to try.

The LibraryChatbotGUI class builds the window, which has a sidebar, a scrolling chat area, an input box, and a Clear button.

Customizing it

To add or change books, edit the BOOKS list. Every book needs all eight fields. If you add a new genre, also add it to the genre_keywords list in respond(), or searches for that genre won't work. The footer text says "10 sample books," so update that too if you change the number of books.

Limitations

The book data is hardcoded, so there's no database and availability can't be changed from the app. The bot matches keywords rather than understanding language, so unusual wording may confuse it. The interface uses the Segoe UI font, which looks best on Windows and falls back to a default font elsewhere.
