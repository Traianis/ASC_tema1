"""ROUTTTT"""
import os
import json
from time import sleep

from flask import request, jsonify
from app import webserver

# Example endpoint definition
@webserver.route('/api/post_endpoint', methods=['POST'])
def post_endpoint():
    """/api/post_endpoint"""
    if request.method == 'POST':
        # Assuming the request contains JSON data
        data = request.json

        # Process the received data
        # For demonstration purposes, just echoing back the received data
        response = {"message": "Received data successfully", "data": data}

        # Sending back a JSON response
        return jsonify(response)
    # Method Not Allowed
    return jsonify({"error": "Method not allowed"}), 405

@webserver.route('/api/get_results/<job_id>', methods=['GET'])
def get_response(job_id):
    """/api/get_results/<job_id>"""
    webserver.logger.info(f"Accessed endpoint /api/get_results/{job_id}")
    if (int(job_id) >= webserver.job_counter or int(job_id) <= 0):
        webserver.logger.error(f"Invalid job_id: {job_id}")
        return jsonify({
        "status": "error",
        "reason": "Invalid job_id"
        })
    if len(webserver.tasks_runner.tasks_finished[int(job_id)]) == 0:
        webserver.logger.info(f"Job with ID {job_id} is still running")
        return jsonify({
           "status": "running"
       })
    webserver.logger.info(f"Job with ID {job_id} is done")
    return jsonify({
           "status": "done",
           "data": webserver.tasks_runner.tasks_finished[int(job_id)]
       })

@webserver.route('/api/states_mean', methods=['POST'])
def states_mean_request():
    """/api/states_mean"""
    data = request.json
    webserver.logger.info("Received request for states_mean")
    webserver.tasks_runner.add_task(["question", webserver.job_counter, "1", data["question"]])
    webserver.job_counter += 1
    return jsonify({"job_id": webserver.job_counter - 1})

@webserver.route('/api/state_mean', methods=['POST'])
def state_mean_request():
    """/api/state_mean"""
    webserver.logger.info("Received request for state_mean")
    data = request.json
    webserver.tasks_runner.add_task(["question", webserver.job_counter, "2",
                                     data["question"], data["state"]])
    webserver.job_counter += 1
    return jsonify({"job_id": webserver.job_counter - 1})

@webserver.route('/api/best5', methods=['POST'])
def best5_request():
    """/api/best5"""
    webserver.logger.info("Received request for best5")
    data = request.json
    webserver.tasks_runner.add_task(["question", webserver.job_counter, "3", data["question"]])
    webserver.job_counter += 1
    return jsonify({"job_id": webserver.job_counter - 1})


@webserver.route('/api/worst5', methods=['POST'])
def worst5_request():
    """/api/worst5"""
    webserver.logger.info("Received request for worst5")
    data = request.json
    webserver.tasks_runner.add_task(["question", webserver.job_counter, "4", data["question"]])
    webserver.job_counter += 1
    return jsonify({"job_id": webserver.job_counter - 1})

@webserver.route('/api/global_mean', methods=['POST'])
def global_mean_request():
    """/api/global_mean"""
    webserver.logger.info("Received request for global_mean")
    data = request.json
    input = ["question", webserver.job_counter, "5", data["question"]]
    webserver.tasks_runner.add_task(input)
    webserver.job_counter += 1
    return jsonify({"job_id": webserver.job_counter - 1})

@webserver.route('/api/diff_from_mean', methods=['POST'])
def diff_from_mean_request():
    """/api/diff_from_mean"""
    webserver.logger.info("Received request for diff_from_mean")
    data = request.json
    webserver.tasks_runner.add_task(["question", webserver.job_counter, "6", data["question"]])
    webserver.job_counter += 1
    return jsonify({"job_id": webserver.job_counter - 1})

@webserver.route('/api/state_diff_from_mean', methods=['POST'])
def state_diff_from_mean_request():
    """/api/state_diff_from_mean"""
    webserver.logger.info("Received request for state_diff_from_mean")
    data = request.json
    webserver.tasks_runner.add_task(["question", webserver.job_counter, "7",
                                     data["question"], data["state"]])
    webserver.job_counter += 1
    return jsonify({"job_id": webserver.job_counter - 1})

@webserver.route('/api/mean_by_category', methods=['POST'])
def mean_by_category_request():
    """/api/mean_by_category"""
    webserver.logger.info("Received request for mean_by_category")
    data = request.json
    webserver.tasks_runner.add_task(["question", webserver.job_counter, "8", data["question"]])
    webserver.job_counter += 1
    return jsonify({"job_id": webserver.job_counter - 1})

@webserver.route('/api/state_mean_by_category', methods=['POST'])
def state_mean_by_category_request():
    """/api/state_mean_by_category"""
    webserver.logger.info("Received request for state_mean_by_category")
    data = request.json
    webserver.tasks_runner.add_task(["question", webserver.job_counter, "9", data["question"],
                                     data["state"]])
    webserver.job_counter += 1
    return jsonify({"job_id": webserver.job_counter - 1})

@webserver.route('/api/graceful_shutdown', methods =['GET'])
def shutdown():
    """/api/graceful_shutdown"""
    webserver.logger.info("Received SHUTDOWN")
    webserver.tasks_runner.stop()
    return jsonify({"status": "done"})


@webserver.route('/api/jobs', methods =['GET'])
def jobs_status_request():
    """/api/jobs"""
    webserver.logger.info("Received request for jobs")
    res = {}
    for key, value in webserver.tasks_runner.tasks_finished.items():
        if len(value) == 0:
            res[key] = "running"
        else:
            res[key] = "done"
    return jsonify({"status": "done", "data" : res})

@webserver.route('/api/num_jobs', methods =['GET'])
def num_jobs():
    """/api/num_jobs"""
    webserver.logger.info("Received request for num_jobs")
    nr = 0
    for key, value in webserver.tasks_runner.tasks_finished.items():
        if len(value) == 0:
            nr += 1
    return jsonify({"status": "done", "data" : nr})

@webserver.route('/')
@webserver.route('/index')
def index():
    """index"""
    routes = get_defined_routes()
    msg = "Hello, World!\n Interact with the webserver using one of the defined routes:\n"

    # Display each route as a separate HTML <p> tag
    paragraphs = ''.join([f"<p>{route}</p>" for route in routes])

    msg += paragraphs
    return msg

def get_defined_routes():
    """defined routes"""
    routes = []
    for rule in webserver.url_map.iter_rules():
        methods = ', '.join(rule.methods)
        routes.append(f"Endpoint: \"{rule}\" Methods: \"{methods}\"")
    return routes
