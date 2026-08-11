import os.path
import NurTestingPycharm.UtilNur as Util
import re
import ast
import time
from haversine import haversine

class SOS_AdaptiveV2:
    def __init__(self):
        print("SOS Spatial and SOS Adaptive using soical-spatial both")
        self.flagMinMax = "MaxSumMin"  # MaxMin, MaxSum, MaxSumMin score calculation of a set based on min max of diversity
        self.flagRandomSort = False  # arrange the S_Rel w.r.t. rel score?

        self.alpha = 0.5
        self.beta = 0.5
        self.omega = 0.5
        self.theta = 100
        self.thetaGS = 0.4
        self.k = 80  # 2, 4, 6, 8, 10    20, 40, 60, 80, 100
        self.m = 10  # return top m sets
        self.topSet_Score_m = []
        self.binId = "bin200"  # bin50, bin100, bin200, bin500, bin1000
        self.iterateN_Times = 1000

        self.baseFolder = "D:\\BACKUPMyWorks\\ExpDataUDI\\ExperimentFolder"
        self.datasetName = "Gowalla"   #Gowalla, Brightkite, Flickr, Yelp
        self.operatingFolder = os.path.join(self.baseFolder, self.datasetName)
        self.outputFolder = os.path.join(self.operatingFolder, "SOS")

        if self.datasetName == "Flickr":
            self.userLocationDict = self.convert_EachLines_Into_Dict(self.operatingFolder, "user_allChkIn_ListDict.txt")
            print("first dict loaded Flickr")
            self.socialNetwork = Util.convert_String_Into_Dict2(self, self.operatingFolder, "Flickr_edges_anonomyzed_Dict.txt")
            print("Len: ", len(self.socialNetwork))
        elif self.datasetName == "Yelp":
            self.userLocationDict = self.convert_EachLines_Into_Dict(self.operatingFolder, "user_allChkIn_ListDict.txt")
            print("first dict loaded Yelp")
            self.socialNetwork = Util.convert_String_Into_Dict2(self, self.operatingFolder, "Yelp_edges_anonym_Dict_New.txt")
            print("Len: ", len(self.socialNetwork))
        else:
            self.userLocationDict = Util.convert_String_Into_Dict2(self, self.operatingFolder, "user_allChkIn_location_dictRound.txt")
            print("first dict loaded")
            self.socialNetwork = Util.convert_String_Into_Dict2(self, self.operatingFolder, self.datasetName + "_edges_Dict.txt")
            print("Len: ", len(self.socialNetwork))
        #self.userLocationDict = Util.convert_String_Into_Dict2(self, self.operatingFolder, "user_allChkIn_location_dictRound.txt")
        #self.socialNetwork = Util.convert_String_Into_Dict2(self, self.operatingFolder,  self.datasetName+"_edges_Dict.txt")

        # self.userLocationDictUserList = ["4"]
        self.userLocationDictUserList = self.convert_String_Into_List(os.path.join(self.outputFolder, "CheckinBins"), self.binId + ".txt")
        print("size: ", len(self.userLocationDictUserList))
        # self.userLocationDictUserList = ["8991"]

        self.newUserList = []

        for user in self.userLocationDictUserList:
            L = self.userLocationDict[user]
            noOfLoc = len(L)
            if user in self.socialNetwork.keys() and len(self.socialNetwork[user]) > 5 and len(set(L)) > self.k:
                # print("len: self.socialNetwork[user]): ", len(self.socialNetwork[user]), "len(set(L)): ",len(set(L)))
                self.newUserList.append(user)  # Will process only these users further as they have satisfied minimum requirements

        # for user in self.userLocationDict.keys():
        self.startBegin = time.time()

        mmdStr = ""
        mmdStrDgs = ""
        itr = 0
        for user in self.newUserList:
            itr = itr + 1
            if (itr > self.iterateN_Times):
                break
            self.bestScore = 0
            L = self.userLocationDict[user]
            noOfLoc = len(L)
            if user in self.socialNetwork.keys() and len(self.socialNetwork[user]) > 5 and len(set(L)) > self.k:
                ngbrsList = self.socialNetwork[user]
                #self.socialNetwork = {} ##############################################Release memory, but please comment in original execution
                ngbrLocs = []
                for ngbrs in ngbrsList:
                    if ngbrs in self.userLocationDict.keys():
                        ngbrLocs = ngbrLocs + self.userLocationDict[ngbrs]
                self.ngbrLocCombinedUnique = list(set(ngbrLocs))
                #print("processing user:", user, ", self.k:", self.k, ", friends:", len(ngbrsList), ", ngbr number of loc:", len(self.ngbrLocCombinedUnique), ", noOfLoc: ", noOfLoc, ", uniQ Loc: ", len(set(L)))
                if len(self.ngbrLocCombinedUnique) < 1:
                    continue
                locIdLocMap = {}
                strLoc = ""
                lId = 0
                self.locNameAndLocId = {}
                for l in L:
                    self.locNameAndLocId[l] = lId
                    l = str(l).replace("(", "").replace(")", "").strip()
                    strLoc = strLoc + str(lId) + "\t" + str(l) + "\n"
                    locIdLocMap[lId] = l
                    lId += 1
                #self.createFile(os.path.join(self.outputFolder, "Location", str(user) + ".txt"), strLoc)

                startEachLoop = time.time()

                self.L = list(set(L))  # converting into set rather than list. set will contain unique elements
                self.maxD = self.calcMaxD(self.L)
                self.socialScoreDict = self.calcSocialScore(self.L, ngbrsList, user)
                #self.loadDgsContents(os.path.join(self.outputFolder, "Diversity", str(user) + ".txt"))  # loading self.content and creating self.locAndIndex

                returnTempSocSpatDict = self.socialAndSpatialSimilarity(self.L, ngbrsList, user)
                self.totalSimEachLocDict = returnTempSocSpatDict[0]
                self.totalSocSpatSimEachLocDict = returnTempSocSpatDict[1]

                self.twoDArray = self.loadDgsContents(os.path.join(self.outputFolder, "GeoSocialSimilarity", str(user) + ".txt"))  # loading self.content and creating self.locAndIndex

                #Spatial SOS starts
                sorted_d_Spatial = Util.sortDictByValueWithKey(self.totalSimEachLocDict)  # return (-37.73, 145.06): 0.99, (-37.19, 145.28): 0.98, (-37.56, 145.92): 0.97 in descending order
                self.arrangedList_Spatial = [x[0] for x in sorted_d_Spatial]
                self.S_Spatial = []
                if len(self.arrangedList_Spatial) > self.k:
                    while len(self.S_Spatial) < self.k and len(self.arrangedList_Spatial) > 0:
                        topLoc = self.arrangedList_Spatial[0]
                        self.S_Spatial.append(topLoc)
                        self.arrangedList_Spatial.remove(topLoc)
                        for loc2 in self.arrangedList_Spatial:
                            dist = haversine(topLoc, loc2)
                            if dist < self.theta:
                                self.arrangedList_Spatial.remove(loc2)

                #print("Spatial Set: S_Spatial ", self.S_Spatial)

                # SocioSpatial SOS starts
                sorted_d_SocSpatial = Util.sortDictByValueWithKey(self.totalSocSpatSimEachLocDict)  # return (-37.73, 145.06): 0.99, (-37.19, 145.28): 0.98, (-37.56, 145.92): 0.97 in descending order
                self.arrangedList_SocSpatial = [x[0] for x in sorted_d_SocSpatial]
                self.S_SocSpatial = []
                if len(self.arrangedList_SocSpatial) > self.k:
                    while len(self.S_SocSpatial) < self.k and len(self.arrangedList_SocSpatial) > 0:
                        topLoc = self.arrangedList_SocSpatial[0]
                        self.S_SocSpatial.append(topLoc)
                        self.arrangedList_SocSpatial.remove(topLoc)
                        for loc2 in self.arrangedList_SocSpatial:
                            similarity = self.dictOfDgsFromFileAndFlyNewLatest(topLoc, loc2)
                            if similarity > self.theta:
                                self.arrangedList_Spatial.remove(loc2)
                #print("Social Spatial Set: S_SocioSpatial ", self.S_SocSpatial)

                process = psutil.Process(os.getpid())
                rssMemoryTemp = float(process.memory_info().rss)
                totalRssMemory = totalRssMemory + rssMemoryTemp
                if rssMemoryTemp > maxRssMemory:
                    maxRssMemory = rssMemoryTemp
                endEachLoop = time.time()
                print("Each loop time diff:", endEachLoop - startEachLoop, "memory: ", round(maxRssMemory / (1024 * 1024), 2))

                #self.createFile(os.path.join(self.outputFolder, "Results", str(self.binId), str(self.k), str(user)+"_Spat_"+str(self.k) + ".txt"), self.S_Spatial)
                #self.createFile(os.path.join(self.outputFolder, "Results", str(self.binId), str(self.k), str(user) + "_SocSpat_" + str(self.k) + ".txt"), self.S_SocSpatial)

                continue

                minDistTotal = 0
                minDistTotalDgs = 0
                for ngbrs in ngbrsList:
                    if ngbrs in self.userLocationDict.keys():
                        ngbrLocs = self.userLocationDict[ngbrs]
                        tempList = []
                        tempListDgs = []
                        for ngbrloc in ngbrLocs:
                            tempList.append(min([haversine(ngbrloc, loc, miles=False) for loc in self.S_Spatial]))
                            tempListDgs.append(min([(1 - self.dictOfDgsFromFileAndFlyNewLatest(ngbrloc, loc)) for loc in self.S_Spatial]))
                        minDist = round(min(tempList),2)
                        minDistTotal = minDistTotal + minDist

                        minDistDgs = round(min(tempListDgs), 2)
                        minDistTotalDgs = minDistTotalDgs + minDistDgs
                mmdStr = mmdStr + str(user) + "\t" + str(round(minDistTotal / len(ngbrsList), 2)) + "\n"
                mmdStrDgs = mmdStrDgs + str(user) + "\t" + str(round(minDistTotalDgs / len(ngbrsList), 2)) + "\n"
        self.createFile(os.path.join(self.outputFolder, "mmdSpatial_k"+str(self.k)+".txt"), mmdStr)
        self.createFile(os.path.join(self.outputFolder, "mmdSocioSpatial_k"+str(self.k)+".txt"), mmdStrDgs)

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

    def calcSocialScore(self, L, socialNetworkNgbrList, userId):
        userDegree = len(socialNetworkNgbrList)
        socScore = {}
        strTemp = ""
        for loc in L:
            totalNgbrChks = 0
            for ngbr in socialNetworkNgbrList:
                if ngbr in self.userLocationDict.keys() and loc in self.userLocationDict[ngbr]:
                    totalNgbrChks += 1
            socScore[loc] = round(totalNgbrChks / userDegree, 2)
            strTemp = strTemp + str(loc) + "\t" + str(round(totalNgbrChks / userDegree, 2)) + "\n"
        self.createFile(os.path.join(self.outputFolder, "SocialScore", str(userId)+ ".txt"), strTemp)
        return socScore

    def calcMaxD(self, L):
        maxD = 0
        for loc1 in L:
            maxTemp = max([Util.haversineDist(loc1, lc) for lc in L])
            if maxTemp > maxD:
                maxD = maxTemp
        return round(maxD, 2)

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
            #print("locations are not available in self.locAndIndex list")
            return 0

    def socialAndSpatialSimilarity(self, L, socialNetworkNgbrList, userId):
        locationNgbrCheckinDict = {}
        locationNgbrCheckinText = ""

        for loc in L:
            tempList = []
            for ngbr in socialNetworkNgbrList:
                if ngbr in self.userLocationDict.keys() and loc in self.userLocationDict[ngbr]:
                    tempList.append(ngbr)
            locationNgbrCheckinDict[loc] = tempList
            #locationNgbrCheckinText = locationNgbrCheckinText + str(loc) + "\t" + str(tempList) + "\n"
        #self.createFile(os.path.join(self.outputFolder, "LocChknNgbr", str(userId) + ".txt"), locationNgbrCheckinText)

        soicalSimilarity = ""
        geoSoicalSimilarity = ""
        socSimToWhole_Dict = {}
        geoSocSimToWhole_Dict = {}
        for loc in L:
            tempPerRow = str(loc)
            tempPerRowGS = str(loc)
            socSimTotal = 0
            geoSocSimTotal = 0
            for loc2 in L:
                if loc in locationNgbrCheckinDict.keys() and loc2 in locationNgbrCheckinDict.keys():
                    common = len(set(locationNgbrCheckinDict[loc]).intersection(locationNgbrCheckinDict[loc2]))
                    union = len(set(locationNgbrCheckinDict[loc]).union(locationNgbrCheckinDict[loc2]))
                    dist = round(Util.haversineDist(loc, loc2), 2)
                    if union > 0:
                        socSim = round((common / union), 2)
                    else:
                        socSim = 0
                    spatSim = 1 - round((dist / self.maxD), 2)

                    geoSocSimFinal = round((self.beta * socSim + (1 - self.beta) * spatSim), 2)
                    tempPerRow = tempPerRow + "\t" + str(socSim)
                    tempPerRowGS = tempPerRowGS + "\t" + str(geoSocSimFinal)

                    socSimTotal = socSimTotal + socSim
                    geoSocSimTotal = geoSocSimTotal + geoSocSimFinal
            soicalSimilarity = soicalSimilarity + tempPerRow + "\n"
            geoSoicalSimilarity = geoSoicalSimilarity + tempPerRowGS + "\n"
            # socSpatDivCalcStr = socSpatDivCalcStr + str(loc) + "\t" + str(loc2) + "\t" + str(common) + "\t" + str(union) + "\t" + str(socDiv) + "\t" + str(dist) + "\t" + str(self.maxD) + "\t" + str(spatDiv) + "\t" + str(geoSocDivFinal) + "\n"
            socSimToWhole_Dict[loc] = socSimTotal
            geoSocSimToWhole_Dict[loc] = geoSocSimTotal

        #logging.info("Going to create socia spatial diversity file. Header is: loc1, loc2, common user count, union count, social div, dist in KM, maxD, spatial diversity, geo-Social Diversity")
        self.createFile(os.path.join(self.outputFolder, "SocialSimilarity", str(userId) + ".txt"), soicalSimilarity)
        self.createFile(os.path.join(self.outputFolder, "GeoSocialSimilarity", str(userId) + ".txt"), geoSoicalSimilarity)
        return [socSimToWhole_Dict, geoSocSimToWhole_Dict]

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

    def createFile(self, fileNameFullPath, contents):
        try:
            fw_fileName = open(fileNameFullPath, "w", encoding="utf8")
            fw_fileName.write(contents.__str__())
            fw_fileName.close()
        except KeyError:
            print("Error while creating file.. ", KeyError)
            pass

obj = SOS_AdaptiveV2()