from sqlalchemy_declarative import Page, Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///database.db')
Base.metadata.bind = engine
DBSession = sessionmaker()
DBSession.bind = engine
session = DBSession()

# DIFFERENT QUERY EXAMPLES
all_pages = session.query(Page).all()		# all tuples in table Page
first_page = session.query(Page).first()	# first tuple in Page
google = session.query(Page).get(1234)		# tuple in table Page with primary key "1234"

print(google.url)
