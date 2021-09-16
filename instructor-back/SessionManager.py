import random
import json
import datetime
from Utils import Utils

class SessionManager:
    gazesession = {}
    calibration_track = {}

    @staticmethod
    def updateGazeStream(stream):
        screenHeight = stream["screenHeight"]
        screenWidth  = stream["screenWidth"]
        cur_session  = stream["session"]

        if cur_session not in SessionManager.gazesession:
            SessionManager.gazesession[cur_session] = []

        gazestream = []
        # print("received data from {} -- {} gaze points".format(cur_session, len(gazestream)))
        for data in stream["gaze"]:
            gaze = data["gaze"]
            timestamp = data["timestamp"]
            x = gaze["x"] / screenWidth
            y = gaze["y"] / screenHeight
            x = round(x, 3)
            y = round(y, 3)
            gazestream.append({
                "gaze"      : {"x": x, "y": y},
                "timestamp" : timestamp
            })
        
        print("received data from {} -- {} gaze points".format(cur_session, len(gazestream)))
        SessionManager.gazesession[cur_session] += gazestream


    @staticmethod
    def clearGazeSession():
        SessionManager.gazesession.clear()
        SessionManager.calibration_track.clear()
        print(SessionManager.gazesession)

    @staticmethod
    def updateCalibrationInfo(data):
        if(data["session"] not in SessionManager.calibration_track):
            SessionManager.calibration_track[data["session"]] = data
            print("registered calibration for session >> ", data["session"])
        else:
            SessionManager.calibration_track[data["session"]] = data
            print("calibration update >> {}".format(data["session"]))

    @staticmethod
    def saveCurrentSession():
        timestamp = datetime.datetime.now().isoformat()
        path = "saved_sessions/session_{}/".format(timestamp)
        Utils.makeDirectory(path)
        with open(path + "session_{}.json".format(timestamp), "w") as f:
            json.dump(SessionManager.gazesession, f)
        
        with open(path + "calibration_{}.json".format(timestamp), "w") as f:
            json.dump(SessionManager.calibration_track, f)
        
        path += "individual/"
        Utils.makeDirectory(path)
        for session in SessionManager.gazesession:
            with open(path + "{}.json".format(session), "w") as f:
                json.dump(SessionManager.gazesession[session], f)

        print(" --- Saved current session data --- >> {} individual sesions".format(len(list(SessionManager.gazesession.keys()))))

        return timestamp