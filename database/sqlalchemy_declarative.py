from sqlalchemy import create_engine, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, ForeignKey, Integer, String, Float, DateTime

Base = declarative_base()

### EACH CLASS BELOW IS MAPPED TO A TABLE IN THE DATABASE

class Page(Base):
	__tablename__ = "page"
	# Define columns for the table "page"
    # Each column is also a normal Python instance variable
	id = Column(Integer, primary_key=True, nullable=False)
	url = Column(String)

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

# Create an engine that stores data in the local directory's
# "database.db" file.
engine = create_engine('sqlite:///database.db')

# Create all tables in the engine. This is equivalent to "Create Table"
# statements in raw SQL. This only needs to be run once.
Base.metadata.create_all(engine)
