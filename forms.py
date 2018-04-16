#forms.py

from wtforms import Form, StringField	#Must do pip install WTForms to work

class keywordSearch(Form):
	
	search = StringField('Enter keyword:', '')
	
