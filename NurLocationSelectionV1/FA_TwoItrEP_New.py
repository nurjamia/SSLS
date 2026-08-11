import os.path
import operator
from scipy.spatial.distance import cdist
import NurTestingPycharm.UtilNur as Util
import logging
import time
import random
import re
import ast
import psutil
import heapq
from pathlib import Path

class FA_New:
    def __init__(self):
        print("more clean and flexible FA_New, only considers Preprocessed file...")
        self.flagMinMax = "MaxSumMin"  # MaxMin, MaxSum, MaxSumMin score calculation of a set based on min max of diversity
        flagRemoveExistingFiles = False  # True will remove the .txt already exists in the folders 'Diversity, RelScore, Location, LocChknNgbr'
        self.flagRandomSort = False # arrange the S_Rel w.r.t. rel score?

        self.alpha = 0.5
        self.beta = 0.5
        self.omega = 0.5
        self.k = 20  # top k items should be returned 2, 4, 6, 8, 10    20, 40, 60, 80, 100
        self.m = 10 # return top m sets
        self.topSet_Score_m = []
        self.binId = "bin200" # bin50, bin100, bin200, bin500, bin1000
        self.iterateN_Times = 1000
        self.numberOfLoopsToIterate = 2 #The parameter to iterate the outerloops

        self.baseFolder = "D:\\BACKUPMyWorks\\ExpDataUDI\\ExperimentFolder"
        self.datasetName = "Yelp" #Gowalla, Brightkite, Flickr, Yelp
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
            self.socialNetwork = Util.convert_String_Into_Dict2(self, self.operatingFolder, self.datasetName+"_edges_Dict.txt")

        #self.userLocationDictUserList = ["4"]
        self.userLocationDictUserList = self.convert_String_Into_List(os.path.join(self.outputFolder, "CheckinBins"), self.binId+".txt")
        print("size: ", len(self.userLocationDictUserList))
        #self.userLocationDictUserList = ["10"]

        # Delete existing .txt files from the Folders Diversity, RelScore, Location, LocChknNgbr folders under self.outputFolder Path
        if flagRemoveExistingFiles:
            self.deleteFilesInFolder(os.path.join(self.outputFolder, "Location", self.binId))
            self.deleteFilesInFolder(os.path.join(self.outputFolder, "Diversity", self.binId))
            self.deleteFilesInFolder(os.path.join(self.outputFolder, "RelScore", self.binId))
            self.deleteFilesInFolder(os.path.join(self.outputFolder, "LocChknNgbr", self.binId))

        self.newUserList = []

        for user in self.userLocationDictUserList:
            L = self.userLocationDict[user]
            noOfLoc = len(L)
            if user in self.socialNetwork.keys() and len(self.socialNetwork[user]) > 5 and len(set(L)) > self.k:
                # print("len: self.socialNetwork[user]): ", len(self.socialNetwork[user]), "len(set(L)): ",len(set(L)))
                self.newUserList.append(user)  # Will process only these users further as they have satisfied minimum requirements
        '''
        # for user in self.userLocationDict.keys():
        for user in self.userLocationDictUserList:
            self.bestScore = 0
            L = self.userLocationDict[user]
            noOfLoc = len(L)
            if user in self.socialNetwork.keys() and len(self.socialNetwork[user]) > 5 and len(set(L)) > self.k:
                # print("len: self.socialNetwork[user]): ", len(self.socialNetwork[user]), "len(set(L)): ",len(set(L)))
                self.newUserList.append(user)  # Will process only these users further as they have satisfied minimum requirements
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
                self.L = list(set(L))  # converting into set rather than list. set will contain unique elements

                locIdLocMap = {}
                strLoc = ""
                lId = 0
                self.locNameAndLocId = {}
                for l in self.L:
                    self.locNameAndLocId[l] = lId
                    l = str(l).replace("(", "").replace(")", "").strip()
                    strLoc = strLoc + str(lId) + "\t" + str(l) + "\n"
                    locIdLocMap[lId] = l
                    lId += 1
                self.createFile(os.path.join(self.outputFolder, "Location", self.binId, str(user) + ".txt"), strLoc)

                self.socialScoreDict = self.calcSocialScore(self.L, ngbrsList)
                self.d_m_dict = self.calcMaxDist(self.L, self.ngbrLocCombinedUnique)
                # print("d_m: ", self.d_m)
                self.maxD = self.calcMaxD(self.L)
                self.spatialScoreDict = self.calcSpatialScore(self.L, ngbrsList)
                self.S_gs_Dict = self.calcRelevanceScore(self.socialScoreDict, self.spatialScoreDict, user)

                self.socialSpatialDiversity(self.L, ngbrsList, user)
                contents = self.loadDgsContents(os.path.join(self.outputFolder, "Diversity", self.binId, str(user) + ".txt"))  # loading self.content and creating self.locAndIndex
        '''
        # original EP starts here.
        start = time.time()
        maxRssMemory = 0
        totalRssMemory = 0
        print("total users to process in newUserList: ", len(self.newUserList))
        itr = 0
        for userId in self.newUserList:
            itr = itr + 1
            if(itr > self.iterateN_Times):
                print(itr, "done")
                break
            self.bestScore = 0
            if os.path.exists(os.path.join(self.outputFolder, "RelScore", self.binId, str(userId) + "_Rel.txt")) == False:
                continue
            f = open(os.path.join(self.outputFolder, "RelScore", self.binId, str(userId) + "_Rel.txt"), "r")
            content = f.readlines()
            content = [x.strip() for x in content]
            self.locAndIndex = []
            self.Rel_Score_Array = []
            self.loc_relScore_dict = {}
            for i in range(len(content)):
                splitArray = content[i].split("\t")
                if len(splitArray) > 1:
                    loc = eval(splitArray[1].strip())
                    self.locAndIndex.append(loc)
                    relScore = float(splitArray[4].strip())
                    self.Rel_Score_Array.append(relScore)
                    self.loc_relScore_dict[loc] = relScore
            f.close()

            if os.path.exists(os.path.join(self.outputFolder, "Diversity", self.binId, str(userId) + ".txt")) == False:
                continue
            f_div = open(os.path.join(self.outputFolder, "Diversity", self.binId, str(userId) + ".txt"), "r")
            content_div = f_div.readlines()
            self.content_div = [x.strip() for x in content_div]

            startEachLoop = time.time()
            S_I = []
            self.S_Rel = self.sortDesc(self.loc_relScore_dict)
            if self.flagRandomSort:
                random.shuffle(self.S_Rel)

            self.l = tuple
            self.S = []
            self.ResultListStr = ""
            self.ResultList = []

            # S_R = list(self.S_R) #making a different list S_R
            outerloop = 0

            #while True:
            if outerloop <= self.numberOfLoopsToIterate:
                outerloop += 1 # outerloop is useful for Fast Approximate Approach
                S_R = list(self.S_Rel)  # making a different list S_R, everytime S_R will decrease when S_Rel decreases and make list at that time
                if len(self.S_Rel) < self.k:
                    break
                if len(S_I) == 0:
                    self.l = S_R[0] #pop the top relevant location from S_R
                    S_R.remove(self.l)
                    self.S_Rel.remove(self.S_Rel[0])  # no user of S_Rel, just to iterate the list
                    #print("self.l ", self.l)
                    S_I.append(self.l)
                    # print("After pop, length of SR: ", len(S_R))

                while len(S_I) < self.k:
                    if len(S_I) > 1 and self.bestScore > 0:
                        flag = self.earlyTerminationNew(self.bestScore, S_I, S_R, self.k)
                        if flag:
                            # print("Early terminate for location root: ,,,,,,,,,, ", S_I[0])
                            #print("break: SI ", S_I)
                            S_I = []
                            break
                    topRelLoc = S_R[0]
                    topRelScore = self.loc_relScore_dict[topRelLoc]
                    D_max = self.calcDgsMax(S_R, S_I)
                    lowerRelBoundSgs = self.calcRelLowerBound(topRelScore, D_max, topRelLoc, S_I)
                    tempSR = list(S_R)
                    tempSR.remove(topRelLoc)
                    VP = self.potentialLocs(tempSR, lowerRelBoundSgs)
                    referenceTopSet = list(S_I)
                    referenceTopSet.append(topRelLoc)
                    self.scoreTop = self.calcTotalScoreofSet(referenceTopSet)
                    # print("scoreTop: ", self.scoreTop)

                    # print("S_I old: ", S_I, "S_R old: ", S_R)
                    for loc in VP:
                        tempLocSet = list(S_I)
                        tempLocSet.append(loc)
                        score = self.calcTotalScoreofSet(tempLocSet)
                        if score > self.scoreTop:
                            self.scoreTop = score
                            topRelLoc = loc  # dont confuse the term topRelLoc!!!

                    S_I.append(topRelLoc)
                    S_R.remove(topRelLoc)
                    S_R = list(self.arrangeListBasedOnRelScore(S_R))

                    if len(S_I) == self.k:
                        if self.scoreTop > self.bestScore:
                            self.bestScore = self.scoreTop
                            self.S = list(S_I)
                        S_I = []
                        break

            #print("user id: ", userId, "Result R: ", self.S)

            # memory consumed max and average in bytes
            process = psutil.Process(os.getpid())
            rssMemoryTemp = float(process.memory_info().rss)
            totalRssMemory = totalRssMemory + rssMemoryTemp
            if rssMemoryTemp > maxRssMemory:
                maxRssMemory = rssMemoryTemp
            endEachLoop = time.time()
            print("Each loop time diff:", endEachLoop - startEachLoop, "memory: ", round(maxRssMemory / (1024 * 1024), 2))

        endTime = time.time()
        print("Max Memory consumed: ", round(maxRssMemory / (1024 * 1024), 2), "MB, and Average memory: ", round(totalRssMemory / (1024 * 1024 * len(self.newUserList)), 2), "MB")
        print("Start Time: ", start, ", end time: ", endTime, "Difference: ", endTime - start, "Filtered Size: ", len(self.newUserList), "Original Size in Bin:", len(self.userLocationDictUserList), "Iterated: ", self.iterateN_Times)

    def earlyTerminationNew(self, bestScore, S_I, S_R, k):
        statFlag = False
        scoreSI = self.calcTotalScoreofSet(S_I)
        relSR_temp =[]
        divSR_temp = []
        for loc in S_R:
            relSR_temp.append(self.loc_relScore_dict[loc])
            dgsTemp = []
            for loc2 in S_I:
                dgsTemp.append(self.dictOfDgsFromFileAndFlyNew(loc, loc2))
            divSR_temp.append(min(dgsTemp))
        topRelScoresAdd = sum(heapq.nlargest(k - len(S_I), relSR_temp))
        topDivWithSIAdd = sum(heapq.nlargest(k - len(S_I), divSR_temp))

        #F_max = k * (self.omega * relScore + (1 - self.omega) * DgsM)
        F_max = scoreSI + self.omega*topRelScoresAdd + (1 - self.omega)*topDivWithSIAdd
        if bestScore > F_max:
            statFlag = True
        return statFlag

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

    def calcSocialScore(self, L, socialNetworkNgbrList):
        userDegree = len(socialNetworkNgbrList)
        socScore = {}

        for loc in L:
            totalNgbrChks = 0
            for ngbr in socialNetworkNgbrList:
                if ngbr in self.userLocationDict.keys() and loc in self.userLocationDict[ngbr]:
                    totalNgbrChks += 1
            socScore[loc] = round(totalNgbrChks / userDegree, 2)
        return socScore

    def calcMaxDist(self, L, ngbrLocCombinedUnique):
        logging.info("Going to calculate max Dist between location checked-in by user and location checked-in by neighbors using Haversine.")
        maxDist = 0
        maxDistEachLocAllNgbrs = {}
        for loc in L:
            dtempMax = max([Util.haversineDist(loc, lc) for lc in ngbrLocCombinedUnique])
            maxDistEachLocAllNgbrs[loc] = round(dtempMax, 2)
            #if dtempMax > maxDist:
            #    maxDist = dtempMax
        return maxDistEachLocAllNgbrs

    def calcMaxD(self, L):
        logging.info("Calculating the maxD maximum distance of checkin locaitons of particular user u.")
        maxD = 0
        for loc1 in L:
            maxTemp = max([Util.haversineDist(loc1, lc) for lc in L])
            if maxTemp > maxD:
                maxD = maxTemp
        return round(maxD, 2)

    def calcSpatialScore(self, L, socialNetworkNgbrList):
        logging.info("Going to calculate spatial score of each location w.r.t. user u")
        userDegree = len(socialNetworkNgbrList)
        spatialScore = {}
        for loc in L:
            totalDist = 0
            for ngbr in socialNetworkNgbrList:
                if ngbr in self.userLocationDict.keys():
                    locListNgbr = self.userLocationDict[ngbr]
                    misDistTemp = min([Util.haversineDist(loc, l) for l in locListNgbr])
                    totalDist += misDistTemp
            if self.d_m_dict[loc] > 0:
                scoreSPTemp = 1 - (totalDist/(self.d_m_dict[loc] * userDegree))
            else:
                scoreSPTemp = 0
            spatialScore[loc] = round(scoreSPTemp, 2)
        return spatialScore

    def calcRelevanceScore(self, S_sc, S_sp, userId):
        S_gs = {}
        S_gs_Text = ""
        for loc in S_sc.keys():
            if loc in S_sp.keys():
                lId = self.locNameAndLocId[loc]
                score = round((self.alpha*S_sc[loc] + (1-self.alpha)*S_sp[loc]), 2)
                S_gs[loc] = score
                S_gs_Text = S_gs_Text + str(lId) + "\t" + str(loc) + "\t" + str(S_sc[loc]) + "\t" + str(S_sp[loc]) + "\t" + str(score) + "\n"
        self.createFile(os.path.join(self.outputFolder, "RelScore", str(userId) + "_Rel.txt"), S_gs_Text)
        return S_gs

    def socialSpatialDiversity(self, L, socialNetworkNgbrList, userId):
        logging.info("Spatial diversity and social diversity calculation")
        locationNgbrCheckinDict = {}
        locationNgbrCheckinText = ""

        for loc in L:
            tempList = []
            for ngbr in socialNetworkNgbrList:
                if ngbr in self.userLocationDict.keys() and loc in self.userLocationDict[ngbr]:
                    tempList.append(ngbr)
            locationNgbrCheckinDict[loc] = tempList
            locationNgbrCheckinText = locationNgbrCheckinText + str(loc)+ "\t" + str(tempList)+ "\n"
        self.createFile(os.path.join(self.outputFolder, "LocChknNgbr", str(userId) + ".txt"), locationNgbrCheckinText)

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

        logging.info("Going to create socia spatial diversity file. Header is: loc1, loc2, common user count, union count, social div, dist in KM, maxD, spatial diversity, geo-Social Diversity")
        self.createFile(os.path.join(self.outputFolder, "Diversity", str(userId) + ".txt"), socSpatDivCalcStr)

    def loadDgsContents(self, filePath):
        f = open(filePath, "r")
        self.content = f.readlines()
        self.content = [x.strip() for x in self.content]
        self.locAndIndex = []
        for i in range(len(self.content)):
            splitArray = self.content[i].split("\t")
            if len(splitArray) > 1:
                loc = eval(splitArray[0].strip())
                self.locAndIndex.append(loc)

        return self.content

    def dictOfDgsFromFileAndFly(self, content, locAndIndex, loc1_Q, loc2_Q):
        '''
        for i in range(len(content)):
            splitArray = content[i].split("\t")
            if len(splitArray) > 1:
                loc = eval(splitArray[0].strip())
                locAndIndex.append(loc)
        '''
        for i in range(len(content)):
            splitArray = content[i].split("\t")
            if len(splitArray) > 1:
                loc1Temp = eval(splitArray[0].strip())
                if loc1Temp == loc1_Q and loc2_Q in locAndIndex:
                    loc2Index = locAndIndex.index(loc2_Q)
                    tempValDgs = splitArray[loc2Index + 1]

                    return float(tempValDgs)

    def dictOfDgsFromFileAndFlyNew(self, loc1_Q, loc2_Q):
        if loc1_Q in self.locAndIndex and loc2_Q in self.locAndIndex:
            loc1_Index = self.locAndIndex.index(loc1_Q)
            loc2_Index = self.locAndIndex.index(loc2_Q)
            if len(self.content_div) >= loc1_Index:
                splitArray = self.content_div[loc1_Index].split("\t")
                if len(splitArray) > 1:
                    tempValDgs = splitArray[loc2_Index + 1]

                    return float(tempValDgs)
        else:
            print("locations are not available in self.locAndIndex list")
            return 0

    def sortDesc(self, dictInput):
        logging.info("Arrange dict w.r.t. descending.")
        #sorted_d = dict(sorted(socialScoreDict.items(), key=operator.itemgetter(1), reverse=True))
        sorted_d = Util.sortDictByValueWithKey(dictInput) #return (-37.73, 145.06): 0.99, (-37.19, 145.28): 0.98, (-37.56, 145.92): 0.97 in descending order
        arrangedKeysOnly = [x[0] for x in sorted_d]
        return arrangedKeysOnly # return [(-37.73, 145.06), (-37.19, 145.28), (-37.56, 145.92)] as list
        #return sorted_d #return (-37.73, 145.06): 0.99, (-37.19, 145.28): 0.98, (-37.56, 145.92): 0.97 in descending order

    def earlyTermination(self, bestScore, relScore, DgsM, k):
        statFlag = False
        F_max = k*(self.omega*relScore + (1 - self.omega)*DgsM)
        if bestScore > F_max:
            statFlag = True
        return statFlag

    def calcDgsMax(self, S_R, S_I):
        tt = []
        for loc in S_R:
            tt.append(self.calcDgsOfLocToSet(loc, S_I))
        maxDiv = max(tt)
        return maxDiv

    def calcDgsOfLocToSet(self, loc, S):
        #minDgs = min([self.DgsDictAll[(loc, l)] for l in S]) #*********************************************
        #minDgs = min([self.dictOfDgsFromFileAndFly(self.content, self.locAndIndex, loc, l) for l in S]) #*********************************************
        minDgs = min([self.dictOfDgsFromFileAndFlyNew(loc, l) for l in S])  # *********************************************
        return minDgs

    def calcRelLowerBound(self, topRelScore, D_max, topRelLoc, S_I):
        S_I_dash = list(S_I)
        S_I_dash.append(topRelLoc)
        Dgs_SI_dash = self.calcDgsOfSet(S_I_dash)
        Dgs_SI = self.calcDgsOfSet(S_I)
        #print("Dgs_SI_dash: ", Dgs_SI_dash, ", Dgs_SI", Dgs_SI)
        Sgs_lower = topRelScore + ((1-self.omega)/self.omega)*(Dgs_SI_dash - Dgs_SI - D_max)
        #print("Sgs_lower: ", Sgs_lower)
        return round(Sgs_lower,2)

    def calcDgsOfSet(self, S):
        totalDgs = 0
        #S = [(-37.73, 145.06), (-37.56, 145.92), (-37.18, 145.38), (-37.33, 145.29)]
        if len(S) <= 1:
            return 0
        for loc in S:
            S_setminus = set(S)
            S_setminus.remove(loc)
            #if (loc, l) in self.DgsDictAll.keys:
            #minDgs = min([self.DgsDictAll[(loc, l)] for l in S_setminus]) #*********************************************
            #minDgs = min([self.dictOfDgsFromFileAndFly(self.content, self.locAndIndex, loc, l) for l in S_setminus]) #*********************************************
            minDgs = min([self.dictOfDgsFromFileAndFlyNew(loc, l) for l in S_setminus])  # *********************************************
            totalDgs += minDgs
        return totalDgs

    def potentialLocs(self, S_R_copy, lowerRelBoundSgs_copy):
        potentialLocDict = {}
        for loc in S_R_copy:
            if self.loc_relScore_dict[loc] > lowerRelBoundSgs_copy:
                potentialLocDict[loc] = self.loc_relScore_dict[loc]
        #arrange w.r.t. rel score
        arrangedPotLoc = self.sortDesc(potentialLocDict)
        #print("potentialLocDict", potentialLocDict, "arrangedPotLoc: ", arrangedPotLoc)
        return arrangedPotLoc

    def calcTotalScoreofSet(self, S):
        if self.flagMinMax == "MaxMin":
            totalSgs = 0
            minDgsTemp = []
            for loc in S:
                totalSgs += self.loc_relScore_dict[loc]
                S_setminus = set(S)
                S_setminus.remove(loc)
                for loc2 in S_setminus:
                    #minDgsTemp.append(self.DgsDictAll[loc, loc2]) #*********************************************
                    #minDgsTemp.append(self.dictOfDgsFromFileAndFly(self.content, self.locAndIndex, loc, loc2)) #*********************************************
                    minDgsTemp.append(self.dictOfDgsFromFileAndFlyNew(loc, loc2))  # *********************************************
            minDgsSet = min(minDgsTemp)
            totalscore = self.omega * totalSgs + (1 - self.omega) * minDgsSet
            return round(totalscore, 2)

        if self.flagMinMax == "MaxSum":
            totalSgs = 0
            totalDgs = 0
            for loc in S:
                totalSgs += self.loc_relScore_dict[loc]
                S_setminus = set(S)
                S_setminus.remove(loc)
                for loc2 in S_setminus:
                    #totalDgs += self.dictOfDgsFromFileAndFly(self.content, self.locAndIndex, loc, loc2)
                    totalDgs += self.dictOfDgsFromFileAndFlyNew(loc, loc2)
            totalscore = self.omega*totalSgs + (1 - self.omega)*totalDgs
            return round(totalscore, 2)

        if self.flagMinMax == "MaxSumMin":
            totalSgs = 0
            totalDgs = 0
            for loc in S:
                minDgsTemp = []
                totalSgs += self.loc_relScore_dict[loc]
                S_setminus = set(S)
                S_setminus.remove(loc)
                for loc2 in S_setminus:
                    #totalDgs += self.DgsDictAll[loc, loc2] #*********************************************
                    #minDgsTemp.append(self.dictOfDgsFromFileAndFly(self.content, self.locAndIndex, loc, loc2)) #*********************************************
                    minDgsTemp.append(self.dictOfDgsFromFileAndFlyNew(loc, loc2))  # *********************************************
                totalDgs += min(minDgsTemp)
            totalscore = self.omega*totalSgs + (1 - self.omega)*totalDgs
            return round(totalscore, 2)

    def arrangeListBasedOnRelScore(self, lst):
        tempDict = {}
        for l in lst:
            tempDict[l] = self.loc_relScore_dict[l]
        arrabgeList = self.sortDesc(tempDict)
        return arrabgeList

    def minDiversitySetOfEachLoc(self, finalS):
        print("Going to calculate <loc1 loc2 minDiv> for final set.")
        textMinDivEachLoc = ""
        for loc in finalS:
            lId = self.locNameAndLocId[loc]
            S_setminus = set(finalS)
            S_setminus.remove(loc)
            # if (loc, l) in self.DgsDictAll.keys:
            #minDgs = min([self.DgsDictAll[(loc, l)] for l in S_setminus]) # *************************************************
            #minDgs = min([self.dictOfDgsFromFileAndFly(self.content, self.locAndIndex, loc, l) for l in S_setminus]) # *************************************************
            minDgs = min([self.dictOfDgsFromFileAndFlyNew(loc, l) for l in S_setminus])  # *************************************************
            locTemp = ""
            for lc in S_setminus:
                #if (self.dictOfDgsFromFileAndFly(self.content, self.locAndIndex, loc, lc) == minDgs): #********************************************
                if (self.dictOfDgsFromFileAndFlyNew(loc, lc) == minDgs):  # ********************************************
                    locTemp = lc
            textMinDivEachLoc = textMinDivEachLoc + str(lId) + "\t" + str(loc) + "\t" + str(self.loc_relScore_dict[loc]) + "\t" + str(self.locNameAndLocId[locTemp]) + "\t" + str(locTemp) + "\t" + str(minDgs) + "\n"
        self.createFile("E:\\NurProjectPython\\PycharmProjects\\All\\NurLocationSelection\\finalSetWithDivPlus.txt", textMinDivEachLoc)

    def deleteFilesInFolder(self, folderPath):
        for f in Path(folderPath).glob('*.txt'):
            try:
                f.unlink()
            except OSError as e:
                print("Error: %s : %s" % (f, e.strerror))

    def createFile(self, fileNameFullPath, contents):
        try:
            fw_fileName = open(fileNameFullPath, "w", encoding="utf8")
            fw_fileName.write(contents.__str__())
            fw_fileName.close()
        except KeyError:
            print("Error while creating file.. ", KeyError)
            pass

objec = FA_New()