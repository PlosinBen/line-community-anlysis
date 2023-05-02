from os import getenv
import random
import string
from flask import Blueprint, request, jsonify, make_response
from pathlib import Path
from ..service import line_community
from ...core.lib.config import config

line_community_analysis = Blueprint('line_community_analysis', __name__)


def _get_random_string(length: int = 10) -> str:
    return ''.join(random.choice(string.ascii_letters + string.digits) for x in range(10))


@line_community_analysis.route('/line_community_analysis', methods=['POST'])
def upload_line_community_file():
    file_column_name = 'file'
    if file_column_name not in request.files or request.files[file_column_name].filename == '':
        return "", 400

    file_path = Path(config.data_path) / 'upload'
    if not file_path.exists():
        file_path.mkdir()

    extension_name = request.files[file_column_name].filename.split('.')[-1]

    upload_file = file_path / '{}.{}'.format(
        _get_random_string(),
        extension_name
    )

    request.files[file_column_name].save(upload_file)

    hash_name = line_community.save_message_data(upload_file)

    line_community.analysis(hash_name)

    return jsonify(
        hash=hash_name
    )


@line_community_analysis.get('/line_community_analysis/<hash_name>')
def get_basic_analysis(hash_name: str):
    try:
        return jsonify(
            analysis=line_community.analysis(hash_name)
        )
    except line_community.FileNotExistsException:
        return '', 404
    except line_community.FileProcessing:
        return jsonify(
            status='processing'
        )


@line_community_analysis.get('/line_community_analysis/<hash_name>/chart')
def chart(hash_name: str):
    try:
        return jsonify(
            messages=line_community.get_message_data(Path(getenv('DATA_PATH')) / 'messages' / hash_name)
        )
    except line_community.FileNotExistsException:
        return None, 404


@line_community_analysis.get('/line_community_analysis/<hash_name>/world_cloud')
def word_cloud(hash_name: str):
    pass
