import operator
#from scipy.spatial.distance import cdist
import NurTestingPycharm.UtilNur as Util
import logging
import time
import os.path
import ast
import re

class ExactNurV1:
    def __init__(self):
        print("Version 1 of ExactNur Exhaustive Algo.")
        self.flagMinMax = "MaxSumMin"  # MaxMin, MaxSum, MaxSumMin score calculation of a set based on min max of diversity
        self.alpha = 0.5
        self.beta = 0.5
        self.omega = 0.5
        self.k = 6  # top k items should be returned
        self.m = 10  # return top m sets
        self.topSet_Score_m = []
        self.binId = "bin1000"  # bin50, bin100, bin200, bin500, bin1000
        self.P = []  # already computed S_I for del_dbl_dash

        self.baseFolder = "I:\\ExpDataUDI\\ExperimentFolder"
        self.datasetName = "Gowalla"
        self.operatingFolder = os.path.join(self.baseFolder, self.datasetName)
        self.outputFolder = os.path.join(self.operatingFolder, "ExpResult2")

        self.userLocationDict = Util.convert_String_Into_Dict2(self, self.operatingFolder, "user_allChkIn_location_dictRound.txt")
        self.socialNetwork = Util.convert_String_Into_Dict2(self, self.operatingFolder, "Gowalla_edges_Dict.txt")

        self.userLocationDictUserList = ["4"]
        #self.userLocationDictUserList = self.convert_String_Into_List(os.path.join(self.outputFolder, "CheckinBins"), self.binId + ".txt")

        for user in self.userLocationDictUserList:
            self.bestScore = 0
            L = self.userLocationDict[user]
            noOfLoc = len(L)
            if user in self.socialNetwork.keys() and len(self.socialNetwork[user]) > 10 and len(set(L)) > self.k:
                ngbrsList = self.socialNetwork[user]
                #self.socialNetwork = {} ##############################################Release memory, but please comment in original execution
                ngbrLocs = []
                for ngbrs in ngbrsList:
                    if ngbrs in self.userLocationDict.keys():
                        ngbrLocs = ngbrLocs + self.userLocationDict[ngbrs]
                self.ngbrLocCombinedUnique = list(set(ngbrLocs))
                print("processing user:", user, ", self.k:", self.k, ", friends:", len(ngbrsList), ", ngbr number of loc:", len(self.ngbrLocCombinedUnique), ", noOfLoc: ", noOfLoc, ", uniQ Loc: ", len(set(L)))

                locIdLocMap = {}
                strLoc = ""
                lId = 0
                self.locNameAndLocId = {}
                for l in L:
                    self.locNameAndLocId[l] = lId
                    l = str(l).replace("(", "").replace(")", "").strip()
                    #strLoc = strLoc + str(lId) + "\t" + str(l) + "\n"
                    locIdLocMap[lId] = l
                    lId += 1
                #self.createFile(os.path.join(self.outputFolder, "Location", str(user) + ".txt"), strLoc)

                self.L = list(set(L))  # converting into set rather than list. set will contain unique elements
                self.socialScoreDict = self.calcSocialScore(self.L, ngbrsList)
                self.d_m_dict = self.calcMaxDist(self.L, self.ngbrLocCombinedUnique)
                #print("d_m: ", self.d_m)
                self.maxD = self.calcMaxD(self.L)
                self.spatialScoreDict = self.calcSpatialScore(self.L, ngbrsList)
                self.S_gs_Dict = self.calcRelevanceScore(self.socialScoreDict, self.spatialScoreDict, user)

                self.socialSpatialDiversity(self.L, ngbrsList, user)
                contents = self.loadDgsContents(os.path.join(self.outputFolder, "Diversity", str(user) + ".txt"))  # loading self.content and creating self.locAndIndex

                # dgs = self.dictOfDgsFromFileAndFly(self.content, self.locAndIndex, loc1_Q, loc2_Q)
                # self.DgsDictAll = self.dictOfDgsFromFile(os.path.join(self.outputFolder, "Diversity", str(user) + ".txt")) #contains D_gs of pair of locaitons

                # Now the original code starts
                start = time.time()

                self.S_I = []
                self.S_Rel = self.sortDesc(self.S_gs_Dict)
                self.S_R = list(self.S_Rel)  # Put as backup S_Rel arranged by relevance score
                self.Q = []  # initialize
                self.l = tuple
                self.S = set
                self.Q.append((list(self.S_I), list(self.S_R), 0))
                iterNo = 0
                while len(self.Q) > 0:
                    print("Length Q: ", len(self.Q))
                    firstElement = self.Q.pop(0)
                    S_I = firstElement[0]
                    S_R = firstElement[1]
                    print("S_I len:", len(S_I), "\t SR len:", len(S_R))
                    if (len(S_I) == self.k):
                        continue
                    while len(S_I) < self.k and len(S_I) + len(S_R) >= self.k:
                        if (len(S_R) > 0):
                            if (len(S_I) == 0):
                                self.l = S_R.pop(0)
                                S_I.append(self.l)
                                print("After pop, length of SR", len(S_R))
                                lowerDel_d_dblDash = self.calcLowerBoundDelD_dblDsh(S_I, S_R)
                                del_d_dblDash = self.calcDel_d_dblDash(S_I, S_R)
                                del_d_dblDash_Filtered = {}
                                for l in del_d_dblDash.keys():
                                    if del_d_dblDash[l] > lowerDel_d_dblDash:
                                        del_d_dblDash_Filtered[l] = del_d_dblDash[l]
                                    else:
                                        print("location ", l, " not considered")
                                S_R = self.sortDesc(del_d_dblDash_Filtered)

                                dict_S_I = {}  # used to arrange S_I in descending order, and then append to self.P
                                for lc in S_I:
                                    dict_S_I[lc] = self.S_gs_Dict[lc]
                                self.P.append(self.sortDesc(dict_S_I))
                            else:
                                # if(S_I not in self.P):
                                lowerDel_d_dblDash = self.calcLowerBoundDelD_dblDsh(S_I, S_R)
                                del_d_dblDash = self.calcDel_d_dblDash(S_I, S_R)
                                del_d_dblDash_Filtered = {}
                                for l in del_d_dblDash.keys():
                                    if del_d_dblDash[l] > lowerDel_d_dblDash:
                                        del_d_dblDash_Filtered[l] = del_d_dblDash[l]
                                    else:
                                        print("location ", l, " not considered")
                                S_R = self.sortDesc(del_d_dblDash_Filtered)

                                dict_S_I = {}  # used to arrange S_I in descending order, and then append to self.P
                                for lc in S_I:
                                    dict_S_I[lc] = self.S_gs_Dict[lc]
                                self.P.append(self.sortDesc(dict_S_I))

                                # Advance Terminate code:
                                if len(S_I) == (self.k - 1) and self.bestScore > 0:  # checking the S_I length is equal to k-1,
                                    lowerDel_d_dblDashTerminate = self.calcAdvTermLowerBound(S_I, S_R)
                                    del_d_dblDash = self.calcDel_d_dblDash(S_I, S_R)

                                    #lowerDel_d_dblDash = self.calcLowerBoundDelD_dblDsh(S_I, S_R)
                                    #del_d_dblDash = self.calcDel_d_dblDash(S_I, S_R)

                                    topVal = round(list(del_d_dblDash.values())[0], 2)
                                    print("topVal", topVal)
                                    if topVal < lowerDel_d_dblDashTerminate:
                                        print("Advanced Terminate...")
                                        break
                                # if(S_I not in self.P) ends

                                print("S_I", S_I, "exists in P")
                                self.l = S_R.pop(0)
                                S_I.append(self.l)

                            print("len P: ", len(self.P))
                            if (len(S_I) == self.k):
                                # set_S_I = set(self.returnKeysOfArrangedDict(S_I))
                                # score = self.calcTotalScoreofSet(set_S_I)
                                score = self.calcTotalScoreofSet(S_I)
                                if score > self.bestScore:
                                    self.bestScore = score
                                    self.S = S_I
                                    print("set output: ", self.S, ", score: ", self.bestScore)

                            if (len(S_I) > 1):
                                tempSI = list(S_I)
                                tempSI.remove(self.l)
                                scoreS_I = self.calcTotalScoreofSet(set(S_I))
                                score_tempSI = self.calcTotalScoreofSet(set(tempSI))
                                indx = 0
                                for tupl in self.Q:
                                    scr = tupl[2]
                                    if scoreS_I > scr:
                                        self.Q.insert(indx, (list(S_I), list(S_R), scoreS_I))
                                        break
                                    indx += 1

                                indx2 = 0
                                for tupl2 in self.Q:
                                    scr2 = tupl2[2]
                                    if score_tempSI > scr2:
                                        self.Q.insert(indx2, (tempSI, list(S_R), score_tempSI))
                                        break
                                    indx2 += 1
                                print("Q third element score at end: ", [ele[2] for ele in self.Q])
                                break  # out of first while
                            else:
                                tempSI = list(S_I)
                                tempSI.remove(self.l)
                                if len(S_I) == 1:
                                    scoreS_I = self.S_gs_Dict[S_I[0]]
                                else:
                                    scoreS_I = 0
                                # score_tempSI = self.calcTotalScoreofSet(set(tempSI))

                                self.Q.append((list(S_I), list(S_R), scoreS_I))
                                self.Q.append((tempSI, list(S_R), 0))
                                print("Q third element score at end1: ", [ele[2] for ele in self.Q])
                                break
                        else:
                            break

                    iterNo += 1
                    print("iteration done: ", iterNo)
                print("Final S: ", self.S, "score: ", self.calcTotalScoreofSet(set(self.S)))

                locText = ""
                for loc in self.S:
                    loc = str(loc).replace("(", "").replace(")", "").strip()
                    locText = locText + loc + "\n"
                self.createFile("E:\\NurProjectPython\\PycharmProjects\\All\\NurLocationSelection\\finalSetExactV1.txt", locText)

                #self.minDiversitySetOfEachLoc(self.S)

                elapsed_time_fl = (time.time() - start)
                print("Elapsed Time: ", elapsed_time_fl)

    def calcAdvTermLowerBound(self, S_I_copy, S_R_copy):
        S_gs_SI = sum([self.S_gs_Dict[loc] for loc in S_I_copy])
        del_s_max = max([self.S_gs_Dict[loc] for loc in S_R_copy])
        listBestDivScoreTemp = []
        for loc in S_R_copy:
            # set_S_I = [(-37.73, 145.06), (-37.56, 145.92), (-37.18, 145.38), (-37.33, 145.29)]
            # divOfOneLocToSetSI = min([self.DgsDictAll[(loc, l)] for l in S_I_copy]) # *************************************************
            divOfOneLocToSetSI = min([self.dictOfDgsFromFileAndFlyNew(loc, l) for l in S_I_copy])
            # print(max(temp), type(max(temp)))
            listBestDivScoreTemp.append(divOfOneLocToSetSI)
        delDash_d_max = max(listBestDivScoreTemp)
        del_dblDsh_dTermLower1 = round((self.bestScore - self.omega*(S_gs_SI + del_s_max))/(1-self.omega), 2) - delDash_d_max
        return round(del_dblDsh_dTermLower1, 2)

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
        del ngbrLocCombinedUnique
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
        del S_gs_Text
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
        f.close()
        return self.content

    def sortDesc(self, dictInput):
        logging.info("Arrange dict w.r.t. descending.")
        #sorted_d = dict(sorted(socialScoreDict.items(), key=operator.itemgetter(1), reverse=True))
        sorted_d = Util.sortDictByValueWithKey(dictInput) #return (-37.73, 145.06): 0.99, (-37.19, 145.28): 0.98, (-37.56, 145.92): 0.97 in descending order
        arrangedKeysOnly = [x[0] for x in sorted_d]
        return arrangedKeysOnly #Return list of locations  only

    def calcLowerBoundDelD_dblDsh(self, S_I_copy, S_R_copy):
        logging.info("Calculating lower bound based on S_I and S_R")
        D_gsS_I = self.caldDgsOfSet(S_I_copy)
        delS_max_relScore = max([self.S_gs_Dict[x] for x in S_R_copy]) #or can use: maxRelScoreRemaining = max(map(operator.itemgetter(1), S_R))
        listBestDivScoreTemp = []
        for loc in S_R_copy:
            #set_S_I = [(-37.73, 145.06), (-37.56, 145.92), (-37.18, 145.38), (-37.33, 145.29)]
            #divOfOneLocToSetSI = min([self.DgsDictAll[(loc, l)] for l in S_I_copy]) # *************************************************
            divOfOneLocToSetSI = min([self.dictOfDgsFromFileAndFlyNew(loc, l) for l in S_I_copy])
            #print(max(temp), type(max(temp)))
            listBestDivScoreTemp.append(divOfOneLocToSetSI)
        delDash_d_max = max(listBestDivScoreTemp)

        lowerBound = D_gsS_I - delDash_d_max - (self.omega/(1-self.omega))*delS_max_relScore
        lowerBound = round(lowerBound, 2)
        print("lowerBound:", lowerBound)
        return lowerBound

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

    def caldDgsOfSet(self, SetNew):
        #S = [(-37.73, 145.06), (-37.56, 145.92), (-37.18, 145.38), (-37.33, 145.29)]
        if len(SetNew) <= 1:
            return 0

        if self.flagMinMax == "MaxMin":
            minOfMin = []
            for loc in SetNew:
                S_setminus = set(SetNew)
                S_setminus.remove(loc)
                minDgs = min([self.dictOfDgsFromFileAndFlyNew(loc, l) for l in S_setminus])
                minOfMin.append(minDgs)
            return min(minOfMin)

        if self.flagMinMax == "MaxSum":
            totalDgs = 0
            for loc in SetNew:
                S_setminus = set(SetNew)
                S_setminus.remove(loc)
                minDgs = sum([self.dictOfDgsFromFileAndFlyNew(loc, l) for l in S_setminus])
                totalDgs += minDgs
            return totalDgs

        if self.flagMinMax == "MaxSumMin":
            totalDgs = 0
            for loc in SetNew:
                S_setminus = set(SetNew)
                S_setminus.remove(loc)
                minDgs = min([self.dictOfDgsFromFileAndFlyNew(loc, l) for l in S_setminus])
                totalDgs += minDgs
            return totalDgs

    def calcDel_d_dblDash(self, S_I_copy, S_R_copy):
        logging.info("Calculating del''_d of each location of S_R w.r.t. current S_I. ")
        #set_S_I = set(self.returnKeysOfArrangedDict(S_I))
        '''
        S_I = [(-37.73, 145.06), (-37.56, 145.92), (-37.18, 145.38), (-37.33, 145.29)]
        S_R = [x for x in S_R if x not in S_I]
        print("length SR: ", len(S_R))
        '''
        #set_S_R = set(self.returnKeysOfArrangedDict(S_R))
        minList = [] #contains minimum of each location fo S_R w.r.t. S_I, then we will add them
        del_d_dbl_Dash_Dict = {}

        for loc in S_R_copy:
            if len(S_I_copy) > 1:
                '''
                tempSum = 0
                for loc2 in S_I:
                    S_setminus = list(S_I)
                    S_setminus.remove(loc2)
                    #minDgs = min([self.DgsDictAll[(loc2, l)] for l in S_setminus]) # *************************************************
                    minDgs = min([self.dictOfDgsFromFileAndFlyNew(loc2, l) for l in S_setminus])  # *************************************************
                    #dgs_lDash_l = self.DgsDictAll[loc2, loc] # *************************************************
                    dgs_lDash_l = self.dictOfDgsFromFileAndFlyNew(loc2, loc)  # *************************************************
                    minimumAmongTwo = min(minDgs, dgs_lDash_l)
                    tempSum += minimumAmongTwo
                del_d_dbl_Dash_Dict[loc] = round(tempSum, 2)
                '''
                S_I_copy_temp = list(S_I_copy)
                S_I_copy_temp.append(loc)
                del_d_dbl_Dash_Dict[loc] = self.calcTotalDgsOfSet(S_I_copy_temp) - min([self.dictOfDgsFromFileAndFlyNew(loc, l) for l in S_I_copy])
            else:
                S_I_copy_temp = list(S_I_copy)
                S_I_copy_temp.append(loc)
                #del_dbl_Dash_Dict[loc] = self.dictOfDgsFromFileAndFlyNew(S_I[0], loc)
                del_d_dbl_Dash_Dict[loc] = self.calcTotalDgsOfSet(S_I_copy_temp) - self.dictOfDgsFromFileAndFlyNew(S_I_copy[0], loc)

        return del_d_dbl_Dash_Dict

    def calcTotalDgsOfSet (self, S):
        if self.flagMinMax == "MaxMin":
            minDgsTemp = []
            for loc in S:
                S_setminus = set(S)
                S_setminus.remove(loc)
                for loc2 in S_setminus:
                    # minDgsTemp.append(self.DgsDictAll[loc, loc2]) #*********************************************
                    # minDgsTemp.append(self.dictOfDgsFromFileAndFly(self.content, self.locAndIndex, loc, loc2)) #*********************************************
                    minDgsTemp.append(self.dictOfDgsFromFileAndFlyNew(loc, loc2))  # *********************************************
            minDgsSet = min(minDgsTemp)
            return round(minDgsSet, 2)

        if self.flagMinMax == "MaxSum":
            totalDgs = 0
            for loc in S:
                S_setminus = set(S)
                S_setminus.remove(loc)
                for loc2 in S_setminus:
                    # totalDgs += self.dictOfDgsFromFileAndFly(self.content, self.locAndIndex, loc, loc2)
                    totalDgs += self.dictOfDgsFromFileAndFlyNew(loc, loc2)
            return round(totalDgs, 2)

        if self.flagMinMax == "MaxSumMin":
            totalDgs = 0
            for loc in S:
                minDgsTemp = []
                S_setminus = set(S)
                S_setminus.remove(loc)
                for loc2 in S_setminus:
                    # totalDgs += self.DgsDictAll[loc, loc2] #*********************************************
                    # minDgsTemp.append(self.dictOfDgsFromFileAndFly(self.content, self.locAndIndex, loc, loc2)) #*********************************************
                    minDgsTemp.append(self.dictOfDgsFromFileAndFlyNew(loc, loc2))  # *********************************************
                totalDgs += min(minDgsTemp)
            return round(totalDgs, 2)

    def calcTotalScoreofSet(self, S):
        if len(S) == 1:
            return self.S_gs_Dict[list(S)[0]]
        if len(S) == 0:
            return 0

        if self.flagMinMax == "MaxMin":
            totalSgs = 0
            minDgsTemp = []
            for loc in S:
                totalSgs += self.S_gs_Dict[loc]
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
                totalSgs += self.S_gs_Dict[loc]
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
                totalSgs += self.S_gs_Dict[loc]
                S_setminus = set(S)
                S_setminus.remove(loc)
                for loc2 in S_setminus:
                    # totalDgs += self.DgsDictAll[loc, loc2] #*********************************************
                    # minDgsTemp.append(self.dictOfDgsFromFileAndFly(self.content, self.locAndIndex, loc, loc2)) #*********************************************
                    minDgsTemp.append(self.dictOfDgsFromFileAndFlyNew(loc, loc2))  # *********************************************
                totalDgs += min(minDgsTemp)
            totalscore = self.omega * totalSgs + (1 - self.omega) * totalDgs
            return round(totalscore, 2)

    def dictOfDgsFromFileAndFlyNew(self, loc1_Q, loc2_Q):
        if loc1_Q in self.locAndIndex and loc2_Q in self.locAndIndex:
            loc1_Index = self.locAndIndex.index(loc1_Q)
            loc2_Index = self.locAndIndex.index(loc2_Q)
            if len(self.content) >= loc1_Index:
                splitArray = self.content[loc1_Index].split("\t")
                if len(splitArray) > 1:
                    tempValDgs = splitArray[loc2_Index + 1]

                    return float(tempValDgs)
        else:
            print("locations are not available in self.locAndIndex list")
            return 0

    def createFile(self, fileNameFullPath, contents):
        try:
            fw_fileName = open(fileNameFullPath, "w", encoding="utf8")
            fw_fileName.write(contents.__str__())
            fw_fileName.close()
        except KeyError:
            print("Error while creating file.. ", KeyError)
            pass
obj = ExactNurV1()