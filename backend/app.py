from flask import Flask

from .server.text.text_statistics_path import text_statistics
from .server.word.word_cloud_path import word_cloud
from .server.file_upload.file_upload_path import file_upload

app = Flask(__name__)

prefix = '/api'

# inject controller
app.register_blueprint(text_statistics, url_prefix=prefix)
app.register_blueprint(word_cloud, url_prefix=prefix)
app.register_blueprint(file_upload, url_prefix=prefix)


if __name__ == '__main__':
    app.run(debug=True)
