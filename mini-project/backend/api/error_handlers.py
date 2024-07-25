from flask import jsonify
from werkzeug.exceptions import HTTPException
from logger import error_logger

def handle_bad_request_error(error):
    error_logger.error(f"Bad request: {error}")
    return jsonify({'error': 'Bad request', 'message': str(error)}), 400

def handle_not_found_error(error):
    error_logger.error(f"Not found: {error}")
    return jsonify({'error': 'Not found', 'message': str(error)}), 404

def handle_request_entity_too_large_error(error):
    error_logger.error(f"File too large: {error}")
    return jsonify({'error': 'File too large', 'message': 'The file is too large'}), 413

def handle_exception(e):
    code = 500
    if isinstance(e, HTTPException):
        code = e.code
    error_logger.error(f"Internal server error: {e}")
    return jsonify({'error': 'Internal server error', 'message': str(e)}), code
