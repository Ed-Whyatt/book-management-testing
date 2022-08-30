from flask import flash, render_template, request, redirect, session, url_for
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
from moviemanager import app, db, mongo, client
from moviemanager.models import Category, Users


@app.route("/")
@app.route("/get_movies")
def get_movies():
    movies = mongo.db.movies.find()
    return render_template("movies.html", movies=movies)


@app.route("/add_movie")
def add_movie():
    return render_template("add_movie.html")


@app.route("/search", methods=["GET", "POST"])
def search():
    query = request.form.get("query")
    movies = client.search(query)
    return render_template("search_results.html", movies=movies)


@app.route("/select_movie/<movie_title>", methods=["GET", "POST"])
def select_movie(movie_title):
    if "user" not in session:
        flash("You need to be logged in to add a task")
        return redirect(url_for("get_movies"))

    movie = client.get(title=movie_title, fullplot=False, tomatoes=True)
    if request.method == "POST":
        task = {
            "category_id": request.form.get("category_id"),
            "title": movie.get("title"),
            "poster": movie.get("poster"),
            "director": movie.get("director"),
            "genre": movie.get("genre"),
            "actors": movie.get("actors"),
            "year": movie.get("year"),
            "type": movie.get("type"),
            "rated": movie.get("rated"),
            "imdb_rating": movie.get("imdb_rating"),
            "plot": movie.get("plot"),
            "created_by": session["user"]
        }
        mongo.db.movies.insert_one(task)
        flash("Movie Added")
        return redirect(url_for("get_movies"))

    categories = list(Category.query.order_by(Category.category_name).all())
    return render_template(
        "select_this_movie.html", categories=categories, movie=movie)


@app.route("/get_categories")
def get_categories():

    if "user" not in session or session["user"] != "admin":
        flash("You must be admin to manage categories!")
        return redirect(url_for("get_tasks"))
        
    categories = list(Category.query.order_by(Category.category_name).all())
    return render_template("categories.html", categories=categories)


@app.route("/add_category", methods=["GET", "POST"])
def add_category():

    if "user" not in session or session["user"] != "admin":
        flash("You must be admin to manage categories!")
        return redirect(url_for("get_tasks"))

    if request.method == "POST":
        category = Category(category_name=request.form.get("category_name"))
        db.session.add(category)
        db.session.commit()
        return redirect(url_for("get_categories"))
    return render_template("add_category.html")


@app.route("/edit_category/<int:category_id>", methods=["GET", "POST"])
def edit_category(category_id):
    if "user" not in session or session["user"] != "admin":
        flash("You must be admin to manage categories!")
        return redirect(url_for("get_tasks"))
    
    category = Category.query.get_or_404(category_id)
    if request.method == "POST":
        category.category_name = request.form.get("category_name")
        db.session.commit()
        return redirect(url_for("get_categories"))
    return render_template("edit_category.html", category=category)


@app.route("/delete_category/<int:category_id>")
def delete_category(category_id):
    if session["user"] != "admin":
        flash("You must be admin to manage categories!")
        return redirect(url_for("/get_tasks"))

    category = Category.query.get_or_404(category_id)
    db.session.delete(category)
    db.session.commit()
    mongo.db.tasks.delete_many({"category_id": str(category_id)})
    return redirect(url_for("get_categories"))


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # check if username already exists in db
        existing_user = Users.query.filter(Users.user_name == \
                                           request.form.get("username").lower()).all()
        
        if existing_user:
            flash("Username already exists")
            return redirect(url_for("register"))
        
        user = Users(
            user_name=request.form.get("username").lower(),
            password=generate_password_hash(request.form.get("password"))
        )
        
        db.session.add(user)
        db.session.commit()

        # put the new user into 'session' cookie
        session["user"] = request.form.get("username").lower()
        flash("Registration Successful!")
        return redirect(url_for("profile", username=session["user"]))

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # check if username exists in db
        existing_user = Users.query.filter(Users.user_name == \
                                           request.form.get("username").lower()).all()

        if existing_user:
            print(request.form.get("username"))
            # ensure hashed password matches user input
            if check_password_hash(
                    existing_user[0].password, request.form.get("password")):
                        session["user"] = request.form.get("username").lower()
                        flash("Welcome, {}".format(
                            request.form.get("username")))
                        return redirect(url_for(
                            "profile", username=session["user"]))
            else:
                # invalid password match
                flash("Incorrect Username and/or Password")
                return redirect(url_for("login"))

        else:
            # username doesn't exist
            flash("Incorrect Username and/or Password")
            return redirect(url_for("login"))

    return render_template("login.html")


@app.route("/profile/<username>", methods=["GET", "POST"])
def profile(username):
        
    if "user" in session:
        return render_template("profile.html", username=session["user"])

    return redirect(url_for("login"))


@app.route("/logout")
def logout():
    # remove user from session cookie
    flash("You have been logged out")
    session.pop("user")
    return redirect(url_for("login"))