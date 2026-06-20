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


## requirements.txt
```
mysql-connector-python
pandas
```
