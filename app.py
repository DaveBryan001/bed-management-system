from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager
from config import Config
from database import db
from models import User
from resources.auth import UserRegistration, UserLogin
from resources.hospitals import HospitalResource, HospitalListResource
from resources.departments import DepartmentResource, DepartmentListResource
from resources.beds import BedResource, BedListResource
from resources.patients import PatientResource, PatientListResource

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
api = Api(app)
jwt = JWTManager(app)

@app.route('/')
def home():
    return 'Welcome to the Bed Management System!'

api.add_resource(UserRegistration, '/register')
api.add_resource(UserLogin, '/login')

api.add_resource(HospitalResource, '/hospitals/<int:hospital_id>')
api.add_resource(HospitalListResource, '/hospitals')

api.add_resource(DepartmentResource, '/departments/<int:department_id>')
api.add_resource(DepartmentListResource, '/departments')

api.add_resource(BedResource, '/beds/<int:bed_id>')
api.add_resource(BedListResource, '/beds')

api.add_resource(PatientResource, '/patients/<int:patient_id>')
api.add_resource(PatientListResource, '/patients')


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        app.run(debug=True)