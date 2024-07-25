import logging
import os

# Ensure logs directory exists
os.makedirs('logs', exist_ok=True)

# General logger
general_logger = logging.getLogger('general')
general_logger.setLevel(logging.INFO)
general_handler = logging.FileHandler('logs/general.log')
general_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
general_logger.addHandler(general_handler)

# Error logger
error_logger = logging.getLogger('error')
error_logger.setLevel(logging.ERROR)
error_handler = logging.FileHandler('logs/error.log')
error_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
error_logger.addHandler(error_handler)
