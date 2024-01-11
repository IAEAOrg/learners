from flask import Blueprint, jsonify
from backend.functions.database import (
    db_get_all_exercises_sorted,
    db_get_completion_percentage,
)
from backend.functions.helpers import convert_to_dict
from backend.jwt_manager import admin_required

exercises_api = Blueprint("exercises_api", __name__)


@exercises_api.route("/exercises", methods=["GET"])
@admin_required()
def getExercises():
    exercises = []
    sorted_exercises = convert_to_dict(db_get_all_exercises_sorted())

    for exercise in sorted_exercises:
        exercise["completion_percentage"] = db_get_completion_percentage(exercise.get("id"))
        exercises.append(exercise)

    return jsonify(exercises=exercises)
