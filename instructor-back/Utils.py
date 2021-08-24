import os

class Utils:
    @staticmethod
    def makeDirectory(path):
        try:
            os.mkdir(path)
            print("created directory @" + path)
        except FileExistsError:
            print("Folder of same already exists!!")
            pass

    @staticmethod
    def getSecondFromTimeStamp(timestamp):
        return timestamp["hour"]*60*60 + timestamp["minute"]*60 + timestamp["seconds"]