import random
import json
import datetime
from Utils import Utils
from SessionManager import SessionManager

class GazeManager:
    gazeContainer = {}

    @staticmethod
    def updateGazeContainer(processed_gaze_arr):
        for gaze in processed_gaze_arr:
            x = round(gaze['x'], 3)
            y = round(gaze['y'], 3)
            if((x, y) not in GazeManager.gazeContainer):
                GazeManager.gazeContainer[(x, y)] = 0
            GazeManager.gazeContainer[(x, y)] += gaze['value']

    @staticmethod
    def clearGazeContainer():
        GazeManager.gazeContainer.clear()

    @staticmethod
    def getCurrentHeatmap():
        gazeContainer = GazeManager.gazeContainer
        heatmap = []
        for cord in gazeContainer:
            heatmap.append({
                "x"     : cord[0],
                "y"     : cord[1],
                "value" : gazeContainer[cord] 
            })
        return heatmap

    @staticmethod
    def processGazeDataFromStudents(data):
        screenHeight = data["screenHeight"]
        screenWidth  = data["screenWidth"]
        gazedata = []
        for kx in data["gaze"]:
            x = int(kx)/screenWidth
            for ky in data["gaze"][kx]:
                y = int(ky)/screenHeight
                value = data["gaze"][kx][ky]
                gazedata.append({
                    "x"     : x,
                    "y"     : y,
                    "value" : value 
                })
        return gazedata

    @staticmethod
    def saveCurrentHeatmap():
        path = "saved_gazedata/iict_1/"
        Utils.makeDirectory(path)
        with open(path + "gaze_{}.json".format(datetime.datetime.now().isoformat()), "w") as f:
            json.dump(GazeManager.getCurrentHeatmap(), f)

    @staticmethod
    def getRandomGaze(limit = 20):
        screenHeight = 641
        screenWidth = 1310

        gazedata = []
        while(limit>0):
            x = random.randint(0, screenWidth)
            y = random.randint(0, screenHeight)
            x /= screenWidth
            y /= screenHeight
            gazedata.append({
                "x": x,
                "y": y,
                "value": random.randint(0,10)
            })
            limit -= 1

        return gazedata

    ###########################################################################

    @staticmethod
    def getHeatmapFromSession(limit_second = 10):
        GazeManager.clearGazeContainer()

        latest = 0
        all_sessions = SessionManager.gazesession
        for session in all_sessions:
            curr = all_sessions[session][-1]["timestamp"]
            time_now = Utils.getSecondFromTimeStamp(curr)
            latest = max(latest, time_now)
        
        frm = latest
        for session in  all_sessions:
            it = 1
            if(len(all_sessions[session]) == 0):
                print("session {} do not have any data yet to plot".format(session))
                continue
            while(True):
                # print(" >>>> ", len(all_sessions[session]))
                if(it > len(all_sessions[session])):
                    break
                data = all_sessions[session][-it]
                time_now = Utils.getSecondFromTimeStamp(data["timestamp"])
                if(time_now < latest - limit_second):
                    break
                frm = min(latest, time_now)
                x = data["gaze"]["x"]
                y = data["gaze"]["y"]

                x = max(0, x)
                x = min(x, data["gazefeatures"]["screen"][0])

                y = max(0, y)
                y = min(y, data["gazefeatures"]["screen"][1])

                if((x, y) not in GazeManager.gazeContainer):
                    GazeManager.gazeContainer[(x, y)] = 0
                GazeManager.gazeContainer[(x, y)] += 1

                it+=1

        print("loaded gaze data from {} to {}".format(frm, latest))

        return GazeManager.getCurrentHeatmap()

    @staticmethod
    def getFullSession():
        GazeManager.clearGazeContainer()
        all_sessions = SessionManager.gazesession

        session_cnt = 0
        gaze_point_cnt = 0
        for session in  all_sessions:
            session_cnt += 1
            for i in range(len(all_sessions[session])):
                data = all_sessions[session][-i]
                x = data["gaze"]["x"]
                y = data["gaze"]["y"]

                if((x, y) not in GazeManager.gazeContainer):
                    GazeManager.gazeContainer[(x, y)] = 0
                GazeManager.gazeContainer[(x, y)] += 1
                gaze_point_cnt += 1


        print("loaded full session data -- session count: {} -- gaze points: {}".format(session_cnt, gaze_point_cnt))
        return GazeManager.getCurrentHeatmap()
