from database.schema import *


class Database:
    def __init__(self, base):
        self.base = base

    # CALL THIS METHOD WHENEVER DONE USING DATABASE
    def close(self):
        self.base.session.remove()

    # -------------------- Page --------------------------------
    def insert_page(self, url):
        if Page.query.get(url) is None:
            # owner of the website uses this
            self.base.session.add(Page(
                url=url,
                avgActiveRatio=0,
                avgFocusRatio=0,
                avgVisitTime=0
            ))
            self.base.session.commit()

    def insert_default(self):
        if User.query.filter_by(username="admin").first() is None:
            admin = User(username="admin", password="password")
            self.base.session.add(admin)
            self.base.session.commit()

    def get_all_pages(self):
        return self.base.session.query(Page).all()

    def get_page(self, url):
        return self.base.session.query(Page).get(url)

    def get_page_popularity_by_keyword(self, url):
        '''# returns the total popularity of the page according to keyword search history'''
        keywords = self.base.session.query(PageKeyword).filter_by(page_url=url).all()
        hits = 0

        for kw in keywords:
            if (kw.keywordSearches is None): #to make sure no null values existe before addition
                kw.keywordSearches = 0
            hits = hits + kw.keywordSearches

        self.base.session.commit()
        return hits

    # -------------------- User ---------------------------------

    def get_user(self, user):
        user_name = self.base.session.query(User).filter_by(username=user).first()
        return user_name

    def get_id(self, id_user):
        user_name = self.base.session.query(User).get(int(id_user))
        return user_name

    # -------------------- PageVisit -----------------------------
    def insert_page_visit(self, url, activeRatio, focusRatio, visitTime):
        # Insert the web page visit
        self.base.session.add(PageVisit(
            focusRatio=focusRatio,
            activeRatio=activeRatio,
            visitTime=visitTime,
            url=url))

        # Update average focus/active ratio every time a new visit
        visits = PageVisit.query.filter_by(url=url).all()
        activeRatios = 0
        focusRatios = 0
        visitTimes = 0
        for visit in visits:
            if visit.activeRatio is not None and visit.focusRatio is not None:
                activeRatios += visit.activeRatio
                focusRatios += visit.focusRatio
                visitTimes += visit.visitTime
        page = Page.query.get(url)
        page.avgActiveRatio = activeRatios / len(visits)
        page.avgFocusRatio = focusRatios / len(visits)
        page.avgVisitTime = visitTimes / len(visits)

        self.base.session.commit()

    def get_page_visits(self, url):
        return self.base.session.query(PageVisit).filter_by(url=url).all()

    # -------------------- PageKeyword ---------------------
    def insert_keywords(self, url, keywords):
        for kw in keywords:
            if len(PageKeyword.query.filter_by(keyword=kw, page_url=url).all()) == 0:
                self.base.session.add(PageKeyword(keyword=kw,
                                                  page_url=url))
        self.base.session.commit()

    def update_search_history(self, search_string): #updates the number of times a keyword is searched
        keywords = self.base.session.query(PageKeyword).filter_by(keyword=search_string).all()
        for kw in keywords:
            if (kw.keywordSearches is None): #to make sure no null values exist before update
                kw.keywordSearches =0
            kw.keywordSearches += 1
        self.base.session.commit()

    '''def insert_keyword_sections(self, kw, url, sections):
        kw = self.base.session.query(PageKeyword).filter_by(keyword=kw, page_url= url).first()
        kw.sections = str(sections)

        self.base.session.commit()'''

    # Returns a list of pages that a keyword is found on
    def get_pages_from_kw(self, kw):
        pages = self.base.session.query(PageKeyword).filter_by(keyword=kw).all()
        return [page.page_url for page in pages]
