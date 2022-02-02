from flask import Flask
app = Flask(__name__) # Creates instance of Flask class here
app.secret_key = "itsasecrettoeverybody" # Secret key goes here