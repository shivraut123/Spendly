# Spec: Backend Routes For Profile Page

## Overview
Wire the `/profile` route to real database data. Step 04 built a fully designed profile page driven by hardcoded Python dicts. This step replaces every hardcoded value with live queries against `users` and `expenses`. On completion, a logged-in user will see their own name, email, join date, real transaction history, accurate summary stats, and a correct category breakdown — all pulled from `spendly.db` at request time.

## Depends on
- Step 01 — Database setup (`users`, `expenses` tables, `get_db()`)
- Step 02 — Registration (`users` rows exist)
- Step 03 — Login and Logout (`session['user_id']` is set on login)
- Step 04 — Profile Page Design (`templates/profile.html` exists with the correct variable names)

## Routes
- `GET /profile` — render profile page with live DB data — logged-in only (already exists; upgrade it)

No new routes.

## Database changes
No new tables or columns. Three new helper functions must be added to `database/db.py`:

- `get_user_by_id(user_id)` — fetches a single row from `users` by primary key; returns `sqlite3.Row` or `None`.
- `get_expenses_by_user(user_id)` — returns all expense rows for the given user ordered by `date DESC`, `created_at DESC`.
- `get_category_totals(user_id)` — returns per-category totals as rows of `(category, total)` ordered by `total DESC`, computed with a GROUP BY query.

## Templates
- **Modify**: `templates/profile.html` — no structural changes; ensure `user.member_since` renders a formatted date string (e.g. "April 2026") not a raw ISO timestamp.

## Files to change
- `app.py` — rewrite the `/profile` view function body:
  1. Guard: `session.get("user_id")` → redirect to login if absent (already present, keep it).
  2. Fetch user row via `get_user_by_id(session["user_id"])`.
  3. Fetch expenses via `get_expenses_by_user(session["user_id"])`.
  4. Compute `stats` dict inline (total amount, count, top category from first category-totals row).
  5. Build `transactions` list (last 5 expenses, formatted for template).
  6. Fetch `categories` via `get_category_totals(session["user_id"])`, compute `pct` as percentage of grand total.
  7. Build `user` dict with `name`, `initials` (first letter of first word), `email`, `member_since` (formatted from `created_at`).
  8. Pass all four dicts/lists to `render_template("profile.html", ...)`.
- `database/db.py` — add `get_user_by_id`, `get_expenses_by_user`, `get_category_totals`.

## Files to create
None.

## New dependencies
No new dependencies.

## Rules for implementation
- No SQLAlchemy or ORMs — use raw `sqlite3` via `get_db()` only
- Parameterised queries only — never use f-strings or `.format()` in SQL
- Passwords hashed with werkzeug (no auth changes in this step)
- Use CSS variables — never hardcode hex values
- All templates extend `base.html`
- Amount formatting: render as `₹{amount:,.2f}` (e.g. `₹2,500.00`) — do this in Python, not in the template
- `member_since` must be a human-readable string like `"April 2026"` — parse `created_at` (ISO datetime) and format with `datetime.strptime` / `strftime`
- `initials`: take the first character of `user["name"]`, uppercased
- `pct` per category: `round(category_total / grand_total * 100)` — guard against division by zero (0 if no expenses)
- `transactions` list: show the 5 most recent expenses; each dict must have keys `date` (e.g. `"Apr 10"`), `description`, `category`, `amount`
- `categories` list: each dict must have keys `name`, `amount` (formatted string), `pct` (integer)
- If the user has no expenses, `stats["total"]` = `"₹0.00"`, `stats["count"]` = 0, `stats["top_category"]` = `"—"`, `transactions` = `[]`, `categories` = `[]`

## Definition of done
- [ ] Visiting `/profile` while logged in as the demo user shows `"Demo User"` (not hardcoded)
- [ ] `user.email` on the profile page shows the real email from the `users` table
- [ ] `member_since` shows the correct join month and year (e.g. `"April 2026"`)
- [ ] The summary stats reflect the actual sum and count of expenses in the database
- [ ] The top category shown is whichever category has the highest total in the DB
- [ ] The transaction history table shows real rows from the `expenses` table, ordered newest first
- [ ] The category breakdown percentages add up to 100 (±1 due to rounding)
- [ ] Seeding a second user and logging in as them shows only that user's data
- [ ] Visiting `/profile` with no expenses shows zeros and empty lists without crashing
- [ ] No hardcoded strings remain in the `profile()` view function in `app.py`
