"""
Project: Library Management System
Course: CS 3330 - Database Systems
Team: 16

Description:
    This program is a Library Management System developed for CS 3330 - Database Systems course.
    It provides an interface for managing a library's catalog and user transactions.
    The system allows for adding, updating, and deleting books in the catalog.
    It also handles user checkouts, returns, and tracks overdue items.
    The system uses a SQLite database to store and manage all data.
"""

__author__ = "Gavin Meyer, Matthew Moran, and Nicholas Doerfler"

# Imports
import tkinter as tk
from tkinter import messagebox, Toplevel, ttk, font
import sqlite3
from typing import Any


def initialize_tables(LMS: sqlite3.Connection) -> None:
    """
    Function that initializes the tables in the database with data.

    Args:
        - LMS (sqlite3.Connection): The connection to the database.
    """

    with LMS:
        # TABLES

        # Borrower
        LMS.execute(
            """
            CREATE TABLE IF NOT EXISTS BORROWER
            (
            Card_No INTEGER PRIMARY KEY AUTOINCREMENT,
            Name    TEXT,
            Address TEXT,
            Phone   TEXT
            );
            """
        )

        # Library_Branch
        LMS.execute(
            """
            CREATE TABLE IF NOT EXISTS LIBRARY_BRANCH
            (
            Branch_Id       INTEGER PRIMARY KEY AUTOINCREMENT,
            Branch_Name     TEXT,
            Branch_Address  TEXT
            );
            """
        )

        # Publisher
        LMS.execute(
            """
            CREATE TABLE IF NOT EXISTS PUBLISHER
            (
            Publisher_Name  VARCHAR(30) PRIMARY KEY,
            Phone           TEXT,
            Address         TEXT
            );
            """
        )

        # Book
        LMS.execute(
            """
            CREATE TABLE IF NOT EXISTS BOOK
            (
            Book_Id         INTEGER     PRIMARY KEY AUTOINCREMENT,
            Title           TEXT,
            Publisher_Name  VARCHAR(30)
            );
            """
        )

        # Book_Loans
        LMS.execute(
            """
            CREATE TABLE IF NOT EXISTS BOOK_LOANS
            (
            Book_Id       INTEGER,
            Branch_Id     INTEGER,
            Card_No       INTEGER,
            Date_Out      DATE,
            Due_Date      DATE,
            Returned_date DATE,
            PRIMARY KEY (Book_Id, Branch_Id, Card_No),
            FOREIGN KEY (Book_Id)   REFERENCES BOOK(Book_Id),
            FOREIGN KEY (Branch_Id) REFERENCES LIBRARY_BRANCH(Branch_Id),
            FOREIGN KEY (Card_No)   REFERENCES BORROWER(Card_No)
            );
            """
        )

        # Book_Copies
        LMS.execute(
            """
            CREATE TABLE IF NOT EXISTS BOOK_COPIES
            (
            Book_Id       INTEGER,
            Branch_Id     INTEGER,
            No_Of_Copies  INTEGER,
            PRIMARY KEY (Book_Id, Branch_Id),
            FOREIGN KEY (Book_Id)   REFERENCES BOOK(Book_Id),
            FOREIGN KEY (Branch_Id) REFERENCES LIBRARY_BRANCH(Branch_Id)
            );
            """
        )

        # Book_Authors
        LMS.execute(
            """
            CREATE TABLE IF NOT EXISTS BOOK_AUTHORS
            (
            Book_Id     INTEGER,
            Author_Name VARCHAR(50),
            PRIMARY KEY (Book_Id, Author_Name),
            FOREIGN KEY (Book_Id) REFERENCES BOOK(Book_Id)
            );
            """
        )

        # INSERTS

        # Borrower
        LMS.execute(
            """
            INSERT OR IGNORE INTO BORROWER (Card_No, Name, Address, Phone)
            VALUES
            (123456, 'John Smith', '456 Oak St, Arizona, AR 70010', '205-555-5555'),
            (789012, 'Jane Doe', '789 Maple Ave, New Jersey, NJ 32542', '555-235-5556'),
            (345678, 'Bob Johnson', '12 Elm St, Arizona, AR 70345', '545-234-5557'),
            (901234, 'Sarah Kim', '345 Pine St, New York, NY 10065', '515-325-2158'),
            (567890, 'Tom Lee', '678 S Oak St, New York, NY 10045', '209-525-5559'),
            (234567, 'Emily Lee', '389 Oaklay St, Arizona, AR 70986', '231-678-5560'),
            (890123, 'Michael Park', '123 Pinewood St, New Jersey, NJ 32954', '655-890-2161'),
            (456789, 'Laura Chen', '345 Mapman Ave, Arizona, AR 70776', '565-985-9962'),
            (111111, 'Alex Kim', '983 Sine St, Arizona, AR 70451', '678-784-5563'),
            (222222, 'Rachel Lee', '999 Apple Ave, Arizona, AR 70671', '231-875-5564'),
            (333333, 'William Johnson', '705 Paster St, New Jersey, 32002', '235-525-5567'),
            (444444, 'Ethan Martinez', '466 Deeplm St, New York, NY 10321', '555-555-5569'),
            (555555, 'Grace Hernandez', '315 Babes St, Arizona, AR 70862', '455-567-5587'),
            (565656, 'Sophia Park', '678 Dolphin St, New York, NY 10062', '675-455-5568'),
            (676767, 'Olivia Lee', '345 Spine St, New York, NY 10092', '435-878-5569'),
            (787878, 'Noah Thompson', '189 GreenOak Ave, New Jersey, NJ 32453', '245-555-5571'),
            (989898, 'Olivia Smith', '178 Elm St, New Jersey, NJ 32124', '325-500-5579'),
            (121212, 'Chloe Park', '345 Shark St, Arizona, AR 72213', '755-905-5572'),
            (232323, 'William Chen', '890 Sting St, New York, NY 10459', '406-755-5580'),
            (343434, 'Olivia Johnson', '345 Pine St, New Jersey, NJ 32095', '662-554-5575'),
            (454545, 'Dylan Kim', '567 Cowboy way St, New Jersey, NJ 32984', '435-254-5578');
            """
        )

        # Library_Branch
        LMS.execute(
            """
            INSERT OR IGNORE INTO LIBRARY_BRANCH (Branch_Id, Branch_Name, Branch_Address)
            VALUES
            (1, 'Main Branch', '123 Main St, New York, NY 10003'),
            (2, 'West Branch', '456 West St, Arizona, AR 70622'),
            (3, 'East Branch', '789 East St, New Jersey, NY 32032');
            """
        )

        # Publisher
        LMS.execute(
            """
            INSERT OR IGNORE INTO PUBLISHER (Publisher_Name, Phone, Address)
            VALUES
            ('HarperCollins', '212-207-7000', '195 Broadway, New York, NY 10007'),
            ('Penguin Books', '212-366-3000', '475 Hudson St, New York, NY 10014'),
            ('Penguin Classics', '212-366-2000', '123 Main St, California, CA 01383'),
            ('Scribner', '212-207-7474', '19 Broadway, New York, NY 10007'),
            ('Harper & Row', '212-207-7000', '1195 Border street, Montana, MT 59007'),
            ('Little, Brown and Company', '212-764-2000', '111 Huddle St, New Jersey, NJ 32014'),
            ('Faber and Faber', '201-797-3800', '463 south centre street, Arizona, AR 71653'),
            ('Chatto & Windus', '442-727-3800', 'Bloomsbury House, 7477 Great Russell St, Arizona, AR 72965'),
            ('Ward, Lock and Co.', '647-242-3434', '456 Maple Ave, Texas, TX 76013'),
            ('Random House India', '291-225-6634', '423 baywatch centre street, Alabama, AL 30513'),
            ('Thomas Cautley Newby', '243-353-2352', '890 Elmwood Dr, Floride, FL 98238'),
            ('Allen & Unwin', '212-782-9001', '22 New Wharf Rd, Arizona, AR 70654'),
            ('Pan Books', '313-243-5353', '567 Pine Tree Rd, Colorado, CO 87348'),
            ('Bantam Books', '313-243-5354', '1745 Broadway, New York, NY 10019'),
            ('Doubleday', '212-782-9000', '789 Division St, Minnesota, MN 55344'),
            ('American Publishing Company', '682-243-3524', '7652 Northgate way lane, Georgia, GA 30054'),
            ('Chapman and Hall', '833-342-2343', '789 Oak St, Texas, TX 76010');
            """
        )

        # Book
        LMS.execute(
            """
            INSERT OR IGNORE INTO BOOK (Book_Id, Title, Publisher_Name)
            VALUES
            (1, 'To Kill a Mockingbird', 'HarperCollins'),
            (2, '1984', 'Penguin Books'),
            (3, 'Pride and Prejudice', 'Penguin Classics'),
            (4, 'The Great Gatsby', 'Scribner'),
            (5, 'One Hundred Years of Solitude', 'Harper & Row'),
            (6, 'Animal Farm', 'Penguin Books'),
            (7, 'The Catcher in the Rye', 'Little, Brown and Company'),
            (8, 'Lord of the Flies', 'Faber and Faber'),
            (9, 'Brave New World', 'Chatto & Windus'),
            (10, 'The Picture of Dorian Gray', 'Ward, Lock and Co.'),
            (11, 'The Alchemist', 'HarperCollins'),
            (12, 'The God of Small Things', 'Random House India'),
            (13, 'Wuthering Heights', 'Thomas Cautley Newby'),
            (14, 'The Hobbit', 'Allen & Unwin'),
            (15, 'The Lord of the Rings', 'Allen & Unwin'),
            (16, 'The Hitchhiker''s Guide to the Galaxy', 'Pan Books'),
            (17, 'The Diary of a Young Girl', 'Bantam Books'),
            (18, 'The Da Vinci Code', 'Doubleday'),
            (19, 'The Adventures of Huckleberry Finn', 'Penguin Classics'),
            (20, 'The Adventures of Tom Sawyer', 'American Publishing Company'),
            (21, 'A Tale of Two Cities', 'Chapman and Hall');
            """
        )

        # Book_Loans
        LMS.execute(
            """
            INSERT OR IGNORE INTO BOOK_LOANS (Book_Id, Branch_Id, Card_No, Date_Out, Due_Date, Returned_date)
            VALUES
            (1, 1, 123456, '2022-01-01', '2022-02-01', '2022-02-01'),
            (2, 1, 789012, '2022-01-02', '2022-02-02', NULL),
            (3, 2, 345678, '2022-01-03', '2022-02-03', NULL),
            (4, 3, 901234, '2022-01-04', '2022-02-04', '2022-02-04'),
            (5, 1, 567890, '2022-01-05', '2022-02-05', '2022-02-09'),
            (6, 2, 234567, '2022-01-06', '2022-02-06', '2022-02-10'),
            (7, 2, 890123, '2022-01-07', '2022-02-07', '2022-03-08'),
            (8, 3, 456789, '2022-01-08', '2022-02-08', '2022-03-10'),
            (9, 1, 111111, '2022-01-09', '2022-02-09', '2022-02-06'),
            (10, 2, 222222, '2022-01-10', '2022-02-10', '2022-02-07'),
            (11, 1, 333333, '2022-03-01', '2022-03-08', '2022-03-08'),
            (12, 3, 444444, '2022-03-03', '2022-03-10', '2022-03-10'),
            (13, 3, 555555, '2022-02-03', '2022-03-03', '2022-02-18'),
            (14, 1, 565656, '2022-01-14', '2022-02-14', '2022-03-31'),
            (15, 3, 676767, '2022-01-15', '2022-02-15', '2022-02-21'),
            (16, 2, 787878, '2022-03-05', '2022-03-12', '2022-03-24'),
            (17, 3, 989898, '2022-03-23', '2022-03-30', '2022-03-30'),
            (18, 3, 121212, '2022-01-18', '2022-02-18', '2022-02-18'),
            (19, 1, 232323, '2022-03-24', '2022-03-31', '2022-03-31'),
            (20, 3, 343434, '2022-01-21', '2022-02-21', '2022-02-21'),
            (21, 3, 454545, '2022-01-24', '2022-02-24', '2022-02-24');
            """
        )

        # Book_Copies
        LMS.execute(
            """
            INSERT OR IGNORE INTO BOOK_COPIES (Book_Id, Branch_Id, No_Of_Copies)
            VALUES
            (1, 1, 3),
            (2, 1, 2),
            (3, 2, 1),
            (4, 3, 4),
            (5, 1, 5),
            (6, 2, 3),
            (7, 2, 2),
            (8, 3, 1),
            (9, 1, 4),
            (10, 2, 2),
            (11, 1, 3),
            (12, 3, 2),
            (13, 3, 1),
            (14, 1, 5),
            (15, 3, 1),
            (16, 2, 3),
            (17, 3, 2),
            (18, 3, 2),
            (19, 1, 5),
            (20, 3, 1),
            (21, 3, 1);
            """
        )

        # Book_Authors
        LMS.execute(
            """
            INSERT OR IGNORE INTO BOOK_AUTHORS (Book_Id, Author_Name)
            VALUES
            (1, 'Harper Lee'),
            (2, 'George Orwell'),
            (3, 'Jane Austen'),
            (4, 'F. Scott Fitzgerald'),
            (5, 'Gabriel Garcia Marquez'),
            (6, 'George Orwell'),
            (7, 'J.D. Salinger'),
            (8, 'William Golding'),
            (9, 'Aldous Huxley'),
            (10, 'Oscar Wilde'),
            (11, 'Paulo Coelho'),
            (12, 'Arundhati Roy'),
            (13, 'Emily Bronte'),
            (14, 'J.R.R. Tolkien'),
            (15, 'J.R.R. Tolkien'),
            (16, 'Douglas Adams'),
            (17, 'Anne Frank'),
            (18, 'Dan Brown'),
            (19, 'Mark Twain'),
            (20, 'Mark Twain'),
            (21, 'Charles Dickens');
            """
        )

        # Add Trigger - Update Book Copies on Book Loan
        LMS.execute(
            """
            CREATE TRIGGER IF NOT EXISTS update_book_copies_after_loan
            AFTER INSERT ON BOOK_LOANS
            BEGIN
            UPDATE BOOK_COPIES
            SET No_Of_Copies = No_Of_Copies - 1
            WHERE Book_Id = NEW.Book_Id AND Branch_Id = NEW.Branch_Id;
            END;
            """
        )


def initialize_column_updates(LMS: sqlite3.Connection) -> None:
    """
    Function that adds column "Late" to BOOK_LOANS table, updates it based on Due_Date and Returned_date.
    Also, adds column "Late_Fee" to LIBRARY_BRANCH table, updates it based on Branch_Id.

    Args:
        - LMS (sqlite3.Connection): The connection to the database.
    """

    with LMS:
        # Task 1: Query 1 - Part 1
        # Add column "Late" to BOOK_LOANS table
        LMS.execute(
            """
            ALTER TABLE BOOK_LOANS
            ADD COLUMN Late INTEGER;
            """
        )

        # Task 1: Query 1 - Part 2
        # Update Late column in BOOK_LOANS table based on Due_Date and Returned_date
        LMS.execute(
            """
            UPDATE BOOK_LOANS
            SET Late =
                CASE
                    WHEN Returned_date > Due_Date THEN 1
                    ELSE 0
                END;
            """
        )

        # Task 1: Query 2 - Part 1
        # Add column "Late_Fee" to LIBRARY_BRANCH table
        LMS.execute(
            """
            ALTER TABLE LIBRARY_BRANCH
            ADD COLUMN Late_Fee INTEGER;
            """
        )

        # Task 1: Query 2 - Part 2
        # Update Late_Fee row for Branch_Id 1 in LIBRARY_BRANCH table to 10
        LMS.execute(
            """
            UPDATE LIBRARY_BRANCH
            SET Late_Fee = 10
            WHERE Branch_Id = 1;
            """
        )

        # Task 1: Query 2 - Part 2
        # Update Late_Fee row for Branch_Id 2 in LIBRARY_BRANCH table to 5
        LMS.execute(
            """
            UPDATE LIBRARY_BRANCH
            SET Late_Fee = 5
            WHERE Branch_Id = 2;
            """
        )

        # Task 1: Query 2 - Part 2
        # Update Late_Fee row for Branch_Id 3 in LIBRARY_BRANCH table to 15
        LMS.execute(
            """
            UPDATE LIBRARY_BRANCH
            SET Late_Fee = 15
            WHERE Branch_Id = 3;
            """
        )


def delete_tables(cursor: sqlite3.Cursor) -> None:
    """
    Function that deletes all tables.

    Args:
        - cursor (sqlite3.Cursor): The cursor object to execute the SQL statements.
    """

    tables: list[str] = [
        "BORROWER",
        "LIBRARY_BRANCH",
        "PUBLISHER",
        "BOOK",
        "BOOK_LOANS",
        "BOOK_COPIES",
        "BOOK_AUTHORS",
    ]

    for table in tables:
        cursor.execute(f"DROP TABLE IF EXISTS {table};")


def autosize_tree_columns(tree: Any) -> None:
    """
    Function that resizes the columns in a Treeview widget to fit the data.

    Args:
        - tree (Any): The Treeview widget to resize.
    """
    for column in tree["columns"]:
        tree.column(column, width=font.Font().measure(column.title()))
        for row in tree.get_children():
            item_width: int = font.Font().measure(tree.set(row, column))
            if tree.column(column, width=None) < item_width:
                tree.column(column, width=item_width)


def display_table_data(root: tk.Tk, cursor: sqlite3.Cursor, table_name: Any) -> None:
    """
    Function that displays the data in a table in a new window.

    Args:
        - root (tk.Tk): The root window.
        - cursor (sqlite3.Cursor): The cursor object to execute the SQL statements.
        - table_name (Any): The name of the table to display.
    """

    data_window = tk.Toplevel(root)
    data_window.title(table_name)

    # Frame for Treeview and Scrollbar
    frame = tk.Frame(data_window)
    frame.pack(expand=True, fill="both")

    # Create a Treeview widget with a vertical scrollbar
    tree = ttk.Treeview(frame, show="headings")
    vsb = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=vsb.set)

    tree.pack(side="left", fill="both", expand=True)
    vsb.pack(side="right", fill="y")

    # Query the database for column names
    cursor.execute(f"PRAGMA table_info({table_name});")
    columns: list[Any] = [
        desc[1] for desc in cursor.fetchall()
    ]  # Get column names from the description

    # Define the columns in the tree
    tree["columns"] = columns
    for col in columns:
        tree.column(col, anchor="w")
        tree.heading(col, text=col, anchor="w")

    # Fetching data from the table
    cursor.execute(f"SELECT * FROM {table_name};")
    rows: list[Any] = cursor.fetchall()

    # Inserting data into the tree
    for row in rows:
        tree.insert("", "end", values=row)

    autosize_tree_columns(tree)


def open_table_display_window(root: tk.Tk, cursor: sqlite3.Cursor) -> None:
    """
    Function that opens a new window to display the tables in the database.

    Args:
        - root (tk.Tk): The root window.
        - cursor (sqlite3.Cursor): The cursor object to execute the SQL statements.
    """

    table_window = Toplevel(root)
    table_window.title("Tables")
    table_window.geometry("250x300")

    tables: list[str] = [
        "BORROWER",
        "LIBRARY_BRANCH",
        "PUBLISHER",
        "BOOK",
        "BOOK_LOANS",
        "BOOK_COPIES",
        "BOOK_AUTHORS",
    ]

    for table in tables:
        tk.Button(
            table_window,
            text=table,
            command=lambda t=table: display_table_data(root, cursor, t),
        ).pack(expand=True, anchor="center")


def add_borrower(root: tk.Tk, cursor: sqlite3.Cursor, LMS: sqlite3.Connection) -> None:
    """
    Function that opens a new window to add a new borrower to the database.

    Args:
        - root (tk.Tk): The root window.
        - cursor (sqlite3.Cursor): The cursor object to execute the SQL statements.
        - LMS (sqlite3.Connection): The connection to the database.

    Inner Function:
        - submit_borrower -- Submits the data entered in the window to the database.
    """

    def submit_borrower() -> None:
        name: str = name_entry.get()
        address: str = address_entry.get()
        phone: str = phone_entry.get()
        sql = "INSERT INTO BORROWER (Name, Address, Phone) VALUES (?, ?, ?)"
        cursor.execute(sql, (name, address, phone))
        LMS.commit()
        last_card_no: int | None = cursor.lastrowid
        messagebox.showinfo(
            "Success", f"Borrower added successfully!\nCard Number: {last_card_no}"
        )
        borrower_window.destroy()

    borrower_window = tk.Toplevel(root)
    borrower_window.title("Add Borrower")
    borrower_window.geometry("300x100")

    tk.Label(borrower_window, text="Name:").grid(row=0, column=0)
    name_entry = tk.Entry(borrower_window)
    name_entry.grid(row=0, column=1)

    tk.Label(borrower_window, text="Address:").grid(row=1, column=0)
    address_entry = tk.Entry(borrower_window)
    address_entry.grid(row=1, column=1)

    tk.Label(borrower_window, text="Phone:").grid(row=2, column=0)
    phone_entry = tk.Entry(borrower_window)
    phone_entry.grid(row=2, column=1)

    submit_btn = tk.Button(
        borrower_window, text="Add Borrower", command=submit_borrower
    )
    submit_btn.grid(row=3, column=1)


def check_out_book(
    root: tk.Tk, cursor: sqlite3.Cursor, LMS: sqlite3.Connection
) -> None:
    """
    Function that opens a new window to check out a book.

    Args:
        - root (tk.Tk): The root window.
        - cursor (sqlite3.Cursor): The cursor object to execute the SQL statements.
        - LMS (sqlite3.Connection): The connection to the database.

    Inner Function:
        - submit_checkout -- Submits the data entered in the window to the database.

    Exceptions:
        - sqlite3.Error -- Displays an error message if an error occurs while inserting the data.
    """

    def submit_checkout() -> None:
        book_id: str = book_id_entry.get()
        branch_id: str = branch_id_entry.get()
        card_no: str = card_no_entry.get()
        date_out: str = date_out_entry.get()
        due_date: str = due_date_entry.get()

        try:
            # Check if the book is available at the specified branch
            cursor.execute(
                """
                SELECT COUNT(*)
                FROM BOOK_COPIES
                WHERE Book_Id = ? AND Branch_Id = ? AND No_of_Copies > 0
                """,
                (book_id, branch_id),
            )

            available_books: Any = cursor.fetchone()[0]

            if available_books > 0:
                # Fetch the number of copies before checkout
                cursor.execute(
                    """
                    SELECT No_of_Copies
                    FROM BOOK_COPIES
                    WHERE Book_Id = ? AND Branch_Id = ?
                    """,
                    (book_id, branch_id),
                )

                copies_before_checkout: Any = cursor.fetchone()[0]

                # Book is available, proceed with checkout
                cursor.execute(
                    """
                    INSERT INTO BOOK_LOANS (Book_Id, Branch_Id, Card_No, Date_Out, Due_Date)
                    VALUES (?, ?, ?, ?, ?)
                    """,
                    (book_id, branch_id, card_no, date_out, due_date),
                )

                LMS.commit()

                # Fetch the number of copies after checkout
                cursor.execute(
                    """
                    SELECT No_of_Copies
                    FROM BOOK_COPIES
                    WHERE Book_Id = ? AND Branch_Id = ?
                    """,
                    (book_id, branch_id),
                )

                copies_after_checkout: Any = cursor.fetchone()[0]

                # Updating BOOK_LOANS table to set Late column
                cursor.execute(
                    """
                    UPDATE BOOK_LOANS
                    SET Late =
                        CASE
                            WHEN Returned_date > Due_Date THEN 1
                            ELSE 0
                        END
                    WHERE Book_Id = ? AND Branch_Id = ? AND Card_No = ?
                    """,
                    (book_id, branch_id, card_no),
                )

                LMS.commit()

                # Display the message with book and copy details
                messagebox.showinfo(
                    "Success",
                    f"Book checked out successfully!\nBook ID: {book_id}\nBranch ID: {branch_id}\nCopies Before: {copies_before_checkout}, Copies After: {copies_after_checkout}",
                )

            else:
                # Display error message if book is not available at the branch
                messagebox.showerror(
                    "Error", "This library branch does not have that book"
                )

        except sqlite3.Error as e:
            messagebox.showerror("Database Error", str(e))
        checkout_window.destroy()

    checkout_window = tk.Toplevel(root)
    checkout_window.title("Check Out Book")
    checkout_window.geometry("300x150")

    tk.Label(checkout_window, text="Book ID:").grid(row=0, column=0)
    book_id_entry = tk.Entry(checkout_window)
    book_id_entry.grid(row=0, column=1)

    tk.Label(checkout_window, text="Branch ID:").grid(row=1, column=0)
    branch_id_entry = tk.Entry(checkout_window)
    branch_id_entry.grid(row=1, column=1)

    tk.Label(checkout_window, text="Card Number:").grid(row=2, column=0)
    card_no_entry = tk.Entry(checkout_window)
    card_no_entry.grid(row=2, column=1)

    tk.Label(checkout_window, text="Date Out (YYYY-MM-DD):").grid(row=3, column=0)
    date_out_entry = tk.Entry(checkout_window)
    date_out_entry.grid(row=3, column=1)

    tk.Label(checkout_window, text="Due Date (YYYY-MM-DD):").grid(row=4, column=0)
    due_date_entry = tk.Entry(checkout_window)
    due_date_entry.grid(row=4, column=1)

    checkout_btn = tk.Button(checkout_window, text="Check Out", command=submit_checkout)
    checkout_btn.grid(row=5, column=1)


def add_new_book(root: tk.Tk, cursor: sqlite3.Cursor, LMS: sqlite3.Connection) -> None:
    """
    Function that opens a new window to add a new book to the database.

    Args:
        - root (tk.Tk): The root window.
        - cursor (sqlite3.Cursor): The cursor object to execute the SQL statements.
        - LMS (sqlite3.Connection): The connection to the database.

    Inner Function:
        - submit_book -- Submits the data entered in the window to the database.

    Exceptions:
        - sqlite3.Error -- Displays an error message if an error occurs while inserting the data.
    """

    def submit_book() -> None:
        # Gather input data
        title: str = title_entry.get()
        publisher_name: str = publisher_entry.get()
        author_name: str = author_entry.get()

        # Insert the book and author details into the database
        try:
            cursor.execute(
                """
                INSERT INTO BOOK (Title, Publisher_Name) VALUES (?, ?)
                """,
                (title, publisher_name),
            )

            book_id: int | None = cursor.lastrowid  # Fetch the newly created book ID

            cursor.execute(
                """
                INSERT INTO BOOK_AUTHORS (Book_Id, Author_Name) VALUES (?, ?)
                """,
                (book_id, author_name),
            )

            # Adding 5 copies of the book to each branch
            for branch_id in range(1, 4):
                cursor.execute(
                    """
                    INSERT INTO BOOK_COPIES (Book_Id, Branch_Id, No_Of_Copies) VALUES (?, ?, ?)
                    """,
                    (book_id, branch_id, 5),
                )

            LMS.commit()
            messagebox.showinfo(
                "Success",
                "Book added successfully along with author details and copies to branches.",
            )

        except sqlite3.Error as e:
            messagebox.showerror("Database Error", str(e))

        book_window.destroy()

    book_window = tk.Toplevel(root)
    book_window.title("Add New Book")
    book_window.geometry("300x100")

    tk.Label(book_window, text="Book Title:").grid(row=0, column=0)
    title_entry = tk.Entry(book_window)
    title_entry.grid(row=0, column=1)

    tk.Label(book_window, text="Publisher Name:").grid(row=1, column=0)
    publisher_entry = tk.Entry(book_window)
    publisher_entry.grid(row=1, column=1)

    tk.Label(book_window, text="Author Name:").grid(row=2, column=0)
    author_entry = tk.Entry(book_window)
    author_entry.grid(row=2, column=1)

    submit_btn = tk.Button(book_window, text="Add Book", command=submit_book)
    submit_btn.grid(row=3, column=1)


def report_loaned_books(root: tk.Tk, cursor: sqlite3.Cursor) -> None:
    """
    Function that opens a new window to display the books loaned out by a borrower.

    Args:
        - root (tk.Tk): The root window.
        - cursor (sqlite3.Cursor): The cursor object to execute the SQL statements.

    Inner Function:
        - show_report -- Displays the report in a new window.

    Exceptions:
        - sqlite3.Error -- Displays an error message if an error occurs while querying the database.
    """

    def show_report() -> None:
        book_title: str = book_title_entry.get()

        try:
            cursor.execute(
                """
                SELECT LB.Branch_Id, LB.Branch_Name, COUNT(*)
                FROM BOOK_LOANS BL
                JOIN BOOK B ON BL.Book_Id = B.Book_Id
                JOIN LIBRARY_BRANCH LB ON BL.Branch_Id = LB.Branch_Id
                WHERE B.Title = ?
                GROUP BY LB.Branch_Id
                """,
                (book_title,),
            )

            rows: list[Any] = cursor.fetchall()
            if not rows:
                messagebox.showinfo(
                    "No Results", f"No loans found for the book titled '{book_title}'."
                )
                return

            report_text: str = f"Loan Report for '{book_title}':\n\n"
            for row in rows:
                report_text += f"Branch ID: {row[0]}, Branch Name: {row[1]}, Copies Loaned Out: {row[2]}\n"

            messagebox.showinfo("Loan Report", report_text)

        except sqlite3.Error as e:
            messagebox.showerror("Database Error", str(e))

        report_window.destroy()

    report_window = tk.Toplevel(root)
    report_window.title("Book Loan Report")
    report_window.geometry("300x75")

    tk.Label(report_window, text="Book Title:").grid(row=0, column=0)
    book_title_entry = tk.Entry(report_window)
    book_title_entry.grid(row=0, column=1)

    report_btn = tk.Button(report_window, text="Show Report", command=show_report)
    report_btn.grid(row=1, column=1)


def report_late_returns(root: tk.Tk, cursor: sqlite3.Cursor) -> None:
    """
    Function that opens a new window to display the late returns between two dates.

    Args:
        - root (tk.Tk): The root window.
        - cursor (sqlite3.Cursor): The cursor object to execute the SQL statements.

    Inner Function:
        - show_report -- Displays the report in a new window.

    Exceptions:
        - sqlite3.Error -- Displays an error message if an error occurs while querying the database.
    """

    def show_report() -> None:
        start_date: str = start_date_entry.get().strip()
        end_date: str = end_date_entry.get().strip()

        try:
            cursor.execute(
                """
                SELECT BL.Book_Id, BL.Branch_Id, BL.Card_No, BL.Due_Date, BL.Returned_date,
                    JULIANDAY(BL.Returned_date) - JULIANDAY(BL.Due_Date) AS Days_Late
                FROM BOOK_LOANS BL
                WHERE (BL.Due_Date BETWEEN ? AND ? AND BL.Returned_date > BL.Due_Date) OR BL.Returned_date IS NULL
                """,
                (start_date, end_date),
            )

            rows: list[Any] = cursor.fetchall()
            if not rows:
                result_text_area.delete("1.0", tk.END)  # Clear existing text
                result_text_area.insert(
                    tk.END,
                    f"No late returns found between '{start_date}' and '{end_date}'.",
                )
                return

            report_text: str = (
                f"Late Returns Report (From {start_date} to {end_date}):\n\n"
            )

            # Iterate through the rows and format the report text
            for row in rows:
                if row[4] is None:
                    report_text += f"Book ID: {row[0]}, Branch ID: {row[1]}, Card No: {row[2]}, Due Date: {row[3]}, Returned Date: Not Returned, Days Late: Not Returned\n"
                else:
                    report_text += f"Book ID: {row[0]}, Branch ID: {row[1]}, Card No: {row[2]}, Due Date: {row[3]}, Returned Date: {row[4]}, Days Late: {int(row[5])}\n"

            result_text_area.delete("1.0", tk.END)  # Clear existing text
            result_text_area.insert(tk.END, report_text)

        except sqlite3.Error as e:
            messagebox.showerror("Database Error", str(e))

    report_window = tk.Toplevel(root)
    report_window.title("Late Returns Report")
    report_window.geometry("1000x600")

    tk.Label(report_window, text="Start Due Date (YYYY-MM-DD):").grid(row=0, column=0)
    start_date_entry = tk.Entry(report_window, width=20)
    start_date_entry.grid(row=0, column=1)

    tk.Label(report_window, text="End Due Date (YYYY-MM-DD):").grid(row=1, column=0)
    end_date_entry = tk.Entry(report_window, width=20)
    end_date_entry.grid(row=1, column=1)

    report_btn = tk.Button(report_window, text="Show Report", command=show_report)
    report_btn.grid(row=2, column=1)

    # Text area for results
    result_text_area = tk.Text(
        report_window, height=25, width=120
    )  # Adjust size as needed
    result_text_area.grid(row=3, column=0, columnspan=2, padx=10, pady=10)


def borrower_info(root: tk.Tk, cursor: sqlite3.Cursor) -> None:
    """
    Function that opens a new window to display the information about a borrower.

    Args:
        - root (tk.Tk): The root window.
        - cursor (sqlite3.Cursor): The cursor object to execute the SQL statements.

    Inner Function:
        - search_borrower -- Searches the database for the borrower information.

    Exceptions:
        - sqlite3.Error -- Displays an error message if an error occurs while querying the database.
    """

    def search_borrower() -> None:
        search_id: str = borrower_id_entry.get().strip()
        search_name: str = borrower_name_entry.get().strip()
        search_query: str = f"%{search_name}%"

        try:
            cursor.execute(
                """
                SELECT
                    B.Card_No,
                    B.Name,
                    COALESCE(SUM(CASE WHEN julianday(BL.Returned_date) - julianday(BL.Due_Date) > 0 THEN LB.Late_Fee * (julianday(BL.Returned_date) - julianday(BL.Due_Date)) ELSE 0 END), 0.00) AS LateFeeBalance
                FROM
                    BORROWER B
                LEFT JOIN
                    BOOK_LOANS BL ON B.Card_No = BL.Card_No
                LEFT JOIN
                    LIBRARY_BRANCH LB ON BL.Branch_Id = LB.Branch_Id
                WHERE
                    (B.Card_No = ? OR ? = '') AND
                    (B.Name LIKE ? OR ? = '')
                GROUP BY
                    B.Card_No, B.Name
                ORDER BY
                    LateFeeBalance DESC;
                """,
                (search_id, search_id, search_query, search_query),
            )

            rows: list[Any] = cursor.fetchall()
            result_text = "Borrower Information:\n\n"
            for row in rows:
                result_text += (
                    f"ID: {row[0]}, Name: {row[1]}, Late Fee Balance: ${row[2]:.2f}\n"
                )

            result_text_area.delete("1.0", tk.END)
            result_text_area.insert(tk.END, result_text)

        except sqlite3.Error as e:
            messagebox.showerror("Database Error", str(e))

    borrower_window = tk.Toplevel(root)
    borrower_window.title("Borrower Information")
    borrower_window.geometry("800x600")

    # Configure grid rows and columns
    borrower_window.grid_rowconfigure(
        3, weight=1
    )  # Make the row of Text widget growable
    borrower_window.grid_columnconfigure(1, weight=1)  # Make the second column growable

    tk.Label(borrower_window, text="Borrower ID:").grid(row=0, column=0)
    borrower_id_entry = tk.Entry(borrower_window, width=20)
    borrower_id_entry.grid(row=0, column=1)

    tk.Label(borrower_window, text="Borrower Name:").grid(row=1, column=0)
    borrower_name_entry = tk.Entry(borrower_window, width=20)
    borrower_name_entry.grid(row=1, column=1)

    search_btn = tk.Button(borrower_window, text="Search", command=search_borrower)
    search_btn.grid(row=2, column=1)

    result_text_area = tk.Text(borrower_window)
    result_text_area.grid(
        row=3, column=0, columnspan=2, sticky="nsew", padx=10, pady=10
    )


def book_info(root: tk.Tk, cursor: sqlite3.Cursor) -> None:
    """
    Function that opens a new window to display the information about a book.

    Args:
        - root (tk.Tk): The root window.
        - cursor (sqlite3.Cursor): The cursor object to execute the SQL statements.

    Inner Function:
        - search_book -- Searches the database for the book information.

    Exceptions:
        - sqlite3.Error -- Displays an error message if an error occurs while querying the database.
    """

    def search_book() -> None:
        borrower_id: str = borrower_id_entry.get().strip()
        book_id: str = book_id_entry.get().strip()
        book_title: str = book_title_entry.get().strip()
        search_title: str = f"%{book_title}%"

        try:
            cursor.execute(
                """
                SELECT
                    BL.Book_Id AS 'Book ID',
                    BK.Title AS 'Title',
                    BL.Date_Out AS 'Date Out',
                    BL.Due_Date AS 'Due Date',
                    BL.Returned_date AS 'Returned Date',
                    CASE
                        WHEN julianday(BL.Returned_date) - julianday(BL.Due_Date) > 0 THEN '$' || printf("%.2f", LB.Late_Fee * (julianday(BL.Returned_date) - julianday(BL.Due_Date)))
                        ELSE 'Non-Applicable'
                    END AS 'Late Fee'
                FROM
                    BOOK_LOANS BL
                JOIN
                    BOOK BK ON BL.Book_Id = BK.Book_Id
                JOIN
                    LIBRARY_BRANCH LB ON BL.Branch_Id = LB.Branch_Id
                WHERE
                    (BL.Card_No = ? OR ? = '') AND
                    (BL.Book_Id = ? OR ? = '') AND
                    (BK.Title LIKE ? OR ? = '')
                ORDER BY
                    CASE
                        WHEN julianday(BL.Returned_date) - julianday(BL.Due_Date) > 0 THEN LB.Late_Fee * (julianday(BL.Returned_date) - julianday(BL.Due_Date))
                        ELSE 0
                    END DESC;
                """,
                (
                    borrower_id,
                    borrower_id,
                    book_id,
                    book_id,
                    search_title,
                    search_title,
                ),
            )

            rows: list[Any] = cursor.fetchall()
            result_text = "Book Information:\n\n"
            for row in rows:
                result_text += f"Book ID: {row[0]}, Title: {row[1]}, Date Out: {row[2]}, Due Date: {row[3]}, Returned Date: {row[4]}, Late Fee: {row[5]}\n"

            result_text_area.delete("1.0", tk.END)
            result_text_area.insert(tk.END, result_text)

        except sqlite3.Error as e:
            messagebox.showerror("Database Error", str(e))

    book_window = tk.Toplevel(root)
    book_window.title("Book Information")
    book_window.geometry("1250x600")

    # Configure grid rows and columns
    book_window.grid_rowconfigure(4, weight=1)  # Make the row of Text widget growable
    book_window.grid_columnconfigure(1, weight=1)  # Make the second column growable

    tk.Label(book_window, text="Borrower ID:").grid(row=0, column=0)
    borrower_id_entry = tk.Entry(book_window, width=20)
    borrower_id_entry.grid(row=0, column=1)

    tk.Label(book_window, text="Book ID:").grid(row=1, column=0)
    book_id_entry = tk.Entry(book_window, width=20)
    book_id_entry.grid(row=1, column=1)

    tk.Label(book_window, text="Book Title:").grid(row=2, column=0)
    book_title_entry = tk.Entry(book_window, width=20)
    book_title_entry.grid(row=2, column=1)

    search_btn = tk.Button(
        book_window,
        text="Search",
        command=search_book,
    )
    search_btn.grid(row=3, column=1)

    result_text_area = tk.Text(book_window)
    result_text_area.grid(
        row=4, column=0, columnspan=2, sticky="nsew"
    )  # Stick to all sides


def buttons(root: tk.Tk, cursor: sqlite3.Cursor, LMS: sqlite3.Connection) -> None:
    """
    Function that creates the buttons in the main window.

    Args:
        - root (tk.Tk): The root window.
        - cursor (sqlite3.Cursor): The cursor object to execute the SQL statements.
        - LMS (sqlite3.Connection): The connection to the database.
    """

    # Initialize Tables Button
    initialize_tables_btn = tk.Button(
        root, text="Initialize Tables", command=lambda: initialize_tables(LMS)
    )

    # Initialize Column Updates Button
    initialize_column_updates_btn = tk.Button(
        root,
        text="Initialize Column Updates",
        command=lambda: initialize_column_updates(LMS),
    )

    # Delete Tables Button
    delete_tables_btn = tk.Button(
        root, text="Delete Tables", command=lambda: delete_tables(cursor)
    )

    # Display Tables Button
    display_tables_btn = tk.Button(
        root,
        text="Display Tables",
        command=lambda: open_table_display_window(root, cursor),
    )

    # Borrower Button
    borrower_btn = tk.Button(
        root, text="Add Borrower", command=lambda: add_borrower(root, cursor, LMS)
    )

    # Check Out Book Button
    checkout_btn = tk.Button(
        root, text="Check Out Book", command=lambda: check_out_book(root, cursor, LMS)
    )

    # Add New Book Button
    add_book_btn = tk.Button(
        root, text="Add New Book", command=lambda: add_new_book(root, cursor, LMS)
    )

    # Book Loan Report Button
    loan_report_btn = tk.Button(
        root, text="Book Loan Report", command=lambda: report_loaned_books(root, cursor)
    )

    # Late Returns Report Button
    late_returns_report_btn = tk.Button(
        root,
        text="Late Returns Report",
        command=lambda: report_late_returns(root, cursor),
    )

    # Borrower Information Button
    borrower_info_btn = tk.Button(
        root, text="Borrower Information", command=lambda: borrower_info(root, cursor)
    )

    # Book Information Button
    book_info_btn = tk.Button(
        root, text="Book Information", command=lambda: book_info(root, cursor)
    )

    # Packing the buttons
    initialize_tables_btn.pack(expand=True, anchor="center")
    initialize_column_updates_btn.pack(expand=True, anchor="center")
    delete_tables_btn.pack(expand=True, anchor="center")
    display_tables_btn.pack(expand=True, anchor="center")
    borrower_btn.pack(expand=True, anchor="center")
    checkout_btn.pack(expand=True, anchor="center")
    add_book_btn.pack(expand=True, anchor="center")
    loan_report_btn.pack(expand=True, anchor="center")
    late_returns_report_btn.pack(expand=True, anchor="center")
    borrower_info_btn.pack(expand=True, anchor="center")
    book_info_btn.pack(expand=True, anchor="center")


def main() -> None:
    """
    Main function that creates the main window.
    """

    LMS: sqlite3.Connection = sqlite3.connect("LMS.db")
    cursor: sqlite3.Cursor = LMS.cursor()

    root: tk.Tk = tk.Tk()
    root.title("Library Management System")
    root.geometry("350x400")

    buttons(root, cursor, LMS)

    root.mainloop()
    LMS.commit()
    LMS.close()


if __name__ == "__main__":
    main()
