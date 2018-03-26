from flask_sqlalchemy import SQLAlchemy
from database.schema import Page, WebsiteVisits
import json


# api to interact with database
class Database:
    def __init__(self, base):
        self.base = base
        self.visits = 0  # keep track of visit number

    # CALL THIS METHOD WHENEVER DONE USING DATABASE
    def close(self):
        self.base.session.remove()

    # -------------------- Page --------------------------------
    def insert_page(self, url, locations):  # location is a list of possible ad locations
        # owner of the website uses this
        self.base.session.add(Page(
            url=url,
            rank=1,
            locations=json.dumps(locations),
            avgActiveRatio=0,  # default
            avgFocusRatio=0  # default
        ))
        self.base.session.commit()

    def search_page(self, url):
        return self.session.query(Page).get(url)

    # -------------------- Ad_Location_Visit --------------------
    def insert_webpage_visit(self, url, keywords, activeRatio, focusRatio):
        self.base.session.add(WebsiteVisits(
            visitID=self.visits,
            focusRatio=focusRatio,
            activeRatio=activeRatio,
            url=url,
            keywords=json.dumps(keywords)))  # returns a string representation of a json object
        self.base.session.commit()
