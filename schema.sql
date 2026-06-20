-- schema.sql
-- Run this in MySQL first: mysql -u root -p < schema.sql

CREATE DATABASE IF NOT EXISTS library_db;
USE library_db;

CREATE TABLE IF NOT EXISTS books (
    book_id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(150) NOT NULL,
    author VARCHAR(100),
    genre VARCHAR(50),
    total_copies INT NOT NULL,
    available_copies INT NOT NULL
);

CREATE TABLE IF NOT EXISTS members (
    member_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100),
    phone VARCHAR(15)
);

CREATE TABLE IF NOT EXISTS transactions (
    txn_id INT AUTO_INCREMENT PRIMARY KEY,
    book_id INT NOT NULL,
    member_id INT NOT NULL,
    issue_date DATE NOT NULL,
    due_date DATE NOT NULL,
    return_date DATE,
    FOREIGN KEY (book_id) REFERENCES books(book_id),
    FOREIGN KEY (member_id) REFERENCES members(member_id)
);

-- A few sample rows so the app has something to show on first run
INSERT INTO books (title, author, genre, total_copies, available_copies) VALUES
('Clean Code', 'Robert C. Martin', 'Tech', 3, 3),
('Atomic Habits', 'James Clear', 'Self-help', 2, 2),
('The Pragmatic Programmer', 'Andy Hunt', 'Tech', 2, 2);

INSERT INTO members (name, email, phone) VALUES
('Ruchitha M', 'ruchitha1299@gmail.com', '9347017972');
