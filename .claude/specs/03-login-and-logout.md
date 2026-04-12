# Spec: Login and Logout

## Overview
Implement login and logout so registered users can authenticate with Spendly. This step upgrades the existing stub `GET /login` route into a full `GET/POST` form that verifies credentials against the `users` table, writes the authenticated user's id into the Flask session, and redirects to the dashboard (or a placeholder until Step 4). The logout route clears the session and redirects to the landing page. After this step, the app has a complete auth cycle: register → login → logout.

## Depends on
- Step 01 — Database setup (`users` table, `get_db()`)
- Step 02 — Registration (`create_user()`, `users` rows exist to log in against)

## Routes
- `GET /login` — render login form — public (already exists, upgrade to GET/POST)
- `POST /login` — validate credentials, set session, redirect to `/profile` — public
- `GET /logout` — clear session, redirect to `/` — logged-in (currently a stub string)

## Database changes
No new tables or columns. A new DB helper must be added to `database/db.py`:
- `get_user_by_email(email)` — fetches a single row from `users` matching the email; returns a `sqlite3.Row` or `None` if not found.

## Templates
- **Modify**: `templates/login.html`
  - Change the form `action` to `url_for('login')` with `method="post"`
  - Add `name` attributes to inputs: `email`, `password`
  - Add a block to display flash error messages (e.g. "Invalid email or password")
  - Keep all existing visual design

## Files to change
- `app.py` — upgrade `login()` to handle GET and POST; add `logout()` implementation; import `session` and `check_password_hash`
- `database/db.py` — add `get_user_by_email(email)` helper
- `templates/login.html` — wire up form action/method and flash message display

## Files to create
None.

## New dependencies
No new dependencies. Uses `werkzeug.security.check_password_hash` (already installed) and Flask's built-in `session`, `flash`, `redirect`, `url_for`.

## Rules for implementation
- No SQLAlchemy or ORMs
- Parameterised queries only — never use f-strings in SQL
- Verify passwords with `werkzeug.security.check_password_hash` — never compare plaintext
- Use Flask `session` (dict-based) to store the logged-in user: `session['user_id']` and `session['user_name']`
- `app.secret_key` is already set in `app.py` — do not change it
- On POST /login:
  1. Fetch user by email — if not found, flash a generic error ("Invalid email or password") and re-render the form
  2. Check password hash — if wrong, flash the same generic error and re-render (do not reveal which field was wrong)
  3. On success, set `session['user_id']` and `session['user_name']`, then redirect to `url_for('profile')`
- On GET /logout: call `session.clear()`, flash a confirmation message, redirect to `url_for('landing')`
- Never expose whether the email exists — always use a single generic error message
- All templates extend `base.html`
- Use CSS variables — never hardcode hex values
- Use `url_for()` for every internal link — never hardcode URLs

## Definition of done
- [ ] `GET /login` renders the login form without errors
- [ ] Submitting valid credentials sets the session and redirects to `/profile`
- [ ] Submitting an unregistered email re-renders the form with a generic error, no session set
- [ ] Submitting a wrong password re-renders the form with the same generic error, no session set
- [ ] Submitting with any empty field re-renders the form with an error message
- [ ] `GET /logout` clears the session and redirects to the landing page
- [ ] After logout, navigating to `/profile` does not reveal user data (returns the stub string, which is acceptable until Step 4)
- [ ] The demo user (`demo@spendly.com` / `demo123`) seeded in Step 01 can log in successfully
