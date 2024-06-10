from flask_restful import Resource, reqparse
from models import Patient, Bed
from database import db
from flask_jwt_extended import jwt_required

patient_parser = reqparse.RequestParser()
patient_parser.add_argument(
    'name',
    type=str,
    required=True,
    help='Name of Patient'
)
patient_parser.add_argument(
    'age',
    type=int,
    required=True,
    help='Age of Patient'
)
patient_parser.add_argument(
    'bed_id',
    type=int,
    required=True,
    help='Bed id'
)

# get all patients
class PatientListResource(Resource):
    @jwt_required()
    def get(self):
        patients = Patient.query.all()
        return [{'id': p.id, 'name': p.name, 'age': p.age, 'bed_id': p.bed_id} for p in patients]

# create patient record
    @jwt_required()
    def post(self):
        args = patient_parser.parse_args()
        bed = Bed.query.get(args['bed_id'])
        if not bed:
            return {'message': 'Bed not found'}, 404
        if bed and bed.status == 'occupied':
            return {'message': 'Bed is occupied'}, 400
        
        bed.status = 'occupied'
        patient = Patient(name=args['name'], age=args['age'], bed_id=args['bed_id'])
        db.session.add(patient)
        db.session.commit()
        return {'id': patient.id, 'name': patient.name, 'age': patient.age, 'bed_id': patient.bed_id}, 201


# get patient record
class PatientResource(Resource):
    @jwt_required()
    def get(self, patient_id):
        patient = Patient.query.get_or_404(patient_id)
        return {'id': patient.id, 'name': patient.name, 'age': patient.age, 'bed_id': patient.bed_id}

# update patient record
    @jwt_required()
    def put(self, patient_id):
        args = patient_parser.parse_args()
        patient = Patient.query.get_or_404(patient_id)
        bed = Bed.query.get(args['bed_id'])
        if not bed:
            return {'message': 'Bed not found'}, 404
        if bed and bed.status == 'occupied':
            return {'message': 'Bed is already occupied'}, 400

        if patient.bed_id:
            old_bed = Bed.query.get(patient.bed_id)
            old_bed.status = 'available'
            
        patient.name = args['name']
        patient.age = args['age']
        patient.bed_id = args['bed_id']
        if bed:
            bed.status = 'occupied'
        db.session.commit()
        return {'id': patient.id, 'name': patient.name, 'age': patient.age, 'bed_id': patient.bed_id}

# delete patient from patient record
    @jwt_required()
    def delete(self, patient_id):
        patient = Patient.query.get_or_404(patient_id)
        if patient.bed_id:
            bed = Bed.query.get(patient.bed_id)
            bed.status = 'available'
        db.session.delete(patient)
        db.session.commit()
        return {'message': 'Patient deleted'}