import random
import json
import datetime
from Utils import Utils

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
        path = "saved_gazedata/user_4/"
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