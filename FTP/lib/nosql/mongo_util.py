from FTP.lib.nosql.base import Base

class MongoUtil(object):
	"""docstring for MongoUtil"""
	def __init__(self, project_name, collection_name):
		self.conn = Base.client[project_name][collection_name]

	def save(self, doc_or_doc_lst):
		return self.conn.insert(doc_or_doc_lst)

	def get_one(self, kwargs):
		return self.conn.find_one(kwargs)

	def get_all(self, kwargs):
		return list(self.conn.find(kwargs))

	def update(self, kwargs, docunment):
		self.conn.update(kwargs, document)

	def delete(self, kwargs):
		self.conn.remove(kwargs)