from flask import Flask
from controller.text_statistics import text_statistics

app = Flask(__name__)

#inject controller
app.register_blueprint(text_statistics)


if __name__ == '__name__':
    app.run(debug = True)
