#Store the settings for the application
from flask import Flask

#create the app object
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///./database.db" #The path to the Database
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
