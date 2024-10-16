"""INIT"""
import os
import logging
from logging.handlers import RotatingFileHandler

from flask import Flask
import time
webserver = Flask(__name__)

# Configure logging
og_formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
log_file = 'webserver.log'
log_handler = RotatingFileHandler(log_file, maxBytes=100000, backupCount=10)
log_handler.setLevel(logging.INFO)
webserver.logger.addHandler(log_handler)
webserver.logger.setLevel(logging.INFO)
logging.Formatter.converter = time.gmtime

from app.data_ingestor import DataIngestor

from app.task_runner import ThreadPool

from app import routes

webserver.data_ingestor = DataIngestor("./nutrition_activity_obesity_usa_subset.csv")

webserver.tasks_runner = ThreadPool(webserver.data_ingestor.df,
                                    webserver.data_ingestor.data_dict,
                                    webserver.data_ingestor.questions_best_is_min,
                                    webserver.logger)

webserver.tasks_runner.start()

# Create 'results' directory if not exist
os.system("mkdir results")

webserver.job_counter = 1
