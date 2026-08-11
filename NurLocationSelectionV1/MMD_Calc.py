import os.path
import NurTestingPycharm.UtilNur as Util
import re
import ast
import time
from haversine import haversine

class MMDCalc:
    def __init__(self):
        print("Calculating MMD of Exact results.")

        self.alpha = 0.5
        self.beta = 0.5
        self.omega = 0.5
        self.theta = 500
        self.thetaGS = 0.4
        #self.k = 10  # 2, 4, 6, 8, 10
        kList = [2, 4, 6, 8, 10]
        self.m = 10  # return top m sets
        self.topSet_Score_m = []
        self.binId = "bin100"  # bin id 100 is fixed here, bin50, bin100, bin200, bin500, bin1000

        self.baseFolder = "I:\\ExpDataUDI\\ExperimentFolder"
        self.insideFolders = "ExpResult2\Results"
        self.datasetName = "Flickr"

        self.operatingFolderOrig = os.path.join(self.baseFolder, self.datasetName)
        self.operatingFolder = os.path.join(self.baseFolder, self.datasetName, self.insideFolders, self.binId)

        #self.outputFolder = os.path.join(self.operatingFolder, "MMD", str(self.k))
        #self.resultFilesPath = os.path.join(self.operatingFolder, str(self.k))

        self.diversityFolder = os.path.join(self.operatingFolderOrig, "ExpResult2\DiversityWithNgbrLocs")

        if self.datasetName == "Flickr":
            self.userLocationDict = self.convert_EachLines_Into_Dict(self.operatingFolderOrig, "user_allChkIn_ListDict.txt")
            print("first dict loaded Flickr")
            self.socialNetwork = Util.convert_String_Into_Dict2(self, self.operatingFolderOrig, "Flickr_edges_anonomyzed_Dict.txt")
            print("Len: ", len(self.socialNetwork))
        elif self.datasetName == "Yelp":
            self.userLocationDict = self.convert_EachLines_Into_Dict(self.operatingFolderOrig, "user_allChkIn_ListDict.txt")
            print("first dict loaded Yelp")
            self.socialNetwork = Util.convert_String_Into_Dict2(self, self.operatingFolderOrig, "Yelp_edges_anonym_Dict_New.txt")
            print("Len: ", len(self.socialNetwork))
        else:
            self.userLocationDict = Util.convert_String_Into_Dict2(self, self.operatingFolder, "user_allChkIn_location_dictRound.txt")
            print("first dict loaded")
            self.socialNetwork = Util.convert_String_Into_Dict2(self, self.operatingFolder, self.datasetName + "_edges_Dict.txt")

        #self.userLocationDict = Util.convert_String_Into_Dict2(self, self.operatingFolderOrig, "user_allChkIn_location_dictRound.txt")
        #self.socialNetwork = Util.convert_String_Into_Dict2(self, self.operatingFolderOrig, self.datasetName + "_edges_Dict.txt")

        for k in kList:
            self.k = k

            self.outputFolder = os.path.join(self.operatingFolder, "MMD", str(self.k))
            self.resultFilesPath = os.path.join(self.operatingFolder, str(self.k))

            listResultFiles = os.listdir(self.resultFilesPath)

            mmdStr = ""
            mmdStrDgs = ""
            spatTotal = 0
            socSpatTotal = 0
            fileNo = 0
            for files in listResultFiles:
                '''
                fileNo += 1
                if fileNo == 100:
                    print("processed 100 files")
                    break
                '''
                if files.replace(".txt", "").__contains__("_"):
                    user = files.replace(".txt", "").split("_")[0]
                else:
                    continue
                print(files)
                ngbrsList = self.socialNetwork[user]
                L = self.userLocationDict[user]
                self.L = list(set(L))
                self.maxD = self.calcMaxD(self.L)
                self.socialSpatialDiversity(self.userLocationDict[user], ngbrsList, user)

                self.twoDArray = self.loadDgsContents(os.path.join(self.diversityFolder, str(user) + ".txt"))  # loading self.content and creating self.locAndIndex

                locsList = self.selectedListOfLocs(self.resultFilesPath, files)

                minDistTotal = 0
                minDistTotalDgs = 0
                for ngbrs in ngbrsList:
                    if ngbrs in self.userLocationDict.keys():
                        ngbrLocs = list(set(self.userLocationDict[ngbrs]))
                        tempList = []
                        tempListDgs = []
                        for ngbrloc in ngbrLocs:
                            #print(ngbrloc)
                            tempList.append(min([haversine(ngbrloc, loc, miles=False) for loc in locsList]))
                            tempListDgs.append(min([self.dictOfDgsFromFileAndFlyNewLatest(ngbrloc, loc) for loc in locsList]))
                        minDist = round(min(tempList), 2)
                        minDistTotal = minDistTotal + minDist

                        minDistDgs = round(min(tempListDgs), 2)
                        minDistTotalDgs = minDistTotalDgs + minDistDgs

                mmdStr = mmdStr + str(user) + "\t" + str(round(minDistTotal / len(ngbrsList), 2)) + "\n"
                mmdStrDgs = mmdStrDgs + str(user) + "\t" + str(round(minDistTotalDgs / len(ngbrsList), 2)) + "\n"
                spatTotal = spatTotal + round(minDistTotal / len(ngbrsList), 2)
                socSpatTotal = socSpatTotal + round(minDistTotalDgs / len(ngbrsList), 2)

            self.createFile(os.path.join(self.outputFolder, "mmdSpatial_k" + str(self.k) + ".txt"), mmdStr)
            self.createFile(os.path.join(self.outputFolder, "mmdSocioSpatial_k" + str(self.k) + ".txt"), mmdStrDgs)
            FinalResults = "Spat: ", round(spatTotal/len(listResultFiles), 2), "\n", "SocSpat: ", round(socSpatTotal/len(listResultFiles), 2)
            self.createFile(os.path.join(self.outputFolder, "FinalMMD_k" + str(self.k) + ".txt"), FinalResults)

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

    def selectedListOfLocs(self, PathOfResultSet, fileName):
        f = open(os.path.join(PathOfResultSet, fileName), "r")
        self.content = f.readlines()
        self.content = [x.strip() for x in self.content]
        locsList = []
        for i in range(len(self.content)):
            splitArray = self.content[i].split("\t")
            # locsList = ast.literal_eval(splitArray[2].strip())
            locsList.append(eval(splitArray[1].strip()))
        f.close()
        # print(locsList)
        return locsList

    def loadDgsContents(self, filePath):
        f = open(filePath, "r")
        self.content = f.readlines()
        self.content = [x.strip() for x in self.content]
        self.locAndIndex = []
        self.twoDArray = []
        for i in range(len(self.content)):
            splitArray = self.content[i].split("\t")
            loc = eval(splitArray.pop(0).strip())  # remove the first element that contains location
            # print(type(loc))
            self.twoDArray.append(splitArray)
            self.locAndIndex.append(loc)
        f.close()
        return self.twoDArray

    def dictOfDgsFromFileAndFlyNewLatest(self, loc1_Q, loc2_Q):
        if loc1_Q in self.locAndIndex and loc2_Q in self.locAndIndex:
            loc1_Index = self.locAndIndex.index(loc1_Q)
            loc2_Index = self.locAndIndex.index(loc2_Q)
            if len(self.twoDArray) >= loc1_Index:
                tempValDgs = self.twoDArray[loc1_Index][loc2_Index]
                return float(tempValDgs)
        else:
            print("locations are not available in self.locAndIndex list")
            return 0

    def socialSpatialDiversity(self, L, socialNetworkNgbrList, userId):
        locationNgbrCheckinDict = {}
        locationNgbrCheckinText = ""

        for loc in L:
            tempList = []
            for ngbr in socialNetworkNgbrList:
                if ngbr in self.userLocationDict.keys() and loc in self.userLocationDict[ngbr]:
                    tempList.append(ngbr)
            locationNgbrCheckinDict[loc] = tempList
            #locationNgbrCheckinText = locationNgbrCheckinText + str(loc)+ "\t" + str(tempList)+ "\n"
        #self.createFile(os.path.join(self.outputFolder, "LocChknNgbr", str(userId) + ".txt"), locationNgbrCheckinText)

        socSpatDivCalcStr = ""
        for loc in L:
            tempPerRow = str(loc)
            for loc2 in L:
                if loc in locationNgbrCheckinDict.keys() and loc2 in locationNgbrCheckinDict.keys():
                    common = len(set(locationNgbrCheckinDict[loc]).intersection(locationNgbrCheckinDict[loc2]))
                    union = len(set(locationNgbrCheckinDict[loc]).union(locationNgbrCheckinDict[loc2]))
                    dist = round(Util.haversineDist(loc, loc2), 2)
                    if union > 0:
                        socDiv = round((1 - common/union), 2)
                    else:
                        socDiv = 1.0
                    spatDiv = round((dist/self.maxD), 2)

                    geoSocDivFinal = round((self.beta*socDiv + (1-self.beta)*spatDiv), 2)
                    tempPerRow = tempPerRow + "\t" + str(geoSocDivFinal)
            socSpatDivCalcStr = socSpatDivCalcStr + tempPerRow + "\n"
                    #socSpatDivCalcStr = socSpatDivCalcStr + str(loc) + "\t" + str(loc2) + "\t" + str(common) + "\t" + str(union) + "\t" + str(socDiv) + "\t" + str(dist) + "\t" + str(self.maxD) + "\t" + str(spatDiv) + "\t" + str(geoSocDivFinal) + "\n"

        self.createFile(os.path.join(self.diversityFolder, str(userId) + ".txt"), socSpatDivCalcStr)

    def createFile(self, fileNameFullPath, contents):
        try:
            fw_fileName = open(fileNameFullPath, "w", encoding="utf8")
            fw_fileName.write(contents.__str__())
            fw_fileName.close()
        except KeyError:
            print("Error while creating file.. ", KeyError)
            pass

    def calcMaxD(self, L):
        maxD = 0
        for loc1 in L:
            maxTemp = max([Util.haversineDist(loc1, lc) for lc in L])
            if maxTemp > maxD:
                maxD = maxTemp
        return round(maxD, 2)
obj = MMDCalc()