#!/usr/bin/env python3
"""New view for Session Authentication"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models.user import User
from os import getenv


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login_with_session():
    """Login a user with session_auth"""
    email = request.form.get('email')
    password = request.form.get('password')

    if email is None:
        return jsonify({"error": "email missing"}), 400
    if password is None:
        return jsonify({"error": "password missing"}), 400
    users = User.search({'email': email})
    if not users:
        return jsonify({"error": "no user found for this email"}), 404
    for u in users:
        if u.is_valid_password(password):
            from api.v1.app import auth
            user_id = u.id
            print(auth)
            session_id = auth.create_session(user_id)
            res = jsonify(u.to_json())
            res.set_cookie(getenv('SESSION_NAME'), session_id)
            return res
        return jsonify(error='wrong password'), 402
    return jsonify({"error": "no user found for this email"}), 404


def logout():
    """ DELETE /auth_session/logout
    Return:
      - Response
    """
    from api.v1.app import auth
    if auth.destroy_session(request):
        return jsonify({}), 200
    abort(404)
