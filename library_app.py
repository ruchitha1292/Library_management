"""
Library Management System
A CLI app demonstrating Python + MySQL CRUD operations + Pandas reporting.

Setup:
    1. Create the database: mysql -u root -p < schema.sql
    2. pip install mysql-connector-python pandas
    3. Update DB_CONFIG below with your MySQL username/password
    4. python library_app.py
"""

import mysql.connector
from mysql.connector import Error
import pandas as pd
from datetime import date, timedelta

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "Ruchi@1299",
    "database": "library_db",
}


def get_connection():
    return mysql.connector.connect(**DB_CONFIG)


# ---------- BOOK CRUD ----------

def add_book(title, author, genre, copies):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO books (title, author, genre, total_copies, available_copies) "
        "VALUES (%s, %s, %s, %s, %s)",
        (title, author, genre, copies, copies),
    )
    conn.commit()
    cur.close()
    conn.close()
    print(f"Added '{title}'.")


def view_books():
    conn = get_connection()
    df = pd.read_sql("SELECT * FROM books", conn)
    conn.close()
    print(df.to_string(index=False))


def update_book_copies(book_id, new_total):
    conn = get_connection()
    cur = conn.cursor()
    # Keep available_copies consistent: adjust by the same delta as total
    cur.execute("SELECT total_copies, available_copies FROM books WHERE book_id=%s", (book_id,))
    row = cur.fetchone()
    if not row:
        print("Book not found.")
        return
    old_total, old_available = row
    delta = new_total - old_total
    new_available = max(0, old_available + delta)
    cur.execute(
        "UPDATE books SET total_copies=%s, available_copies=%s WHERE book_id=%s",
        (new_total, new_available, book_id),
    )
    conn.commit()
    cur.close()
    conn.close()
    print("Updated.")


def delete_book(book_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM books WHERE book_id=%s", (book_id,))
    conn.commit()
    cur.close()
    conn.close()
    print("Deleted.")


# ---------- MEMBER CRUD ----------

def add_member(name, email, phone):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO members (name, email, phone) VALUES (%s, %s, %s)",
        (name, email, phone),
    )
    conn.commit()
    cur.close()
    conn.close()
    print(f"Added member '{name}'.")


def view_members():
    conn = get_connection()
    df = pd.read_sql("SELECT * FROM members", conn)
    conn.close()
    print(df.to_string(index=False))


# ---------- ISSUE / RETURN ----------

def issue_book(book_id, member_id, loan_days=14):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT available_copies FROM books WHERE book_id=%s", (book_id,))
    row = cur.fetchone()
    if not row or row[0] <= 0:
        print("No copies available.")
        cur.close()
        conn.close()
        return

    issue_date = date.today()
    due_date = issue_date + timedelta(days=loan_days)
    cur.execute(
        "INSERT INTO transactions (book_id, member_id, issue_date, due_date) "
        "VALUES (%s, %s, %s, %s)",
        (book_id, member_id, issue_date, due_date),
    )
    cur.execute(
        "UPDATE books SET available_copies = available_copies - 1 WHERE book_id=%s",
        (book_id,),
    )
    conn.commit()
    cur.close()
    conn.close()
    print(f"Issued. Due back {due_date}")


def return_book(txn_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT book_id, return_date FROM transactions WHERE txn_id=%s", (txn_id,))
    row = cur.fetchone()
    if not row:
        print("Transaction not found.")
        return
    book_id, already_returned = row
    if already_returned:
        print("Already returned.")
        return

    cur.execute(
        "UPDATE transactions SET return_date=%s WHERE txn_id=%s",
        (date.today(), txn_id),
    )
    cur.execute(
        "UPDATE books SET available_copies = available_copies + 1 WHERE book_id=%s",
        (book_id,),
    )
    conn.commit()
    cur.close()
    conn.close()
    print("Returned.")


# ---------- REPORTING (Pandas) ----------

def overdue_report(export_csv=True):
    conn = get_connection()
    df = pd.read_sql(
        """
        SELECT t.txn_id, b.title, m.name AS member, t.issue_date, t.due_date
        FROM transactions t
        JOIN books b ON t.book_id = b.book_id
        JOIN members m ON t.member_id = m.member_id
        WHERE t.return_date IS NULL AND t.due_date < CURDATE()
        """,
        conn,
    )
    conn.close()
    print(df.to_string(index=False) if not df.empty else "No overdue books.")
    if export_csv:
        df.to_csv("overdue_report.csv", index=False)
        print("Exported to overdue_report.csv")
    return df


# ---------- CLI MENU ----------

MENU = """
1. Add book
2. View books
3. Update book copies
4. Delete book
5. Add member
6. View members
7. Issue book
8. Return book
9. Overdue report
0. Exit
"""

def main():
    while True:
        print(MENU)
        choice = input("Choose an option: ").strip()
        try:
            if choice == "1":
                add_book(input("Title: "), input("Author: "), input("Genre: "), int(input("Copies: ")))
            elif choice == "2":
                view_books()
            elif choice == "3":
                update_book_copies(int(input("Book ID: ")), int(input("New total copies: ")))
            elif choice == "4":
                delete_book(int(input("Book ID: ")))
            elif choice == "5":
                add_member(input("Name: "), input("Email: "), input("Phone: "))
            elif choice == "6":
                view_members()
            elif choice == "7":
                issue_book(int(input("Book ID: ")), int(input("Member ID: ")))
            elif choice == "8":
                return_book(int(input("Transaction ID: ")))
            elif choice == "9":
                overdue_report()
            elif choice == "0":
                break
            else:
                print("Invalid option.")
        except Error as e:
            print(f"Database error: {e}")
        except ValueError:
            print("Please enter a valid number.")


if __name__ == "__main__":
    main()
