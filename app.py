from flask import Flask,make_response
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resoure,Api,fields,marshal_with,reqparse
from werkzeup.exceptions import HTTPExtensions
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///api_database.sqlite3'
db =SQLAlchemy()
db.init_app(app)
api =Api(app)
 #MODELS
class student(db.Model):
    __tablename__ = 'student'
    student_id =db.Column(db.integer, primary_key = True, autoincrement = True)
    roll_number = db.Column(db.String, unique = True, nullable = False)
    first_name = db.Column(db.String,nullable = False)
    last_name = db.Column(db.String)
    courses = db.reltationship("Courses, backref ")