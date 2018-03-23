from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_declarative import *
import json

class Database:
	def __init__(self):
		self.engine = create_engine('sqlite:///database.db')
		self.DBSession = sessionmaker(bind=self.engine)
		self.session = self.DBSession()

	# CALL THIS METHOD WHENEVER DONE USING DATABASE
	def close(self):
		self.session.close()


	# -------------------- Page --------------------------------
	def insert_page(self,url,keywords, locations): #location is a list of possible locations
		#owner of the website uses this
		ar = 50
		fr = 50
		rank = 1
		row = Page(url= url, rank = rank, keywords = json.dumps(keywords), locations = json.dumps(locations), avgActiveRatio = ar, avgFocusRatio = fr)
		self.session.add(row)
		self.session.commit()

	def search_page(self, id):
		return self.session.query(Page).get(id)

	# def delete_page(self, id):
	# 	self.session.delete(self.search_page(id))
	# 	self.session.commit()


	# -------------------- Ad_Location_Visit --------------------
	'''def insert_ad_location_visit(self, values):
		row = Ad_Location_Visit(
			id=values[0],
			page_location=values[1],
			focus_ratio=values[2],
			active_ratio=values[3],
			total_spent=values[4],
			page_id=values[5],
			created_at=values[6])
		self.session.add(row)
		self.session.commit()'''

	def insert_webpage_visit(self, url, keywords, activeRatio, focusRatio):
		row = WebsiteVisits(
			focusRatio= focusRatio,
			activeRatio=activeRatio,
			visitUrl= url,
			keywords= json.dumps(keywords))
		self.session.add(row)
		self.session.commit()

db = Database()

print("Database Created")
db.insert_page("yahoo.com", ['sports', 'money'], [1,5,8])
print("Page Created")
db.insert_webpage_visit("yahoo.com", ['sports', 'money'], 99, 100)
db.session.query(WebsiteVisits)
	'''def search_ad_location_visit(self, id):
		return self.session.query(Ad_Location_Visit).get(id)

	# def delete_ad_location_visit(self, id):
	# 	self.session.delete(self.search_ad_location_visit(id))
	# 	self.session.commit()


	# -------------------- Page_Keyword -------------------------
	def insert_page_keyword(self, values):
		row = Page_Keyword(keyword=values[0], page_id=values[1])
		self.session.add(row)
		self.session.commit()

	def search_page_keyword(self, id: int):
		return self.session.query(Page_Keyword).filter_by(page_id=id).all()

	def search_page_keyword(self, keyword: str):
		return self.session.query(Page_Keyword).filter_by(keyword=keyword).all()'''
