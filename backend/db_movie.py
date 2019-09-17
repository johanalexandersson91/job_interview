from google.appengine.ext import ndb

class Movie(ndb.Model):
	title = ndb.StringProperty()
	data = ndb.StringProperty()
	omdb_id = ndb.StringProperty()