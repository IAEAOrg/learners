from datetime import datetime, timezone

from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, get_jwt, get_jwt_identity, jwt_required, verify_jwt_in_request
from jwt.exceptions import ExpiredSignatureError
import jwt
from sqlalchemy.exc import IntegrityError
from backend.conf.config import cfg
from backend.conf.db_models import TokenBlocklist
from backend.database import db
from backend.functions.authentication import check_password
from backend.functions.helpers import get_user_from_request
from backend.logger import logger

authentication_api = Blueprint("authentication_api", __name__)


@authentication_api.route("/login", methods=["POST"])
def postLoginData():
    data = request.get_json()

    username = data.get("username", None)
    password = data.get("password", None)

    if not check_password(cfg.users, username, password):
        logger.info(f"[auth] user: { username } - Login failed.")
        return jsonify(authenticated=False)

    admin = cfg.users.get(username).get("admin")
    user_role = cfg.users.get(username).get("role")

    jwt = create_access_token(identity=username, additional_claims={"admin": admin, "role": user_role})
    logger.info(f"[auth] user: { username } - Login successful.")

    return jsonify(authenticated=True, jwt=jwt), 200


@authentication_api.route("/logout", methods=["POST"])
def logout():
    try:
        verify_jwt_in_request()
        jti = get_jwt()["jti"]
        username = get_jwt_identity()

        # Adding token to blocklist
        now = datetime.now(timezone.utc)
        db.session.add(TokenBlocklist(jti=jti, created_at=now))
        db.session.commit()

        logger.info(f"[auth] user: { username } - Logged out.")
        return jsonify(logged_out=True), 200

    except IntegrityError as integrity_error:
        # Handle IntegrityError if the token is already in the blocklist
        db.session.rollback()
        logger.error(f"[auth] IntegrityError: { integrity_error }")
        return jsonify(logged_out=True, error="Token already in blocklist"), 200

    except ExpiredSignatureError:
        # Handle Signature has expired error
        username = get_user_from_request(request)
        logger.info(f"[auth] user: { username } - Signature has expired.")
        return jsonify(logged_out=True, error="Signature has expired"), 200

    except Exception as e:
        # Log the unexpected error and return a generic error response
        logger.error(f"Unexpected Error: {e}")
        return jsonify(error="Internal Server Error"), 500


@authentication_api.route("/authentication", methods=["GET"])
@jwt_required(optional=True)
def verifyAuthentication():
    current_identity = get_jwt_identity()
    return jsonify(user=current_identity), 200
