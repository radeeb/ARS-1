from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_declarative import Base, Page, Ad_Location_Visit, Page_Keyword

class Database:
	def __init__(self):
		self.engine = create_engine('sqlite:///database.db')
		self.DBSession = sessionmaker(bind=self.engine)
		self.session = self.DBSession()

	# CALL THIS METHOD WHENEVER DONE USING DATABASE
	def close(self):
		self.session.close()


	# -------------------- Page --------------------------------
	def insert_page(self, values):
		row = Page(id=values[0], url=values[1])
		self.session.add(row)
		self.session.commit()

	def search_page(self, id):
		return self.session.query(Page).get(id)

	# def delete_page(self, id):
	# 	self.session.delete(self.search_page(id))
	# 	self.session.commit()


	# -------------------- Ad_Location_Visit --------------------
	def insert_ad_location_visit(self, values):
		row = Ad_Location_Visit(
			id=values[0],
			page_location=values[1],
			focus_ratio=values[2],
			active_ratio=values[3],
			total_spent=values[4],
			page_id=values[5],
			created_at=values[6])
		self.session.add(row)
		self.session.commit()

	def search_ad_location_visit(self, id):
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
		return self.session.query(Page_Keyword).filter_by(keyword=keyword).all()
