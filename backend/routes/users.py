from flask import Blueprint, jsonify
from backend.functions.database import db_get_all_usergroups, db_get_all_users
from backend.jwt_manager import admin_required

users_api = Blueprint("users_api", __name__)


@users_api.route("/users", methods=["GET"])
@admin_required()
def getUsers():
    db_userlist = db_get_all_users()
    userlist = []
    for user in db_userlist:
        userlist.append({"id": user.id, "name": user.name})

    return jsonify(users=userlist), 200


@users_api.route("/usergroups", methods=["GET"])
@admin_required()
def getUsergroups():
    db_usergroups = db_get_all_usergroups()
    grouplist = []
    for name, ids in db_usergroups.items():
        grouplist.append({"name": name, "ids": ids})

    return jsonify(groups=grouplist), 200
