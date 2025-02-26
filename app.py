from flask import Flask,make_response
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource,Api,fields,marshal_with,reqparse
from werkzeug.exceptions import HTTPException
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///api_database.sqlite3'
db =SQLAlchemy()
db.init_app(app)

api =Api(app)
 #MODELS
class student(db.Model):
    __tablename__ = 'student'
    student_id =db.Column(db.Integer, primary_key = True, autoincrement = True)
    roll_number = db.Column(db.String, unique = True, nullable = False)
    first_name = db.Column(db.String,nullable = False)
    last_name = db.Column(db.String)
    courses =db.relationship("Course",backref = "student", secondary ="enrollment",cascade="all,delete")

class course(db.Model):
    __tablename__ ='course'
    course_id =db.Column(db.Integer, primary_key = True, autoincrement = True)
    course_code = db.Column(db.String, unique = True, nullable = False)
    course_name = db.Column(db.String,nullable = False)
    course_description = db.Column(db.String)

class enrollments(db.Model):
    __tablename__ ='enrollment'
    entollment_id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    estudent_id = db.Column(db.Integer, db.ForeignKey("student.student_id"), nullable =False )
    course_id = db.Column(db.Integer, db.ForeignKey("course.course_id"), nullable =False )   

#with app.app_context():
    #db.create_all()
app.app_context().push()
#Exceptions
class founderror(HTTPException):
    def __init__(self,status_code,message=''):
        self.response = make_response(message, status_code)

class notgivenerror(HTTPException):
     def __init__(self, status_code, error_code,error_message):
         message ={"error_code":error_code, "error_message":error_message}
         self.response = make_response(json.dumps(message),status_code)

#Outputfields

student_fields ={
    "student_id":fields.Integer,
    "first_name":fields.String,
    "last_name":fields.String,
    "roll_number":fields.String,
}

course_fields = {
    "course_id":fields.Integer,
    "course_name":fields.String,
    "course_code":fields.String,
    "course_description":fields.String,
}

#parsers
course_parse = reqparse.RequestParser()
course_parse.add_argument("course_name")
course_parse.add_argument("course_code")
course_parse.add_argument("course_description")
student_parse =reqparse.RequestParser()
student_parse.add_argument("first_name")
student_parse.add_argument("last_name")
student_parse.add_argument("roll_number")
enrollment_parse =reqparse.RequestParser()
enrollment_parse.add_argument("course_id")


#apis
class CourseAPI(Resource):
    @marshal_with(course_fields)
    def get(self,course_id):
        Course = course.query.filter(course.course_id == course_id).first()
        if Course:
            return Course
        else:
            raise founderror(status_code =404)
        
    @marshal_with(course_fields)    
    def post(self):
        args = course_parse.parse_args()
        course_name = args.get('course_name',None)
        course_code=args.get('course_code',None)
        course_description=args.get('course_description',None)
        if course_name is None:
            raise notgivenerror(status_code =400, error_code ="COURSE001", error_message ="Course Name is required")
        elif course_code is None:            
            raise notgivenerror(status_code =400, error_code ="COURSE002", error_message ="Course Code is required")
        Course= course.query.filter(course.course_code == course_code).first()
        else Course is None:
            Course = course(course_name=course_name,course_code=course_code,course_description=course_description)
            db.session.add(course)
            db.session.commit()
            return Course, 201
        else:
            founderror(status_code=400)


#adding resources
api.add_resource(CourseAPI,"/api/course/<int:course_id>")
                           



if __name__ == "__main__":
    app.run(debug=True,port=5000)