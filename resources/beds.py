from flask_restful import Resource, reqparse
from models import Bed
from database import db
from flask_jwt_extended import jwt_required
import spacy
from flask import Flask, request, jsonify

bed_parser = reqparse.RequestParser()
bed_parser.add_argument(
    'bed_number',
    type=int,
    required=True,
    help='Bed number is required'
)
bed_parser.add_argument(
    'status',
    type=str,
    required=True,
    choices=('available', 'occupied'),
    help='Bed status'
)
bed_parser.add_argument(
    'department_id',
    type=int,
    required=True,
    help='Department id is required'
)
# get all beds
class BedListResource(Resource):
    @jwt_required()
    def get(self):
        beds = Bed.query.all()
        return [{'id': b.id, 'department_id': b.department_id, 'bed_number': b.bed_number, 'status': b.status} for b in beds]

# create bed record
    @jwt_required()
    def post(self):
        args = bed_parser.parse_args()
        bed = Bed(department_id=args['department_id'], bed_number=args['bed_number'], status=args['status'])
        db.session.add(bed)
        db.session.commit()
        return {'id': bed.id, 'department_id': bed.department_id, 'bed_number': bed.bed_number, 'status': bed.status }, 201

# get bed record
class BedResource(Resource):
    @jwt_required()
    def get(self, bed_id):
        bed = Bed.query.get_or_404(bed_id)
        return {'id': bed.id, 'department_id': bed.department_id, 'bed_number': bed.bed_number, 'status': bed.status}

# update bed record
    @jwt_required()
    def put(self, bed_id):
        args = bed_parser.parse_args()
        bed = Bed.query.get_or_404(bed_id)
        bed.department_id = args['department_id']
        bed.bed_number = args['bed_number']
        bed.status = args['status']
        db.session.commit()
        return {'id': bed.id, 'department_id': bed.department_id, 'bed_number': bed.bed_number, 'status': bed.status}

# delete bed from bed record
    @jwt_required()
    def delete(self, bed_id):
        bed = Bed.query.get_or_404(bed_id)
        db.session.delete(bed)
        db.session.commit()
        return {'message': 'Bed deleted'}
    
    
    

nlp = spacy.load("en_core_web_sm")

def find_available_beds(query, db): 
    """Processes a query to find available beds and queries the database.

    Args:
        query (str): The user's query about bed availability.
        db: Your SQLAlchemy database instance (e.g., `db` from your database module).

    Returns:
        dict: A dictionary containing the response message, department (if any),
              and a list of available beds (or an empty list if none).
    """

    doc = nlp(query)
    department = None

    for ent in doc.ents:
        if ent.label_ == "ORG":  
            department = ent.text
            break  

    available_beds = []
    if department:
        available_beds = db.session.query(Bed).filter_by(status='available', department_id=department).all()
    else:
        available_beds = db.session.query(Bed).filter_by(status='available').all()

    num_beds = len(available_beds)

    if num_beds == 1:
        bed = available_beds[0]
        response = {
            "message": f"Yes, there is one bed available",
            "department": department if department else "All departments",
            "beds": [{"id": bed.id, "bed_number": bed.bed_number}]  
        }
    elif num_beds > 1:
        response = {
            "message": f"Yes, there are {num_beds} available beds",
            "department": department if department else "All departments",
            "beds": [{"id": bed.id, "bed_number": bed.bed_number} for bed in available_beds] 
        }
    else:
        response = {
            "message": f"Sorry, there are no available beds" +
                       (f" in {department}" if department else "") +
                       " at the moment."
        }

    return response

class BedAvailabilityResource(Resource):
    def post(self):
        data = request.get_json()
        query = data.get('query')

        if not query:
            return jsonify({"message": "Please provide a query."}), 400

        response = find_available_beds(query, db)
        return jsonify(response)
