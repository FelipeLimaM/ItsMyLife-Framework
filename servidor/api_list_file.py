import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import json


def init():
	cred = credentials.Certificate('')
	fb = firebase_admin.initialize_app(cred, {
	    'databaseURL': ''
	})

	ref = db.reference("/").get()
	firebase_admin.delete_app(fb)

	for item in ref:
		print item
		for value in ref[item]:
			print ("{} : {} ".format(value,ref[item][value]))


	return (ref)

	# for item in j:
	# 	print item
	# 	for value in j[item]:
	# 		print ("{} : {} ".format(value,j[item][value]))
