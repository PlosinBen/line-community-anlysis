from flask import Flask

from backend.controller.line_community_analysis import line_community_analysis
from backend.controller.risk_parity_calculator import risk_parity_calculator

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
app.register_blueprint(risk_parity_calculator, url_prefix=prefix)

if __name__ == '__main__':
    app.run(debug=True)
