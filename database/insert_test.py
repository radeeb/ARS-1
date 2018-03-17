from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_declarative import Page, Base

engine = create_engine('sqlite:///database.db')
DBSession = sessionmaker(bind=engine)

# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()

# Create a few pages
google = Page(id=1234, url="www.google.com")
facebook = Page(id=532, url="www.facebook.com")
apple = Page(id=734213, url="www.apple.com")

# Add them to the session and commit
session.add_all([google, facebook, apple])
session.commit()