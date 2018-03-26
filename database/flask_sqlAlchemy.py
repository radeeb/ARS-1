from flask_sqlalchemy import SQLAlchemy
import json

Base = SQLAlchemy()

#EACH CLASS BELOW IS MAPPED TO A TABLE IN THE DATABASE
class Page(Base.Model):
    url = Base.Column(Base.String(100), primary_key=True, unique=True)
    rank = Base.Column(Base.Integer)
    avgActiveRatio = Base.Column(Base.Float) #accumulated active ratio avg of all website visits
    avgFocusRatio = Base.Column(Base.Float)   #accumulated focus ratio avg of all website visits
    keywords = Base.Column(Base.Text)
    locations = Base.Column(Base.Text)
    visits = Base.relationship('WebsiteVisits', backref="page", lazy="dynamic")


class WebsiteVisits(Base.Model):
    visitID = Base.Column(Base.Integer, primary_key=True)
    url = Base.Column(Base.String(100), Base.ForeignKey('page.url'))
    keywords = Base.Column(Base.Text)
    activeRatio = Base.Column(Base.Float)
    focusRatio = Base.Column(Base.Float)

class Database:
    def __init__(self, base):
        self.base = base
        self.visits = 0


    # CALL THIS METHOD WHENEVER DONE USING DATABASE
    def close(self):
        self.base.session.remove()

    # -------------------- Page --------------------------------
    def insert_page(self, url, keywords, locations):  # location is a list of possible locations
        # owner of the website uses this
        self.base.session.add(Page(
            url=url,
            rank=1,
            keywords=json.dumps(keywords),
            locations=json.dumps(locations),
            avgActiveRatio=50,
            avgFocusRatio=50
        ))
        self.base.session.commit()

    def search_page(self, id):
        return self.session.query(Page).get(id)

    # -------------------- Ad_Location_Visit --------------------
    def insert_webpage_visit(self, url, keywords, activeRatio, focusRatio):
        self.visits+=1 #increment visit number
        self.base.session.add(WebsiteVisits(
            visitID=self.visits,
            focusRatio=focusRatio,
            activeRatio=activeRatio,
            url=url,
            keywords=json.dumps(keywords)))
        self.base.session.commit()

