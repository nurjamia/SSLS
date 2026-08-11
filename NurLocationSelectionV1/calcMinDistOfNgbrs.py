import os.path
import NurTestingPycharm.UtilNur as Util
import re
import ast
import time
from haversine import haversine

class calcMinDistOfNgbrs:
    def __init__(self):
        print("Calculating average minimum distance of users to neighbors in each dataset.")
        self.binId = "bin100"  # bin50, bin100, bin200, bin500, bin1000

        self.baseFolder = "I:\\ExpDataUDI\\ExperimentFolder"
        self.datasetName = "Flickr"  # Gowalla, Brightkite, Flickr, Yelp
        self.operatingFolder = os.path.join(self.baseFolder, self.datasetName)
        self.outputFolder = os.path.join(self.operatingFolder, "ExpResult2")

        if self.datasetName == "Flickr":
            self.userLocationDict = self.convert_EachLines_Into_Dict(self.operatingFolder, "user_allChkIn_ListDict.txt")
            print("first dict loaded")
            self.socialNetwork = Util.convert_String_Into_Dict2(self, self.operatingFolder, "Flickr_edges_anonomyzed_Dict.txt")
            print("Len: ", len(self.socialNetwork))
        elif self.datasetName == "Yelp":
            self.userLocationDict = self.convert_EachLines_Into_Dict(self.operatingFolder, "user_allChkIn_ListDict.txt")
            print("first dict loaded")
            self.socialNetwork = Util.convert_String_Into_Dict2(self, self.operatingFolder, "Yelp_edges_anonym_Dict_New.txt")
            print("Len: ", len(self.socialNetwork))
        else:
            self.userLocationDict = Util.convert_String_Into_Dict2(self, self.operatingFolder, "user_allChkIn_location_dictRound.txt")
            print("first dict loaded")
            self.socialNetwork = Util.convert_String_Into_Dict2(self, self.operatingFolder, self.datasetName + "_edges_Dict.txt")

        # self.userLocationDictUserList = ["4"]
        self.userLocationDictUserList = self.convert_String_Into_List(os.path.join(self.outputFolder, "CheckinBins"), self.binId + ".txt")
        print("size: ", len(self.userLocationDictUserList))

        minDistForEachUserToNgbr = []
        minDistForEachUserToNgbr2 = []
        for user in self.userLocationDictUserList:
            self.bestScore = 0
            L = list(set(self.userLocationDict[user]))
            noOfLoc = len(L)
            if user in self.socialNetwork.keys() and len(self.socialNetwork[user]) > 5 and len(L)>0:
                ngbrsList = self.socialNetwork[user]
                #self.socialNetwork = {} ##############################################Release memory, but please comment in original execution
                minDistToEachNgbrsTempList = []
                tempList = []
                tempList2 = []
                for ngbrs in ngbrsList:
                    if ngbrs in self.userLocationDict.keys() and len(list(set(self.userLocationDict[ngbrs]))) > 0:
                        locOfNgbrAsList = list(set(self.userLocationDict[ngbrs]))
                        for loc in L:
                            mindistToEachNgbr =  min([Util.haversineDist(loc, l) for l in locOfNgbrAsList])
                            minDistToEachNgbrsTempList.append(mindistToEachNgbr)
                        tempList.append(min(minDistToEachNgbrsTempList))
                        tempList2.append(round(sum(minDistToEachNgbrsTempList)/len(minDistToEachNgbrsTempList)))
                if len(tempList) > 0:
                    minDistForEachUserToNgbr.append(min(tempList))
                    minDistForEachUserToNgbr2.append(min(tempList2))
        avg = round(sum(minDistForEachUserToNgbr)/len(self.userLocationDictUserList))
        avg2 = round(sum(minDistForEachUserToNgbr2) / len(self.userLocationDictUserList))

        print("average dist: ", self.datasetName, "avg: ", avg, "avg2: ", avg2)

    def convert_EachLines_Into_Dict(self, baseDirectory, fileInListForm):
        filePath = os.path.join(baseDirectory, fileInListForm)
        with open(filePath) as f:
            content = f.readlines()
        content = [x.strip() for x in content]

        tempDict = {}
        for i in range(len(content)):
            splitArray = content[i].split("\t")
            if len(splitArray) > 1:
                userid = str(splitArray[0])
                locsListStr = ast.literal_eval(splitArray[1])
                tempDict[userid] = locsListStr
        return tempDict

    def convert_String_Into_List(self, baseDirectory, fileName_to_convertDict):

        joinedPath = os.path.join(baseDirectory, fileName_to_convertDict)
        tt = []
        try:
            # f = open(joinedPath, "r", encoding="utf8")
            f = open(joinedPath, "r", encoding="ISO-8859-1")

            for line in f:
                line = re.sub(r'[^\x00-\x7f]', r' ', line)  # remove non ascii
                tt = ast.literal_eval(line)
            f.close()
        except:
            # f.close()
            # f = open(joinedPath, "r", encoding="ISO-8859-1")
            pass

        return tt

obj = calcMinDistOfNgbrs()