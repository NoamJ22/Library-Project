# create a __init__.py file in the models folder to make all the model act as a package if you dont have it already , also you can make one file with all the models just copy ythe all the code in the files into it
from models import db
from datetime import datetime 

class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(200), nullable=False)
    password = db.Column(db.String(200), nullable=False)



