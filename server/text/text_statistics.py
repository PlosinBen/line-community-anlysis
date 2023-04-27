from flask import Blueprint

text_statistics= Blueprint('text_statistics', __name__)

# path

@text_statistics.route('/')
def statistics():
    return 'statistics'

