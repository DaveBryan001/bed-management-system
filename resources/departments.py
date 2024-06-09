from flask_restful import Resource, reqparse
from models import Department
from database import db
from flask_jwt_extended import jwt_required

department_parser = reqparse.RequestParser()
department_parser.add_argument('name',
    type=str,
    required=True,
    help='Name of the department'
    )
department_parser.add_argument('hospital_id',
    type=int,
    required=True,
    help='ID of the hospital'
    )

class DepartmentListResource(Resource):
    @jwt_required()
    def get(self):
        departments = Department.query.all()
        return [{'id': d.id, 'name': d.name, 'hospital_id': d.hospital_id} for d in departments]

# Create a new department
    @jwt_required()
    def post(self):
        args = department_parser.parse_args()
        department = Department(name=args['name'], hospital_id=args['hospital_id'])
        db.session.add(department)
        db.session.commit()
        return {'id': department.id, 'name': department.name, 'hospital_id': department.hospital_id}, 201

# Get a department by ID
class DepartmentResource(Resource):
    @jwt_required()
    def get(self, department_id):
        department = Department.query.get_or_404(department_id)
        return {'id': department.id, 'name': department.name, 'hospital_id': department.hospital_id}

# Update a department
    @jwt_required()
    def put(self, department_id):
        args = department_parser.parse_args()
        department = Department.query.get_or_404(department_id)
        department.name = args['name']
        department.hospital_id = args['hospital_id']
        db.session.commit()
        return {'id': department.id, 'name': department.name, 'hospital_id': department.hospital_id}

# Delete a department
    @jwt_required()
    def delete(self, department_id):
        department = Department.query.get_or_404(department_id)
        db.session.delete(department)
        db.session.commit()
        return {'message': 'Department deleted'}, 204