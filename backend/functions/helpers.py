import json
import os
import time
import jwt
from datetime import datetime
from backend.logger import logger

from backend.conf.config import cfg


def utc_to_local(utc_datetime: str, date: bool = True) -> str:
    if utc_datetime is None:
        return None
    now_timestamp = time.time()
    offset = datetime.fromtimestamp(now_timestamp) - datetime.utcfromtimestamp(now_timestamp)
    return (utc_datetime + offset).strftime("%m/%d/%Y, %H:%M:%S") if date else (utc_datetime + offset).strftime("%H:%M:%S")


def extract_json_content(app, json_file_path, info="") -> list:
    gen_list = []

    if (json_file_path).startswith("/"):
        json_file = json_file_path
    else:
        json_file = os.path.join(app.root_path, json_file_path)

    try:
        with open(json_file, "r") as input_file:
            json_data = json.load(input_file)
            gen_list.extend(element for _, element in json_data.items())

    except Exception:
        err = f"\n\tERROR: Could not read JSON file: {json_file}.\n{info}"
        logger.warning(err)

    return gen_list


def extract_history(executions):
    return {
        str(i + 1): {
            "start_time": utc_to_local(execution.get("execution_timestamp"), date=True),
            "response_time": utc_to_local(execution.get("response_timestamp"), date=False),
            "completed": bool(execution.get("completed")),
            "msg": execution.get("msg"),
            "partial": bool(execution.get("partial")),
        }
        for i, execution in enumerate(executions)
    }


def append_key_to_dict(dictobj: dict, parent: str, baseobj: dict = None) -> dict:
    if not dictobj.get(parent):
        dictobj[parent] = baseobj or {}
    return dictobj


def append_or_update_subexercise(parent_exercise: dict, child_exercise: dict) -> dict:
    parent_exercise["total"] += child_exercise.get("total")
    parent_exercise["done"] += child_exercise.get("done")

    for i, element in enumerate(parent_exercise.get("exercises")):
        if element.get("title") == child_exercise.get("title"):
            parent_exercise["exercises"][i]["total"] += child_exercise.get("total")
            parent_exercise["exercises"][i]["done"] += child_exercise.get("done")
            return parent_exercise

    parent_exercise["exercises"].append(child_exercise)

    return parent_exercise


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in cfg.allowed_extensions


def replace_attachhment_with_url(formData):
    if formData:
        from backend.functions.database import db_get_filename_from_hash

        for key, value in formData.items():
            if key == "attachment":
                filename = db_get_filename_from_hash(value)
                hyperlink = f"/upload/{filename}"
                formData[key] = hyperlink
            if isinstance(value, dict):
                formData[key] = replace_attachhment_with_url(value)
                continue

    return formData


def sse_create_and_publish(
    event: str = "notification",
    _type: str = "standard",
    message: str = "",
    user=None,
    page=None,
    exercise=None,
    recipients=None,
    positions=None,
    question=None,
) -> bool:
    # Import
    from backend.classes.SSE import SSE_Event, sse
    from backend.functions.database import db_create_notification, db_get_admin_users

    # Conditional publishing
    if _type == "submission":
        message = f"<h4>New submission</h4>User: {user.name}<br>Exercise: {exercise.exercise_name}"
        recipients = [admin_user.id for admin_user in db_get_admin_users()]

    if _type == "comment":
        message = f"<h4>New Comment</h4>User: {user.name}<br>Page: {page}"
        recipients = [admin_user.id for admin_user in db_get_admin_users()]

    if _type == "content":
        message = """
            <h3>
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6" style="width: 1.5rem; float: left;margin-right: 10px; margin-top: -2px;">
                <path stroke-linecap="round" stroke-linejoin="round" d="M9.813 15.904L9 18.75l-.813-2.846a4.5 4.5 0 00-3.09-3.09L2.25 12l2.846-.813a4.5 4.5 0 003.09-3.09L9 5.25l.813 2.846a4.5 4.5 0 003.09 3.09L15.75 12l-2.846.813a4.5 4.5 0 00-3.09 3.09zM18.259 8.715L18 9.75l-.259-1.035a3.375 3.375 0 00-2.455-2.456L14.25 6l1.036-.259a3.375 3.375 0 002.455-2.456L18 2.25l.259 1.035a3.375 3.375 0 002.456 2.456L21.75 6l-1.035.259a3.375 3.375 0 00-2.456 2.456zM16.894 20.567L16.5 21.75l-.394-1.183a2.25 2.25 0 00-1.423-1.423L13.5 18.75l1.183-.394a2.25 2.25 0 001.423-1.423l.394-1.183.394 1.183a2.25 2.25 0 001.423 1.423l1.183.394-1.183.394a2.25 2.25 0 00-1.423 1.423z" />
                </svg>
            Content Update </h3>
            """
        message += f'New content: "{page}"'

    if not positions:
        positions = ["all"]

    new_event = SSE_Event(event=event, _type=_type, message=message, question=question, recipients=recipients, positions=positions)

    # Create Database entry
    db_create_notification(new_event)

    # Notify Users
    sse.publish(new_event)


def is_json(json_string):
    try:
        json.loads(json_string)
        return True
    except ValueError:
        return False


# remove instance element from db result
def convert_to_dict(input):
    if single := not isinstance(input, list):
        input = [input]

    output = []
    for element in input:
        element = element.__dict__
        element.pop("_sa_instance_state")
        output.append(element)

    return output[0] if single else output


def get_user_from_request(req):
    try:
        raw_jwt = req.__dict__["headers"]["Authorization"].split("Bearer ")[1]
        return jwt.decode(raw_jwt, options={"verify_signature": False}).get("sub")
    except:
        return ""
