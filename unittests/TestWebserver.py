import requests
import json
import unittest

from datetime import datetime, timedelta
from time import sleep
import os
from flask import jsonify

import sys
try:
    from io import StringIO
except:
    from StringIO import StringIO

import pylint.lint

from deepdiff import DeepDiff
 
total_score = 0

class TestWebserver(unittest.TestCase):
    

    def test_1(self):
        """api/global_mean"""
        global total_score
        with open("unittests/job-1.json", "r") as fin:
            data = json.load(fin)
        sleep(1)
        resp = requests.post("http://127.0.0.1:5000/api/global_mean",json=data)
        self.assertEqual(resp.status_code, 200)
        total_score+=10

    def test_2(self):
        """api/state_diff_from_mean 1"""
        global total_score
        with open("unittests/job-2.json", "r") as fin:
            data = json.load(fin)
        sleep(1)
        resp = requests.post("http://127.0.0.1:5000/api/state_diff_from_mean",json=data)
        self.assertEqual(resp.status_code, 200)
        total_score+=10

    def test_3(self):
        """api/state_diff_from_mean 2"""
        global total_score
        with open("unittests/job-3.json", "r") as fin:
            data = json.load(fin)
        sleep(1)
        resp = requests.post("http://127.0.0.1:5000/api/state_diff_from_mean",json=data)
        self.assertEqual(resp.status_code, 200)
        total_score+=10

    def test_4(self):
        global total_score
        sleep(4)
        resp = requests.get("http://127.0.0.1:5000/api/jobs")
        self.assertEqual(resp.status_code, 200)
        result = {'1' : "done", '2' : "done", '3' : "done"} 
        self.assertEqual(resp.json()["data"],result)
        total_score+=10

    def test_5(self):
        """/api/graceful_shutdown"""
        global total_score
        resp = requests.get("http://127.0.0.1:5000/api/graceful_shutdown")
        self.assertEqual(resp.status_code, 200)

    def test_6(self):
        global total_score
        resp = requests.get("http://127.0.0.1:5000/api/num_jobs")
        self.assertEqual(resp.status_code, 200)
        result = 0
        self.assertEqual(resp.json()["data"],result)
        total_score+=10
    




if __name__ == '__main__':
    try:
        unittest.main()
    finally:
        print(f"Total: {total_score}/50")