import json
import string


class SubmissionResponse:
    def __init__(
        self,
        completed: bool = False,
        executed: bool = False,
        msg: string = "",
        response_timestamp: string = "",
        connection_failed: bool = False,
        history: list = [],
        partial: bool = False,
        exercise_type: string = "",
        filename: string = "",
        uuid: string = "",
    ):
        self.completed = completed
        self.executed = executed
        self.msg = msg
        self.response_timestamp = response_timestamp
        self.connection_failed = connection_failed
        self.history = history
        self.partial = partial
        self.exercise_type = exercise_type
        self.filename = filename
        self.uuid = uuid

    def update(self, executions) -> dict:
        if not len(executions):
            return

        if isinstance(executions, list):
            from backend.functions.helpers import extract_history

            last_execution = executions[0]
            self.history = extract_history(executions)
        else:
            last_execution = executions

        self.msg = last_execution.get("msg")
        self.response_timestamp = last_execution.get("response_timestamp")
        self.connection_failed = last_execution.get("connection_failed")
        self.partial = last_execution.get("partial")
        self.completed = last_execution.get("completed")
        self.exercise_type = last_execution.get("exercise_type")

        if self.connection_failed:
            self.executed = False
            self.msg = "Connection failed."

        if self.response_timestamp:
            if self.exercise_type == "form":
                self.executed = True
            else:
                # Get error msg
                error = json.loads(last_execution.get("response_content")).get("stderr")
                self.executed = bool(not error)
                # Apply error msg to msg if none given
                self.msg = self.msg or error
