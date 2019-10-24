from pyrebase import pyrebase


def download(inputfile,output):

	config = {
	  "serviceAccount": "",
	  "apiKey": "",
      "authDomain": "",
      "databaseURL": "",
      "storageBucket": "",
	}

	firebase = pyrebase.initialize_app(config)

	firebase.storage().child(inputfile).download(filename=output)
