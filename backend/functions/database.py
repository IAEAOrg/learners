import hashlib
import json
from datetime import datetime, timezone
import string
from typing import Tuple
from backend.classes.SSE import SSE_Event

from backend.logger import logger
from backend.conf.config import cfg
from backend.conf.db_models import (
    Attachment,
    Cache,
    Execution,
    Exercise,
    Notification,
    QuestionnaireAnswer,
    User,
    Page,
    Comment,
    Questionnaire,
    QuestionnaireQuestion,
    Usergroup,
    UsergroupAssociation,
    VenjixExecution,
)
from backend.database import db
from backend.functions.helpers import convert_to_dict, extract_json_content


def db_insert_initial_usergroups(*args, **kwargs):
    for username, userDetails in cfg.users.items():
        db_user = db_get_user_by_name(username)
        usergroups = ["all"]

        usergroups.append(f"{userDetails.get('role', '')}s")
        if "instructor" in userDetails.get("role", ""):
            usergroups.append("admins")

        for g in json.loads(userDetails.get("meta")).get("groups", []):
            usergroups.append(g)

        for group in usergroups:
            db_create_or_update(Usergroup, ["name"], {"name": group})
            usergroup = Usergroup.query.filter_by(name=group).first()

            new_usergroup_association = {
                "user": db_user,
                "usergroup": usergroup,
            }

            db_create_or_update(UsergroupAssociation, ["user", "usergroup"], new_usergroup_association)

    db.session.commit()


def db_insert_initial_users(*args, **kwargs):
    for user_name, userDetails in cfg.users.items():
        user = {"name": user_name, "role": userDetails.get("role"), "admin": userDetails.get("admin"), "meta": userDetails.get("meta")}
        db_create_or_update(User, ["name"], user)


def db_insert_pages(app, *args, **kwargs):
    page_json = f"{cfg.statics.get('base_url')}/hugo/pages.json"
    pages = extract_json_content(app, page_json)

    for page in sorted(pages, key=lambda p: p["hierarchy"]):
        default_title = "root" if page.get("hierarchy") == 0 else ""
        params = page.get("params")

        hidden = False
        if hideopts := params.get("hideopts"):
            if hideopts == "hidden":
                hidden = True

        new_page = {
            "page_id": page["page_id"],
            "page_title": page.get("params").get("title", default_title),
            "language": page["language"],
            "root_page_id": page["root_page"],
            "params": json.dumps(page["params"]),
            "hierarchy": page["hierarchy"],
            "hidden": hidden,
            # Force new linking in case the structure changed
            "childs": [],
            "parent": [],
        }

        db_create_or_update(Page, ["page_id"], new_page, nolog=True)
        db.session.flush()

        if len(page.get("parents")) > 1:
            for parent_id in page["parents"]:
                parent = generic_getter(Page, "page_id", parent_id)
                child = generic_getter(Page, "page_id", page["page_id"])

                if child not in parent.childs.all():
                    parent.childs.append(generic_getter(Page, "page_id", page["page_id"]))
                    db.session.flush()

    # Remove orphans
    for current in generic_getter(Page, all=True):
        if not current.parent.all() and not current.childs.all():
            db.session.delete(current)
            db.session.flush()


def db_insert_exercises(app, *args, **kwargs):
    exercise_json = f"{cfg.statics.get('base_url')}/hugo/exercises.json"
    exercises = extract_json_content(app, exercise_json)
    for exercise in exercises:
        db_create_or_update(Exercise, ["global_exercise_id"], exercise)


def db_insert_questionnaires(app, *args, **kwargs):
    questionnaire_json = f"{cfg.statics.get('base_url')}/hugo/questionnaires.json"
    questionnaires = extract_json_content(app, questionnaire_json)
    for questionnaire in questionnaires:
        new_questionnaire = {
            "global_questionnaire_id": questionnaire["global_questionnaire_id"],
            "page_title": questionnaire["page_title"],
            "parent_page_title": questionnaire["parent_page_title"],
            "root_weight": questionnaire["root_weight"],
            "parent_weight": questionnaire["parent_weight"],
            "child_weight": questionnaire["child_weight"],
            "order_weight": questionnaire["order_weight"],
        }

        db_create_or_update(Questionnaire, ["global_questionnaire_id"], new_questionnaire)
        db.session.flush()

        for language in questionnaire["questions"]:
            for question in questionnaire["questions"][language]:
                new_question = {
                    "global_question_id": question["global_question_id"],
                    "id": question["id"],
                    "question": question["question"],
                    "answer_options": json.dumps(question["answers"]),
                    "language": language,
                    "multiple": question.get("multiple") or False,
                    "global_questionnaire_id": questionnaire["global_questionnaire_id"],
                }

                db_create_or_update(QuestionnaireQuestion, ["global_question_id", "language"], new_question)


def db_create_or_update(db_model, filter_keys: list = [], passed_element: dict = None, nolog: bool = False) -> bool:
    # check if element already exists
    try:
        session = db.session.query(db_model)
        for filter_key in filter_keys:
            kwargs = {filter_key.strip(): passed_element[filter_key.strip()]}
            session = session.filter_by(**kwargs)
        current_db_entry = session.first()
    except Exception as e:
        logger.exception(e)
        return False

    if current_db_entry:
        # Update existing
        for key in passed_element:
            if getattr(current_db_entry, key) != passed_element[key]:
                setattr(current_db_entry, key, passed_element[key])
                db.session.flush()
                if not nolog:
                    logger.info(f"Updated: {key}")
    else:
        # Create new
        new_element = db_model()
        for key in passed_element:
            setattr(new_element, key, passed_element[key])
        db.session.add(new_element)
    try:
        db.session.commit()
    except Exception as e:
        logger.exception(e)
        return False
    return True


def db_create_venjix_execution(execution_uuid: str, user_id: int, script_name: str) -> bool:
    try:
        execution = VenjixExecution(
            script=script_name,
            execution_uuid=execution_uuid,
            user_id=user_id,
        )

        db.session.add(execution)
        db.session.commit()
        return True

    except Exception as e:
        logger.exception(e)


def db_update_venjix_execution(
    execution_uuid: str,
    connection_failed: bool = False,
    response_timestamp: str = None,
    response_content: str = None,
    completed: bool = False,
    msg: str = None,
    partial: bool = False,
) -> bool:
    try:
        execution = VenjixExecution.query.filter_by(execution_uuid=execution_uuid).first()
        for key, value in list(locals().items())[:-1]:
            if value:
                setattr(execution, key, value)
        db.session.commit()
        return True

    except Exception as e:
        logger.exception(e)
        return False


def db_get_running_executions_by_name(user_id: int, script: str) -> dict:
    try:
        running_executions = (
            VenjixExecution.query.filter_by(user_id=user_id)
            .filter_by(script=script)
            .filter_by(connection_failed=False)
            .filter_by(response_timestamp=None)
            .order_by(VenjixExecution.execution_timestamp.desc())
            .all()
        )
        return convert_to_dict(running_executions)

    except Exception as e:
        logger.exception(e)
        return None


def db_get_venjix_execution(execution_uuid: str) -> dict:
    try:
        execution = generic_getter(VenjixExecution, "execution_uuid", execution_uuid)
        return convert_to_dict(execution)

    except Exception as e:
        logger.exception(e)
        return None


def db_create_execution(exercise_type: str, global_exercise_id: str, data: dict, user_id: int, execution_uuid: str) -> bool:
    form_data = json.dumps(data, indent=4, sort_keys=False)

    try:
        exercise_id = db_get_exercise_by_global_exercise_id(global_exercise_id).id

        execution = Execution(
            exercise_type=exercise_type,
            script="script",
            form_data=form_data,
            execution_uuid=execution_uuid,
            user_id=user_id,
            exercise_id=exercise_id,
        )

        if exercise_type == "form":
            execution.completed = True
            execution.response_timestamp = datetime.now(timezone.utc)

        db.session.add(execution)
        db.session.commit()
        return True

    except Exception as e:
        logger.exception(e)
        return False


def db_create_comment(comment: str, page: str, user_id: int) -> bool:
    try:
        new_comment = {
            "user_id": user_id,
            "comment": comment,
            "page": page,
        }
        db_create_or_update(Comment, ["user_id", "page"], new_comment)
        return True

    except Exception as e:
        logger.exception(e)
        return False


def db_get_current_submissions(user_id: int, global_exercise_id: string) -> Tuple[dict, dict]:
    try:
        exercise = db_get_exercise_by_global_exercise_id(global_exercise_id)
        submissions = (
            db.session.query(Execution)
            .filter_by(user_id=user_id)
            .filter_by(exercise_id=exercise.id)
            .order_by(Execution.response_timestamp.desc(), Execution.execution_timestamp.desc())
            .all()
        )
        return submissions
    except Execution as e:
        logger.exception(e)
        return None, None


def db_get_exercise_by_name(exercise_name: str) -> dict:
    return generic_getter(Exercise, "exercise_name", exercise_name)


def db_get_exercise_by_global_exercise_id(global_exercise_id: str) -> dict:
    return generic_getter(Exercise, "global_exercise_id", global_exercise_id)


def db_get_questionnaire_by_global_questionnaire_id(global_questionnaire_id: str) -> dict:
    return generic_getter(Questionnaire, "global_questionnaire_id", global_questionnaire_id)


def db_get_questionnaire_question_by_global_question_id(global_question_id: str) -> dict:
    return generic_getter(QuestionnaireQuestion, "global_question_id", global_question_id)


def db_get_all_questionnaires_questions(global_questionnaire_id: str) -> dict:
    try:
        return (
            db.session.query(QuestionnaireQuestion)
            .filter_by(global_questionnaire_id=global_questionnaire_id)
            .order_by(QuestionnaireQuestion.local_question_id.asc())
            .all()
        )
    except Exception as e:
        logger.exception(e)
        return None


def db_get_questionnaire_results_by_global_question_id(global_question_id: str) -> dict:
    questionnaire_question = generic_getter(QuestionnaireQuestion, "global_question_id", global_question_id)
    questionnaire_answers = generic_getter(QuestionnaireAnswer, "global_question_id", global_question_id, all=True)

    labels = json.loads(questionnaire_question.answer_options)
    results = [0] * len(labels)

    for questionnaire_answer in questionnaire_answers:
        for answer in json.loads(questionnaire_answer.answers):
            results[answer] += 1

    return labels, results


def db_get_exercise_by_id(id: int) -> dict:
    return generic_getter(Exercise, "id", id)


def db_get_user_by_name(name: str) -> dict:
    return generic_getter(User, "name", name)


def db_get_user_by_id(id: int) -> dict:
    return generic_getter(User, "id", id)


def db_get_users_by_role(role: str) -> list:
    return generic_getter(User, "role", role, all=True)


def db_get_admin_users() -> list:
    return generic_getter(User, "admin", True, all=True)


def db_get_all_users() -> list:
    return generic_getter(User, "role", "participant", all=True)


def db_get_all_userids() -> list:
    return [id[0] for id in db.session.query(User).with_entities(User.id).all()]


def db_get_all_exercises() -> list:
    return generic_getter(Exercise, all=True)


def db_get_all_comments() -> list:
    return generic_getter(Comment, all=True)


def db_get_comment_by_id(id: int) -> dict:
    return generic_getter(Comment, "id", id)


def db_get_comments_by_userid(id: int) -> dict:
    return generic_getter(Comment, "user_id", id, all=True)


def db_get_all_pages() -> dict:
    return generic_getter(Page, all=True)


def db_get_page_by_id(page_id) -> dict:
    return generic_getter(Page, "page_id", page_id)


def db_get_all_active_pages() -> dict:
    active_pages = []
    db_active_pages = generic_getter(Page, "hidden", False, all=True)
    for page in db_active_pages:
        hidden = False
        for parent in page.parent.all():
            if parent not in db_active_pages:
                hidden = True
        if not hidden:
            active_pages.append(page)

    return active_pages


def get_direct_childs(page, usergroups):
    childs = {}

    for child in page.childs.all():
        if child.hierarchy <= page.hierarchy + 1:
            if "admins" in usergroups or any(group in usergroups for group in json.loads(child.params).get("groups", ["all"])):
                hidden = child.hidden
            else:
                hidden = True

            childs[f"{child.page_title}_{child.page_id}"] = {
                "page_id": child.page_id,
                "params": child.params,
                "hidden": hidden,
                "childs": get_direct_childs(child, usergroups),
            }

    return childs


def db_get_page_tree(user) -> dict:
    tree_roots = generic_getter(Page, "hierarchy", 0, all=True)
    tree = {}

    for root in tree_roots:
        if not root.page_title == "root":
            tree[f"{root.page_title}_{root.page_id}"] = {
                "page_id": root.page_id,
                "params": root.params,
                "hidden": root.hidden,
                "childs": get_direct_childs(root, db_get_usergroups_by_user(user)),
            }

    return tree


def db_toggle_page_visibility(page_id):
    page = generic_getter(Page, "page_id", page_id)
    if page:
        page.hidden = not page.hidden
        db.session.commit()
        return True
    return False


def db_get_exercise_groups() -> list:
    try:
        session = db.session.query(Exercise.parent_page_title).group_by(Exercise.parent_page_title).all()
        return [groupname for groupname, in session]
    except Exception as e:
        logger.exception(e)
        return None


def db_get_userids_by_usergroups(usergroups) -> list:
    try:
        userids = []
        for groupname in usergroups:
            group = generic_getter(Usergroup, "name", groupname)
            if group:
                for groupuser in group.users:
                    userids.append(groupuser.user.id)

        return userids

    except Exception as e:
        logger.exception(e)
        return None


def db_get_all_usergroups() -> list:
    try:
        usergroups = {}
        session = db.session.query(Usergroup).all()
        for usergroup in session:
            usergroups[usergroup.name] = []
            for userassociation in usergroup.users:
                usergroups[usergroup.name].append(userassociation.user.id)
        return usergroups
    except Exception as e:
        logger.exception(e)
        return None


def db_get_usergroup_by_name(groupname: str) -> list:
    try:
        usergroup = []
        session = db.session.query(Usergroup).filter_by(name=groupname).first()
        for userassociation in session.users:
            usergroup.append(userassociation.user.id)
        return usergroup
    except Exception as e:
        logger.exception(e)
        return None


def db_get_usergroups_by_user(user: User) -> list:
    try:
        usergroups = []
        for g in user.usergroups:
            usergroups.append(g.usergroup.name)
        return usergroups
    except Exception as e:
        logger.exception(e)
        return []


def db_get_exercises_by_group(parent_page_title: str) -> list:
    try:
        session = db.session.query(Exercise).filter_by(parent_page_title=parent_page_title)
        return session.all()
    except Exception as e:
        logger.exception(e)
        return None


def generic_getter(db_model, filter_keys: list = [], filter_value: list = [], all: bool = False) -> dict:
    try:
        if not isinstance(filter_keys, list):
            filter_keys = [filter_keys]
            filter_value = [filter_value]

        session = db.session.query(db_model)

        for idx, filter_key in enumerate(filter_keys):
            kwargs = {filter_key.strip(): filter_value[idx]}
            session = session.filter_by(**kwargs)
        return session.all() if all else session.first()
    except Exception as e:
        logger.exception(e)
        return None


def db_convert_usernames_to_ids(usernames: list = []) -> list:
    user_ids = [user.id for user in generic_getter(User, all=True) if user.name in usernames]
    return user_ids


def db_convert_ids_to_usernames(user_ids: list = []) -> list:
    usernames = [user.name for user in generic_getter(User, all=True) if user.id in user_ids]
    return usernames


def db_get_executions_by_user_exercise(user_id: int, exercise_id: int) -> list:
    try:
        return (
            db.session.query(Execution)
            .filter_by(user_id=user_id)
            .filter_by(exercise_id=exercise_id)
            .order_by(Execution.execution_timestamp.desc())
            .all()
        )
    except Exception as e:
        logger.exception(e)
        return None


def db_get_completed_state(user_id: int, exercise_id: int) -> dict:
    try:
        return (
            db.session.query(User)
            .filter_by(id=user_id)
            .join(Execution)
            .filter_by(exercise_id=exercise_id)
            .with_entities(Execution.completed)
            .all()
        )
    except Exception as e:
        logger.exception(e)
        return None


def db_create_file(filename: str, user_id: int) -> str:
    try:
        filename_hash = hashlib.md5(filename.encode("utf-8")).hexdigest()
        file = Attachment(filename=filename, filename_hash=filename_hash, user_id=user_id)
        db.session.add(file)
        db.session.commit()
        return filename_hash

    except Exception as e:
        logger.exception(e)
        return None


def db_get_filename_from_hash(filename_hash):
    try:
        return db.session.query(Attachment).filter_by(filename_hash=filename_hash).first().filename
    except Exception as e:
        logger.exception(e)
        return None


def db_get_cache_by_ids(user_id: int, global_exercise_id: str) -> dict:
    try:
        return db.session.query(Cache).filter_by(user_id=user_id).filter_by(global_exercise_id=global_exercise_id).first()
    except Exception as e:
        logger.exception(e)
        return None


def db_get_all_exercises_sorted() -> list:
    try:
        return db.session.query(Exercise).order_by(Exercise.order_weight.asc()).all()
    except Exception as e:
        logger.exception(e)
        return None


def db_get_all_questionnaires_sorted() -> list:
    try:
        return db.session.query(Questionnaire).order_by(Questionnaire.order_weight.asc()).all()
    except Exception as e:
        logger.exception(e)
        return None


def db_get_grouped_questionnaires() -> list:
    try:
        questionnaires = db.session.query(Questionnaire).order_by(Questionnaire.order_weight.asc()).all()
        grouped_questionnaires = []

        for questionnaire in questionnaires:
            # extract questions
            questions = []
            for question in questionnaire.questions:
                questions.append(
                    {
                        "id": question.id,
                        "question": question.question,
                        "answer_options": question.answer_options,
                        "language": question.language,
                        "active": question.active,
                        "global_question_id": question.global_question_id,
                    }
                )

            questionnaire_object = convert_to_dict(questionnaire)

            # append questions
            questionnaire_object["questions"] = questions
            grouped_questionnaires.append(questionnaire_object)

        return grouped_questionnaires

    except Exception as e:
        logger.exception(e)
        return None


def db_activate_questioniare_question(global_question_id) -> bool:
    try:
        question = db.session.query(QuestionnaireQuestion).filter_by(global_question_id=global_question_id).first()

        # Set active state
        setattr(question, "active", True)
        db.session.flush()
        db.session.commit()

        questionnaire = db.session.query(Questionnaire).filter_by(global_questionnaire_id=question.global_questionnaire_id).first()
        question_dict = convert_to_dict(question)

        # Adjust dict
        question_dict["multiple"] = bool(question_dict.get("multiple"))
        question_dict["active"] = bool(question_dict.get("active"))
        question_dict["page_title"] = questionnaire.page_title

        return question_dict

    except Exception as e:
        logger.exception(e)
        return False


def db_create_questionnaire_answer(global_question_id: str, answers: str, user_id: int) -> bool:
    try:
        if isinstance(answers, int):
            answers = [answers]

        submission = QuestionnaireAnswer(answers=json.dumps(answers), user_id=user_id, global_question_id=global_question_id)

        db.session.add(submission)
        db.session.commit()
        return True

    except Exception as e:
        logger.exception(e)
        return False


def db_get_questionnaire_question_answers_by_user(global_question_id: str, user_id: int) -> list:
    answers = generic_getter(QuestionnaireAnswer, ["global_question_id", "user_id"], [global_question_id, user_id], all=True)
    return answers


def db_get_completion_percentage(exercise_id):
    users = db_get_all_users()

    try:
        executions = (
            db.session.query(Execution)
            .filter_by(exercise_id=exercise_id)
            .join(User)
            .group_by(User.id)
            .with_entities(db.func.max(Execution.completed))
            .all()
        )
        return len(executions) / len(users) * 100

    except Exception as e:
        logger.exception(e)
        return 0


def db_create_notification(sse_Event: SSE_Event) -> bool:
    try:
        notification = Notification(
            event=sse_Event.event,
            message=sse_Event.message,
            _type=sse_Event._type,
            recipients=json.dumps(sse_Event.recipients),
            positions=json.dumps(sse_Event.positions),
        )
        db.session.add(notification)
        db.session.commit()

        return notification.id

    except Exception as e:
        logger.exception(e)
        return False


def db_get_last_notification() -> dict:
    try:
        # allow to execute from within sse context
        from backend import app

        with app.app_context():
            session = db.session.query(Notification).order_by(Notification.id.desc())
            notification = session.first()
            return notification

    except Exception as e:
        logger.exception(e)
        return False


def db_get_notification_by_id(notification_id: int) -> dict:
    try:
        # allow to execute from within sse context
        from backend import app

        with app.app_context():
            session = db.session.query(Notification)
            notification = session.filter_by(id=notification_id).first()

            return notification

    except Exception as e:
        logger.exception(e)
        return False


def db_get_all_notifications() -> dict:
    try:
        session = db.session.query(Notification)
        notifications = session.all()

        return notifications

    except Exception as e:
        logger.exception(e)
        return False


def db_get_notifications_by_user(user_id: int) -> dict:
    try:
        session = db.session.query(Notification).all()

        notifications = []
        for notification in session:
            # Convert json lists to lists
            notification.recipients = json.loads(notification.recipients)
            notification.positions = json.loads(notification.positions)
            notification._type = notification._type
            if user_id in notification.recipients:
                notifications.append(notification)

        return notifications

    except Exception as e:
        logger.exception(e)
        return False
