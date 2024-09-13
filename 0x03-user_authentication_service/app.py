#!/usr/bin/env python3

"""This modules starts a flask app"""

from flask import Flask, abort, jsonify, request, make_response, redirect
from auth import Auth


app = Flask(__name__)
AUTH = Auth()


@app.route("/")
def index():
    """returns a simple json response"""

    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=["POST"], strict_slashes=False)
def register_user():
    """API to register a new user"""

    user_payload = request.form

    if user_payload is None:
        abort(400, description="Not a JSON")

    email = user_payload.get('email')
    password = user_payload.get('password')

    try:
        AUTH.register_user(email, password)
    except ValueError:
        return jsonify({"message": "email already registered"}), 400

    return jsonify({"email": email, "message": "user created"}), 200


@app.route("/sessions", methods=["POST"], strict_slashes=False)
def login():
    """
    Creates a new session for the user, store it the session ID
    as a cookie with key "session_id" on the response
    and return a JSON payload of the form
    """

    user_payload = request.form

    if user_payload is None:
        abort(400, description="Not a JSON")

    email = user_payload.get('email')
    password = user_payload.get('password')

    if not AUTH.valid_login(email, password):
        abort(401)

    session_id = AUTH.create_session(email)

    res = make_response({"email": email, "message": "logged in"})

    res.set_cookie("session_id", session_id)

    return res


@app.route("/sessions", methods=["DELETE"], strict_slashes=False)
def logout():
    """
    Finds the user with the requested session ID and
    destroy the session and redirect the user to GET /
    """

    session_id = request.cookies.get('session_id')

    user = AUTH.get_user_from_session_id(session_id)

    if not user:
        abort(403)

    AUTH.destroy_session(user.id)
    return redirect("/")


@app.route("/profile", strict_slashes=False)
def profile():
    """Finds the user with the requested session ID"""

    session_id = request.cookies.get('session_id')

    user = AUTH.get_user_from_session_id(session_id)

    if not user:
        abort(403)

    return jsonify({"email": user.email}), 200


@app.route("/reset_password", methods=["POST"], strict_slashes=False)
def get_reset_password_token():
    """
    Generates a password reset token and returns it for
    a user with a specific email
    """

    user_payload = request.form

    if user_payload is None:
        abort(400, description="Not a JSON")

    email = user_payload.get("email")

    try:
        reset_token = AUTH.get_reset_password_token(email)
    except ValueError:
        abort(403)

    return jsonify({"email": email, "reset_token": reset_token}), 200


@app.route("/reset_password", methods=["PUT"], strict_slashes=False)
def update_password():
    """
    Updates the password for a user with a specific email
    """

    user_payload = request.form

    if user_payload is None:
        abort(400, description="Not a JSON")

    email = user_payload.get("email")
    reset_token = user_payload.get("reset_token")
    new_password = user_payload.get("new_password")

    try:
        AUTH.update_password(reset_token, new_password)
    except ValueError:
        abort(403)

    return jsonify({"email": email, "message": "Password updated"}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
