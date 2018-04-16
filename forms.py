#forms.py

from wtforms import Form, StringField

class keywordSearch(Form):
	
	search = StringField('Enter URL:', '')
	