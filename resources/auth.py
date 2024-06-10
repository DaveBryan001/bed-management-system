from flask import request
from flask_restful import Resource
from models import User
from database import db
from flask_jwt_extended import create_access_token

# User Registration API
class UserRegistration(Resource):
    def post(self):
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        if User.query.filter_by(username=username).first():
            return {'message': 'User already exists'}, 409

        new_user = User(username=username)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()

        return {'message': 'User created successfully'}, 201

            
# User Login API
class UserLogin(Resource):
    def post(self):
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            access_token = create_access_token(identity={'username':username})
            return {'access_token': access_token}, 200
        else:
            return {'message': 'Invalid credentials'}, 401