from flask import Blueprint, jsonify, request
from src.db.service import UserService

user_api = Blueprint('users_api', __name__, url_prefix='/api/users')

@user_api.route('/')
def all_users():
    users = [user.as_dict() for user in UserService().get_all()]
    return jsonify({"success": True, "result": users})

@user_api.route('/<int:user_id>/profile')
def user_info(user_id: int):
    user = UserService().get_user_by_id(user_id)

    if user is None:
        return jsonify({"success": False, "message": f"User with id {user_id} not found."})
    
    return jsonify({"success": True, "result": user.as_dict()})

@user_api.route('/register', methods=['POST'])
def register_user():
    req_body = request.json
    if not req_body:
        return jsonify({"success": False, "message": "Request body not provided"})
    
    username, email, password = req_body.get('username'), req_body.get('email'), req_body.get('')
    if not username or not email or not password:
        return jsonify({"success": False, "message": f"User data not provided: {username=}, {email=}, {password=}"})
    
    user = UserService().register_user(username=username, email=email, password=password)
    return jsonify({"success": True, "reusult": user.as_dict()})

@user_api.route("/remove", methods=['POST'])
def delete_user():
    req_body = request.json
    if not req_body:
        return jsonify({"success": False, "message": "Request body not provided"})
    
    user_id = req_body.get('id')
    if not user_id:
        return jsonify({"success": False, "message": f"User data not provided: {user_id=}"})
    
    user = UserService().delete_user_by_id(user_id=user_id)
    if not user: 
        return jsonify({"success": False, "message": f"User with id: {user_id} not found"})
    
    return jsonify({"success": True, "reusult": user.as_dict()})