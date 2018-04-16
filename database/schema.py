from flask_sqlalchemy import SQLAlchemy

# Declarative base for the SQLAlchemy ORM
Base = SQLAlchemy()


# EACH CLASS BELOW IS MAPPED TO A TABLE IN THE DATABASE

class Page(Base.Model):
    url = Base.Column(Base.String(100), primary_key=True)
    rank = Base.Column(Base.Integer)
    avgActiveRatio = Base.Column(Base.Float(precision='3,2'))  # averaged active ratio avg of all website visits
    avgFocusRatio = Base.Column(Base.Float(precision='3,2'))  # averaged focus ratio avg of all website visits
    avgVisitTime = Base.Column(Base.Float(precision='3,2')) # averaged visit time avg of all website visits
    locations = Base.Column(Base.Text)  # list of ad locations
    visits = Base.relationship('WebsiteVisits', backref="page",
                               lazy="dynamic")  # one to many relationship with website visits


'''backref is a simple way to also declare a new property on the WebsiteVisits and Keywords class.
You can then use a_keyword.page to get to the page for that keyword'''


class WebsiteVisits(Base.Model):
    visitID = Base.Column(Base.Integer, primary_key=True, autoincrement=True)
    url = Base.Column(Base.String(100), Base.ForeignKey('page.url'))
    activeRatio = Base.Column(Base.Float)
    focusRatio = Base.Column(Base.Float)
    visitTime = Base.Column(Base.Float)


class PageKeyword(Base.Model):
    keyword = Base.Column(Base.String, primary_key=True)
    page_url = Base.Column(Base.Integer, Base.ForeignKey("page.url"), primary_key=True)
