#!/usr/bin/env python3
"""This module handles session authentication method"""

from api.v1.views import app_views
from flask import abort, jsonify, request, make_response
from models.user import User
from os import getenv


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def session_login():
    """Creates a session for the user when he/she logs in"""

    email = request.form.get("email")
    password = request.form.get("password")

    if not email:
        return jsonify({"error": "email missing"}), 400

    if not password:
        return jsonify({"error": "password missing"}), 400

    try:
        user = User.search({"email": email})
    except Exception:
        return jsonify({"error": "no user found for this email"}), 404

    if not user:
        return jsonify({"error": "no user found for this email"}), 404

    if not user[0].is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401

    from api.v1.app import auth

    session_id = auth.create_session(user[0].id)

    res = make_response(jsonify(user[0].to_json()))
    res.set_cookie(getenv("SESSION_NAME"), session_id)

    return res


@app_views.route('/auth_session/logout', methods=['DELETE'],
                 strict_slashes=False)
def session_logout():
    """Deletes the session for the user when he/she logs out"""

    from api.v1.app import auth

    if not auth.destroy_session(request):
        abort(404)

    return jsonify({}), 200
