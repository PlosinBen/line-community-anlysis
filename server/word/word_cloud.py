from flask import Blueprint

word_cloud= Blueprint('word_cloud', __name__)

# path
@word_cloud.route('/')
def cloud():
    return 'word_cloud_path'

