import random

class GazeManager:
    gazeContainer = []
    
    def updateGazeContainer(processed_gaze_arr):
        GazeManager.gazeContainer = []
        GazeManager.gazeContainer += processed_gaze_arr

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