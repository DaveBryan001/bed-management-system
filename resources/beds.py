from flask_restful import Resource, reqparse
from models import Bed
from database import db
from flask_jwt_extended import jwt_required

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