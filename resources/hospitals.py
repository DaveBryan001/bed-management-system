from flask_restful import Resource, reqparse
from database import db
from flask_jwt_extended import jwt_required
from models import Hospital

hospital_parser = reqparse.RequestParser()
hospital_parser.add_argument(
    'name',
    type=str,
    required=True,
    help='Name of the hospital is required'
)
hospital_parser.add_argument(
    'location',
    type=str,
    required=True,
    help='Location of the hospital is required'
)
# get all hospitals
class HospitalListResource(Resource):
    @jwt_required()
    def get(self):
        hospitals = Hospital.query.all()
        return [{'id': h.id, 'name': h.name, 'location': h.location} for h in hospitals]

    @jwt_required()
    def post(self):
        args = hospital_parser.parse_args()
        hospital = Hospital(name=args['name'], location=args['location'])
        db.session.add(hospital)
        db.session.commit()
        return {'id': hospital.id, 'name': hospital.name, 'location': hospital.location}, 201

# get hospital record
class HospitalResource(Resource):
    @jwt_required()
    def get(self, hospital_id):
        hospital = Hospital.query.get_or_404(hospital_id)
        return {'id': hospital.id, 'name': hospital.name, 'location': hospital.location}

# update hospital record
    @jwt_required()
    def put(self, hospital_id):
        args = hospital_parser.parse_args()
        hospital = Hospital.query.get_or_404(hospital_id)
        hospital.name = args['name']
        hospital.location = args['location']
        db.session.commit()
        return {'id': hospital.id, 'name': hospital.name, 'location': hospital.location}

# delete hospital record
    @jwt_required()
    def delete(self, hospital_id):
        hospital = Hospital.query.get_or_404(hospital_id)
        db.session.delete(hospital)
        db.session.commit()
        return {'message': 'Hospital deleted'}