from flask import request
from logger import general_logger

def before_request_func():
    general_logger.info(f"Handling request to {request.path}")

def after_request_func(response):
    general_logger.info(f"Completed request to {request.path} with status {response.status_code}")
    return response
