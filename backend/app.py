from flask import Flask

from .server.controller.text.text_statistics_path import text_statistics
from .server.controller.word.word_cloud_path import word_cloud
from .server.controller.file.file_upload_path import file_upload

app = Flask(__name__)

prefix = '/api'

# inject controller
app.register_blueprint(text_statistics, url_prefix=prefix)
app.register_blueprint(word_cloud, url_prefix=prefix)
app.register_blueprint(file_upload, url_prefix=prefix)


if __name__ == '__main__':
    app.run(debug=True)
