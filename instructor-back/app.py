from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import json
import random

from GazeManager import GazeManager
from SessionManager import SessionManager



app = Flask(__name__)
CORS(app, supports_credentials=True)

#######################################################################
@app.route('/')
def hello():
    return "<h1>Attention Checker Backend is Active!!!</h1>"

@app.route('/api/cors', methods=['POST']) 
def cors_check():
    data = request.json
    print("received ==> {}".format(data))
    return "cors check >> {}\n".format(data)
#######################################################################

@app.route('/api/get_random_gaze')
def getRandomGaze(limit = 20):
    gazedata = GazeManager.getRandomGaze(limit)
    return jsonify(gazedata)

@app.route('/api/get_current_gaze')
def getCurrentGaze():
    print("")
    return jsonify(GazeManager.getCurrentHeatmap())

@app.route('/api/save_gaze')
def saveCurrentGaze():
    GazeManager.saveCurrentHeatmap()
    return "saved gaze"

@app.route('/api/post_gaze', methods=['POST']) 
def receiveGazeDataFromStudents():
    GazeManager.clearGazeContainer()
    data = request.json
    print(json.dumps(data, indent=2), type(data))
    processed = GazeManager.processGazeDataFromStudents(data)
    print(json.dumps(processed, indent=2), type(processed))
    GazeManager.updateGazeContainer(processed)
    return jsonify(processed)

@app.route("/api/clearGazeContainer")
def clearGazeContainer():
    GazeManager.clearGazeContainer()
    return "cleared gaze contaner"

@app.route('/api/post_gaze_sim', methods=['POST']) 
def receiveGazeDataFromStudents__Simulation():
    data = request.data
    print(data, type(data))
    data = data.decode('utf8').replace("'", '"')
    data = json.loads(data)
    print(json.dumps(data, indent=2), type(data))

    userid = data["userid"]
    gazedata = data["gazedata"]

    GazeManager.updateGazeContainer(gazedata)
    return "Successfully pushed data to container <> {}".format(userid)
    # GazeManager.updateGazeContainer(data)


############################################################################################################

@app.route('/api/post_gazestream', methods=['POST']) 
def receiveGazeStreamFromStudents():
    data = request.json
    # print(json.dumps(data, indent=2), type(data))
    
    SessionManager.updateGazeStream(data)
    return "received gaze stream"

@app.route("/api/clear_session")
def clearSession():
    SessionManager.clearGazeSession()
    return "cleared gaze session data"


@app.route("/api/save_session")
def saveSession():
    timestamp = SessionManager.saveCurrentSession()
    return "saved current session -- {}".format(timestamp)


@app.route("/api/load_session_last/<limit_second>")
def loadHeatMapFromSession(limit_second = 10):
    return jsonify(GazeManager.getHeatmapFromSession(int(limit_second)))


@app.route("/api/load_session")
def loadHeatMapFromFullSession():
    return jsonify(GazeManager.getFullSession())


# ASSETS_DIR = os.path.dirname(os.path.abspath(__file__))

if __name__ == "__main__":
    # print("assets directory >> ", ASSETS_DIR)
    # context = ('local.crt', 'local.key')#certificate and key files
    with open("backend_config.json", "r") as f:
        config = json.load(f)
    print(json.dumps(config, indent=2))
    context = (config["certificate"], config["key"])
    app.run(
        host=os.getenv('IP', '0.0.0.0'), 
        port=int(os.getenv('PORT', 3005)), 
        debug=True,
        ssl_context=context
    )
