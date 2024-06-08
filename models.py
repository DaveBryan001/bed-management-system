from database import db
from flask-bcrypt import Bcrypt


bcrypt = Bcrypt()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullabble=False)

    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)
    

class Hospital(db.model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    location = db.Column(db.String(255), nullable=False)
    departments = db.relationship('Department', backref='hospial', lazy=True)


class Department(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    hospital_id = db.column(db.Integer, db.ForeignKey('hospital.id') nullable=False)
    beds = db.relationship('Bed', backref='department', lazy=True)
   
    
class Bed(db.model):
    id = db.Column(db.Integer, primary_key=True)
    department_id = db.Column(db.Integer, db.ForeignKey('hospital.id'), nullable=False)
    bed_number = db.Column(db.Integer, db.ForeignKey('department_id'), nullable=False)
    status = db.Column(db.String(50),nullable=False, default='available')
    patients = db.relationship('Patient', backref='bed', lazy=True)
    

class Patient(db.model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    age = db.Column(db.integer, nullable=False)
    bed_id = db.Column(db.Integer, db.ForeignKey('bed_id'), nullable=True)
    


