from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

# Declarative base for the SQLAlchemy ORM
Base = SQLAlchemy()


# EACH CLASS BELOW IS MAPPED TO A TABLE IN THE DATABASE

class Page(Base.Model):
    url = Base.Column(Base.String(100), primary_key=True)
    avgActiveRatio = Base.Column(Base.Float(precision='3,2'))  # averaged active ratio avg of all website visits
    avgFocusRatio = Base.Column(Base.Float(precision='3,2'))  # averaged focus ratio avg of all website visits
    avgVisitTime = Base.Column(Base.Float(precision='3,2'))  # averaged visit time avg of all website visits
    abandonmentRate = Base.Column(Base.Float(precision='3,2'))
    visits = Base.relationship('PageVisit', backref="page",
                               lazy="dynamic")  # one to many relationship with website visits


class User(UserMixin, Base.Model):
    id = Base.Column(Base.Integer, primary_key=True, autoincrement=True)
    username = Base.Column(Base.String(20), unique=True)
    password = Base.Column(Base.String(20))


'''backref is a simple way to also declare a new property on the PageVisit and Keywords class.
You can then use a_keyword.page to get to the page for that keyword'''


class PageVisit(Base.Model):
    visitID = Base.Column(Base.Integer, primary_key=True, autoincrement=True)
    url = Base.Column(Base.String(100), Base.ForeignKey('page.url'))
    activeRatio = Base.Column(Base.Float)
    focusRatio = Base.Column(Base.Float)
    visitTime = Base.Column(Base.Float)
    abandonment = Base.Column(Base.String(6))


class PageKeyword(Base.Model):
    keyword = Base.Column(Base.String, primary_key=True)
    page_url = Base.Column(Base.Integer, Base.ForeignKey("page.url"), primary_key=True)
    keywordSearches = Base.Column(Base.Integer)

class Section(Base.Model):
    name = Base.Column(Base.String(100), primary_key=True)
    url = Base.Column(Base.String(100), Base.ForeignKey('page.url'))
    avgActiveRatio = Base.Column(Base.Float(precision='3,2'))  # averaged active ratio avg of all website visits
    avgClockTime = Base.Column(Base.Float(precision='3,2'))
    focusRatio = Base.Column(Base.Float(precision='3,2'))
    visits = Base.relationship('SectionVisit', backref="section",
                               lazy="dynamic")  # one to many relationship with section visits

class SectionVisit(Base.Model):
    visitID = Base.Column(Base.Integer, primary_key=True, autoincrement=True)
    name = Base.Column(Base.Integer, Base.ForeignKey('section.name'))
    url = Base.Column(Base.String(100))
    activeRatio = Base.Column(Base.Float)
    clockTime = Base.Column(Base.Float)
