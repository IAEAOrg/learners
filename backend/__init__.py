from flask import Flask
from backend.logger import STARTUP, logger


def main():
    app = Flask(__name__)

    welcome_text = """

         _      ______          _____  _   _ ______ _____   _____
        | |    |  ____|   /\   |  __ \| \ | |  ____|  __ \ / ____|
        | |    | |__     /  \  | |__) |  \| | |__  | |__) | (___
        | |    |  __|   / /\ \ |  _  /| . ` |  __| |  _  / \___ \\
        | |____| |____ / ____ \| | \ \| |\  | |____| | \ \ ____) |
        |______|______/_/    \_\_|  \_\_| \_|______|_|  \_\_____/

        Learners - web framework developed by the International Atomic Energy Agency (IAEA)
        and the Austrian Institute of Technology (AIT) for streamlined training courses,
        with a specific emphasis on information and computer security.

        """

    logger.log(STARTUP, welcome_text)

    with app.app_context():
        from backend.conf.config import build_config

        build_config(app)
        from backend.database import build_db

        build_db(app)
        from backend.jwt_manager import init_jwt

        init_jwt(app)

        from flask_cors import CORS

        CORS(app)

    import backend.routes as routes

    app.register_blueprint(routes.authentication_api)
    app.register_blueprint(routes.notifications_api)
    app.register_blueprint(routes.stream_api)
    app.register_blueprint(routes.questionnaires_api)
    app.register_blueprint(routes.executions_api)
    app.register_blueprint(routes.comments_api)
    app.register_blueprint(routes.cache_api)
    app.register_blueprint(routes.callback_api)
    app.register_blueprint(routes.statics_api)
    app.register_blueprint(routes.setup_api)
    app.register_blueprint(routes.exercises_api)
    app.register_blueprint(routes.users_api)
    app.register_blueprint(routes.pages_api)

    return app


app = main()
