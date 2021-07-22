from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import json
import random

from GazeManager import GazeManager

app = Flask(__name__)
CORS(app, supports_credentials=True)


@app.route('/')
def hello():
    return "Hello World!"

@app.route('/api/get_random_gaze')
def getRandomGaze(limit = 20):
    gazedata = GazeManager.getRandomGaze(limit)
    return jsonify(gazedata)

@app.route('/api/get_current_gaze')
def getCurrentGaze():
    return jsonify(GazeManager.gazeContainer)

@app.route('/api/post_gaze', methods=['POST']) 
def receiveGazeDataFromStudents():
    data = request.json
    print(json.dumps(data, indent=2), type(data))
    processed = GazeManager.processGazeDataFromStudents(data)
    print(json.dumps(processed, indent=2), type(processed))

    GazeManager.updateGazeContainer(processed)
    return jsonify(processed)

if __name__ == "__main__":
    app.run(
        host=os.getenv('IP', '0.0.0.0'), 
        port=int(os.getenv('PORT', 5000)), 
        debug=True
    )
