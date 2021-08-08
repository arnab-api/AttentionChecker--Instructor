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