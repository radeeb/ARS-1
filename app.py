# --------------------------------Imports---------------------------------------
from flask import Flask, render_template, request
from database.schema import *
from database.api import Database
import os, json
import modules.keywordFinder.keyword_finder as kwf
# ------------------------------------------------------------------------------


# --------------------------------Application setup-----------------------------
app = Flask(__name__)
localPort = 8080
app.config.from_object(__name__)
app.config.update(dict(
    SQLALCHEMY_DATABASE_URI='sqlite:///' + os.path.join(app.root_path + "/database", "database.db"),
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
    SECRET_KEY="a722c63db8ec8625af6cf71cb8c2d939"))

# setup the database
Base.init_app(app)  # bind the database instance to this application
app.app_context().push()  # useful when you have more than 1 flask app
Base.create_all()  # create all the tables
DB = Database(Base)

try:
    if (Page.query.first() == None):
        DB.insert_page("/news", [1, 5, 8])
except Exception as e:
    print(e)
# ------------------------------------------------------------------------------


# --------------------------------Web Interface---------------------------------
@app.route("/", methods=["GET"])
def index():
    site = "index.html"
    return render_template(site)


# route for our local news website
@app.route("/news", methods=["GET"])
def viewNews():
    site = "news.html"
    return render_template(site)


@app.route("/visit", methods=["POST"])
def visit():
    response = "You visited an ARS website!"
    # load the data then put in database
    data = json.loads(request.data)  # decoding JSON to dictionary
    DB.insert_webpage_visit(data["url"], data["activeRatio"], data["focusRatio"])
    print("Visit successfully recorded in database")
    return response


@app.route("/report", methods=["GET"])
def report():
    site = "report.html"
    return render_template(site)
# ------------------------------------------------------------------------------


# --------------------------------Functions/Classes-----------------------------
# keys = kwf.getKeys("www.ky3.com")
# print(keys)
# ------------------------------------------------------------------------------


# --------------------------------Program Main----------------------------------
if (__name__ == "__main__"):
    app.run(host="0.0.0.0", port=localPort)
# ------------------------------------------------------------------------------
