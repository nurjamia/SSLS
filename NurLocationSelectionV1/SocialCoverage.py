import os.path
import NurTestingPycharm.UtilNur as Util
from haversine import haversine
import ast

class SociaCoverage:
    def __init__(self):
        print("calculating social coverage when Theta = 0 and Theta = 100 KM, The SOS version is in SocialCoverageSOS.py")
        self.alpha = 0.5
        self.beta = 0.5
        self.omega = 0.5
        self.theta = 500
        self.thetaGS = 0.4
        self.ThetaForSC = 100 #one can also use 50; the default is Exact and 100
        self.k = 10  # 2, 4, 6, 8, 10
        self.m = 10  # return top m sets
        self.topSet_Score_m = []
        self.binId = "bin100"  # bin50, bin100, bin200, bin500, bin1000

        self.baseFolder = "I:\\ExpDataUDI\\ExperimentFolder"
        self.datasetName = "Gowalla" #Gowalla, Brightkite, Flickr, Yelp
        self.insideFolders = "ExpResult2\Results"

        self.operatingFolderOrig = os.path.join(self.baseFolder, self.datasetName)
        self.operatingFolder = os.path.join(self.baseFolder, self.datasetName, self.insideFolders, self.binId)
        self.outputFolder = os.path.join(self.operatingFolder, "SocialCoverSC", str(self.k))
        self.resultFilesPath = os.path.join(self.operatingFolder, str(self.k))

        #self.diversityFolder = os.path.join(self.operatingFolderOrig, "ExpResult2\DiversityWithNgbrLocs")

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

        listResultFiles = os.listdir(self.resultFilesPath)

        strContent = ""
        strColocatedAvg = ""
        strWithinAvg = ""
        finalCoLocated = 0
        finalWithinTheta = 0
        for files in listResultFiles:
            avgExact = 0
            avgWithin = 0
            totalExactCoLocated = 0
            totalwithinTheta = 0
            if files.replace(".txt", "").__contains__("_"):
                user = files.replace(".txt", "").split("_")[0]
            else:
                continue
            print(files)
            ngbrsListOrig = self.socialNetwork[user]
            L = self.userLocationDict[user]
            self.L = list(set(L))
            locsList = self.selectedListOfLocs(self.resultFilesPath, files)

            ngbrsList = []
            for ngbr in ngbrsListOrig:
                if ngbr in self.userLocationDict.keys() and len(list(set(self.userLocationDict[ngbr]))) > 5:
                    ngbrsList.append(ngbr)

            for ngbrs in ngbrsList:
                alreadyCountedNgbrFlag = False #flag that considers whether a ngbr has already counted
                exactColocated = 0
                withinThetaKM = 0
                if ngbrs in self.userLocationDict.keys():
                    ngbrLocs = list(set(self.userLocationDict[ngbrs]))
                    for ngbrloc in ngbrLocs:
                        # print(ngbrloc)
                        minDist = min([haversine(ngbrloc, loc, miles=False) for loc in locsList])
                        if minDist == 0:
                            print("Exact co-located")
                            exactColocated += 1
                            if alreadyCountedNgbrFlag == False:
                                withinThetaKM += 1
                            break
                        elif alreadyCountedNgbrFlag == False and minDist <= self.ThetaForSC:
                            print("dist: ", minDist)
                            withinThetaKM += 1
                            alreadyCountedNgbrFlag = True
                totalExactCoLocated = totalExactCoLocated + exactColocated
                totalwithinTheta = totalwithinTheta + withinThetaKM
            if len(ngbrsList) > 0:
                avgExact = avgExact + round(totalExactCoLocated/len(ngbrsList), 2)
                avgWithin = avgWithin + round(totalwithinTheta / len(ngbrsList), 2)
                strContent = strContent + str(user) + "\t" + str(avgExact) + "\t" + str(avgWithin) + "\n"
                finalCoLocated = finalCoLocated + avgExact
                finalWithinTheta = finalWithinTheta + avgWithin

        self.createFile(os.path.join(self.outputFolder, "SC_count_k" + str(self.k) +"_"+ str(self.ThetaForSC) + "KM.txt"), strContent)
        FinalResults = "Exact: ", round(finalCoLocated / len(listResultFiles), 2), "\n", "WithinTheta: ", round(finalWithinTheta / len(listResultFiles), 2)
        self.createFile(os.path.join(self.outputFolder, "FinalSC_k" + str(self.k) +"_"+ str(self.ThetaForSC)+ "KM.txt"), FinalResults)

        print("Done: k and bins ", self.k, self.binId)

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

    def createFile(self, fileNameFullPath, contents):
        try:
            fw_fileName = open(fileNameFullPath, "w", encoding="utf8")
            fw_fileName.write(contents.__str__())
            fw_fileName.close()
        except KeyError:
            print("Error while creating file.. ", KeyError)
            pass
obj = SociaCoverage()