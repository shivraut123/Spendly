import sqlite3 # You'll need this for catching duplicate emails later
from flask import Flask, render_template, request, flash, redirect, url_for
from database.db import get_db, init_db, seed_db, create_user # Assuming create_user is added

app = Flask(__name__)
app.secret_key = "super-secret-development-key" # Required for flash() to work

with app.app_context():
    init_db()
    seed_db()

# ------------------------------------------------------------------ #
# Routes                                                              #
# ------------------------------------------------------------------ #

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
    return "Logout — coming in Step 3"


@app.route("/profile")
def profile():
    return "Profile page — coming in Step 4"


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
