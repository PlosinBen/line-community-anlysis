from flask import Blueprint
from ...service.file_upload.file_instance import file_instance

file_upload = Blueprint('file_upload', __name__)

# path

@file_upload.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    if file:
        file_instance(file)
        return 'File upload success.'
    else:
        return 'File upload failed.'