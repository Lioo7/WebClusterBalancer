import os
import logging
import socket
from logging.handlers import RotatingFileHandler
from flask import Flask

app = Flask(__name__)

# Get the directory path of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))
log_file = os.path.join(script_dir, 'logs/app.log')

# Configure logging to write to the log file
handler = RotatingFileHandler(log_file, maxBytes=10000, backupCount=1)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
app.logger.addHandler(handler)
app.logger.setLevel(logging.INFO)


@app.route('/')
def hello():
    app.logger.info('Endpoint accessed: /')
    return f"Container ID: {socket.gethostname()}"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8002)
