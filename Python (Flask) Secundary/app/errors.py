from flask import Blueprint, jsonify
from werkzeug.exceptions import HTTPException

errors_bp = Blueprint("errors", __name__)

@errors_bp.app_errorhandler(Exception)
def handle_error(e: Exception):
    status = 500
    payload = {
        "timestamp": __import__("datetime").datetime.utcnow().isoformat() + "Z",
        "status": status,
        "message": "Internal server error",
    }
    if isinstance(e, HTTPException):
        status = e.code or 500
        msg = e.description or e.name
        payload.update({"status": status, "message": msg})
    else:
        payload["error"] = e.__class__.__name__
        if __import__("os").getenv("NODE_ENV") != "production":
            payload["stack"] = str(e)
    return jsonify(payload), status
