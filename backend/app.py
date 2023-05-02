from flask import Flask

from .server.controller.text.text_statistics_path import text_statistics
from .server.controller.word.word_cloud_path import word_cloud
from .server.controller.file.file_upload_path import file_upload
from .server.controller.line_community_analysis import line_community_analysis

import logging, sys

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

app = Flask(__name__)

prefix = '/api'

# inject controller
app.register_blueprint(line_community_analysis, url_prefix=prefix)
app.register_blueprint(text_statistics, url_prefix=prefix)
app.register_blueprint(word_cloud, url_prefix=prefix)
app.register_blueprint(file_upload, url_prefix=prefix)

if __name__ == '__main__':
    app.run(debug=True)
