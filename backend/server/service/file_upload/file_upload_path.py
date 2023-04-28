from flask import Blueprint
from .file_instance import file_instance

file_upload = Blueprint('file_upload', __name__)

# path

@file_upload.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    if file:
        content = file.read().decode('utf-8')
        file_instance(file)
        return 'File upload success.'
    else:
        return 'File upload failed.'