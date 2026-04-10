 # CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**Spendly** is a personal expense tracker web app targeting Indian users (rupee-based currency). It uses a F lask backend with Jinja2 templates and vanilla CSS/JS frontend. The frontend UI is largely complete; backend features (auth, database, expense CRUD) are pending implementation.

## Development Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Run the development server (http://localhost:5001)
python app.py

# Run tests
pytest

# Run a single test file
pytest tests/test_foo.py
```

## Architecture

**Stack:** Python Flask 3.1.3 + SQLite + Jinja2 + Vanilla CSS/JS

**Entry point:** `app.py` — initializes the Flask app, defines all routes, runs on port 5001 with `debug=True`.

**Templates** (`templates/`): Jinja2-based. `base.html` is the master layout with a `content` block. All other templates extend it.

**Database layer** (`database/db.py`): Currently a stub. When implemented, it should provide:
- `get_db()` — SQLite connection using `row_factory` and enabling foreign keys
- `init_db()` — creates `users`, `expenses`, and `categories` tables
- `seed_db()` — inserts sample data for development

**Planned schema:**
```sql
users (id, name, email, password, created_at)
expenses (id, user_id, amount, category, description, date, created_at)
categories (id, name, user_id)
```

**Static assets** (`static/`):
- `css/style.css` — full design system (783 lines): color palette, typography, layout, all components
- `js/main.js` — currently empty; will handle modal toggles, form validation, etc.

## Route Implementation Status

Routes are stubbed in `app.py` with step-by-step comments guiding implementation:

| Route | Status |
|-------|--------|
| `GET /` | Done — renders `landing.html` |
| `GET/POST /login` | GET done; POST backend pending |
| `GET/POST /register` | GET done; POST backend pending |
| `GET /logout` | Stub |
| `GET /profile` | Stub |
| `GET/POST /expenses/add` | Stub |
| `GET/POST /expenses/<id>/edit` | Stub |
| `GET /expenses/<id>/delete` | Stub |
| `GET /terms`, `GET /privacy` | Done |

## Design System

- **Fonts:** DM Serif Display (headings), DM Sans (body) — loaded from Google Fonts in `base.html`
- **Colors:** Background `#f7f6f3`, text `#0f0f0f`, primary `#1a472a` (dark green), accent `#c17f24` (gold), danger `#c0392b`
- **Responsive breakpoints:** 900px and 600px
- **Button variants:** `.btn-primary`, `.btn-ghost`, `.btn-submit`
