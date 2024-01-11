import json
import time
from typing import Tuple

import requests
from backend.logger import logger
from backend.conf.config import cfg
from backend.functions.database import db_get_venjix_execution, db_update_venjix_execution


def call_venjix(username: str, script: str, execution_uuid: str) -> Tuple[bool, bool]:
    try:
        response = requests.post(
            # TODO: Remove verify line
            verify=False,
            url=f"{cfg.venjix.get('url')}/{script}",
            headers=cfg.venjix.get("headers"),
            data=json.dumps(
                {
                    "script": script,
                    "user_id": username,
                    "callback": f"/callback/{execution_uuid}",
                }
            ),
        )

        resp = response.json()
        if response.status_code != 200:
            connected = False
            executed = False
            msg = f"{response.status_code}: {resp['response']}"
        else:
            connected = True
            executed = bool(resp["response"] == "script started")
            msg = resp.get("msg") or None

    except Exception as connection_exception:
        logger.exception(connection_exception)
        connected = False
        executed = False
        msg = "Connection failed"

    db_update_venjix_execution(execution_uuid, connection_failed=(not connected), msg=msg)

    return connected, executed


def wait_for_venjix_response(execution_uuid: str) -> dict:
    while True:
        time.sleep(0.5)

        try:
            execution = db_get_venjix_execution(execution_uuid)
            if execution["response_timestamp"] or execution["connection_failed"]:
                if execution["connection_failed"]:
                    execution["executed"] = False
                    execution["msg"] = "Connection failed."
                else:
                    # Get error msg
                    error = json.loads(execution["response_content"]).get("stderr")
                    execution["executed"] = bool(not error)
                    # Apply error msg to msg if none given
                    execution["msg"] = execution["msg"] or error

                return execution

        except Exception as e:
            logger.exception(e)
            return None
