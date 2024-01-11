import json
from backend.conf.db_models import Cache
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, current_user
from backend.functions.database import (
    db_create_or_update,
    db_get_cache_by_ids,
)


cache_api = Blueprint("cache_api", __name__)


# Post new comment
@cache_api.route("/cache", methods=["PUT"])
@jwt_required()
def putCache():
    data = request.get_json()

    new_cache_entry = {
        "user_id": current_user.id,
        "global_exercise_id": data.get("global_exercise_id"),
        "form_data": json.dumps(data.get("form_data")),
    }

    db_create_or_update(Cache, ["user_id", "global_exercise_id"], new_cache_entry)

    return jsonify(updated=True), 200


# Post new comment
@cache_api.route("/cache/<global_exercise_id>", methods=["GET"])
@jwt_required()
def getCache(global_exercise_id):
    if cache := db_get_cache_by_ids(current_user.id, global_exercise_id):
        return jsonify(form_data=cache.form_data), 200
    else:
        return jsonify(form_data=None), 200
