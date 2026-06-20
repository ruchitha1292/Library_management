# Library Management System — 7-Day Plan

Python + MySQL + Pandas. Built to be small enough to fully understand and
explain in an interview.

## Files
- `schema.sql` — creates the database and 3 tables, with sample data
- `library_app.py` — CLI app: CRUD on books/members, issue/return, overdue report
- `requirements.txt` — Python packages needed

## Setup
```
pip install -r requirements.txt
mysql -u root -p < schema.sql
```
Then open `library_app.py` and update `DB_CONFIG` with your MySQL password.
Run with:
```
python library_app.py
```

## Day-by-day

**Day 1 — Understand the schema**
Open `schema.sql`. Don't just run it — draw the 3 tables on paper:
`books`, `members`, `transactions`. Note the foreign keys. Be able to say
*why* transactions is a separate table instead of cramming issue/return
data into `books` (answer: a book can be issued many times over its life —
that's a one-to-many relationship, which is why it needs its own table).

**Day 2 — Run it, break it, fix it**
Set up MySQL locally, run the app, add a few books and members through the
menu. Intentionally try to issue a book with 0 copies left and watch it get
blocked — that's the `if not row or row[0] <= 0` check in `issue_book()`.

**Day 3-4 — Read every function line by line**
Don't skip this. For each function, be able to explain in one sentence
what SQL it runs and why. This is exactly where you got stuck on your
plate-recognition project — don't let it happen twice.

**Day 5 — Reporting**
Look at `overdue_report()`. Understand the JOIN: it pulls book title and
member name into one table by matching IDs across 3 tables, then filters
to unreturned + past-due. Try changing the query yourself — e.g., add a
"most borrowed books" report.

**Day 6 — Error handling and polish**
Look at the `try/except` block in `main()`. Add one more case yourself —
e.g., handle what happens if someone tries to delete a book that's
currently issued (hint: the foreign key will block it — catch that error
and print a friendly message instead of crashing).

**Day 7 — Practice explaining it out loud**
Use the talking points below. Say them out loud, not just read them.

## Interview talking points

**"Walk me through this project."**
"It's a library management CLI in Python that talks to a MySQL database
through three tables — books, members, and transactions. I used the
transactions table to track issue and return events separately from the
books table, since a book can be borrowed many times. I also used Pandas
to pull data out of MySQL for reporting, like an overdue-books report
that I export to CSV."

**"Why MySQL and not just a Python list/dict?"**
"Because the data needs to persist between runs and stay consistent — if
two people issue books at the same time, the database handles that more
safely than an in-memory list would. It also lets me use SQL joins to
combine data across tables efficiently."

**"What was the trickiest part?"**
Pick something true — e.g., keeping `available_copies` in sync when you
update `total_copies`, or writing the JOIN query for the overdue report.

**"What would you improve given more time?"**
Good honest answer: add a simple web front-end (Flask), add input
validation, or add fines for overdue books.

## requirements.txt
```
mysql-connector-python
pandas
```
