import os
from datetime import datetime
from flask import Blueprint, request, send_from_directory, jsonify, url_for
from werkzeug.utils import secure_filename
from config import UPLOAD_FOLDER, DOWNLOAD_FOLDER, ALLOWED_EXTENSIONS
from flask import Blueprint, jsonify, request
from database import File, get_files, add_file  # Adjust import as needed
from excel_dosa import result_analysis

from logger import general_logger


files_blueprint = Blueprint('files', __name__, url_prefix='/files')
database_blueprint = Blueprint('database', __name__, url_prefix='/database')

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_saved_filename(original_filename):
    # Replace this with your actual logic for determining the saved filename
    return secure_filename(original_filename)

@files_blueprint.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part in the request'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file and allowed_file(file.filename):
        original_filename = file.filename
        saved_filename = get_saved_filename(original_filename)
        filepath = os.path.join(UPLOAD_FOLDER, saved_filename)
        file.save(filepath)
        general_logger.info(f"File {original_filename} successfully uploaded as {saved_filename}")

        # Process the file
        processed_filename = result_analysis(filepath, DOWNLOAD_FOLDER)
        general_logger.info(f"File {saved_filename} successfully processed to {processed_filename}")

        # Store New File in DB
        full_path = os.path.join(filepath, processed_filename)
        if os.path.exists(full_path):
           add_file(processed_filename, datetime.now(), 'CSE')
        return jsonify({'message': 'File successfully uploaded and processed', 'processed_file': processed_filename}), 201

    return jsonify({'error': 'File type not allowed'}), 400

@files_blueprint.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    try:
        general_logger.info(f"File {filename} successfully downloaded")
        return send_from_directory(DOWNLOAD_FOLDER, filename, as_attachment=True)
    except FileNotFoundError:
        return jsonify({'error': 'File not found'}), 404


@database_blueprint.route('/history', methods=['GET'])
def view_history():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    sort_by = request.args.get('sort_by', 'created_on')
    order = request.args.get('order', 'desc')

    file_page = get_files(page=page, per_page=per_page, sort_by=sort_by, order=order)
    
    files = [
        {
            'id': file.id,
            'name': file.name,
            'created_on': file.created_on.isoformat(),
            'department': file.department_code,
            'file_url': url_for('files.download_file', filename=file.name, _external=True)
        }
        for file in file_page.items
    ]

    return jsonify({
        'files': files,
        'pagination': {
            'page': file_page.page,
            'per_page': file_page.per_page,
            'totalPages': file_page.total,
            'pages': file_page.pages,
            'has_prev': file_page.has_prev,
            'has_next': file_page.has_next
        }
    })