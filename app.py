# --------------------------------Imports---------------------------------------
import json
import os

from flask import Flask, flash, redirect, render_template, request, url_for
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
# from forms import keywordSearch
from wtforms import Form, StringField, PasswordField
from wtforms.validators import InputRequired
from flask_login import LoginManager, login_user, login_required, logout_user

import modules.keywordFinder.keyword_finder as kwf
from database.api import Database
from database.schema import Base

# ------------------------------------------------------------------------------


# --------------------------------Application setup-----------------------------
# BASE PRICES FOR THE ARS
MIN_PRICE = 1
MAX_PRICE = 200

app = Flask(__name__)
Bootstrap(app)

localPort = 8080
app.config.from_object(__name__)
app.config.update(dict(
    SQLALCHEMY_DATABASE_URI='sqlite:///' + os.path.join(app.root_path + "/database", "database.db"),
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
    SECRET_KEY="a722c63db8ec8625af6cf71cb8c2d939"))

# Setup the database
Base.init_app(app)  # bind the database instance to this application
app.app_context().push()  # useful when you have more than 1 flask app
Base.create_all()  # create all the tables
DB = Database(Base)
DB.insert_default()

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


# ------------------------------------------------------------------------------


# --------------------------------Web Interface---------------------------------
@login_manager.user_loader
def load_user(user_id):
    username = DB.get_id(user_id)
    return username


@app.route("/", methods=["GET"])
def index():
    site = "index.html"
    return render_template(site)


# Route for our local news website
@app.route("/news", methods=["GET"])
def viewNews():
    site = "news.html"
    return render_template(site)


# Route for our local world news
@app.route("/worldNews", methods=["GET"])
def viewWorldNews():
    site = "worldNews.html"
    return render_template(site)


# Route for our local sports website
@app.route("/sports", methods=["GET"])
def viewSports():
    site = "sports.html"
    return render_template(site)


@app.route("/visit", methods=["POST"])
def visit():
    response = "You visited an ARS website!"
    # Decode JSON into dictionary
    data = json.loads(request.data)
    # Store the page 
    DB.insert_page(data["url"])
    # Store the page visit
    DB.insert_page_visit(data["url"], data["activeRatio"], data["focusRatio"], data["visitTime"])
    # Store the keywords
    store_keywords(data["url"])
    print("Visit successfully recorded in database")
    return response


# Builds a report from the pages in the database
@app.route("/adminReport", methods=["GET"])
@login_required
def adminReport():
    pages = DB.get_all_pages()
    reports = [dict(URL=page.url,
                    ActiveRatio=format(page.avgActiveRatio, ".2f"),
                    FocusRatio=format(page.avgFocusRatio, ".2f"),
                    visitTime=format(page.avgVisitTime, ".2f"),
                    numberOfVisits=len(DB.get_page_visits(page.url))) for page in pages]
    return render_template("adminReport.html", Reports=reports)


# Builds a report from the pages in the database
@app.route("/customerReport", methods=["GET"])
def customerReport():
    pages = DB.get_all_pages()
    reports = [dict(URL=page.url,
                    Price=ad_price(page.url)) for page in pages]
    return render_template("customerReport.html", Reports=reports)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    site = "login.html"
    if form.validate_on_submit():
        username = form.username.data
        user = DB.get_user(username)
        if user:
            if user.password == form.password.data:
                login_user(user)
                return redirect(url_for('adminReport'))

        flash("Username/password invalid")
        return redirect('/login')
        # return '<h1>' + form.username.data + ' ' + form.password.data + '</h1>'
    return render_template(site, form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route("/search", methods=['GET', 'POST'])
def search():
    search = keywordSearch(request.form)
    if request.method == 'POST':
        return search_results(search)
    return render_template("search.html", form=search)


@app.route("/results")
def search_results(search):
    search_string = search.data["search"]
    if search.data["search"] == "":
        flash("Please enter a valid keyword")
        return redirect('/search')

    # Sends entered data to search function in api.py and either returns a report with returned values or flashes no
    # results found.
    else:
        page_urls = DB.get_pages_from_kw(search_string)
        pages = [DB.get_page(page) for page in page_urls]
        found = [dict(URL=page.url, Price=ad_price(page.url)) for page in pages]
        if len(found) == 0:
            flash("No results found!")
            return redirect("/search")
    return render_template("results.html", table=found)


# ------------------------------------------------------------------------------


# --------------------------------Functions/Classes-----------------------------
# This class is used for login form
class LoginForm(FlaskForm):
    username = StringField("username", validators=[InputRequired()])
    password = PasswordField("password", validators=[InputRequired()])


# This class is used for keyword search form
class keywordSearch(Form):
    search = StringField('Enter keyword:', '')


# Stores the keywords found on a given url in the DB
def store_keywords(url):
    keywords = kwf.getKeys("http://localhost:8080" + url)
    DB.insert_keywords(url, keywords)


# Engagement index for a specific page
def engagement_index(url):
    num_visits = len(DB.get_page_visits(url))
    page = DB.get_page(url)
    eng_index = (page.avgVisitTime / 60) * num_visits * (page.avgActiveRatio / 100) * (page.avgFocusRatio / 100)
    return eng_index


# Price based on engagement index
def ad_price(url):
    EI = engagement_index(url)
    price = MAX_PRICE * EI / 100
    price = round(price, 2)
    if price > MAX_PRICE:
        price = MAX_PRICE
    elif price < MIN_PRICE:
        price = MIN_PRICE
    price = format(price, '.2f')
    return price


# ------------------------------------------------------------------------------


# --------------------------------Program Main----------------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=localPort, threaded=True)
# ------------------------------------------------------------------------------
