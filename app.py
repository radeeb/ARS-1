# --------------------------------Imports---------------------------------------
import json
import os

from flask import Flask, render_template, request

import modules.keywordFinder.keyword_finder as kwf
from database.api import Database
from database.schema import Base

# ------------------------------------------------------------------------------


# --------------------------------Application setup-----------------------------
app = Flask(__name__)
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


# ------------------------------------------------------------------------------


# --------------------------------Web Interface---------------------------------
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
    DB.insert_page(data["url"], [1, 5, 8])
    # Store the page visit
    DB.insert_page_visit(data["url"], data["activeRatio"], data["focusRatio"], data["visitTime"])
    # Store the keywords
    store_keywords("http://localhost:8080" + data["url"])
    print("Visit successfully recorded in database")
    return response


# Builds a report from the pages in the database
@app.route("/adminReport", methods=["GET"])
def adminReport():
    pages = DB.get_all_pages()
    reports = [dict(URL=page.url,
                    Rank=page.rank,
                    ActiveRatio=page.avgActiveRatio,
                    FocusRatio=page.avgFocusRatio,
                    visitTime=page.avgVisitTime,
                    numberOfVisits=len(DB.get_page_visits(page.url)),
                    Locations=page.locations) for page in pages]
    return render_template("adminReport.html", Reports=reports)


# Builds a report from the pages in the database
@app.route("/customerReport", methods=["GET"])
def customerReport():
    pages = DB.get_all_pages()
    reports = [dict(URL=page.url,
                    Price=ad_price(page.url, 200, 1),
                    Locations=page.locations) for page in pages]
    return render_template("customerReport.html", Reports=reports)


# ------------------------------------------------------------------------------


# --------------------------------Functions/Classes-----------------------------
# Stores the keywords found on a given url in the DB
def store_keywords(url):
    keywords = kwf.getKeys(url)
    DB.insert_keywords(url, keywords)


# Engagement index for a specific page
def engagement_index(url):
    num_visits = len(DB.get_page_visits(url))
    page = DB.get_page(url)
    eng_index = (page.avgVisitTime / 60) * num_visits * (page.avgActiveRatio / 100) * (page.avgFocusRatio / 100)
    return eng_index


# Price based on engagement index
def ad_price(url, max_price, min_price):
    EI = engagement_index(url)
    price = max_price * EI / 100
    price = round(price, 2)
    if price > max_price:
        price = max_price
    elif price < min_price:
        price = min_price
    price = format(price, '.2f')
    return price

# ------------------------------------------------------------------------------


# --------------------------------Program Main----------------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=localPort, threaded=True)
# ------------------------------------------------------------------------------
