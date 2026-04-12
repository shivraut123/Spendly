import sqlite3
import os
from werkzeug.security import generate_password_hash

# Sets the database file to be created in your main project folder
DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "spendly.db")


def get_db():
    """Connect to the database and return the connection object."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    # Enable foreign key constraints in SQLite
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    """Initialize the database with the required tables."""
    conn = get_db()
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS users (
            id            INTEGER PRIMARY KEY AUTOINCREMENT,
            name          TEXT    NOT NULL,
            email         TEXT    UNIQUE NOT NULL,
            password_hash TEXT    NOT NULL,
            created_at    TEXT    DEFAULT (datetime('now'))
        );

        CREATE TABLE IF NOT EXISTS expenses (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id     INTEGER NOT NULL REFERENCES users(id),
            amount      REAL    NOT NULL,
            category    TEXT    NOT NULL,
            date        TEXT    NOT NULL,
            description TEXT,
            created_at  TEXT    DEFAULT (datetime('now'))
        );
    """)
    conn.close()


def seed_db():
    """Seed the database with a demo user and sample expenses if it is empty."""
    conn = get_db()
    count = conn.execute("SELECT COUNT(*) FROM users").fetchone()[0]
    
    # If users already exist, skip seeding to prevent duplicates
    if count > 0:
        conn.close()
        return

    # Create a demo user
    cursor = conn.execute(
        "INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
        ("Demo User", "demo@spendly.com", generate_password_hash("demo123")),
    )
    user_id = cursor.lastrowid

    # Create sample expenses linked to the demo user
    expenses = [
        (user_id, 450.00,  "Food",          "2026-04-01", "Grocery shopping"),
        (user_id, 120.00,  "Transport",     "2026-04-02", "Auto rickshaw"),
        (user_id, 1200.00, "Bills",         "2026-04-03", "Electricity bill"),
        (user_id, 350.00,  "Health",        "2026-04-05", "Pharmacy"),
        (user_id, 600.00,  "Entertainment", "2026-04-07", "Movie tickets"),
        (user_id, 2500.00, "Shopping",      "2026-04-09", "Clothes"),
        (user_id, 80.00,   "Other",         "2026-04-10", "Miscellaneous"),
        (user_id, 220.00,  "Food",          "2026-04-10", "Restaurant lunch"),
    ]

    conn.executemany(
        "INSERT INTO expenses (user_id, amount, category, date, description) VALUES (?, ?, ?, ?, ?)",
        expenses,
    )
    conn.commit()
    conn.close()


def get_user_by_email(email):
    """Return the users row for email, or None if not found."""
    conn = get_db()
    user = conn.execute(
        "SELECT * FROM users WHERE email = ?", (email,)
    ).fetchone()
    conn.close()
    return user


def create_user(name, email, password):
    """Hash the password and insert a new user into the database."""
    hash_pw = generate_password_hash(password)
    
    conn = get_db()
    cursor = conn.execute(
        "INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
        (name, email, hash_pw),
    )
    conn.commit()
    user_id = cursor.lastrowid
    conn.close()
    
    return user_id