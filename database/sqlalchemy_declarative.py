'''from sqlalchemy import create_engine, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Table, Column, ForeignKey, Integer, String, Float, DateTime
from sqlalchemy.orm import relationship'''

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.orderinglist import ordering_list
import json
Base = SQLAlchemy()

#Base = declarative_base()

### EACH CLASS BELOW IS MAPPED TO A TABLE IN THE DATABASE
class Page(database.Model):
	url = database.Column(database.String(100), primary_key=True, unique=True)
	rank = database.Column(database.Integer)
	avgActiveRatio = database.Column(database.Float)
	avgFocusRatio = database.Column(database.Float)
	keywords = database.Column(database.Text)
	locations = database.Column(database.Text)
	websiteVisits = database.relationship('WebsiteVisits')

class WebsiteVisits(database.Model):
	url = database.Column(database.String(100), database.ForeignKey('page.url'), primary_key=True,)
	keywords = database.Column(database.Text)
	activeRatio = database.Column(database.Float)
	focusRatio = database.Column(database.Float)

'''class Page(Base):
	__tablename__ = "page"
	# Define columns for the table "page"
    # Each column is also a normal Python instance variable
	#id = Column(Integer, primary_key=True, nullable=False)
    #owner
	url = Column(String, primary_key=True, nullable=False)
	rank = Column(Integer)
	keywords = Column(String) #can be updated from child keywords
	locations = Column(String)
	avgActiveRatio = Column(Float)
	avgFocusRatio = Column(Float)
	visits = relationship('WebsiteVisits') #one to many relationship

class WebsiteVisits(Base):
	__tablename__ = "WebsiteVisits"
	url = Column(String, ForeignKey('page.url'), primary_key=True)
	activeRatio = Column(Float)
	focusRatio = Column(Float)
	keywords = Column(String) #keywords of every visit


class Ad_Location_Visit(Base):
	__tablename__ = "ad_location_visit"
	id = Column(Integer, primary_key=True, nullable=False)
	page_location = Column(String)
	focus_ratio = Column(Float)
	active_ratio = Column(Float)
	total_spent = Column(Float)
	page_id = Column(Integer, ForeignKey("page.id"))
	created_at = Column(DateTime, default=func.now())



class Page_Keyword(Base):
	__tablename__ = "page_keyword"

	keyword = Column(String, primary_key=True)
	page_id = Column(Integer, ForeignKey("page.id"), primary_key=True)
	value = Column(Float)'''

# Create an engine that stores data in the local directory's
# "database.db" file.
#engine = create_engine('sqlite:///database.db')

# Create all tables in the engine. This is equivalent to "Create Table"
# statements in raw SQL. This only needs to be run once.
#Base.metadata.create_all(engine)

class Database:
	def __init__(self):
		self.engine = create_engine('sqlite:///database.db')
		self.DBSession = sessionmaker(bind=self.engine)
		self.session = self.DBSession()

	# CALL THIS METHOD WHENEVER DONE USING DATABASE
	def close(self):
		self.session.close()

	# -------------------- Page --------------------------------
	def insert_page(self,url,keywords, locations): #location is a list of possible locations
		#owner of the website uses this
		ar = 50.0
		fr = 50.0
		rank = 1
		row = Page(url= url, rank = rank, keywords = json.dumps(keywords), locations = json.dumps(locations), avgActiveRatio = ar, avgFocusRatio = fr)
		#self.session.add(row)
		#self.session.commit()

	def search_page(self, id):
		return self.session.query(Page).get(id)


	# -------------------- Ad_Location_Visit --------------------
	def insert_webpage_visit(self, url, keywords, activeRatio, focusRatio):
		row = WebsiteVisits(
			focusRatio= focusRatio,
			activeRatio=activeRatio,
			url= url,
			keywords= json.dumps(keywords))
		self.session.add(row)
		self.session.commit()
