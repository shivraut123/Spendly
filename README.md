# Spendly - Personal Expense Tracker

A personal finance web application built with Flask that helps users track their expenses, understand spending patterns, and manage budgets.

## Overview

Spendly is a clean, minimal expense tracking app targeting Indian users (rupee-based). It provides a polished UI for logging expenses, categorizing them, and visualizing spending habits.

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python, Flask 3.1.3 |
| Frontend | HTML5, Jinja2, Vanilla CSS, Vanilla JS |
| Database | SQLite (via Python `sqlite3`) |
| Fonts | Google Fonts (DM Serif Display, DM Sans) |
| Testing | pytest 8.3.5, pytest-flask 1.3.0 |

## Project Structure

```
expense-tracker/
├── app.py                  # Main Flask application, routes
├── requirements.txt        # Python dependencies
├── database/
│   ├── __init__.py
│   └── db.py               # SQLite connection, init, seed helpers
├── static/
│   ├── css/
│   │   └── style.css       # Main stylesheet with design system
│   └── js/
│       └── main.js         # Client-side JavaScript
└── templates/
    ├── base.html           # Base layout (navbar, footer)
    ├── landing.html        # Homepage with hero and feature sections
    ├── login.html          # Login form
    ├── register.html       # Registration form
    ├── terms.html          # Terms and Conditions
    └── privacy.html        # Privacy Policy
```

## Routes

| Route | Method | Description | Status |
|---|---|---|---|
| `/` | GET | Landing page | Done |
| `/register` | GET, POST | User registration | UI done, backend pending |
| `/login` | GET, POST | User login | UI done, backend pending |
| `/logout` | GET | User logout | Pending |
| `/profile` | GET | User profile | Pending |
| `/expenses/add` | GET, POST | Add new expense | Pending |
| `/expenses/<id>/edit` | GET, POST | Edit expense | Pending |
| `/expenses/<id>/delete` | GET | Delete expense | Pending |
| `/terms` | GET | Terms and Conditions | Done |
| `/privacy` | GET | Privacy Policy | Done |

## Features

- **Landing page** — Hero section, mock app preview, feature highlights, YouTube video modal
- **Authentication** — Register and login forms (backend implementation pending)
- **Expense CRUD** — Add, edit, delete expenses (pending)
- **Categories** — Food, Travel, Bills, and more with color-coded visualization
- **Legal pages** — Terms of Service and Privacy Policy

## Database Schema (planned)

```sql
users (id, name, email, password, created_at)
expenses (id, user_id, amount, category, description, date, created_at)
categories (id, name, user_id)
```

## Design System

- **Primary font:** DM Serif Display (headings), DM Sans (body)
- **Color palette:**
  - Background: `#f7f6f3` (warm paper)
  - Ink: `#0f0f0f`
  - Accent green: `#1a472a`
  - Accent gold: `#c17f24`
  - Danger: `#c0392b`
- **Responsive breakpoints:** 900px, 600px

## Getting Started

### Prerequisites

- Python 3.10+
- pip

### Installation

```bash
# Clone the repository
git clone <repo-url>
cd expense-tracker

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Running the App

```bash
python app.py
```

The app will be available at `http://localhost:5001`.

### Running Tests

```bash
pytest
```

## Development Status

The frontend and project scaffolding are complete. The following backend features are yet to be implemented:

- [ ] Database initialization (`database/db.py`)
- [ ] User registration (POST `/register`)
- [ ] User login with session management (POST `/login`)
- [ ] Logout (GET `/logout`)
- [ ] User profile page
- [ ] Add expense
- [ ] Edit expense
- [ ] Delete expense

## License

This project is for personal/educational use. See [Terms and Conditions](/terms) and [Privacy Policy](/privacy) for details.
