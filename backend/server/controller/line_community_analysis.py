from flask import Blueprint, request, redirect, FileStorage
from werkzeug.utils import secure_filename

line_community_analysis = Blueprint('line_community_analysis', __name__)


@line_community_analysis.post('/')
def upload_line_community_file():
    file_column_name = 'file'
    if file_column_name not in request.files or request.files[file_column_name].filename == '':
        return "", 400

    file = request.files[file_column_name]

    pass


@line_community_analysis.get('/<hash_str>')
def get_basic_analysis():
    pass


@line_community_analysis.get('/<hash_str>/chart')
def chart():
    pass


@line_community_analysis.get('/<hash_str>/world_cloud')
def word_cloud():
    pass
