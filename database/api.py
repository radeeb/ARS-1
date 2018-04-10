from flask_sqlalchemy import SQLAlchemy
from database.schema import Page, WebsiteVisits
import json


# api to interact with database
class Database:
    def __init__(self, base):
        self.base = base

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

    def get_all_pages(self):
        return self.base.session.query(Page).all()


    # -------------------- WebpageVisits --------------------
    def insert_webpage_visit(self, url, activeRatio, focusRatio):
        # Insert the web page visit
        self.base.session.add(WebsiteVisits(
            focusRatio=focusRatio,
            activeRatio=activeRatio,
            url=url))

        # Update average focus/active ratio for this Page
        visits = WebsiteVisits.query.filter_by(url=url).all()
        activeRatios = 0
        focusRatios = 0
        for visit in visits:
            activeRatios += visit.activeRatio
            focusRatios += visit.focusRatio
        page = Page.query.get(url)
        page.avgActiveRatio = activeRatios / len(visits)
        page.avgFocusRatio = focusRatios / len(visits)

        self.base.session.commit()

    def update_keywords(self, url, keywords):
        # Insert the web page visit
        page = Page.query.get(url)
        page.keywords = keywords
        self.base.session.commit()