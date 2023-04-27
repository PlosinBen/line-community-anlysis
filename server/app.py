from flask import Flask

from text.text_statistics import text_statistics
from word.word_cloud import word_cloud

app = Flask(__name__)

#inject controller
app.register_blueprint(text_statistics, url_prefix = '/statistic')
app.register_blueprint(word_cloud, url_prefix = '/word')


