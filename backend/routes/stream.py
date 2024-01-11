from backend.classes.SSE import sse

from flask import Blueprint, Response
from flask_jwt_extended import jwt_required, current_user

stream_api = Blueprint("stream_api", __name__)


@stream_api.route("/stream")
@jwt_required()
def stream():
    def eventStream(user_id):
        sse_queue = sse.listen()

        while True:
            notification = sse_queue.get()
            if user_id in notification.recipients:
                msg = f"event: {notification.event}\ndata:{ notification.toJson() }\n\n"
                yield msg

    return Response(eventStream(current_user.id), mimetype="text/event-stream")
