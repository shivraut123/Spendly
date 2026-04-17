import sqlite3 # You'll need this for catching duplicate emails later
from flask import Flask, render_template, request, flash, redirect, url_for, session
from database.db import get_db, init_db, seed_db, create_user # Assuming create_user is added

app = Flask(__name__)
app.secret_key = "super-secret-development-key" # Required for flash() to work

with app.app_context():
    init_db()
    seed_db()

# ------------------------------------------------------------------ #
# Routes                                                              #
# ------------------------------------------------------------------ #

@app.route("/")
def landing():
    return render_template("landing.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if session.get("user_id"):
        return redirect(url_for("profile"))
    if request.method == "POST":
        from database.db import get_user_by_email
        from werkzeug.security import check_password_hash
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")
        if not email or not password:
            flash("All fields are required.")
            return render_template("login.html")
        user = get_user_by_email(email)
        if not user or not check_password_hash(user["password_hash"], password):
            flash("Invalid email or password.")
            return render_template("login.html")
        session["user_id"] = user["id"]
        session["user_name"] = user["name"]
        return redirect(url_for("profile"))
    return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # 1. Grab the data from the submitted form
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")
        confirm_password = request.form.get("confirm_password", "")

        # 2. Basic Validation: Check for empty fields
        if not name or not email or not password or not confirm_password:
            flash("All fields are required.")
            return render_template("register.html", name=name, email=email)

        # 3. ---> YOUR SNIPPET GOES HERE <---
        if password != confirm_password:
            flash("Passwords do not match.")
            return render_template("register.html", name=name, email=email)

        # 4. Database Insertion (From Claude's plan)
        try:
            create_user(name, email, password)
        except sqlite3.IntegrityError:
            flash("An account with that email is already registered.")
            return render_template("register.html", name=name, email=email)

        # 5. Success! Redirect to login.
        flash("Account created! Please sign in.")
        return redirect(url_for("login"))

    # If it's a GET request (just visiting the page), render the empty form
    return render_template("register.html")

# ------------------------------------------------------------------ #
# Placeholder routes — students will implement these                  #
# ------------------------------------------------------------------ #

@app.route("/terms")
def terms():
    return render_template("terms.html")


@app.route("/privacy")
def privacy():
    return render_template("privacy.html")


@app.route("/logout")
def logout():
    session.clear()
    flash("You've been signed out.")
    return redirect(url_for("landing"))


@app.route("/profile")
def profile():
    if not session.get("user_id"):
        return redirect(url_for("login"))

    user = {
        "name": "Demo User",
        "initials": "D",
        "email": "demo@spendly.com",
        "member_since": "April 2026",
    }

    stats = {
        "total": "₹5,520.00",
        "count": 8,
        "top_category": "Shopping",
    }

    transactions = [
        {"date": "Apr 10", "description": "Restaurant lunch",  "category": "Food",          "amount": "₹220.00"},
        {"date": "Apr 10", "description": "Miscellaneous",     "category": "Other",         "amount": "₹80.00"},
        {"date": "Apr 09", "description": "Clothes",           "category": "Shopping",      "amount": "₹2,500.00"},
        {"date": "Apr 07", "description": "Movie tickets",     "category": "Entertainment", "amount": "₹600.00"},
        {"date": "Apr 05", "description": "Pharmacy",          "category": "Health",        "amount": "₹350.00"},
    ]

    categories = [
        {"name": "Shopping",      "amount": "₹2,500.00", "pct": 45},
        {"name": "Bills",         "amount": "₹1,200.00", "pct": 22},
        {"name": "Food",          "amount": "₹670.00",   "pct": 12},
        {"name": "Entertainment", "amount": "₹600.00",   "pct": 11},
        {"name": "Health",        "amount": "₹350.00",   "pct": 6},
        {"name": "Transport",     "amount": "₹120.00",   "pct": 2},
        {"name": "Other",         "amount": "₹80.00",    "pct": 1},
    ]

    return render_template(
        "profile.html",
        user=user,
        stats=stats,
        transactions=transactions,
        categories=categories,
    )


@app.route("/expenses/add")
def add_expense():
    return "Add expense — coming in Step 7"


@app.route("/expenses/<int:id>/edit")
def edit_expense(id):
    return "Edit expense — coming in Step 8"


@app.route("/expenses/<int:id>/delete")
def delete_expense(id):
    return "Delete expense — coming in Step 9"


if __name__ == "__main__":
    app.run(debug=True, port=5001)
