from flask import Flask
from flask_cors import CORS
from config import UPLOAD_FOLDER, DOWNLOAD_FOLDER, MAX_CONTENT_LENGTH, SQLALCHEMY_DATABASE_URI
from routes import files_blueprint, database_blueprint
import database
import middleware
import error_handlers

app = Flask(__name__)
CORS(app, resources={r"/files/*": {"origins": "*"}})
CORS(app, resources={r"/database/*": {"origins": "*"}})

# Configuration
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['DOWNLOAD_FOLDER'] = DOWNLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI

# Register middleware
app.before_request(middleware.before_request_func)
app.after_request(middleware.after_request_func)

# Register blueprints
app.register_blueprint(files_blueprint)
app.register_blueprint(database_blueprint)

# Register error handlers
app.register_error_handler(400, error_handlers.handle_bad_request_error)
app.register_error_handler(404, error_handlers.handle_not_found_error)
app.register_error_handler(413, error_handlers.handle_request_entity_too_large_error)
app.register_error_handler(Exception, error_handlers.handle_exception)

if __name__ == '__main__':
    database.init_db(app)
    app.run(debug=True)
