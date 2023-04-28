from flask import Blueprint
from ...service.file_upload.file_instance import file_instance
from ....core.lib.hash_util import hash_string

file_upload = Blueprint('file_upload', __name__)

# path

@file_upload.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    
    if file:
        file_instance(file)
        return hash_string().hash_MD5(file.filename)
    else:
        return 'File upload failed.'