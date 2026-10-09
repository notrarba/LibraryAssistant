import tkinter as tk
from tkinter import ttk
import difflib
import re
BOOKS = [
    {
        "title": "The Alchemist",
        "author": "Paulo Coelho",
        "genre": ["Fiction", "Adventure"],
        "year": 1988,
        "isbn": "9780061122415",
        "price": 399,
        "available": True,
        "description": (
            "A young shepherd named Santiago travels in search of "
            "a treasure and discovers the importance of following "
            "his dreams."
        )
    },

    {
        "title": "1984",
        "author": "George Orwell",
        "genre": ["Dystopian", "Political Fiction"],
        "year": 1949,
        "isbn": "9780451524935",
        "price": 299,
        "available": True,
        "description": (
            "A dystopian novel about a society controlled by an "
            "authoritarian government and constant surveillance."
        )
    },

    {
        "title": "The Hobbit",
        "author": "J.R.R. Tolkien",
        "genre": ["Fantasy", "Adventure"],
        "year": 1937,
        "isbn": "9780547928227",
        "price": 499,
        "available": False,
        "description": (
            "Bilbo Baggins joins a group of dwarves on an adventure "
            "to reclaim their homeland and treasure."
        )
    },

    {
        "title": "Harry Potter and the Philosopher's Stone",
        "author": "J.K. Rowling",
        "genre": ["Fantasy", "Fiction"],
        "year": 1997,
        "isbn": "9780747532743",
        "price": 599,
        "available": True,
        "description": (
            "Harry Potter discovers that he is a wizard and begins "
            "his magical education at Hogwarts."
        )
    },

    {
        "title": "To Kill a Mockingbird",
        "author": "Harper Lee",
        "genre": ["Fiction", "Historical"],
        "year": 1960,
        "isbn": "9780061120084",
        "price": 349,
        "available": True,
        "description": (
            "A story about justice, racism and childhood in "
            "the American South."
        )
    },

    {
        "title": "Clean Code",
        "author": "Robert C. Martin",
        "genre": ["Programming", "Software Engineering"],
        "year": 2008,
        "isbn": "9780132350884",
        "price": 899,
        "available": True,
        "description": (
            "A practical guide to writing clean, readable and "
            "maintainable software."
        )
    },

    {
        "title": "Introduction to Algorithms",
        "author": "Thomas H. Cormen",
        "genre": ["Computer Science", "Algorithms"],
        "year": 2009,
        "isbn": "9780262033848",
        "price": 1299,
        "available": False,
        "description": (
            "A comprehensive textbook covering algorithms, "
            "data structures and algorithm analysis."
        )
    },

    {
        "title": "The Great Gatsby",
        "author": "F. Scott Fitzgerald",
        "genre": ["Fiction", "Classic"],
        "year": 1925,
        "isbn": "9780743273565",
        "price": 299,
        "available": True,
        "description": (
            "A classic novel exploring wealth, love and "
            "the American Dream."
        )
    },

    {
        "title": "Atomic Habits",
        "author": "James Clear",
        "genre": ["Self-help", "Psychology"],
        "year": 2018,
        "isbn": "9780735211292",
        "price": 499,
        "available": True,
        "description": (
            "A guide to building good habits and breaking bad "
            "ones through small, consistent improvements."
        )
    },

    {
        "title": "Pride and Prejudice",
        "author": "Jane Austen",
        "genre": ["Romance", "Classic"],
        "year": 1813,
        "isbn": "9780141439518",
        "price": 249,
        "available": True,
        "description": (
            "A classic novel about relationships, social class, "
            "marriage and misunderstandings."
        )
    }
]

class LibraryBot:

    def __init__(self, books):
        self.books = books
    def normalize(self, text):
        text = text.lower()
        text = text.replace("’", "'")
        text = re.sub(r"[^\w\s']", " ", text)
        text = re.sub(r"\s+", " ", text)
        return text.strip()
    def find_book(self, query):

        query_normalized = self.normalize(query)

        for book in self.books:
            title = self.normalize(book["title"])

            if title == query_normalized:
                return book

        for book in self.books:
            title = self.normalize(book["title"])

            if title in query_normalized:
                return book

        best_book = None
        best_score = 0

        query_words = set(query_normalized.split())

        for book in self.books:

            title_words = set(
                self.normalize(book["title"]).split()
            )

            title_words -= {
                "the",
                "a",
                "an",
                "and",
                "of",
                "to",
                "in"
            }

            matched = len(query_words & title_words)

            if matched > best_score:
                best_score = matched
                best_book = book

        if best_score >= 1:
            return best_book

        # 4. Fuzzy title matching
        titles = [
            self.normalize(book["title"])
            for book in self.books
        ]

        match = difflib.get_close_matches(
            query_normalized,
            titles,
            n=1,
            cutoff=0.45
        )

        if match:
            for book in self.books:
                if self.normalize(book["title"]) == match[0]:
                    return book

        return None
    def books_by_author(self, query):

        query = self.normalize(query)

        results = []

        for book in self.books:

            author = self.normalize(book["author"])

            if author in query or query in author:
                results.append(book)

            else:
                author_words = author.split()

                if any(
                    word in query
                    for word in author_words
                    if len(word) > 3
                ):
                    results.append(book)

        return results
    def books_by_genre(self, query):

        query = self.normalize(query)

        results = []

        for book in self.books:

            for genre in book["genre"]:

                if self.normalize(genre) in query:
                    results.append(book)
                    break

        return results
    def all_books(self):
        return self.books

    def available_books(self):
        return [
            book for book in self.books
            if book["available"]
        ]
    def issued_books(self):
        return [
            book for book in self.books
            if not book["available"]
        ]

    def respond(self, user_message):

        original = user_message.strip()
        text = self.normalize(original)

        if not text:
            return {
                "type": "text",
                "message": "Please type a question."
            }


        greetings = [
            "hi",
            "hello",
            "hey",
            "good morning",
            "good afternoon",
            "good evening"
        ]

        if text in greetings:

            return {
                "type": "text",
                "message": (
                    "Hello! 👋\n\n"
                    "I'm your Library Assistant. I can help you "
                    "find information about our books.\n\n"
                    "Try asking:\n"
                    "• Who wrote 1984?\n"
                    "• Is The Hobbit available?\n"
                    "• Tell me about Clean Code\n"
                    "• Show me programming books\n"
                    "• What is the price of Atomic Habits?"
                )
            }



        if text in ["help", "what can you do", "commands"]:

            return {
                "type": "text",
                "message": (
                    "Here's what I can do:\n\n"
                    "📚 Show all books\n"
                    "✍️ Find books by author\n"
                    "🏷️ Find books by genre\n"
                    "✅ Check availability\n"
                    "💰 Check price\n"
                    "🔢 Find ISBN\n"
                    "📅 Find publication year\n"
                    "📖 Give book descriptions"
                )
            }



        if (
            text == "book"
            or text == "books"
            or "show all books" in text
            or "list all books" in text
            or "list books" in text
            or "show books" in text
            or "library books" in text
        ):

            return {
                "type": "book_list",
                "books": self.all_books()
            }



        if (
            "available books" in text
            or "books available" in text
            or "which books are available" in text
            or "what books are available" in text
            or "available book" in text
        ):

            return {
                "type": "book_list",
                "books": self.available_books(),
                "title": "Available Books"
            }



        if (
            "issued books" in text
            or "unavailable books" in text
            or "borrowed books" in text
        ):

            return {
                "type": "book_list",
                "books": self.issued_books(),
                "title": "Currently Issued Books"
            }



        genre_keywords = [
            "programming",
            "software engineering",
            "computer science",
            "algorithms",
            "fantasy",
            "fiction",
            "adventure",
            "classic",
            "romance",
            "psychology",
            "self help",
            "self-help",
            "dystopian",
            "historical"
        ]

        for genre in genre_keywords:

            if genre in text:

                results = self.books_by_genre(text)

                if results:

                    return {
                        "type": "book_list",
                        "books": results,
                        "title": f"Books in {genre.title()}"
                    }



        author_results = self.books_by_author(text)

        # Only trigger if query contains author-related wording
        author_words = [
            "author",
            "writer",
            "written",
            "books by",
            "novels by"
        ]

        if author_results and any(
            word in text for word in author_words
        ):

            return {
                "type": "book_list",
                "books": author_results,
                "title": "Books by Author"
            }


        book = self.find_book(text)

        if book:



            if (
                "available" in text
                or "availability" in text
                or "borrow" in text
                or "issued" in text
            ):

                if book["available"]:

                    return {
                        "type": "text",
                        "message": (
                            f"✅ Yes! \"{book['title']}\" "
                            f"is currently available."
                        )
                    }

                else:

                    return {
                        "type": "text",
                        "message": (
                            f"❌ \"{book['title']}\" is "
                            f"currently issued."
                        )
                    }

            # -----------------------------------------------
            # Author
            # -----------------------------------------------

            if (
                "author" in text
                or "who wrote" in text
                or "written by" in text
                or "writer" in text
            ):

                return {
                    "type": "text",
                    "message": (
                        f"✍️ \"{book['title']}\" was written by "
                        f"{book['author']}."
                    )
                }

            # -----------------------------------------------
            # Price
            # -----------------------------------------------

            if (
                "price" in text
                or "cost" in text
                or "how much" in text
            ):

                return {
                    "type": "text",
                    "message": (
                        f"💰 The price of \"{book['title']}\" "
                        f"is ₹{book['price']}."
                    )
                }

            # -----------------------------------------------
            # ISBN
            # -----------------------------------------------

            if "isbn" in text:

                return {
                    "type": "text",
                    "message": (
                        f"🔢 ISBN of \"{book['title']}\": "
                        f"{book['isbn']}"
                    )
                }

            # -----------------------------------------------
            # Publication year
            # -----------------------------------------------

            if (
                "year" in text
                or "published" in text
                or "publication" in text
            ):

                return {
                    "type": "text",
                    "message": (
                        f"📅 \"{book['title']}\" was published "
                        f"in {book['year']}."
                    )
                }

            # -----------------------------------------------
            # Genre
            # -----------------------------------------------

            if (
                "genre" in text
                or "category" in text
                or "type of book" in text
            ):

                return {
                    "type": "text",
                    "message": (
                        f"🏷️ \"{book['title']}\" belongs to: "
                        f"{', '.join(book['genre'])}."
                    )
                }

            # -----------------------------------------------
            # Description
            # -----------------------------------------------

            if (
                "about" in text
                or "summary" in text
                or "description" in text
                or "story" in text
                or "what is" in text
                or "tell me" in text
            ):

                return {
                    "type": "text",
                    "message": (
                        f"📖 {book['description']}\n\n"
                        f"Author: {book['author']}\n"
                        f"Genre: {', '.join(book['genre'])}\n"
                        f"Published: {book['year']}"
                    )
                }

            # -----------------------------------------------
            # Book name only
            # -----------------------------------------------

            return {
                "type": "book_detail",
                "book": book
            }

        # ----------------------------------------------------
        # AUTHOR WITHOUT "AUTHOR"
        # ----------------------------------------------------

        known_authors = [
            book["author"].lower()
            for book in self.books
        ]

        for author in known_authors:

            if author in text:

                results = [
                    book
                    for book in self.books
                    if book["author"].lower() == author
                ]

                return {
                    "type": "book_list",
                    "books": results,
                    "title": "Books by Author"
                }

        # ----------------------------------------------------
        # UNKNOWN
        # ----------------------------------------------------

        return {
            "type": "text",
            "message": (
                "🤔 I couldn't find an answer for that.\n\n"
                "Try asking something like:\n"
                "• Show me all books\n"
                "• Who wrote 1984?\n"
                "• Tell me about The Hobbit\n"
                "• Is Clean Code available?\n"
                "• Show me programming books\n"
                "• What is the ISBN of 1984?"
            )
        }


# ============================================================
#                       GUI APPLICATION
# ============================================================

class LibraryChatbotGUI:

    def __init__(self, root):

        self.root = root

        self.root.title("Library Assistant")
        self.root.geometry("1100x700")
        self.root.minsize(900, 600)

        self.root.configure(bg="#f5f7fb")

        self.bot = LibraryBot(BOOKS)

        self.setup_styles()
        self.create_layout()

        # Initial message
        self.add_bot_message(
            "Hello! 👋 I'm your Library Assistant.\n\n"
            "I can help you find books, authors, genres, "
            "availability, prices, ISBNs and more.\n\n"
            "Try asking: \"Show me all books\""
        )

    # ========================================================
    #                       STYLES
    # ========================================================

    def setup_styles(self):

        self.colors = {
            "background": "#f5f7fb",
            "sidebar": "#172033",
            "sidebar_text": "#ffffff",
            "primary": "#4f46e5",
            "primary_dark": "#4338ca",
            "bot": "#ffffff",
            "user": "#4f46e5",
            "text": "#1f2937",
            "muted": "#6b7280",
            "border": "#e5e7eb",
            "available": "#16a34a",
            "unavailable": "#dc2626"
        }

        style = ttk.Style()

        try:
            style.theme_use("clam")
        except tk.TclError:
            pass

        style.configure(
            "Search.TEntry",
            padding=10,
            font=("Segoe UI", 11)
        )

    # ========================================================
    #                       MAIN LAYOUT
    # ========================================================

    def create_layout(self):

        # ----------------------------------------------------
        # Sidebar
        # ----------------------------------------------------

        self.sidebar = tk.Frame(
            self.root,
            bg=self.colors["sidebar"],
            width=260
        )

        self.sidebar.pack(
            side="left",
            fill="y"
        )

        self.sidebar.pack_propagate(False)

        # Logo
        logo_frame = tk.Frame(
            self.sidebar,
            bg=self.colors["sidebar"]
        )

        logo_frame.pack(
            fill="x",
            padx=20,
            pady=(25, 10)
        )

        tk.Label(
            logo_frame,
            text="📚",
            font=("Segoe UI Emoji", 30),
            bg=self.colors["sidebar"],
            fg="white"
        ).pack(anchor="w")

        tk.Label(
            logo_frame,
            text="Library",
            font=("Segoe UI", 22, "bold"),
            bg=self.colors["sidebar"],
            fg="white"
        ).pack(anchor="w")

        tk.Label(
            logo_frame,
            text="ASSISTANT",
            font=("Segoe UI", 9, "bold"),
            bg=self.colors["sidebar"],
            fg="#a5b4fc"
        ).pack(anchor="w")

        # Divider
        tk.Frame(
            self.sidebar,
            height=1,
            bg="#303b52"
        ).pack(
            fill="x",
            padx=20,
            pady=20
        )

        # Quick actions
        tk.Label(
            self.sidebar,
            text="QUICK ACTIONS",
            font=("Segoe UI", 9, "bold"),
            bg=self.colors["sidebar"],
            fg="#94a3b8"
        ).pack(
            anchor="w",
            padx=20,
            pady=(0, 10)
        )

        self.sidebar_button(
            "📚  All Books",
            lambda: self.quick_message("books")
        )

        self.sidebar_button(
            "✅  Available Books",
            lambda: self.quick_message(
                "show available books"
            )
        )

        self.sidebar_button(
            "📕  Issued Books",
            lambda: self.quick_message(
                "show issued books"
            )
        )

        self.sidebar_button(
            "💻  Programming",
            lambda: self.quick_message(
                "show programming books"
            )
        )

        self.sidebar_button(
            "❓  Help",
            lambda: self.quick_message("help")
        )

        # Library stats
        stats = tk.Frame(
            self.sidebar,
            bg="#202b42"
        )

        stats.pack(
            side="bottom",
            fill="x",
            padx=15,
            pady=15
        )

        tk.Label(
            stats,
            text="LIBRARY STATUS",
            font=("Segoe UI", 9, "bold"),
            bg="#202b42",
            fg="#94a3b8"
        ).pack(
            anchor="w",
            padx=15,
            pady=(15, 5)
        )

        available_count = len(
            self.bot.available_books()
        )

        tk.Label(
            stats,
            text=f"📚  {len(BOOKS)} total books",
            font=("Segoe UI", 10),
            bg="#202b42",
            fg="white"
        ).pack(
            anchor="w",
            padx=15,
            pady=3
        )

        tk.Label(
            stats,
            text=f"✅  {available_count} available",
            font=("Segoe UI", 10),
            bg="#202b42",
            fg="#86efac"
        ).pack(
            anchor="w",
            padx=15,
            pady=(3, 15)
        )

        # ----------------------------------------------------
        # Main area
        # ----------------------------------------------------

        self.main = tk.Frame(
            self.root,
            bg=self.colors["background"]
        )

        self.main.pack(
            side="right",
            fill="both",
            expand=True
        )

        self.create_header()
        self.create_chat_area()
        self.create_input_area()

    # ========================================================
    #                    SIDEBAR BUTTON
    # ========================================================

    def sidebar_button(self, text, command):

        button = tk.Button(
            self.sidebar,
            text=text,
            command=command,
            anchor="w",
            font=("Segoe UI", 10),
            bg=self.colors["sidebar"],
            fg="#dbeafe",
            activebackground="#293650",
            activeforeground="white",
            relief="flat",
            bd=0,
            cursor="hand2",
            padx=20,
            pady=12
        )

        button.pack(
            fill="x",
            padx=10,
            pady=2
        )

    # ========================================================
    #                       HEADER
    # ========================================================

    def create_header(self):

        header = tk.Frame(
            self.main,
            bg="white",
            height=75
        )

        header.pack(
            fill="x"
        )

        header.pack_propagate(False)

        left = tk.Frame(
            header,
            bg="white"
        )

        left.pack(
            side="left",
            padx=25
        )

        tk.Label(
            left,
            text="Library Assistant",
            font=("Segoe UI", 18, "bold"),
            bg="white",
            fg=self.colors["text"]
        ).pack(anchor="w")

        tk.Label(
            left,
            text="Ask me anything about the library collection",
            font=("Segoe UI", 9),
            bg="white",
            fg=self.colors["muted"]
        ).pack(anchor="w")

        # Online status
        status = tk.Frame(
            header,
            bg="white"
        )

        status.pack(
            side="right",
            padx=25
        )

        tk.Label(
            status,
            text="●",
            font=("Segoe UI", 12),
            bg="white",
            fg="#22c55e"
        ).pack(
            side="left",
            padx=(0, 5)
        )

        tk.Label(
            status,
            text="Online",
            font=("Segoe UI", 10),
            bg="white",
            fg=self.colors["muted"]
        ).pack(side="left")

    # ========================================================
    #                    CHAT AREA
    # ========================================================

    def create_chat_area(self):

        container = tk.Frame(
            self.main,
            bg=self.colors["background"]
        )

        container.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=(15, 10)
        )

        self.canvas = tk.Canvas(
            container,
            bg=self.colors["background"],
            highlightthickness=0
        )

        scrollbar = ttk.Scrollbar(
            container,
            orient="vertical",
            command=self.canvas.yview
        )

        self.chat_frame = tk.Frame(
            self.canvas,
            bg=self.colors["background"]
        )

        self.chat_window = self.canvas.create_window(
            (0, 0),
            window=self.chat_frame,
            anchor="nw"
        )

        self.canvas.configure(
            yscrollcommand=scrollbar.set
        )

        self.canvas.pack(
            side="left",
            fill="both",
            expand=True
        )

        scrollbar.pack(
            side="right",
            fill="y"
        )

        self.chat_frame.bind(
            "<Configure>",
            self.update_scroll_region
        )

        self.canvas.bind(
            "<Configure>",
            self.resize_chat_frame
        )

    def update_scroll_region(self, event=None):

        self.canvas.configure(
            scrollregion=self.canvas.bbox("all")
        )

        self.canvas.after(
            50,
            self.scroll_to_bottom
        )

    def resize_chat_frame(self, event):

        self.canvas.itemconfig(
            self.chat_window,
            width=event.width
        )

    def scroll_to_bottom(self):

        self.canvas.yview_moveto(1.0)

    # ========================================================
    #                     INPUT AREA
    # ========================================================

    def create_input_area(self):

        outer = tk.Frame(
            self.main,
            bg="white"
        )

        outer.pack(
            fill="x"
        )

        input_container = tk.Frame(
            outer,
            bg="white"
        )

        input_container.pack(
            fill="x",
            padx=20,
            pady=15
        )

        self.input_box = tk.Entry(
            input_container,
            font=("Segoe UI", 11),
            bg="#f8fafc",
            fg=self.colors["text"],
            relief="flat",
            bd=0,
            insertbackground=self.colors["primary"]
        )

        self.input_box.pack(
            side="left",
            fill="x",
            expand=True,
            ipady=12,
            padx=(10, 10)
        )

        self.input_box.insert(
            0,
            "Ask about a book..."
        )

        self.input_box.config(
            fg="#9ca3af"
        )

        self.input_box.bind(
            "<FocusIn>",
            self.clear_placeholder
        )

        self.input_box.bind(
            "<Return>",
            self.send_message
        )

        self.send_button = tk.Button(
            input_container,
            text="Send  ➤",
            command=self.send_message,
            font=("Segoe UI", 10, "bold"),
            bg=self.colors["primary"],
            fg="white",
            activebackground=self.colors["primary_dark"],
            activeforeground="white",
            relief="flat",
            bd=0,
            cursor="hand2",
            padx=20,
            pady=10
        )

        self.send_button.pack(
            side="right"
        )

        # Clear button
        clear_button = tk.Button(
            input_container,
            text="Clear",
            command=self.clear_chat,
            font=("Segoe UI", 9),
            bg="white",
            fg=self.colors["muted"],
            activebackground="white",
            relief="flat",
            bd=0,
            cursor="hand2"
        )

        clear_button.pack(
            side="right",
            padx=10
        )

        tk.Label(
            outer,
            text="Library Assistant • Ask questions about the 10 sample books",
            font=("Segoe UI", 8),
            bg="white",
            fg="#9ca3af"
        ).pack(
            pady=(0, 10)
        )

    # ========================================================
    #                  PLACEHOLDER
    # ========================================================

    def clear_placeholder(self, event=None):

        if self.input_box.get() == "Ask about a book...":

            self.input_box.delete(
                0,
                tk.END
            )

            self.input_box.config(
                fg=self.colors["text"]
            )

    # ========================================================
    #                     SEND MESSAGE
    # ========================================================

    def send_message(self, event=None):

        message = self.input_box.get().strip()

        if not message or message == "Ask about a book...":
            return

        self.input_box.delete(
            0,
            tk.END
        )

        self.input_box.config(
            fg=self.colors["text"]
        )

        self.add_user_message(message)

        # Small delay gives the UI a natural feel
        self.root.after(
            250,
            lambda: self.process_bot_response(message)
        )

    def quick_message(self, message):

        self.input_box.delete(
            0,
            tk.END
        )

        self.input_box.insert(
            0,
            message
        )

        self.send_message()

    # ========================================================
    #                 PROCESS BOT RESPONSE
    # ========================================================

    def process_bot_response(self, message):

        response = self.bot.respond(message)

        response_type = response["type"]

        if response_type == "text":

            self.add_bot_message(
                response["message"]
            )

        elif response_type == "book_detail":

            self.add_book_card(
                response["book"]
            )

        elif response_type == "book_list":

            title = response.get(
                "title",
                "Library Books"
            )

            self.add_book_list(
                response["books"],
                title
            )

    # ========================================================
    #                  USER MESSAGE
    # ========================================================

    def add_user_message(self, message):

        row = tk.Frame(
            self.chat_frame,
            bg=self.colors["background"]
        )

        row.pack(
            fill="x",
            pady=7,
            padx=10
        )

        bubble = tk.Label(
            row,
            text=message,
            font=("Segoe UI", 10),
            bg=self.colors["user"],
            fg="white",
            padx=15,
            pady=10,
            wraplength=550,
            justify="left"
        )

        bubble.pack(
            side="right",
            anchor="e"
        )

        self.scroll_to_bottom()

    # ========================================================
    #                   BOT MESSAGE
    # ========================================================

    def add_bot_message(self, message):

        row = tk.Frame(
            self.chat_frame,
            bg=self.colors["background"]
        )

        row.pack(
            fill="x",
            pady=7,
            padx=10
        )

        avatar = tk.Label(
            row,
            text="🤖",
            font=("Segoe UI Emoji", 17),
            bg=self.colors["background"]
        )

        avatar.pack(
            side="left",
            anchor="n",
            padx=(0, 8)
        )

        bubble = tk.Label(
            row,
            text=message,
            font=("Segoe UI", 10),
            bg=self.colors["bot"],
            fg=self.colors["text"],
            padx=15,
            pady=12,
            wraplength=650,
            justify="left",
            anchor="w"
        )

        bubble.pack(
            side="left",
            anchor="w"
        )

        self.scroll_to_bottom()

    # ========================================================
    #                    BOOK CARD
    # ========================================================

    def add_book_card(self, book):

        row = tk.Frame(
            self.chat_frame,
            bg=self.colors["background"]
        )

        row.pack(
            fill="x",
            pady=8,
            padx=10
        )

        avatar = tk.Label(
            row,
            text="🤖",
            font=("Segoe UI Emoji", 17),
            bg=self.colors["background"]
        )

        avatar.pack(
            side="left",
            anchor="n",
            padx=(0, 8)
        )

        card = tk.Frame(
            row,
            bg="white",
            bd=0,
            highlightthickness=1,
            highlightbackground=self.colors["border"]
        )

        card.pack(
            side="left",
            anchor="w",
            fill="x",
            expand=True,
            padx=(0, 40)
        )

        # Title
        tk.Label(
            card,
            text=book["title"],
            font=("Segoe UI", 15, "bold"),
            bg="white",
            fg=self.colors["text"]
        ).pack(
            anchor="w",
            padx=18,
            pady=(15, 2)
        )

        tk.Label(
            card,
            text=f"by {book['author']}",
            font=("Segoe UI", 10, "italic"),
            bg="white",
            fg=self.colors["muted"]
        ).pack(
            anchor="w",
            padx=18
        )

        # Divider
        tk.Frame(
            card,
            height=1,
            bg=self.colors["border"]
        ).pack(
            fill="x",
            padx=18,
            pady=12
        )

        # Information
        info = tk.Frame(
            card,
            bg="white"
        )

        info.pack(
            fill="x",
            padx=18
        )

        self.book_info(
            info,
            "Genre",
            ", ".join(book["genre"])
        )

        self.book_info(
            info,
            "Published",
            str(book["year"])
        )

        self.book_info(
            info,
            "ISBN",
            book["isbn"]
        )

        self.book_info(
            info,
            "Price",
            f"₹{book['price']}"
        )

        status_text = (
            "Available"
            if book["available"]
            else "Currently Issued"
        )

        status_color = (
            self.colors["available"]
            if book["available"]
            else self.colors["unavailable"]
        )

        status = tk.Label(
            card,
            text=f"●  {status_text}",
            font=("Segoe UI", 9, "bold"),
            bg="white",
            fg=status_color
        )

        status.pack(
            anchor="w",
            padx=18,
            pady=(10, 5)
        )

        # Description
        tk.Label(
            card,
            text=book["description"],
            font=("Segoe UI", 9),
            bg="white",
            fg=self.colors["muted"],
            wraplength=650,
            justify="left"
        ).pack(
            anchor="w",
            padx=18,
            pady=(0, 18)
        )

        self.scroll_to_bottom()

    # ========================================================
    #                 BOOK INFO ROW
    # ========================================================

    def book_info(self, parent, label, value):

        row = tk.Frame(
            parent,
            bg="white"
        )

        row.pack(
            fill="x",
            pady=3
        )

        tk.Label(
            row,
            text=f"{label}:",
            font=("Segoe UI", 9, "bold"),
            bg="white",
            fg=self.colors["text"],
            width=12,
            anchor="w"
        ).pack(
            side="left"
        )

        tk.Label(
            row,
            text=value,
            font=("Segoe UI", 9),
            bg="white",
            fg=self.colors["muted"],
            anchor="w"
        ).pack(
            side="left"
        )

    # ========================================================
    #                   BOOK LIST
    # ========================================================

    def add_book_list(self, books, title):

        self.add_bot_message(
            f"📚 {title}\n"
            f"I found {len(books)} book(s):"
        )

        for book in books:

            self.add_small_book_card(
                book
            )

    # ========================================================
    #              SMALL BOOK CARD
    # ========================================================

    def add_small_book_card(self, book):

        row = tk.Frame(
            self.chat_frame,
            bg=self.colors["background"]
        )

        row.pack(
            fill="x",
            pady=4,
            padx=50
        )

        card = tk.Frame(
            row,
            bg="white",
            highlightthickness=1,
            highlightbackground=self.colors["border"]
        )

        card.pack(
            fill="x",
            expand=True
        )

        title = tk.Label(
            card,
            text=f"📖  {book['title']}",
            font=("Segoe UI", 11, "bold"),
            bg="white",
            fg=self.colors["text"]
        )

        title.pack(
            anchor="w",
            padx=15,
            pady=(10, 2)
        )

        tk.Label(
            card,
            text=f"by {book['author']}  •  "
                 f"{', '.join(book['genre'])}",
            font=("Segoe UI", 9),
            bg="white",
            fg=self.colors["muted"]
        ).pack(
            anchor="w",
            padx=15,
            pady=(0, 5)
        )

        status = (
            "● Available"
            if book["available"]
            else "● Issued"
        )

        status_color = (
            self.colors["available"]
            if book["available"]
            else self.colors["unavailable"]
        )

        tk.Label(
            card,
            text=status,
            font=("Segoe UI", 8, "bold"),
            bg="white",
            fg=status_color
        ).pack(
            anchor="w",
            padx=15,
            pady=(0, 10)
        )

        self.scroll_to_bottom()

    # ========================================================
    #                    CLEAR CHAT
    # ========================================================

    def clear_chat(self):

        for widget in self.chat_frame.winfo_children():
            widget.destroy()

        self.add_bot_message(
            "Chat cleared. 👋\n\n"
            "What would you like to know about the library?"
        )


# ============================================================
#                         RUN APP
# ============================================================

def main():

    root = tk.Tk()

    app = LibraryChatbotGUI(root)

    root.mainloop()


if __name__ == "__main__":
    main()