#--------------------------------Imports---------------------------------------
from flask import Flask, render_template
from database.flask_sqlAlchemy import *
import requests, os
#------------------------------------------------------------------------------

#--------------------------------Application setup-----------------------------
app = Flask(__name__)
localPort = 8080
app.config.from_object(__name__)
app.config.update(dict(
	SQLALCHEMY_DATABASE_URI='sqlite:///'+os.path.join(app.root_path + "/database", "database.db"),
	SQLALCHEMY_TRACK_MODIFICATIONS=False,
	SECRET_KEY="a722c63db8ec8625af6cf71cb8c2d939"))

#setup the database

Base.init_app(app)
app.app_context().push()
Base.create_all()
DB = Database(Base)

#add a page for testing DELETE ME
print("DB setup")
#DB.insert_page("yahoo.com", ['sports', 'money'], [1,5,8])
#======================DELETE ME=========================
#------------------------------------------------------------------------------

#--------------------------------Web Interface---------------------------------
@app.route("/" , methods=["GET"])
def index():
	site = "index.html"
	return render_template(site)

@app.route("/visit", methods=["POST"])
def visit():
	response = "You visited an ARS website!"
	data = request.data
	print(data)
	#push the visit to the database
	return response

@app.route("/report", methods=["GET"])
def report():
	#get the yahoo site
	site = "report.html"
	return render_template(site)

#------------------------------------------------------------------------------

#--------------------------------Functions/Classes-----------------------------
#------------------------------------------------------------------------------

#--------------------------------Program Main----------------------------------
if(__name__ == "__main__"):
	app.run(host="0.0.0.0" , port= localPort)
#------------------------------------------------------------------------------

