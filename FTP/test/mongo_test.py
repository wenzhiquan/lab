import sys
sys.path.append("../..")
from FTP.lib.nosql.mongo_util import MongoUtil


if __name__ == '__main__':
	mongo = MongoUtil("FTP", "filename")
	result = mongo.get_one({"foo":"bar"})
	if result:
		print result
	else:
		print "Not found..."
