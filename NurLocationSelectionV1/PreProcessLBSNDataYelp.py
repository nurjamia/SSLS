import os.path
import NurTestingPycharm.UtilNur as Util
import ast

class PreProcessDatasetsYelp:
    def __init__(self):
        print("Preprocesing of data Yelp.. There are another code in ProcessFlickrRawData/ProcessYelp13.py .. So dont get confused")
        self.baseFolder = "I:\\ExpDataUDI\\ExperimentFolder\\LOC_Select"
        self.datasetName = "Yelp" #Gowalla, Flickr

        #self.operatingFolder = os.path.join(self.baseFolder, self.datasetName)
        self.operatingFolder = os.path.join(self.baseFolder, self.datasetName)

        #self.countCheckinLocsEachUser(os.path.join(self.operatingFolder, "user_allChkIn_ListDict.txt"))

        #exit()

        #loadDict = Util.convert_String_Into_Dict2(self, self.operatingFolder, "user_allChkIn_location_dict.txt")
        loadDict = Util.convert_String_Into_Dict2(self, self.operatingFolder, "user_allChkIn_location_anonym_dict.txt")
        strTemp = ""
        totalCheckinsListDict = {}
        for user in loadDict.keys():
            if len(loadDict[user]) > 5:
                latLongListRound = []
                latLongList = list(loadDict[user])
                for latLong in latLongList:
                    latLongRoundTuple = (round(latLong[0], 2), round(latLong[1], 2))
                    latLongListRound.append(latLongRoundTuple)
                strTemp = strTemp + user + "\t" + str(latLongListRound) + "\n"
                totalCheckinsListDict[user] = latLongListRound

        strTemp2 = ""
        for user in totalCheckinsListDict.keys():
            uniqueLocsNumber = len(set(totalCheckinsListDict[user]))
            strTemp2 = strTemp2 + user + "\t" + str(uniqueLocsNumber) + "\n"
        self.createFile(os.path.join(self.baseFolder, self.datasetName, "NoOfCheckinListUniQ.txt"), strTemp2)

        self.createFile(os.path.join(self.baseFolder, self.datasetName, "user_allChkIn_location_dictRound.txt"), totalCheckinsListDict)
        self.createFile(os.path.join(self.baseFolder, self.datasetName, "user_allChkIn_ListDict.txt"), strTemp)

        #self.createUserLocListDict(os.path.join(self.baseFolder, self.datasetName, "Gowalla_totalCheckins.txt"), "Gowalla_totalCheckinsListDict.txt")

        loadDictEdges = Util.convert_String_Into_Dict2(self, self.operatingFolder, "Yelp_edges_anonym_Dict2.txt")
        strTempEdgesFile = ""
        strTempEdgesDict = {}

        for user in loadDictEdges.keys():
            strTempEdgesFriendList = []
            if user in totalCheckinsListDict.keys():
                ngbrs = list(loadDictEdges[user])
                for ngbr in ngbrs:
                    if ngbr in totalCheckinsListDict.keys():
                        strTempEdgesFile = strTempEdgesFile + str(user) + "\t" + str(ngbr)
                        strTempEdgesFriendList.append(str(ngbr))
            strTempEdgesDict[user] = strTempEdgesFriendList

        self.createFile(os.path.join(self.baseFolder, self.datasetName, "Yelp_edges_anonym_File_New.txt"), strTempEdgesFile)
        self.createFile(os.path.join(self.baseFolder, self.datasetName, "Yelp_edges_anonym_Dict_New.txt"), strTempEdgesDict)



    def countCheckinLocsEachUser(self, filePath):
        with open(filePath) as f:
            content = f.readlines()
        content = [x.strip() for x in content]

        strngTemp = ""
        for i in range(len(content)):
            splitArray = content[i].split("\t")
            if len(splitArray) > 1:
                userId = splitArray[0].strip()
                checkinList = ast.literal_eval(splitArray[1].strip())
                countCheckin = len(checkinList)
                countUniQCheckin = len(set(checkinList))
                strngTemp = strngTemp + str(userId) + "\t" + str(countCheckin) + "\t" + str(countUniQCheckin) + "\n"

        self.createFile(os.path.join(self.operatingFolder, "checkinAndUniqCheckinStats.txt"), strngTemp)

    def createUserLocListDict(self, filePath, fileToSave):
        with open(filePath) as f:
            content = f.readlines()
        content = [x.strip() for x in content]


        dictTemp = {}
        for i in range(len(content)):
            splitArray = content[i].split("\t")
            if len(splitArray) > 1:
                userId = splitArray[0].strip()
                lat = round(float(splitArray[2].strip()), 2)
                long = round(float(splitArray[3].strip()), 2)
                lat_long = (lat, long)

    def createFile(self, fileNameFullPath, contents):
        try:
            fw_fileName = open(fileNameFullPath, "w", encoding="utf8")
            fw_fileName.write(contents.__str__())
            fw_fileName.close()
        except KeyError:
            print("Error while creating file.. ", KeyError)
            pass

obj = PreProcessDatasetsYelp()