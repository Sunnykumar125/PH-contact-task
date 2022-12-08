import os
import yaml
from flask import Flask, render_template,request,jsonify,make_response
from flask_restful import Resource, Api
from flask_api import FlaskAPI
from flask_sqlalchemy import SQLAlchemy
from flask_mysqldb import MySQL
import MySQLdb

#from flask_marshmallow import Marshmallow



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= False
db = SQLAlchemy(app)
api = Api(app)
mysql = MySQL(app)
#ma = Marshmallow(app)




class Department(db.Model):
   id = db.Column (db.Integer, primary_key=True)
   name = db.Column (db.String(60))
   #address = db.Column (db.String(60))
   projects = db.relationship('Project', backref='department')
   employees = db.relationship('Employee', backref='department')
   
class Employee(db.Model):
   id = db.Column (db.Integer, primary_key=True)
   email = db.Column (db.String(60))
   lastname= db.Column (db.String(60))
   firstname= db.Column (db.String(60))
   age = db.Column(db.Integer)
   department_id = db.Column(db.Integer , db.ForeignKey('department.id'))


   def __repr__(self):
      return f"{self.id} - {self.email} = {self.lastname} - {self.firstname} - {self.age}"



class Project(db.Model):
   id = db.Column(db.Integer, primary_key=True)
   name = db.Column(db.String(60))
   client = db.Column(db.Integer)
   department_id = db.Column(db.Integer , db.ForeignKey('department.id'))

   

@app.route('/department')
def department():
   try:
     dept_all = Department.query.all()
     return render_template('department.html',dept_all=dept_all)
   except Exception as e:
      error_text = "<p>The error:<br>" + str(e) + "</p>"
      hed = '<h1>Something is broken.</h1>'
      return hed + error_text



@app.route('/employees')
def employees():
   try:
     emp_all = Employee.query.all()
     return render_template('employees.html',emp_all=emp_all)
   except Exception as e:
     error_text = "<p>The error:<br>" + str(e) + "</p>"
     hed = '<h1>Something is broken.</h1>'
     return hed + error_text

@app.route('/projects')
def projects():
   try:
     pro_all = Project.query.all()
     return render_template('projects.html',pro_all=pro_all)
   except Exception as e:
     error_text = "<p>The error:<br>" + str(e) + "</p>"
     hed = '<h1>Something is broken.</h1>'
     return hed + error_text






# For Get Request All Employee
class getEmployee(Resource):
   def get(self):
      employee= Employee.query.all()
      emp_list = []
      for emp in employee:
         emp_data = {'id':emp.id ,'Email':emp.email,  'lastname':emp.lastname,'Firstname':emp.firstname,'Age':emp.age}

         emp_list.append(emp_data)
      return{'Employee':emp_list},200


# For GET EMPLOYEE BY ID
class getEmployeebyID(Resource):
   def get(self,id):
      employee= Employee.query.get(id)
      emp_data = {'id':employee.id ,'Email':employee.email,  'lastname':employee.lastname,'Firstname':employee.firstname,'Age':employee.age}
      return{'Employee':emp_data},200



# For EDIT Request Employee BY ID
class updateEmployee(Resource):
   def put(self,id):
      if request.is_json:
         emp = Employee.query.get(id)
         if emp is None:
            return {'Error': 'Not Found'},404
         else:
            emp.id = request.json['ID']
            emp.email = request.json['Email']
            emp.lastname = request.json['LastName']
            emp.firstname = request.json['FirstName']
            emp.age = request.json['Age']
            db.session.commit()
            return 'Updated' , 200
      else:
         return {'Error' , 'Request must be JSON'}, 400  



class addEmployee(Resource):
   def post(self):
      if request.is_json:
         emp = Employee(id=request.json['ID'],email=request.json['Email'], lastname=request.json['LastName'],firstname=request.json['FirstName'],age=request.json['Age'])
         db.session.add(emp)
         db.session.commit()
         # return JSON response
         return make_response(jsonify({'Id':emp.id,'Email':emp.email, 'Last Name':emp.lastname,'First Name':emp.firstname,'Age':emp.age}),201)
      
      else:
         return {'Error': 'Request must be JSON'},400

# For Delete Employee By ID
class deleteEmployee(Resource):
   def delete(self,id):
      emp = Employee.query.get(id)
      if emp is None:
         return {'Error': 'Not Found'} , 404
      db.session.delete(emp)
      db.session.commit()
      return f'{id} is deleted' , 200


 






#REST API URL FOR EMPLOYEE
api.add_resource(getEmployee, '/getEmployee')
api.add_resource(getEmployeebyID, '/getEmployeebyID/<int:id>')
api.add_resource(addEmployee, '/addEmployee')
api.add_resource(updateEmployee, '/updateEmployee/<int:id>')
api.add_resource(deleteEmployee, '/deleteEmployee/<int:id>')





class getProject(Resource):
   def get(self):
      project= Project.query.all()
      pro_list = []
      for pro in project:
         pro_data = {'id':pro.id ,'Name':pro.name,  'Client':pro.client,'Department_ID':pro.department_id}
         pro_list.append(pro_data)
      return{'Project':pro_list},200



class getProjectbyID(Resource):
   def get(self,id):
      project= Project.query.get(id)
      pro_data = {'id':project.id ,'Name':project.name,  'Client':project.client,'Department_ID':project.department_id}
      return{'Project':pro_data},200



class addProject(Resource):
   def post(self):
      if request.is_json:
         pro = Project(id=request.json['ID'],name=request.json['Name'], client=request.json['Client'],department_id=request.json['Department_ID'])
         db.session.add(pro)
         db.session.commit()
         # return JSON response
         return make_response(jsonify({'Id':pro.id,'Name':pro.name, 'Client':pro.client,'Department_ID':pro.department_id}),201)
      
      else:
         return {'Error': 'Request must be JSON'},400


class deleteProjectbyID(Resource):
   def delete(self,id):
      pro = Project.query.get(id)
      if pro is None:
         return {'Error': 'Not Found'} , 404
      db.session.delete(pro)
      db.session.commit()
      return f'{id} is deleted' , 200





#REST API URL FOR Projects
api.add_resource(getProject, '/getProject')
api.add_resource(getProjectbyID, '/getProjectbyID/<int:id>')
api.add_resource(addProject, '/addProject')
api.add_resource(deleteProjectbyID, '/deleteProjectbyID/<int:id>')



#--------------------------------------------------------WITH MYSQL DATABASE=======

conn = MySQLdb.connect("localhost","root","","flask" ) 
cursor = conn.cursor() 

@app.route('/example')
def example(): 
    cursor.execute("SELECT  AVG(age),name from employee,department where department.id = employee.department_id GROUP BY department.name;")
    data = cursor.fetchall() #data from database 
    return render_template("example.html", value=data) 


@app.route('/example1')
def example1(): 
    cursor.execute("SELECT count(*) as 'NO OF EMPLOYEE' ,name as 'Department Name' from employee,department WHERE department.id = employee.department_id GROUP BY department_id; ") 
    data = cursor.fetchall() #data from database 
    return render_template("example1.html", value=data) 

@app.route('/example2')
def example2(): 
    cursor.execute("SELECT count(*) as 'No Of Projects', department.name as 'Department Name' from projects,department WHERE department.id = projects.department_id GROUP BY department_id;") 
    data = cursor.fetchall() #data from database 
    return render_template("example2.html", value=data) 




if __name__ == '__main__':
    app.debug = True
    app.run()