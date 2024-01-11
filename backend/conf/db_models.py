from backend.database import db
from sqlalchemy import func


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)
    role = db.Column(db.String(20), unique=False, nullable=False, default="participant")
    admin = db.Column(db.Integer, nullable=False, default=0)
    meta = db.Column(db.String(), unique=False, nullable=True)
    executions = db.relationship("Execution", backref="user", lazy=True)
    usergroups = db.relationship("UsergroupAssociation", back_populates="user")


class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    event = db.Column(db.String(120), nullable=True)
    _type = db.Column(db.String(120), nullable=True)
    message = db.Column(db.String(240), nullable=True)
    recipients = db.Column(db.String(120), nullable=True)
    positions = db.Column(db.String(120), nullable=True)


class Usergroup(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)
    users = db.relationship("UsergroupAssociation", back_populates="usergroup")


class UsergroupAssociation(db.Model):
    usergroup_id = db.Column(db.ForeignKey("usergroup.id"), primary_key=True)
    user_id = db.Column(db.ForeignKey("user.id"), primary_key=True)
    usergroup = db.relationship("Usergroup", back_populates="users")
    user = db.relationship("User", back_populates="usergroups")


class Execution(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    exercise_type = db.Column(db.String(120), nullable=False)
    script = db.Column(db.String(120), nullable=True)
    execution_timestamp = db.Column(db.DateTime, nullable=False, default=func.current_timestamp())
    response_timestamp = db.Column(db.DateTime, nullable=True)
    response_content = db.Column(db.Text, nullable=True)
    form_data = db.Column(db.String(), nullable=True)
    msg = db.Column(db.String(240), nullable=True)
    execution_uuid = db.Column(db.String(120), unique=True, nullable=True)
    completed = db.Column(db.Integer, nullable=False, default=0)
    partial = db.Column(db.Integer, nullable=False, default=0)
    connection_failed = db.Column(db.Integer, nullable=False, default=0)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    exercise_id = db.Column(db.Integer, db.ForeignKey("exercise.id"), nullable=False)


class Attachment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(120), nullable=False)
    filename_hash = db.Column(db.String(120), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)


class Exercise(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    global_exercise_id = db.Column(db.String(32), nullable=False)
    local_exercise_id = db.Column(db.Integer, nullable=False)
    exercise_type = db.Column(db.String(120), nullable=False)
    exercise_name = db.Column(db.String(120), nullable=False)
    page_title = db.Column(db.String(120), nullable=False)
    parent_page_title = db.Column(db.String(120), nullable=False)
    root_weight = db.Column(db.Integer, nullable=False)
    parent_weight = db.Column(db.Integer, nullable=False)
    child_weight = db.Column(db.Integer, nullable=False)
    order_weight = db.Column(db.Integer, nullable=False)
    executions = db.relationship("Execution", backref="exercise", lazy=True)


parent_child_relationship = db.Table(
    "parent_child_relationship",
    db.Column("parent_id", db.Integer, db.ForeignKey("page.id"), primary_key=True),
    db.Column("child_id", db.Integer, db.ForeignKey("page.id"), primary_key=True),
)


class Page(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    page_id = db.Column(db.String(32), nullable=False)
    page_title = db.Column(db.String(120), nullable=True)
    language = db.Column(db.String(3), nullable=True)
    root_page_id = db.Column(db.String(32), nullable=True)
    params = db.Column(db.String(320), nullable=True)
    hierarchy = db.Column(db.Integer, nullable=True)
    hidden = db.Column(db.Integer, nullable=False, default=0)

    childs = db.relationship(
        "Page",
        secondary=parent_child_relationship,
        primaryjoin=(parent_child_relationship.c.parent_id == id),
        secondaryjoin=(parent_child_relationship.c.child_id == id),
        backref=db.backref("parent", lazy="dynamic"),
        lazy="dynamic",
    )


class Cache(db.Model):
    user_id = db.Column(db.ForeignKey("user.id"), primary_key=True)
    global_exercise_id = db.Column(db.ForeignKey("exercise.global_exercise_id"), primary_key=True)
    form_data = db.Column(db.String(), nullable=True)


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String(), nullable=False)
    page = db.Column(db.String(), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)


class Questionnaire(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    global_questionnaire_id = db.Column(db.String(32), nullable=False)
    page_title = db.Column(db.String(120), nullable=False)
    parent_page_title = db.Column(db.String(120), nullable=False)
    root_weight = db.Column(db.Integer, nullable=False)
    parent_weight = db.Column(db.Integer, nullable=False)
    child_weight = db.Column(db.Integer, nullable=False)
    order_weight = db.Column(db.Integer, nullable=False)
    questions = db.relationship("QuestionnaireQuestion", backref="questionnaire", lazy=True)


class QuestionnaireQuestion(db.Model):
    global_question_id = db.Column(db.String(32), primary_key=True)
    id = db.Column(db.Integer, nullable=False)
    question = db.Column(db.String(), nullable=False)
    answer_options = db.Column(db.String(), nullable=False)
    language = db.Column(db.String(), nullable=False, primary_key=True)
    multiple = db.Column(db.Integer, nullable=False, default=1)
    active = db.Column(db.Integer, nullable=False, default=0)
    global_questionnaire_id = db.Column(db.String(), db.ForeignKey("questionnaire.global_questionnaire_id"), primary_key=True)


class QuestionnaireAnswer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    answers = db.Column(db.String(), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=func.current_timestamp())
    global_question_id = db.Column(db.Integer, db.ForeignKey("questionnaire_question.global_question_id"), nullable=False)


class TokenBlocklist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(36), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)


class VenjixExecution(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    script = db.Column(db.String(120), nullable=True)
    execution_timestamp = db.Column(db.DateTime, nullable=False, default=func.current_timestamp())
    response_timestamp = db.Column(db.DateTime, nullable=True)
    response_content = db.Column(db.Text, nullable=True)
    msg = db.Column(db.String(240), nullable=True)
    execution_uuid = db.Column(db.String(120), unique=True, nullable=True)
    completed = db.Column(db.Integer, nullable=False, default=0)
    partial = db.Column(db.Integer, nullable=False, default=0)
    connection_failed = db.Column(db.Integer, nullable=False, default=0)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
