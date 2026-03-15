import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required

# Configure application
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///movies.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    highlighted = db.execute("SELECT * FROM movies ORDER BY year DESC LIMIT 8")
    total_movies = db.execute("SELECT COUNT(*) FROM movies")[0]["COUNT(*)"]
    watchlist_count = db.execute(
        "SELECT COUNT(*) FROM watchlist WHERE user_id = ?", session["user_id"])[0]["COUNT(*)"]

    return render_template("index.html", highlighted=highlighted, total_movies=total_movies, watchlist_count=watchlist_count)


@app.route("/add_to_watchlist", methods=["POST"])
@login_required
def add_to_watchlist():
    movie_id = request.form.get("movie_id")
    if not movie_id:
        return apology("Invalid movie", 400)

    # Add or ignore if already there (rating stays NULL until rated)
    db.execute("INSERT OR IGNORE INTO watchlist (user_id, movie_id) VALUES (?, ?)",
               session["user_id"], movie_id)
    flash("Added to your watchlist!", "success")

    # Redirect back to where they came from (or default to brothers-list)
    return redirect(request.referrer or "/brothers-list")


@app.route("/brothers-list")
@login_required
def brothers_list():
    movies = db.execute("SELECT * FROM movies ORDER BY year DESC, title ASC")
    return render_template("brothers_list.html", movies=movies)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/rate", methods=["POST"])
@login_required
def rate():
    movie_id = request.form.get("movie_id")
    rating = request.form.get("rating")

    if not movie_id:
        return apology("Invalid movie", 400)

    if rating:
        rating = int(rating)
        db.execute("UPDATE watchlist SET rating = ? WHERE user_id = ? AND movie_id = ?",
                   rating, session["user_id"], movie_id)
    else:
        # Clear rating if "Rate 1-10" selected
        db.execute("UPDATE watchlist SET rating = NULL WHERE user_id = ? AND movie_id = ?",
                   session["user_id"], movie_id)
    flash("Rating saved!", "success")

    return redirect("/watchlist")


@app.route("/recent-activity")
@login_required
def recent_activity():
    recent = db.execute("""
        SELECT
            w.added_at,
            u.username,
            m.title,
            m.year,
            m.poster_path,
            m.genres
        FROM watchlist w
        JOIN users u ON w.user_id = u.id
        JOIN movies m ON w.movie_id = m.id
        ORDER BY w.added_at DESC
        LIMIT 60
    """)

    return render_template("recent_activity.html", recent=recent)


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        if not username:
            return apology("must provide username", 400)

        if not password:
            return apology("must provide password", 400)

        if password != confirmation:
            return apology("passwords must match", 400)

        hash = generate_password_hash(password)

        try:
            result = db.execute(
                "INSERT INTO users (username, hash) VALUES(?, ?)",
                username, hash
            )
            session["user_id"] = result
        except:
            return apology("username already exists", 400)

        flash("Registered!")
        return redirect("/")

    else:
        return render_template("register.html")


@app.route("/remove_from_watchlist", methods=["POST"])
@login_required
def remove_from_watchlist():
    movie_id = request.form.get("movie_id")
    if not movie_id:
        flash("Invalid movie.", "danger")
        return redirect("/watchlist")

    db.execute("DELETE FROM watchlist WHERE user_id = ? AND movie_id = ?",
               session["user_id"], movie_id)
    flash("Movie removed from watchlist.", "danger")

    return redirect("/watchlist")


@app.route("/search")
@login_required
def search():
    genre = request.args.get("genre")
    decade = request.args.get("decade")
    director = request.args.get("director")

    query = "SELECT * FROM movies WHERE 1=1"
    params = []

    if genre:
        query += " AND genres LIKE ?"
        params.append(f"%{genre}%")

    if decade:
        if decade == "pre1930":
            query += " AND year < 1930"
        elif decade == "2020":
            query += " AND year >= 2020"
        else:
            start_year = int(decade)
            query += " AND year >= ? AND year < ?"
            params.extend([start_year, start_year + 10])

    if director:
        query += " AND director LIKE ?"
        params.append(f"%{director}%")

    query += " ORDER BY year DESC, title ASC"

    movies = db.execute(query, *params)

    return render_template("search.html", movies=movies)


@app.route("/watchlist")
@login_required
def watchlist():
    # Top 10 rated
    top_rated = db.execute("""
        SELECT m.id, m.title, m.year, m.poster_path, m.genres, w.rating
        FROM watchlist w
        JOIN movies m ON w.movie_id = m.id
        WHERE w.user_id = ? AND w.rating IS NOT NULL
        ORDER BY w.rating DESC, m.title ASC
        LIMIT 10
    """, session["user_id"])

    # All rated movies 
    rated_movies = db.execute("""
        SELECT m.id, m.title, m.year, m.poster_path, m.genres, w.rating
        FROM watchlist w
        JOIN movies m ON w.movie_id = m.id
        WHERE w.user_id = ? AND w.rating IS NOT NULL
        ORDER BY w.rating DESC, m.title ASC
    """, session["user_id"])

    # Unrated movies
    unrated_movies = db.execute("""
        SELECT m.id, m.title, m.year, m.poster_path, m.genres, w.rating
        FROM watchlist w
        JOIN movies m ON w.movie_id = m.id
        WHERE w.user_id = ? AND w.rating IS NULL
        ORDER BY m.title ASC
    """, session["user_id"])

    return render_template("watchlist.html",
                           top_rated=top_rated,
                           rated_movies=rated_movies,
                           unrated_movies=unrated_movies)


def errorhandler(e):
    """Handle error"""
    return apology(e.name, e.code)


for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
