from functools import wraps

from flask import jsonify
from flask_jwt_extended import JWTManager, get_jwt, verify_jwt_in_request
from backend.functions.database import db_get_user_by_name

from backend.logger import logger
from backend.conf.db_models import TokenBlocklist
from backend.database import db

jwt = JWTManager()


@jwt.expired_token_loader
def token_expired(jwt_header, jwt_payload):
    return jsonify(error="Your token is expired. Please login again."), 401


@jwt.invalid_token_loader
def token_invalid(jwt_payload):
    return jsonify(error="Your token is invalid."), 401


@jwt.unauthorized_loader
def token_missing(callback):
    return jsonify(error="Authorization is missing."), 401


@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_payload):
    try:
        jti = jwt_payload["jti"]
        token = db.session.query(TokenBlocklist.id).filter_by(jti=jti).scalar()
        return token is not None
    except Exception as e:
        logger.exception(e)
        return True


@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    return db_get_user_by_name(jwt_data["sub"])


@jwt.revoked_token_loader
def token_revoked(jwt_header, jwt_payload):
    return jsonify(error="Token has been revoked"), 401


def admin_required():
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            if get_jwt().get("admin"):
                return fn(*args, **kwargs)
            else:
                response = jsonify(error="Admins only!")
                response.status_code = 401
                return response

        return decorator

    return wrapper


def only_self_or_admin():
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            current_user_id = db_get_user_by_name(get_jwt().get("sub")).id

            if get_jwt().get("admin") or (int(kwargs["user_id"]) == int(current_user_id)):
                return fn(*args, **kwargs)
            else:
                return jsonify(error="only self or admins allowed"), 401

        return decorator

    return wrapper


def init_jwt(app):
    global jwt
    jwt.init_app(app)
