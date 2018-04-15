from flask_sqlalchemy import SQLAlchemy
from database.schema import *
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
        if (Page.query.get(url) == None):
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

    def get_page(self, url):
        return self.base.session.query(Page).get(url)


    # -------------------- WebpageVisits --------------------
    def insert_webpage_visit(self, url, activeRatio, focusRatio):
        # Insert the web page visit
        self.base.session.add(WebsiteVisits(
            focusRatio=focusRatio,
            activeRatio=activeRatio,
            url=url))

        # Update average focus/active ratio everytime a new visti
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

    def get_webpage_visits(self, url):
        return self.base.session.query(WebsiteVisits).filter_by(url=url).all()


    # -------------------- PageKeyword ---------------------
    def insert_keywords(self, url, keywords):
        for kw in keywords:
            if len(PageKeyword.query.filter_by(keyword=kw, page_url=url).all()) == 0: 
                self.base.session.add(PageKeyword(keyword=kw, 
                                                  page_url=url))
        self.base.session.commit()

    # Returns a list of pages that a keyword is found on
    def get_pages_from_kw(self, kw):
        pages = self.base.session.query(PageKeyword).filter_by(keyword=kw).all()
        return [page.page_url for page in pages]
