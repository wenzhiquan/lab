from FTP.config.base import HOST,PORT
from pymongo import MongoClient


class Base(object):

	client = MongoClient(HOST, PORT)