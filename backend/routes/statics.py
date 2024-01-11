from flask import Blueprint, send_from_directory, make_response, jsonify, request
from werkzeug.exceptions import NotFound
from flask_jwt_extended import jwt_required

from backend.conf.config import cfg

from backend.logger import logger

statics_api = Blueprint("statics_api", __name__)


@statics_api.after_app_request
def after_request_func(response):
    if jwt := request.args.get("jwt"):
        response.set_cookie("jwt_cookie", value=jwt, max_age=None, expires=None, path="/", domain=None, secure=None, httponly=False)
    return response


@statics_api.route("/statics", methods=["GET"])
@statics_api.route("/statics/", methods=["GET"])
@statics_api.route("/statics/<path:path>", methods=["GET"])
@jwt_required()
def getStaticFiles(path=""):
    # Load static defaults
    static_root = cfg.statics.get("base_url")  # Directory holding the static sites

    # Add "index.html" to path if empty or ends with "/"
    if not path or "." not in path:
        path = f"{path}index.html" if path.endswith("/") else f"{path}/index.html"

    try:
        return make_response(send_from_directory(static_root, path))

    except NotFound:
        logger.warning(f"File not found: {path}")
        return jsonify(error="file not found"), 404

    except Exception as e:
        logger.exception(f"An unexpected error occurred: {e}")
        return jsonify(error="internal server error"), 500
