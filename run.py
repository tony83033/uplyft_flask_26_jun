# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

import os
from   flask_migrate import Migrate
from   flask_minify  import Minify
from   sys import exit
from flask_sock import Sock
from gui.database_interface import insert_contact,delete_history, delete_data,inset_bail_amount
import json, datetime
from apps.config import config_dict
from apps import create_app, db
from gui.script import start
import schedule
import threading
import time

# WARNING: Don't run with debug turned on in production!
DEBUG = (os.getenv('DEBUG', 'False') == 'True')

# The configuration
get_config_mode = 'Debug' if DEBUG else 'Production'

# Function to be executed at the specified interval
# Create a separate thread for running the schedule
def run_schedule():
    while True:
        schedule.run_pending()
        time.sleep(1)
def scheduled_task():
    # Code to be executed at the specified interval
    inset_bail_amount(web=True, timeMin = 120)
try:

    # Load the configuration using the default values
    app_config = config_dict[get_config_mode.capitalize()]

except KeyError:
    exit('Error: Invalid <config_mode>. Expected values [Debug, Production] ')

app = create_app(app_config)
Migrate(app, db)
if not DEBUG:
    Minify(app=app, html=True, js=False, cssless=False)
sock = Sock(app)

@sock.route("/echo")
def echo(sock):
    while True:
        data = sock.receive()
        if str(data) == "delete":
            delete_history(web=True)
            delete_data()
            continue
        try:
            json_data = json.loads(data)
            booking_id = json_data["id"]
            pages = json_data["pages"]
            race = json_data["race"]
            age_range = json_data["range"]

            try:
                r_low, r_high = age_range.split('-')
                r_low, r_high = int(r_low), int(r_high)
            except:
                sock.send("Error: Please check age range")
                continue
            last_searched_date = datetime.datetime.now()
            last_searched_date.strftime('%m/%d/%Y')
            insert_contact(age_range,race,booking_id,last_searched_date,pages,True)            
            start(str(booking_id),pages,race=race,range_lower= r_low, range_high=r_high, last_searched_date = last_searched_date, sock=sock)

        except Exception as e:
            print(e)
            sock.send({"message":"Error in parsing data"})

if DEBUG:
    app.logger.info('DEBUG            = ' + str(DEBUG)             )
    app.logger.info('Page Compression = ' + 'FALSE' if DEBUG else 'TRUE' )
    app.logger.info('DBMS             = ' + app_config.SQLALCHEMY_DATABASE_URI)
    app.logger.info('ASSETS_ROOT      = ' + app_config.ASSETS_ROOT )

# Schedule the task to run every two hour
schedule.every(2).hours.do(scheduled_task)

if __name__ == "__main__":
    # Start the scheduler in a separate thread

    # Start the schedule thread
    schedule_thread = threading.Thread(target=run_schedule)
    schedule_thread.start()

    app.run()

