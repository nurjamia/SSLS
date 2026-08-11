import os.path
#from builtins import print

import NurTestingPycharm.UtilNur as Util
import time
import random
import re
import ast
import glob
import psutil
import heapq
from pathlib import Path


class GMC:
    def __init__(self):
        print("Greedy Marginal Contribution. ICDE 2011")
        self.flagMinMax = "MaxSum"  # MaxSum is default according to the orizinal paper. However, we use MaxSumMin in our proposed approach. MaxMin, MaxSum, MaxSumMin score calculation of a set based on min max of diversity
        flagRemoveExistingFiles = False # will remove the .txt already exists in the folders 'Diversity, RelScore, Location, LocChknNgbr'
        self.alpha = 0.5
        self.beta = 0.5
        self.omega = 0.5 # Here lamda and omega carry same meaning
        self.k = 100  # top k items should be returned 2, 4, 6, 8, 10    20, 40, 60, 80, 100
        self.m = 10  # return top m sets
        self.topSet_Score_m = []
        self.binId = "bin500"  # bin50, bin100, bin200, bin500, bin1000
        self.iterateN_Times = 1000

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
            self.socialNetwork = Util.convert_String_Into_Dict2(self, self.operatingFolder, self.datasetName+"_edges_Dict.txt")

        #self.userLocationDictUserList = ["4"]
        self.userLocationDictUserList = self.convert_String_Into_List(os.path.join(self.outputFolder, "CheckinBins"), self.binId+".txt")
        print("size of users in this bin: ", len(self.userLocationDictUserList))
        #self.userLocationDictUserList = ["10"]

        # Delete existing .txt files from the Folders Diversity, RelScore, Location, LocChknNgbr folders under self.outputFolder Path
        if flagRemoveExistingFiles:
            self.deleteFilesInFolder(os.path.join(self.outputFolder, "Location", self.binId))
            self.deleteFilesInFolder(os.path.join(self.outputFolder, "Diversity", self.binId))
            self.deleteFilesInFolder(os.path.join(self.outputFolder, "RelScore", self.binId))
            self.deleteFilesInFolder(os.path.join(self.outputFolder, "LocChknNgbr", self.binId))

        self.newUserList = []

        for user in self.userLocationDictUserList:
            # print("Going to calculate socio-spatial relevance and diversity and save them to files in RelScore and Diversity folders")
            L = self.userLocationDict[user]
            noOfLoc = len(L)
            if user in self.socialNetwork.keys() and len(self.socialNetwork[user]) > 5 and len(set(L)) > self.k:
                #print("len: self.socialNetwork[user]): ", len(self.socialNetwork[user]), "len(set(L)): ", len(set(L)))
                self.newUserList.append(user)  # Will process only these users further as they have satisfied minimum requirements
        '''
        for user in self.userLocationDictUserList:
            #print("Going to calculate socio-spatial relevance and diversity and save them to files in RelScore and Diversity folders")
            L = self.userLocationDict[user]
            noOfLoc = len(L)            
            if user in self.socialNetwork.keys() and len(self.socialNetwork[user]) > 5 and len(set(L)) > self.k:
                print("len: self.socialNetwork[user]): ", len(self.socialNetwork[user]), "len(set(L)): ",len(set(L)))
                self.newUserList.append(user) #Will process only these users further as they have satisfied minimum requirements
                ngbrsList = self.socialNetwork[user]
                # self.socialNetwork = {} ##############################################Release memory, but please comment in original execution
                ngbrLocs = []
                for ngbrs in ngbrsList:
                    if ngbrs in self.userLocationDict.keys():
                        ngbrLocs = ngbrLocs + self.userLocationDict[ngbrs]
                self.ngbrLocCombinedUnique = list(set(ngbrLocs))
                print("processing user:", user, ", self.k:", self.k, ", friends:", len(ngbrsList), ", ngbr number of loc:", len(self.ngbrLocCombinedUnique), ", noOfLoc: ", noOfLoc, ", uniQ Loc: ", len(set(L)))
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

                self.socialSpatialDiversity(self.L, ngbrsList, user) #create the diversity files in Diversity folder.
                #contents = self.loadDgsContents(os.path.join(self.outputFolder, "Diversity", self.binId, str(user) + ".txt"))
        '''
        #original GMC starts here.
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
            self.Loc_user_array = []
            self.Rel_Score_Array = []
            self.loc_relScore_dict = {}
            for i in range(len(content)):
                splitArray = content[i].split("\t")
                if len(splitArray) > 1:
                    loc = eval(splitArray[1].strip())
                    self.Loc_user_array.append(loc)
                    relScore = splitArray[4].strip()
                    self.Rel_Score_Array.append(relScore)
                    self.loc_relScore_dict[loc] = relScore
            f.close()

            if os.path.exists(os.path.join(self.outputFolder, "Diversity", self.binId, str(userId) + ".txt")) == False:
                continue
            f_div = open(os.path.join(self.outputFolder, "Diversity", self.binId, str(userId) + ".txt"), "r")
            content_div = f_div.readlines()
            content_div = [x.strip() for x in content_div]

            startEachLoop = time.time()
            R = []
            S = list(self.Loc_user_array)
            for p in range(1, self.k+1):
                mmc_Loc_Dict = self.calc_mmc(userId, content_div, R, S, p)
                s_i_max = max(mmc_Loc_Dict,key = mmc_Loc_Dict.get) #argmax from mmc_Loc_Dict
                R.append(s_i_max)
                S.remove(s_i_max)
            #print("The final R: ", R, " for userId: ", userId)
            #print("user id: ", userId, "Result R: ", R)

            # memory consumed max and average in bytes
            process = psutil.Process(os.getpid())
            rssMemoryTemp = float(process.memory_info().rss)
            totalRssMemory = totalRssMemory + rssMemoryTemp
            if rssMemoryTemp > maxRssMemory:
                maxRssMemory = rssMemoryTemp
            endEachLoop = time.time()
            print("Each loop time diff:", round(endEachLoop - startEachLoop, 2), "memory: ", round(maxRssMemory / (1024 * 1024), 2))

        endTime = time.time()
        print("Max Memory consumed: ", round(maxRssMemory / (1024 * 1024), 2), "MB, and Average memory: ", round(totalRssMemory / (1024 * 1024 * len(self.newUserList)), 2), "MB")
        print("Start Time: ", start, ", end time: ", endTime, "Difference: ", endTime-start, "Filtered Size: ", len(self.newUserList), "Original Size in Bin:", len(self.userLocationDictUserList))

    def calc_mmc(self, userId, content_div, R, S, p):
        #print("calculate mmc of each location of a user 'user'. Each time, it access the relevance (RelScore folder) and diversity text file to load location information of a user.")
        mmc_dict = {}

        for s_i in S:
            rel_s_i = float(self.loc_relScore_dict[s_i])

            indexPos_si = -99
            try:
                indexPos_si = self.Loc_user_array.index(s_i)
            except:
                print("value s_i not available in List")
                continue
            diversity_all_si_list = content_div[indexPos_si].split("\t")

            del_div_val = []
            for s_j_R in R:
                s_j_R_index = -99
                try:
                    s_j_R_index = self.Loc_user_array.index(s_j_R)
                except:
                    print("value s_j_R_index not available in List")
                    continue
                del_div_val.append(float(diversity_all_si_list[s_j_R_index + 1]))

            del_l_div_all_val = []
            tempS = list(S)
            for s_j in tempS:
                if s_j == s_i:
                    continue
                s_j_tempS_index = -99
                try:
                    s_j_tempS_index = self.Loc_user_array.index(s_j)
                except:
                    print("value s_j_tempS_index not available in List")
                    continue
                del_l_div_all_val.append(float(diversity_all_si_list[s_j_tempS_index + 1]))

            mmc_score = round(self.omega*rel_s_i + ((1-self.omega)/(self.k - 1)) * (sum(del_div_val) + sum(heapq.nlargest(self.k - p, del_l_div_all_val))), 2)
            #print(heapq.nlargest(self.k - p, del_l_div_all_val))
            #print(sum(del_div_val))
            mmc_dict[s_i] = mmc_score
        return mmc_dict

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
        #logging.info("Going to calculate max Dist between location checked-in by user and location checked-in by neighbors using Haversine.")
        maxDist = 0
        maxDistEachLocAllNgbrs = {}
        for loc in L:
            dtempMax = max([Util.haversineDist(loc, lc) for lc in ngbrLocCombinedUnique])
            maxDistEachLocAllNgbrs[loc] = round(dtempMax, 2)
            #if dtempMax > maxDist:
            #    maxDist = dtempMax
        return maxDistEachLocAllNgbrs

    def calcMaxD(self, L):
        #logging.info("Calculating the maxD maximum distance of checkin locaitons of particular user u.")
        maxD = 0
        for loc1 in L:
            maxTemp = max([Util.haversineDist(loc1, lc) for lc in L])
            if maxTemp > maxD:
                maxD = maxTemp
        return round(maxD, 2)

    def calcSpatialScore(self, L, socialNetworkNgbrList):
        #logging.info("Going to calculate spatial score of each location w.r.t. user u")
        userDegree = len(socialNetworkNgbrList)
        spatialScore = {}
        for loc in L:
            totalDist = 0
            for ngbr in socialNetworkNgbrList:
                if ngbr in self.userLocationDict.keys():
                    locListNgbr = self.userLocationDict[ngbr]
                    minDistTemp = min([Util.haversineDist(loc, l) for l in locListNgbr])
                    totalDist += minDistTemp
            if self.d_m_dict[loc] > 0:
                scoreSPTemp = 1 - (totalDist/(self.d_m_dict[loc] * userDegree))
            else:
                scoreSPTemp = 1
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
        self.createFile(os.path.join(self.outputFolder, "RelScore", self.binId, str(userId) + "_Rel.txt"), S_gs_Text)
        return S_gs

    def socialSpatialDiversity(self, L, socialNetworkNgbrList, userId):
        #logging.info("Spatial diversity and social diversity calculation")
        locationNgbrCheckinDict = {}
        locationNgbrCheckinText = ""

        for loc in L:
            tempList = []
            for ngbr in socialNetworkNgbrList:
                if ngbr in self.userLocationDict.keys() and loc in self.userLocationDict[ngbr]:
                    tempList.append(ngbr)
            locationNgbrCheckinDict[loc] = tempList
            locationNgbrCheckinText = locationNgbrCheckinText + str(loc)+ "\t" + str(tempList)+ "\n"
        self.createFile(os.path.join(self.outputFolder, "LocChknNgbr", self.binId, str(userId) + ".txt"), locationNgbrCheckinText)

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

        #logging.info("Going to create socia spatial diversity file. Header is: loc1, loc2, common user count, union count, social div, dist in KM, maxD, spatial diversity, geo-Social Diversity")
        self.createFile(os.path.join(self.outputFolder, "Diversity", self.binId, str(userId) + ".txt"), socSpatDivCalcStr)

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


obj = GMC()