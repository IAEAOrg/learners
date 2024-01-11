import contextlib
import json
import os
from datetime import timedelta
import string

from backend.logger import logger
from strictyaml import YAMLError, load

cfg = None


class Configuration:
    def __init__(self):
        config_file = os.getenv("LEARNERS_CONFIG") or os.path.join(os.getcwd(), "config.yml")

        learners_config = {}
        from backend.conf.config_schema import config_schema

        try:
            with open(config_file, "r") as stream:
                yaml_config = stream.read()
                learners_config = load(yaml_config, config_schema).data
        except YAMLError as yamlerr:
            logger.exception(yamlerr)
            raise
        except EnvironmentError as enverr:
            logger.exception(enverr)
            raise

        self.jwt_secret_key = learners_config.get("jwt").get("jwt_secret_key")
        self.jwt_access_token_expires = timedelta(minutes=learners_config.get("jwt").get("jwt_access_token_duration"))
        self.jwt_for_vnc_access = learners_config.get("jwt").get("jwt_for_vnc_access")

        self.db_uri = learners_config.get("database").get("db_uri")
        self.novnc = {"server": learners_config.get("novnc").get("server")}

        self.users = json.loads(json.dumps(learners_config.get("users")).replace("DEFAULT-VNC-SERVER", self.novnc.get("server")))

        for _, user in self.users.items():
            user.update({"admin": user["role"] in ["admin", "instructor"]})
            user.update({"meta": json.dumps(user.get("meta", {}))})

        self.venjix = {
            "auth_secret": learners_config.get("venjix").get("auth_secret"),
            "url": learners_config.get("venjix").get("url"),
            "headers": {"Content-type": "application/json", "Authorization": f"Bearer {learners_config.get('venjix').get('auth_secret')}"},
        }

        self.theme = learners_config.get("learners").get("theme")

        self.logo = learners_config.get("learners").get("logo")
        self.headline = learners_config.get("learners").get("headline")
        self.welcomeText = learners_config.get("learners").get("welcomeText")

        self.landingpage = learners_config.get("learners").get("landingpage")
        self.language_code = learners_config.get("learners").get("language_code")

        self.statics = {
            "base_url": learners_config.get("statics").get("directory"),
            "serve_mode": learners_config.get("statics").get("serve_mode"),
        }

        self.upload_folder = learners_config.get("learners").get("upload_folder")
        self.allowed_extensions = learners_config.get("learners").get("upload_extensions")
        self.init_notifications = learners_config.get("init_notifications") or []

        self.tabs = learners_config.get("tabs") or {}
        for tabname, tab in self.tabs.items():
            if not tab.get("show"):
                tab.update({"show": ["all"]})


def build_config(app):
    global cfg
    cfg = Configuration()

    config_app(app)

    if os.getenv("REMOVE_DB"):
        logger.warning(" ****** REMOVE_DB is set. Deleting DB file ****** ")

        db_path = (cfg.db_uri).split("sqlite:///")[1]
        if not (db_path).startswith("/"):
            db_path = os.path.join(app.root_path, db_path)

        with contextlib.suppress(Exception):
            os.remove(db_path)


def config_app(app):
    app.config["JSON_SORT_KEYS"] = False
    app.config["SQLALCHEMY_DATABASE_URI"] = cfg.db_uri
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    app.config["JWT_ACCESS_COOKIE_NAME"] = "jwt_cookie"
    app.config["JWT_QUERY_STRING_NAME"] = "jwt"
    app.config["JWT_SECRET_KEY"] = cfg.jwt_secret_key
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = cfg.jwt_access_token_expires
    app.config["JWT_TOKEN_LOCATION"] = ["query_string", "headers", "cookies"]

    app.config["CORS_SUPPORTS_CREDENTIALS"] = True
