import logging
import os
from logging.handlers import RotatingFileHandler
from uuid import UUID

from flask import Blueprint, jsonify
from werkzeug.exceptions import HTTPException

import logic.vars as vars
from logic.controller import blue_print as controller_blue_print

_LOGGER: logging.Logger = None
_APP = None


def config_flask_app(app):

    global _APP
    _APP = app

    error_handler_bp = Blueprint('handlers', __name__)

    @error_handler_bp.app_errorhandler(HTTPException)
    def handle_http(httpe):
        return '', httpe.code

    @error_handler_bp.app_errorhandler(Exception)
    def handle_exception(e: Exception):
        logger().exception(e)
        return jsonify(e.args), 500

    _APP.register_blueprint(error_handler_bp)
    _APP.register_blueprint(controller_blue_print)


def logger() -> logging.Logger:

    if not os.path.exists(vars.LOG_DIR):
        os.makedirs(vars.LOG_DIR, exist_ok=True)

    global _LOGGER

    if _LOGGER:
        return _LOGGER

    formatter = logging.Formatter(
        '%(asctime)s - %(name)s (%(process)d) - %(levelname)s - %(message)s')

    rotating = RotatingFileHandler(
        f'{vars.LOG_DIR}/app.log', maxBytes=vars.LOG_MAX_KB * 1000, backupCount=vars.LOG_BACKUP_COUNT)
    rotating.setLevel(vars.LOG_LEVEL)
    rotating.setFormatter(formatter)

    sh = logging.StreamHandler()
    sh.setLevel(vars.LOG_LEVEL)
    sh.setFormatter(formatter)

    _LOGGER = logging.getLogger("app")
    _LOGGER.setLevel(vars.LOG_LEVEL)
    _LOGGER.addHandler(rotating)
    _LOGGER.addHandler(sh)

    return _LOGGER


def get_raspberry_uuid() -> UUID:
    return UUID('a367742e-4121-4365-ad10-863ce98ad4e3')
