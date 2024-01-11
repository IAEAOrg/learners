from datetime import datetime, timezone

from flask import Blueprint, json, jsonify, request
from backend.functions.database import db_update_venjix_execution
from backend.logger import logger

callback_api = Blueprint("callback_api", __name__)


@callback_api.route("/callback/<execution_uuid>", methods=["POST"])
def callback(execution_uuid):
    try:
        resp = request.get_json()
        db_update_venjix_execution(
            execution_uuid,
            response_timestamp=datetime.now(timezone.utc),
            response_content=json.dumps(resp),
            completed=bool(resp.get("returncode") == 0),
            msg=resp.get("msg") or None,
            partial=resp.get("partial") or False,
        )
        return jsonify(success=True), 200

    except Exception as e:
        logger.exception(e)
        return jsonify(success=False, exception=e), 500
