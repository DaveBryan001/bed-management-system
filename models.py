from database import db
from flask_bcrypt import Bcrypt


bcrypt = Bcrypt()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)
    

class Hospital(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    location = db.Column(db.String(255), nullable=False)
    departments = db.relationship('Department', backref='hospital', lazy=True)


class Department(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    hospital_id = db.Column(db.Integer, db.ForeignKey('hospital.id'), nullable=False)
    beds = db.relationship('Bed', backref='department', lazy=True)
   
    
class Bed(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    department_id = db.Column(db.Integer, db.ForeignKey('department.id'), nullable=False)
    bed_number = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(50), nullable=False)
    patients = db.relationship('Patient', backref='bed', lazy=True)
    

class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    bed_id = db.Column(db.Integer, db.ForeignKey('bed.id'), nullable=True)
    


