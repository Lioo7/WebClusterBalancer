import os
import logging
from logging.handlers import RotatingFileHandler
from flask import Flask, request, make_response
from datetime import datetime
from dotenv import load_dotenv
import socket

from database import Database

load_dotenv()

app = Flask(__name__)

# configure logging
log_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logs/app.log')
handler = RotatingFileHandler(log_file, maxBytes=10000, backupCount=1)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
app.logger.addHandler(handler)
app.logger.setLevel(logging.INFO)

# init the database connection
MYSQL_ROOT_PASSWORD = os.environ.get('MYSQL_ROOT_PASSWORD')
db = Database(host='db', port='3306', user='root', password=MYSQL_ROOT_PASSWORD)
# init the tables
db.create_tables()


@app.route('/')
def display_internal_ip():
    try:
        app.logger.info('Endpoint accessed: /')
        # increment counter by one
        increment_res = db.increment_counter()
        app.logger.info(f'increment_res: {increment_res}')

        # check if the internal_ip cookie already exists
        internal_ip = request.cookies.get('internal_ip')
        if internal_ip is None:
            # if the cookie doesn't exist, create it with the current internal IP
            container_id = socket.gethostname()
            internal_ip = socket.gethostbyname(container_id)
            response = make_response(f"Internal IP address: {internal_ip}")
            response.set_cookie('internal_ip', internal_ip, max_age=300)  # 5 minutes
        else:
            # if the cookie exists, use its value for stickiness
            response = make_response(f"Internal IP address: {internal_ip}")

        # record access log
        client_ip = request.remote_addr
        access_time = datetime.now()
        recored_res = db.record_access_log(access_time, client_ip, internal_ip)
        app.logger.info(f'recored_res: {recored_res}')

        return response

    except Exception as e:
        app.logger.error(f"Error processing request: {e}")
        return "An error occurred on the server. Please try again later.", 500


@app.route('/showcount')
def show_count():
    app.logger.info('Endpoint accessed: /showcount')
    counter = db.get_counter()
    app.logger.info(f"counter: {counter}")
    return f"Thank you for visiting!<br><br>{counter} visitors have visited the website so far"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8002)
