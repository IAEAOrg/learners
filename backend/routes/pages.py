import json
from backend.classes.SSE import SSE_Event, sse
from flask import Blueprint, jsonify, request
from backend.functions.database import (
    db_create_notification,
    db_get_page_by_id,
    db_get_page_tree,
    db_get_userids_by_usergroups,
    db_toggle_page_visibility,
)
from backend.jwt_manager import admin_required
from flask_jwt_extended import current_user, jwt_required
from backend.functions.helpers import sse_create_and_publish

pages_api = Blueprint("pages_api", __name__)


@pages_api.route("/pages", methods=["GET"])
@jwt_required()
def getPages():
    pages = db_get_page_tree(current_user)
    return jsonify(pages=pages)


@pages_api.route("/pages/<page_id>/hidden", methods=["PUT"])
@admin_required()
def updatePage(page_id):
    notify = request.get_json().get("notify")
    updated = db_toggle_page_visibility(page_id)
    new_page = db_get_page_by_id(page_id)

    sse_recipients = db_get_userids_by_usergroups(json.loads(new_page.params).get("groups", ["all"]))

    newNotification = SSE_Event(
        event="content",
        _type="content",
        message=db_get_page_tree(current_user),
        recipients=sse_recipients,
    )

    # Notify Users
    sse.publish(newNotification)

    if not new_page.hidden and notify:
        sse_create_and_publish(_type="content", page=new_page.page_title, recipients=sse_recipients)

        # newNotification = SSE_Event(
        #     event="content",
        #     page=new_page.page_title,
        #     recipients=sse_recipients,
        # )

        # # Create Database entry
        # db_create_notification(newNotification)

        # # Notify Users
        # sse.publish(newNotification)

    return jsonify(updated=updated), 200 if updated else 406
