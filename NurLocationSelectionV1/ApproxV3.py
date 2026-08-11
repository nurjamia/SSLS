import NurTestingPycharm.UtilNur as Util
import logging
import time
import os.path
import ast
import re
import random
import psutil
import heapq
from pathlib import Path


class ApproxV3:
    def __init__(self):
        print("Version 3 of Approximate Algo (Revision Response). where pruning and termination is considered.")
        self.flagMinMax = "MaxSumMin"  # MaxMin, MaxSum, MaxSumMin score calculation of a set based on min max of diversity
        flagRemoveExistingFiles = False  # True will remove the .txt already exists in the folders 'Diversity, RelScore, Location, LocChknNgbr'
        self.flagRandomSort = False  # arrange the S_Rel w.r.t. rel score?
        self.FlagFS = False

        self.alpha = 0.5
        self.beta = 0.5
        self.omega = 0.5
        self.k = 10  # top k items should be returned 2, 4, 6, 8, 10    20, 40, 60, 80, 100
        self.m = 10  # return top m sets
        self.topSet_Score_m = []
        self.binId = "bin100"  # bin50, bin100, bin200, bin500, bin1000
        self.iterateN_Times = 500

        self.baseFolder = "D:\\BACKUPMyWorks\\ExpDataUDI\\ExperimentFolder"
        self.datasetName = "Gowalla"  # Gowalla, Brightkite, Flickr, Yelp
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
        # self.userLocationDictUserList = ["10"]

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
        # original ExactNur starts here.
        start = time.time()
        maxRssMemory = 0
        totalRssMemory = 0
        print("total users to process in newUserList: ", len(self.newUserList))
        itr = 0
        for userId in self.newUserList:
            itr = itr + 1
            if (itr > self.iterateN_Times):
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
            self.S_I = []
            self.S_Rel = self.sortDesc(self.loc_relScore_dict)
            self.S_R = list(self.S_Rel)  # Put as backup S_Rel arranged by relevance score
            if self.flagRandomSort:
                random.shuffle(self.S_Rel)

            self.Q = []  # initialize
            self.l = tuple
            self.S = []
            self.ResultListStr = ""
            self.ResultList = []

            # S_R = list(self.S_R) #making a different list S_R
            outerloop = 0
            self.Q.append((list(self.S_I), list(self.S_R), 0))
            iterNo = 0
            while len(self.Q) > 0:
                # print("Length Q: ", len(self.Q))
                firstElement = self.Q.pop(0)
                S_I = firstElement[0]
                S_R = firstElement[1]
                # print("S_I len:", len(S_I), "\t SR len:", len(S_R))
                if len(S_I) == self.k:
                    continue
                while len(S_I) < self.k <= len(S_I) + len(S_R):
                    if len(S_R) > 0:
                        l = S_R.pop(0)
                        scoreSI_beforeAppend = self.calcTotalScoreofSet(S_I)
                        self.Q.append((list(S_I), list(S_R), scoreSI_beforeAppend))  # append in Q before the S_I gets update
                        S_I.append(l)
                        if self.FlagFS is False:
                            S_R = self.pruneE(S_I, S_R) # Lemma 4
                        else:
                            afterPruneFilteredLocs = self.afterPrunedTList(S_I, S_R, self.bestScore)  # collected the pruned locations based on best score pruneT
                            if len(afterPruneFilteredLocs) == 0:  # terminate using Prop 2
                                break
                            else:
                                S_R = list(afterPruneFilteredLocs)  # Prune using Property 1 pruneT
                        self.Q.append((list(S_I), list(S_R), self.calcTotalScoreofSet(S_I)))  # append in Q before the S_I gets update
                        if len(S_I) == self.k:
                            scoreSI = self.calcTotalScoreofSet(S_I)
                            if scoreSI > self.bestScore:
                                self.FlagFS = True
                                self.bestScore = scoreSI
                                self.S = list(S_I)
                            break

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

    def pruneE(self, S_I, S_R):
        #print("pruneE")
        lowerD_hat = self.calcLowerBoundD_Hat(S_I, S_R)
        D_Hat_Dict = self.calcDel_d_dblDash(S_I, S_R)
        FilteredPruneE = {}
        for l in D_Hat_Dict.keys():
            if D_Hat_Dict[l] > lowerD_hat:
                FilteredPruneE[l] = D_Hat_Dict[l]
            #else:
            #   print("location ", l, " pruneE not considered")
        S_R_pruned_filteredE = self.sortDesc(FilteredPruneE)

        return S_R_pruned_filteredE

    def afterPrunedTList(self, S_I, S_R, bestScore):
        #print("pruneT and Terminate check")
        S_R_copy = list(S_R)
        S_I_copy = list(S_I)
        lower_d_hat = self.calcLowerBound_d_hat(S_I, S_R, bestScore)
        FilteredPruneT = {}
        for loc in S_R_copy:
            # set_S_I = [(-37.73, 145.06), (-37.56, 145.92), (-37.18, 145.38), (-37.33, 145.29)]
            # divOfOneLocToSetSI = min([self.DgsDictAll[(loc, l)] for l in S_I_copy]) # *************************************************
            divOfOneLocToSetSI = round(min([self.dictOfDgsFromFileAndFlyNew(loc, l) for l in S_I_copy]), 2)

            if divOfOneLocToSetSI > lower_d_hat:
                FilteredPruneT[loc] = divOfOneLocToSetSI
            #else:
                #print("location ", loc, " pruneT not considered")

        S_R_pruned_filteredT = self.sortDesc(FilteredPruneT)
        return S_R_pruned_filteredT

    def calcDel_d_dblDash(self, S_I_copy, S_R_copy):
        logging.info("Calculating del''_d of each location of S_R w.r.t. current S_I. ")
        # set_S_I = set(self.returnKeysOfArrangedDict(S_I))
        '''
        S_I = [(-37.73, 145.06), (-37.56, 145.92), (-37.18, 145.38), (-37.33, 145.29)]
        S_R = [x for x in S_R if x not in S_I]
        print("length SR: ", len(S_R))
        '''
        D_Hat_Dict = {}

        for loc in S_R_copy:
            if len(S_I_copy) > 1:
                S_I_copy_temp = list(S_I_copy)
                S_I_copy_temp.append(loc)
                D_Hat_Dict[loc] = round(self.calcDgsOfSet(S_I_copy_temp) - min([self.dictOfDgsFromFileAndFlyNew(loc, l) for l in S_I_copy]), 2)
            else:
                S_I_copy_temp = list(S_I_copy)
                S_I_copy_temp.append(loc)
                # del_dbl_Dash_Dict[loc] = self.dictOfDgsFromFileAndFlyNew(S_I[0], loc)
                D_Hat_Dict[loc] = round(self.calcDgsOfSet(S_I_copy_temp) - self.dictOfDgsFromFileAndFlyNew(S_I_copy[0], loc), 2)

        return D_Hat_Dict

    def calcLowerBoundD_Hat(self, S_I, S_R):
        S_R_copy = list(S_R)
        D_ss_SI = self.calcDgsOfSet(S_I)
        d_hat_max = self.calcDgsMax(S_R, S_I)
        delS_max_relScore = max([self.loc_relScore_dict[x] for x in S_R_copy])  # or can use: maxRelScoreRemaining = max(map(operator.itemgetter(1), S_R))
        lowerBoundD_Hat = D_ss_SI - d_hat_max - (self.omega / (1 - self.omega)) * delS_max_relScore
        return round(lowerBoundD_Hat, 2)

    def calcLowerBound_d_hat(self, S_I, S_R, bestScore):
        if len(S_I) == self.k:
            return -1
        S_R_copy = list(S_R)
        S_I_copy = list(S_I)
        F_SI = self.calcTotalScoreofSet(S_I_copy)
        topK_num = self.k - len(S_I)
        top_k_Minus_SI_Rel_SR = self.topRelScoreSum(S_R_copy, topK_num)
        lowerBound_d_hat = (bestScore - F_SI - self.omega * top_k_Minus_SI_Rel_SR) / ((1 - self.omega) * topK_num)
        return round(lowerBound_d_hat, 2)

    def calcLowerLowerBoundD_Hat(self, S_I, S_R, bestScore):
        S_R_copy = list(S_R)
        S_I_copy = list(S_I)
        Rss_SI = self.totalRelScoreSet(S_I)
        top_k_Minus_SI_Rel_SR = self.topRelScoreSum(S_R, self.k - len(S_I))
        divWithSI = []
        for loc in S_R_copy:
            # set_S_I = [(-37.73, 145.06), (-37.56, 145.92), (-37.18, 145.38), (-37.33, 145.29)]
            # divOfOneLocToSetSI = min([self.DgsDictAll[(loc, l)] for l in S_I_copy]) # *************************************************
            divOfOneLocToSetSI = min([self.dictOfDgsFromFileAndFlyNew(loc, l) for l in S_I_copy])
            # print(max(temp), type(max(temp)))
            divWithSI.append(divOfOneLocToSetSI)
        top_k_Minus_SI_Div_SR = sum(heapq.nlargest(self.k - len(S_I), divWithSI))
        lowerLowerBoundD_Hat = (bestScore - self.omega * (Rss_SI + top_k_Minus_SI_Rel_SR)) / (1 - self.omega) - top_k_Minus_SI_Div_SR

        return round(lowerLowerBoundD_Hat, 2)

    def totalRelScoreSet(self, S_I):
        return sum([self.loc_relScore_dict[x] for x in S_I])

    def topRelScoreSum(self, S_R, k):
        S_R_Rel = [self.loc_relScore_dict[x] for x in S_R]
        return sum(heapq.nlargest(k, S_R_Rel))

    def earlyTerminationNew(self, bestScore, S_I, S_R, k):
        statFlag = False
        scoreSI = self.calcTotalScoreofSet(S_I)
        relSR_temp = []
        divSR_temp = []
        for loc in S_R:
            relSR_temp.append(self.loc_relScore_dict[loc])
            dgsTemp = []
            for loc2 in S_I:
                dgsTemp.append(self.dictOfDgsFromFileAndFlyNew(loc, loc2))
            divSR_temp.append(min(dgsTemp))
        topRelScoresAdd = sum(heapq.nlargest(k - len(S_I), relSR_temp))
        topDivWithSIAdd = sum(heapq.nlargest(k - len(S_I), divSR_temp))

        # F_max = k * (self.omega * relScore + (1 - self.omega) * DgsM)
        F_max = scoreSI + self.omega * topRelScoresAdd + (1 - self.omega) * topDivWithSIAdd
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
            # if dtempMax > maxDist:
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
                scoreSPTemp = 1 - (totalDist / (self.d_m_dict[loc] * userDegree))
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
                score = round((self.alpha * S_sc[loc] + (1 - self.alpha) * S_sp[loc]), 2)
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
            locationNgbrCheckinText = locationNgbrCheckinText + str(loc) + "\t" + str(tempList) + "\n"
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
                        socDiv = round((1 - common / union), 2)
                    else:
                        socDiv = 1.0
                    spatDiv = round((dist / self.maxD), 2)

                    geoSocDivFinal = round((self.beta * socDiv + (1 - self.beta) * spatDiv), 2)
                    tempPerRow = tempPerRow + "\t" + str(geoSocDivFinal)
            socSpatDivCalcStr = socSpatDivCalcStr + tempPerRow + "\n"
            # socSpatDivCalcStr = socSpatDivCalcStr + str(loc) + "\t" + str(loc2) + "\t" + str(common) + "\t" + str(union) + "\t" + str(socDiv) + "\t" + str(dist) + "\t" + str(self.maxD) + "\t" + str(spatDiv) + "\t" + str(geoSocDivFinal) + "\n"

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
        # sorted_d = dict(sorted(socialScoreDict.items(), key=operator.itemgetter(1), reverse=True))
        sorted_d = Util.sortDictByValueWithKey(dictInput)  # return (-37.73, 145.06): 0.99, (-37.19, 145.28): 0.98, (-37.56, 145.92): 0.97 in descending order
        arrangedKeysOnly = [x[0] for x in sorted_d]
        return arrangedKeysOnly  # return [(-37.73, 145.06), (-37.19, 145.28), (-37.56, 145.92)] as list
        # return sorted_d #return (-37.73, 145.06): 0.99, (-37.19, 145.28): 0.98, (-37.56, 145.92): 0.97 in descending order

    def earlyTermination(self, bestScore, relScore, DgsM, k):
        statFlag = False
        F_max = k * (self.omega * relScore + (1 - self.omega) * DgsM)
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
        # minDgs = min([self.DgsDictAll[(loc, l)] for l in S]) #*********************************************
        # minDgs = min([self.dictOfDgsFromFileAndFly(self.content, self.locAndIndex, loc, l) for l in S]) #*********************************************
        minDgs = min([self.dictOfDgsFromFileAndFlyNew(loc, l) for l in S])  # *********************************************
        return minDgs

    def calcRelLowerBound(self, topRelScore, D_max, topRelLoc, S_I):
        S_I_dash = list(S_I)
        S_I_dash.append(topRelLoc)
        Dgs_SI_dash = self.calcDgsOfSet(S_I_dash)
        Dgs_SI = self.calcDgsOfSet(S_I)
        # print("Dgs_SI_dash: ", Dgs_SI_dash, ", Dgs_SI", Dgs_SI)
        Sgs_lower = topRelScore + ((1 - self.omega) / self.omega) * (Dgs_SI_dash - Dgs_SI - D_max)
        # print("Sgs_lower: ", Sgs_lower)
        return round(Sgs_lower, 2)

    def calcDgsOfSet(self, S):
        totalDgs = 0
        # S = [(-37.73, 145.06), (-37.56, 145.92), (-37.18, 145.38), (-37.33, 145.29)]
        if len(S) <= 1:
            return 0
        for loc in S:
            S_setminus = set(S)
            S_setminus.remove(loc)
            # if (loc, l) in self.DgsDictAll.keys:
            # minDgs = min([self.DgsDictAll[(loc, l)] for l in S_setminus]) #*********************************************
            # minDgs = min([self.dictOfDgsFromFileAndFly(self.content, self.locAndIndex, loc, l) for l in S_setminus]) #*********************************************
            minDgs = min([self.dictOfDgsFromFileAndFlyNew(loc, l) for l in S_setminus])  # *********************************************
            totalDgs += minDgs
        return totalDgs

    def potentialLocs(self, S_R_copy, lowerRelBoundSgs_copy):
        potentialLocDict = {}
        for loc in S_R_copy:
            if self.loc_relScore_dict[loc] > lowerRelBoundSgs_copy:
                potentialLocDict[loc] = self.loc_relScore_dict[loc]
        # arrange w.r.t. rel score
        arrangedPotLoc = self.sortDesc(potentialLocDict)
        # print("potentialLocDict", potentialLocDict, "arrangedPotLoc: ", arrangedPotLoc)
        return arrangedPotLoc

    def calcTotalScoreofSet(self, S):
        if len(S) == 0:
            return 0
        if len(S) == 1:
            for loc in S:
                return self.loc_relScore_dict[loc]
        if self.flagMinMax == "MaxMin":
            totalSgs = 0
            minDgsTemp = []
            for loc in S:
                totalSgs += self.loc_relScore_dict[loc]
                S_setminus = set(S)
                S_setminus.remove(loc)
                for loc2 in S_setminus:
                    # minDgsTemp.append(self.DgsDictAll[loc, loc2]) #*********************************************
                    # minDgsTemp.append(self.dictOfDgsFromFileAndFly(self.content, self.locAndIndex, loc, loc2)) #*********************************************
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
                    # totalDgs += self.dictOfDgsFromFileAndFly(self.content, self.locAndIndex, loc, loc2)
                    totalDgs += self.dictOfDgsFromFileAndFlyNew(loc, loc2)
            totalscore = self.omega * totalSgs + (1 - self.omega) * totalDgs
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
                    # totalDgs += self.DgsDictAll[loc, loc2] #*********************************************
                    # minDgsTemp.append(self.dictOfDgsFromFileAndFly(self.content, self.locAndIndex, loc, loc2)) #*********************************************
                    minDgsTemp.append(self.dictOfDgsFromFileAndFlyNew(loc, loc2))  # *********************************************
                totalDgs += min(minDgsTemp)
            totalscore = self.omega * totalSgs + (1 - self.omega) * totalDgs
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
            # minDgs = min([self.DgsDictAll[(loc, l)] for l in S_setminus]) # *************************************************
            # minDgs = min([self.dictOfDgsFromFileAndFly(self.content, self.locAndIndex, loc, l) for l in S_setminus]) # *************************************************
            minDgs = min([self.dictOfDgsFromFileAndFlyNew(loc, l) for l in S_setminus])  # *************************************************
            locTemp = ""
            for lc in S_setminus:
                # if (self.dictOfDgsFromFileAndFly(self.content, self.locAndIndex, loc, lc) == minDgs): #********************************************
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


objec = ApproxV3()
