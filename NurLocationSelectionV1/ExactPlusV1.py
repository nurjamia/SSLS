import os.path
import operator
from scipy.spatial.distance import cdist
import NurTestingPycharm.UtilNur as Util
import logging
import time

class ExactPlus:
    def __init__(self):
        print("Deploying Exact+ Algorithm")
        self.flagMinMax = "MaxSumMin"  # MaxMin, MaxSum, MaxSumMin score calculation of a set based on min max of diversity
        self.bestScore = 0
        self.alpha = 0.5
        self.beta = 0.5
        self.omega = 0.5
        self.k = 10 #top k items should be returned

        self.baseFolder = "I:\\ExpDataUDI\\ExperimentFolder"
        self.datasetName = "Gowalla"
        self.operatingFolder = os.path.join(self.baseFolder, self.datasetName)
        self.outputFolder = os.path.join(self.operatingFolder, "ExpResult2")

        #self.DgsFetchOnTheFly(os.path.join(self.outputFolder, "Diversity", "1.txt"), (46.13, 6.52), (48.42, 3.02))
        #L = [(-37.02,145.33), (-37.45,145.64), (-37.69,145.7), (-37.14,145.1), (-37.44,145.34), (-37.43,145.67), (-37,145.31), (-37.62,145.89), (-37.93,145.66), (-37.87,145.22), (-37.72,145.96), (-37.54,145.28), (-37.89,145.34), (-37.64,145.92), (-37.4,145), (-37.13,145.42), (-37.81,145.71), (-37.89,145.47), (-37.24,145.01), (-37.97,145.06), (-37.28,145.4), (-37.66,145.31), (-37.75,145.92), (-37.34,145.17), (-37.58,145.16), (-37.07,145.16), (-37.98,145.03), (-37.56,145.19), (-37.25,145.07), (-37.48,145.73), (-37.04,145.15), (-37.06,145.76), (-37.96,145.66), (-37.54,145.34), (-37.35,145.99), (-37.16,145.93), (-37.7,145.18), (-37.51,145.41), (-37.96,145.11), (-37.02,145.95), (-37.12,145.9), (-37.74,145.33), (-37.12,145.27), (-37.33,145.87), (-37.1,145.9), (-37.48,145.5), (-37.97,145.77), (-37.45,145.96), (-37.35,145.47), (-37.74,145.05), (-37.97,145.01), (-37.46,145.6), (-37.31,145.56), (-37.15,145.11), (-37.36,145.46), (-37.66,145.28), (-37.99,145.61), (-37.18,145.77), (-37.16,145.1), (-37.9,145.28), (-37.96,145.49), (-37.1,145.35), (-37.54,145.81), (-37.19,145.28), (-37.56,145.92), (-37.95,145.14), (-37.76,145.39), (-37.03,145.86), (-37.36,145.4), (-37.76,145.91), (-37.93,145.4), (-37.88,145.64), (-37.5,145.64), (-37.44,145.16), (-37.96,145.97), (-37.97,145.82), (-37.83,145.92), (-37.98,145.02), (-37.48,145.58), (-37.84,145.49), (-37.44,145.2), (-37.67,145.86), (-37.96,145.83), (-37.9,145.4), (-37.53,145.54), (-37.18,145.38), (-37.77,145.78), (-37.43,145.04), (-37.23,145.1), (-37.4,145.19), (-37.55,145.49), (-37.16,145.24), (-37.46,145.85), (-37.3,145.48), (-37.33,145.29), (-37.11,145.63), (-37.73,145.06), (-37.88,145.55), (-37.72,145.35), (-37.39,145.76)]
        #L = [(-37.02,145.33), (-37.45,145.64), (-37.69,145.7), (-37.14,145.1), (-37.44,145.34), (-37.43,145.67), (-37,145.31), (-37.62,145.89), (-37.93,145.66), (-37.87,145.22), (-37.72,145.96), (-37.54,145.28), (-37.89,145.34), (-37.64,145.92), (-37.4,145), (-37.13,145.42), (-37.81,145.71), (-37.89,145.47), (-37.24,145.01), (-37.97,145.06)]
        #L = [(-37.02, 145.33), (-37.45, 145.64), (-37.69, 145.7), (-37.14, 145.1), (-37.44, 145.34), (-37.43, 145.67), (-37, 145.31), (-37.62, 145.89), (-37.93, 145.66), (-37.87, 145.22), (-37.72,145.96)]
        #L = [(-37.02, 145.33), (-37.45, 145.64), (-37.69, 145.7), (-37.14, 145.1), (-37.44, 145.34), (-37.43, 145.67), (-37, 145.31), (-37.62, 145.89)]
        '''
        socialNetwork = {'1': [(-37.02,145.33), (-37.45,145.64), (-37.69,145.7), (-37.14,145.1), (-37.44,145.34), (-37.43,145.67), (-37,145.31), (-37.62,145.89), (-37.93,145.66), (-37.87,145.22), (-37.72,145.96), (-37.54,145.28), (-37.89,145.34), (-37.64,145.92), (-37.4,145), (-37.13,145.42), (-37.81,145.71), (-37.89,145.47), (-37.24,145.01), (-37.97,145.06), (-37.28,145.4), (-37.66,145.31), (-37.75,145.92), (-37.34,145.17), (-37.58,145.16), (-37.07,145.16), (-37.98,145.03), (-37.56,145.19), (-37.25,145.07), (-37.48,145.73), (-37.04,145.15), (-37.06,145.76), (-37.96,145.66), (-37.54,145.34), (-37.35,145.99), (-37.16,145.93), (-37.7,145.18), (-37.51,145.41), (-37.96,145.11), (-37.02,145.95), (-37.12,145.9), (-37.74,145.33), (-37.12,145.27), (-37.33,145.87), (-37.1,145.9), (-37.48,145.5), (-37.97,145.77), (-37.45,145.96), (-37.35,145.47), (-37.74,145.05), (-37.82,145.06), (-37.88,145.00), (-37.83,145.10), (-37.88,145.02), (-37.83,144.97), (-37.88,145.01), (-37.78,145.05), (-37.79,144.95), (-37.87,145.01), (-37.78,144.91)],
                         '2': [(-37.64,145.92), (-37.4,145), (-37.13,145.42), (-37.81,145.71), (-37.89,145.47), (-37.24,145.01), (-37.97,145.06), (-37.28,145.4), (-37.66,145.31), (-37.75,145.92), (-37.34,145.17), (-37.58,145.16), (-37.07,145.16), (-37.98,145.03), (-37.56,145.19), (-37.25,145.07), (-37.48,145.73), (-37.04,145.15), (-37.06,145.76), (-37.96,145.66), (-37.54,145.34), (-37.35,145.99), (-37.16,145.93), (-37.7,145.18), (-37.51,145.41), (-37.96,145.11), (-37.02,145.95), (-37.12,145.9), (-37.74,145.33), (-37.12,145.27), (-37.33,145.87), (-37.1,145.9), (-37.48,145.5), (-37.97,145.77), (-37.45,145.96), (-37.35,145.47), (-37.74,145.05), (-37.97,145.01), (-37.46,145.6), (-37.31,145.56), (-37.15,145.11), (-37.36,145.46), (-37.66,145.28), (-37.99,145.61), (-37.18,145.77), (-37.16,145.1), (-37.9,145.28), (-37.96,145.49), (-37.1,145.35), (-37.54,145.81), (-37.75,145.08), (-37.75,144.99), (-37.73,144.97), (-37.82,145.01), (-37.79,145.06), (-37.85,145.08), (-37.85,144.96), (-37.84,145.08), (-37.78,144.96), (-37.89,145.02)],
                         '3': [(-37.43,145.67), (-37,145.31), (-37.62,145.89), (-37.93,145.66), (-37.87,145.22), (-37.72,145.96), (-37.54,145.28), (-37.89,145.34), (-37.64,145.92), (-37.4,145), (-37.13,145.42), (-37.81,145.71), (-37.89,145.47), (-37.24,145.01), (-37.97,145.06), (-37.28,145.4), (-37.66,145.31), (-37.75,145.92), (-37.34,145.17), (-37.58,145.16), (-37.07,145.16), (-37.98,145.03), (-37.56,145.19), (-37.25,145.07), (-37.48,145.73), (-37.04,145.15), (-37.06,145.76), (-37.96,145.66), (-37.54,145.34), (-37.35,145.99), (-37.16,145.93), (-37.7,145.18), (-37.51,145.41), (-37.96,145.11), (-37.02,145.95), (-37.12,145.9), (-37.74,145.33), (-37.12,145.27), (-37.33,145.87), (-37.1,145.9), (-37.48,145.5), (-37.97,145.77), (-37.45,145.96), (-37.35,145.47), (-37.74,145.05), (-37.97,145.01), (-37.46,145.6), (-37.31,145.56), (-37.15,145.11), (-37.36,145.46), (-37.8,144.99), (-37.87,145), (-37.78,144.93), (-37.77,144.9), (-37.82,145.1), (-37.86,145.09), (-37.82,144.91), (-37.82,145.04), (-37.75,145.08), (-37.76,144.94)],
                         '4': [(-37.35,145.99), (-37.16,145.93), (-37.7,145.18), (-37.51,145.41), (-37.96,145.11), (-37.02,145.95), (-37.12,145.9), (-37.74,145.33), (-37.12,145.27), (-37.33,145.87), (-37.1,145.9), (-37.48,145.5), (-37.97,145.77), (-37.45,145.96), (-37.35,145.47), (-37.74,145.05), (-37.97,145.01), (-37.46,145.6), (-37.31,145.56), (-37.15,145.11), (-37.36,145.46), (-37.66,145.28), (-37.99,145.61), (-37.18,145.77), (-37.16,145.1), (-37.9,145.28), (-37.96,145.49), (-37.1,145.35), (-37.54,145.81), (-37.19,145.28), (-37.56,145.92), (-37.95,145.14), (-37.76,145.39), (-37.03,145.86), (-37.36,145.4), (-37.76,145.91), (-37.93,145.4), (-37.88,145.64), (-37.5,145.64), (-37.44,145.16), (-37.96,145.97), (-37.97,145.82), (-37.83,145.92), (-37.98,145.02), (-37.48,145.58), (-37.84,145.49), (-37.44,145.2), (-37.67,145.86), (-37.96,145.83), (-37.9,145.4), (-37.75,145.00), (-37.88,145.00), (-37.75,145.07), (-37.75,145.08), (-37.73,145.02), (-37.78,144.91), (-37.86,145.09), (-37.85,145.01), (-37.77,144.98), (-37.82,145.01)],
                         '5': [(-37.33,145.87), (-37.1,145.9), (-37.48,145.5), (-37.97,145.77), (-37.45,145.96), (-37.35,145.47), (-37.74,145.05), (-37.97,145.01), (-37.46,145.6), (-37.31,145.56), (-37.15,145.11), (-37.36,145.46), (-37.66,145.28), (-37.99,145.61), (-37.18,145.77), (-37.16,145.1), (-37.9,145.28), (-37.96,145.49), (-37.1,145.35), (-37.54,145.81), (-37.19,145.28), (-37.56,145.92), (-37.95,145.14), (-37.76,145.39), (-37.03,145.86), (-37.36,145.4), (-37.76,145.91), (-37.93,145.4), (-37.88,145.64), (-37.5,145.64), (-37.44,145.16), (-37.96,145.97), (-37.97,145.82), (-37.83,145.92), (-37.98,145.02), (-37.48,145.58), (-37.84,145.49), (-37.44,145.2), (-37.67,145.86), (-37.96,145.83), (-37.9,145.4), (-37.53,145.54), (-37.18,145.38), (-37.77,145.78), (-37.43,145.04), (-37.23,145.1), (-37.4,145.19), (-37.55,145.49), (-37.16,145.24), (-37.46,145.85), (-37.8,144.91), (-37.88,145.02), (-37.84,144.95), (-37.73,144.98), (-37.83,144.98), (-37.83,144.92), (-37.85,145.09), (-37.86,144.99), (-37.78,145.03), (-37.76,144.92)],
                         '6': [(-37.81,145.71), (-37.89,145.47), (-37.24,145.01), (-37.97,145.06), (-37.28,145.4), (-37.66,145.31), (-37.75,145.92), (-37.34,145.17), (-37.58,145.16), (-37.07,145.16), (-37.98,145.03), (-37.56,145.19), (-37.25,145.07), (-37.48,145.73), (-37.04,145.15), (-37.06,145.76), (-37.96,145.66), (-37.54,145.34), (-37.35,145.99), (-37.16,145.93), (-37.36,145.4), (-37.76,145.91), (-37.93,145.4), (-37.88,145.64), (-37.5,145.64), (-37.44,145.16), (-37.96,145.97), (-37.97,145.82), (-37.83,145.92), (-37.98,145.02), (-37.48,145.58), (-37.84,145.49), (-37.44,145.2), (-37.67,145.86), (-37.96,145.83), (-37.9,145.4), (-37.53,145.54), (-37.18,145.38), (-37.77,145.78), (-37.43,145.04), (-37.23,145.1), (-37.4,145.19), (-37.55,145.49), (-37.16,145.24), (-37.46,145.85), (-37.3,145.48), (-37.33,145.29), (-37.11,145.63), (-37.73,145.06), (-37.88,145.55), (-37.84,144.92), (-37.89,145.05), (-37.82,145.1), (-37.88,144.93), (-37.74,145), (-37.78,145.03), (-37.8,145.02), (-37.85,144.99), (-37.79,144.99), (-37.82,145)],
                         '7': [(-37.46,145.6), (-37.31,145.56), (-37.15,145.11), (-37.36,145.46), (-37.66,145.28), (-37.99,145.61), (-37.18,145.77), (-37.16,145.1), (-37.9,145.28), (-37.96,145.49), (-37.1,145.35), (-37.54,145.81), (-37.19,145.28), (-37.56,145.92), (-37.95,145.14), (-37.76,145.39), (-37.03,145.86), (-37.36,145.4), (-37.76,145.91), (-37.93,145.4), (-37.83,145.92), (-37.98,145.02), (-37.48,145.58), (-37.84,145.49), (-37.44,145.2), (-37.67,145.86), (-37.96,145.83), (-37.9,145.4), (-37.53,145.54), (-37.18,145.38), (-37.77,145.78), (-37.43,145.04), (-37.23,145.1), (-37.4,145.19), (-37.55,145.49), (-37.16,145.24), (-37.46,145.85), (-37.3,145.48), (-37.33,145.29), (-37.11,145.63), (-37.13,145.42), (-37.81,145.71), (-37.89,145.47), (-37.24,145.01), (-37.97,145.06), (-37.28,145.4), (-37.66,145.31), (-37.75,145.92), (-37.34,145.17), (-37.58,145.16), (-37.75,145.00), (-37.88,145.01), (-37.77,144.91), (-37.87,145.07), (-37.80,144.89), (-37.75,144.99), (-37.87,145.00), (-37.86,144.97), (-37.79,145.01), (-37.80,145.01)],
                         '8': [(-37.72,145.96), (-37.54,145.28), (-37.89,145.34), (-37.64,145.92), (-37.4,145), (-37.13,145.42), (-37.81,145.71), (-37.89,145.47), (-37.24,145.01), (-37.97,145.06), (-37.51,145.41), (-37.96,145.11), (-37.02,145.95), (-37.12,145.9), (-37.74,145.33), (-37.12,145.27), (-37.33,145.87), (-37.1,145.9), (-37.48,145.5), (-37.97,145.77), (-37.45,145.96), (-37.35,145.47), (-37.74,145.05), (-37.97,145.01), (-37.46,145.6), (-37.16,145.1), (-37.9,145.28), (-37.96,145.49), (-37.1,145.35), (-37.54,145.81), (-37.19,145.28), (-37.56,145.92), (-37.95,145.14), (-37.76,145.39), (-37.03,145.86), (-37.36,145.4), (-37.76,145.91), (-37.93,145.4), (-37.88,145.64), (-37.5,145.64), (-37.44,145.16), (-37.96,145.97), (-37.97,145.82), (-37.83,145.92), (-37.98,145.02), (-37.48,145.58), (-37.84,145.49), (-37.44,145.2), (-37.67,145.86), (-37.96,145.83), (-37.89,145.05), (-37.77,145), (-37.81,145.08), (-37.82,144.95), (-37.78,145.04), (-37.79,144.97), (-37.78,145.06), (-37.79,144.97), (-37.88,145.01), (-37.79,144.93)],
                         '9': [(-37.69,145.7), (-37.14,145.1), (-37.44,145.34), (-37.43,145.67), (-37,145.31), (-37.62,145.89), (-37.93,145.66), (-37.87,145.22), (-37.72,145.96), (-37.54,145.28), (-37.89,145.34), (-37.64,145.92), (-37.4,145), (-37.13,145.42), (-37.81,145.71), (-37.89,145.47), (-37.24,145.01), (-37.97,145.06), (-37.28,145.4), (-37.66,145.31), (-37.04,145.15), (-37.06,145.76), (-37.96,145.66), (-37.54,145.34), (-37.35,145.99), (-37.16,145.93), (-37.7,145.18), (-37.51,145.41), (-37.96,145.11), (-37.02,145.95), (-37.12,145.9), (-37.74,145.33), (-37.12,145.27), (-37.33,145.87), (-37.1,145.9), (-37.48,145.5), (-37.97,145.77), (-37.45,145.96), (-37.35,145.47), (-37.74,145.05), (-37.19,145.28), (-37.56,145.92), (-37.95,145.14), (-37.76,145.39), (-37.03,145.86), (-37.36,145.4), (-37.76,145.91), (-37.93,145.4), (-37.88,145.64), (-37.5,145.64), (-37.87,144.93), (-37.73,145.01), (-37.82,144.9), (-37.86,144.92), (-37.79,144.92), (-37.79,145.05), (-37.81,144.99), (-37.88,144.99), (-37.87,145.04), (-37.78,145.03)],
                         '10': [(-37.13,145.42), (-37.81,145.71), (-37.89,145.47), (-37.24,145.01), (-37.97,145.06), (-37.28,145.4), (-37.66,145.31), (-37.75,145.92), (-37.34,145.17), (-37.58,145.16), (-37.25,145.07), (-37.48,145.73), (-37.04,145.15), (-37.06,145.76), (-37.96,145.66), (-37.54,145.34), (-37.35,145.99), (-37.16,145.93), (-37.7,145.18), (-37.51,145.41), (-37.96,145.11), (-37.02,145.95), (-37.12,145.9), (-37.74,145.33), (-37.12,145.27), (-37.36,145.46), (-37.66,145.28), (-37.99,145.61), (-37.18,145.77), (-37.16,145.1), (-37.9,145.28), (-37.96,145.49), (-37.1,145.35), (-37.54,145.81), (-37.19,145.28), (-37.5,145.64), (-37.44,145.16), (-37.96,145.97), (-37.97,145.82), (-37.83,145.92), (-37.98,145.02), (-37.18,145.38), (-37.77,145.78), (-37.43,145.04), (-37.23,145.1), (-37.4,145.19), (-37.55,145.49), (-37.3,145.48), (-37.33,145.29), (-37.11,145.63), (-37.73,145.04), (-37.79,144.89), (-37.84,145.08), (-37.82,144.97), (-37.87,145.06), (-37.79,144.95), (-37.81,145.05), (-37.73,144.97), (-37.77,144.99), (-37.76,144.94)]}
        '''
        self.userLocationDict = Util.convert_String_Into_Dict2(self, self.operatingFolder, "user_allChkIn_location_dictRound.txt")
        self.socialNetwork = Util.convert_String_Into_Dict2(self, self.operatingFolder, "Gowalla_edges_Dict.txt")

        self.userLocationDictUserList = ["354"]
        #for user in self.userLocationDict.keys():
        for user in self.userLocationDictUserList:
            L = self.userLocationDict[user]
            noOfLoc = len(L)
            if user in self.socialNetwork.keys() and len(self.socialNetwork[user]) > 10 and noOfLoc > self.k:

                ngbrLocs = []
                for ngbrs in  self.socialNetwork[user]:
                    if ngbrs in self.userLocationDict.keys():
                        ngbrLocs = ngbrLocs + self.userLocationDict[ngbrs]
                self.ngbrLocCombinedUnique = list(set(ngbrLocs))
                print("processing user:", user, ", self.k:", self.k, ", friends:", len(self.socialNetwork[user]), ", ngbr number of loc:", len(self.ngbrLocCombinedUnique), ", noOfLoc: ", noOfLoc, ", uniQ Loc: ", len(set(L)))

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
                self.createFile(os.path.join(self.outputFolder, "Location", str(user)+".txt"), strLoc)


                #self.allNgbrCheckinsMerged = Util.mergeLists_of_Dict(self, socialNetwork)
                #self.ngbrLocCombinedUnique = list(set(self.allNgbrCheckinsMerged))

                self.L = list(set(L)) #converting into set rather than list. set will contain unique elements
                self.socialScoreDict = self.calcSocialScore(self.L, self.socialNetwork[user])
                self.d_m_dict = self.calcMaxDist(self.L, self.ngbrLocCombinedUnique)
                #print("d_m: ", self.d_m)
                self.maxD = self.calcMaxD(self.L)
                self.spatialScoreDict = self.calcSpatialScore(self.L, self.socialNetwork[user])
                self.S_gs_Dict = self.calcRelevanceScore(self.socialScoreDict, self.spatialScoreDict, user)

                self.socialSpatialDiversity(self.L, self.socialNetwork[user], user)
                self.loadDgsContents(os.path.join(self.outputFolder, "Diversity", str(user) + ".txt")) #loading self.content and creating self.locAndIndex

                #dgs = self.dictOfDgsFromFileAndFly(self.content, self.locAndIndex, loc1_Q, loc2_Q)
                #self.DgsDictAll = self.dictOfDgsFromFile(os.path.join(self.outputFolder, "Diversity", str(user) + ".txt")) #contains D_gs of pair of locaitons


                #Now the original code starts
                start = time.time()
                S_I = []
                self.S_Rel = self.sortDesc(self.S_gs_Dict)
                S_R = list(self.S_Rel) #Put as backup arranged by relevance score
                self.l = tuple
                self.S = []

                #S_R = list(self.S_R) #making a different list S_R
                outerloop = 0

                while True:
                    loopstartTime = time.time()
                    outerloop += 1
                    print("outerloop: ", outerloop)
                    S_R = list(self.S_Rel)  # making a different list S_R, everytime S_R will decrease when S_Rel decreases and make list at that time
                    if len(self.S_Rel) < self.k:
                        break
                    #print(outerloop)
                    if len(S_I) == 0:
                        self.l = S_R[0]
                        S_R.remove(self.l)
                        self.S_Rel.remove(self.S_Rel[0])  # no user of S_Rel, just to iterate the list
                        print("self.l ", self.l)
                        S_I.append(self.l)
                        #print("After pop, length of SR: ", len(S_R))

                    while len(S_I) < self.k:
                        if len(S_I)==1 and self.bestScore > 0:
                            #print("self.bestScore: ", self.bestScore)
                            relScore = self.S_gs_Dict[S_I[0]] #S_I contains single location
                            #DgsM = max([self.DgsDictAll[(S_I[0], l)] for l in S_R])  #*************************************************
                            #DgsM = max([self.DgsFetchOnTheFly(os.path.join(self.outputFolder, "Diversity", user+".txt"), S_I[0], l) for l in S_R])  # *************************************************
                            DgsM = max([self.dictOfDgsFromFileAndFly(self.content, self.locAndIndex, S_I[0], l) for l in S_R])  # *************************************************
                            flag = self.earlyTermination(self.bestScore, relScore, DgsM, self.k)
                            if flag:
                                print("Early terminate for location root: ,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,, ", S_I[0])
                                S_I = []
                                break

                        topRelLoc = S_R[0]
                        topRelScore = self.S_gs_Dict[topRelLoc]
                        #print("top relevant location among remaining S_R: ", topRelLoc, " score: ", topRelScore)
                        D_max = self.calcDgsMax(S_R, S_I)
                        lowerRelBoundSgs = self.calcRelLowerBound(topRelScore, D_max, topRelLoc, S_I)
                        minRelInS_R = min(self.S_gs_Dict[l] for l in S_R)
                        tempSR = list(S_R)
                        tempSR.remove(topRelLoc)
                        VP = self.potentialLocs(tempSR, lowerRelBoundSgs)
                        referenceTopSet = list(S_I)
                        referenceTopSet.append(topRelLoc)
                        self.scoreTop = self.calcTotalScoreofSet(referenceTopSet)
                        #print("scoreTop: ", self.scoreTop)

                        #print("S_I old: ", S_I, "S_R old: ", S_R)
                        for loc in VP:
                            tempLocSet = list(S_I)
                            tempLocSet.append(loc)
                            score = self.calcTotalScoreofSet(tempLocSet)
                            if score > self.scoreTop:
                                self.scoreTop = score
                                topRelLoc = loc #dont confuse the term topRelLoc!!!
                        S_I.append(topRelLoc)
                        S_R.remove(topRelLoc)
                        S_R = list(self.arrangeListBasedOnRelScore(S_R))
                        #print("S_I new: ", S_I, "S_R new: ", S_R)

                        if len(S_I) == self.k:
                            print("scoreTop of new set: ", self.scoreTop)
                            if self.scoreTop > self.bestScore:
                                self.bestScore = self.scoreTop
                                self.S = list(S_I)
                                print("yessssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssss")
                            print("self.S: ", self.S, "score of S: ", self.bestScore)
                            S_I = []
                            elapsed_time_loop = (time.time() - loopstartTime)
                            print("elapsed_time_loop: ", elapsed_time_loop)
                            break

                    #self.S_Rel.pop()  # no user of S_Rel, just to iterate the list
                    #print("size S_Rel:", len(self.S_Rel))

                print("Final Set: ", self.S, "score: ", self.calcTotalScoreofSet(set(self.S)))
                locText = ""
                for loc in self.S:
                    lId = self.locNameAndLocId[loc]
                    loc = str(loc).replace("(", "").replace(")", "").strip()
                    locText = locText + str(lId) + "\t" + loc + "\n"
                self.createFile("E:\\NurProjectPython\\PycharmProjects\\All\\NurLocationSelection\\finalSetPlus.txt", locText)

                elapsed_time_fl = (time.time() - start)
                print("Elapsed Time: ", elapsed_time_fl)

                self.minDiversitySetOfEachLoc(self.S)

    def minDiversitySetOfEachLoc(self, finalS):
        print("Going to calculate <loc1 loc2 minDiv> for final set.")
        textMinDivEachLoc = ""
        for loc in finalS:
            lId = self.locNameAndLocId[loc]
            S_setminus = set(finalS)
            S_setminus.remove(loc)
            # if (loc, l) in self.DgsDictAll.keys:
            #minDgs = min([self.DgsDictAll[(loc, l)] for l in S_setminus]) # *************************************************
            minDgs = min([self.dictOfDgsFromFileAndFly(self.content, self.locAndIndex, loc, l) for l in S_setminus]) # *************************************************
            locTemp = ""
            for lc in S_setminus:
                if (self.dictOfDgsFromFileAndFly(self.content, self.locAndIndex, loc, lc) == minDgs): #********************************************
                    locTemp = lc
            textMinDivEachLoc = textMinDivEachLoc + str(lId) + "\t" + str(loc) + "\t" + str(self.S_gs_Dict[loc]) + "\t" + str(self.locNameAndLocId[locTemp]) + "\t" + str(locTemp) + "\t" + str(minDgs) + "\n"
        self.createFile("E:\\NurProjectPython\\PycharmProjects\\All\\NurLocationSelection\\finalSetWithDivPlus.txt", textMinDivEachLoc)

    def earlyTermination(self, bestScore, relScore, DgsM, k):
        statFlag = False
        F_max = k*(self.omega*relScore + (1 - self.omega)*DgsM)
        if bestScore > F_max:
            statFlag = True
        return statFlag

    def potentialLocs(self, S_R_copy, lowerRelBoundSgs_copy):
        potentialLocDict = {}
        for loc in S_R_copy:
            if self.S_gs_Dict[loc] > lowerRelBoundSgs_copy:
                potentialLocDict[loc] = self.S_gs_Dict[loc]
        #arrange w.r.t. rel score
        arrangedPotLoc = self.sortDesc(potentialLocDict)
        #print("potentialLocDict", potentialLocDict, "arrangedPotLoc: ", arrangedPotLoc)
        return arrangedPotLoc

    def arrangeListBasedOnRelScore(self, lst):
        tempDict = {}
        for l in lst:
            tempDict[l] = self.S_gs_Dict[l]
        arrabgeList = self.sortDesc(tempDict)
        return arrabgeList

    def calcRelLowerBound(self, topRelScore, D_max, topRelLoc, S_I):
        S_I_dash = list(S_I)
        S_I_dash.append(topRelLoc)
        Dgs_SI_dash = self.calcDgsOfSet(S_I_dash)
        Dgs_SI = self.calcDgsOfSet(S_I)
        #print("Dgs_SI_dash: ", Dgs_SI_dash, ", Dgs_SI", Dgs_SI)
        Sgs_lower = topRelScore + ((1-self.omega)/self.omega)*(Dgs_SI_dash - Dgs_SI - D_max)
        #print("Sgs_lower: ", Sgs_lower)
        return round(Sgs_lower,2)

    def calcDgsMax(self, S_R, S_I):
        tt = []
        for loc in S_R:
            tt.append(self.calcDgsOfLocToSet(loc, S_I))
        maxDiv = max(tt)
        return maxDiv

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
            maxTemp = max([Util.haversineDist(loc1, l) for l in L])
            #print(maxTemp)
            if maxTemp > maxD:
                maxD = maxTemp
        #print("maxD", maxD)
        return round(maxD, 2)

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

    def sortDesc(self, dictInput):
        logging.info("Arrange dict w.r.t. descending.")
        #sorted_d = dict(sorted(socialScoreDict.items(), key=operator.itemgetter(1), reverse=True))
        sorted_d = Util.sortDictByValueWithKey(dictInput) #return (-37.73, 145.06): 0.99, (-37.19, 145.28): 0.98, (-37.56, 145.92): 0.97 in descending order
        arrangedKeysOnly = [x[0] for x in sorted_d]
        return arrangedKeysOnly
        #return sorted_d #return (-37.73, 145.06): 0.99, (-37.19, 145.28): 0.98, (-37.56, 145.92): 0.97 in descending order

    def returnKeysOfArrangedDict(self, dictInput): ##returns the keys i.e. first elements only, not corresponding scores, do not arrange anything, expect arranged dict
        arrangedKeysOnly = [x for x in dictInput]
        return arrangedKeysOnly #{(-37.73, 145.06): 0.99, (-37.19, 145.28): 0.98, (-37.56, 145.92): 0.97} >>> [(-37.73, 145.06), (-37.19, 145.28), (-37.56, 145.92)]

    def arrangeListOfTuple(self, listOfTuples): #returns arranged keys and values based on values, same as: Util.sortDictByValueWithKey(socialScoreDict), check sortDesc
        listOfTuples.sort(key=operator.itemgetter(1), reverse=True)
        return listOfTuples

    def calcTotalScoreofSet(self, S):
        if self.flagMinMax == "MaxMin":
            totalSgs = 0
            minDgsTemp = []
            for loc in S:
                totalSgs += self.S_gs_Dict[loc]
                S_setminus = set(S)
                S_setminus.remove(loc)
                for loc2 in S_setminus:
                    #minDgsTemp.append(self.DgsDictAll[loc, loc2]) #*********************************************
                    minDgsTemp.append(self.dictOfDgsFromFileAndFly(self.content, self.locAndIndex, loc, loc2)) #*********************************************
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
                    totalDgs += self.dictOfDgsFromFileAndFly(self.content, self.locAndIndex, loc, loc2)
            totalscore = self.omega*totalSgs + (1 - self.omega)*totalDgs
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
                    #totalDgs += self.DgsDictAll[loc, loc2] #*********************************************
                    minDgsTemp.append(self.dictOfDgsFromFileAndFly(self.content, self.locAndIndex, loc, loc2)) #*********************************************
                totalDgs += min(minDgsTemp)
            totalscore = self.omega*totalSgs + (1 - self.omega)*totalDgs
            return round(totalscore, 2)

    def calcDgsOfLocToSet(self, loc, S):
        #minDgs = min([self.DgsDictAll[(loc, l)] for l in S]) #*********************************************
        minDgs = min([self.dictOfDgsFromFileAndFly(self.content, self.locAndIndex, loc, l) for l in S]) #*********************************************
        return minDgs

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
            minDgs = min([self.dictOfDgsFromFileAndFly(self.content, self.locAndIndex, loc, l) for l in S_setminus]) #*********************************************
            totalDgs += minDgs
        return totalDgs

    def DgsFetchOnTheFly(self, filePath, loc1_Q, loc2_Q):
        f = open(filePath, "r")
        content = f.readlines()
        content = [x.strip() for x in content]
        locAndIndex = []
        for i in range(len(content)):
            splitArray = content[i].split("\t")
            if len(splitArray) > 1:
                loc = eval(splitArray[0].strip())
                locAndIndex.append(loc)

        for i in range(len(content)):
            splitArray = content[i].split("\t")
            if len(splitArray) > 1:
                loc1Temp = eval(splitArray[0].strip())
                if loc1Temp == loc1_Q and loc2_Q in locAndIndex:
                    loc2Index = locAndIndex.index(loc2_Q)
                    tempValDgs = splitArray[loc2Index+1]

                    return float(tempValDgs)

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
                    tempValDgs = splitArray[loc2Index+1]

                    return float(tempValDgs)

    def dictOfDgsFromFile(self, filePath):
        #with open(filePath) as f:
        #    content = f.readlines()
        f = open(filePath, "r")
        content = f.readlines()
        content = [x.strip() for x in content]

        locAndIndex = []

        tempDict = {}
        for i in range(len(content)):
            splitArray = content[i].split("\t")
            if len(splitArray) > 1:
                loc1 = eval(splitArray[0].strip())
                locAndIndex.append(loc1)

        for i in range(len(content)):
            splitArray = content[i].split("\t")
            if len(splitArray) > 1:
                loc2 = eval(splitArray[1].strip())
                DgsScore = splitArray[8].strip()
                tempDict[loc1,loc2] = float(DgsScore)
        return tempDict

    def calcSocialScore(self, L, socialNetworkNgbrList):
        userDegree = len(socialNetworkNgbrList)
        socScore = {}

        for loc in L:
            totalNgbrChks = 0
            for ngbr in socialNetworkNgbrList:
                if ngbr in self.userLocationDict.keys() and loc in self.userLocationDict[ngbr]:
                    totalNgbrChks += 1
            socScore[loc] = round(totalNgbrChks/userDegree, 2)
        return socScore

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
        #print("Total relevance score of each locaiton.")
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

    def createFile(self, fileNameFullPath, contents):
        try:
            fw_fileName = open(fileNameFullPath, "w", encoding="utf8")
            fw_fileName.write(contents.__str__())
            fw_fileName.close()
        except KeyError:
            print("Error while creating file.. ", KeyError)
            pass
obj = ExactPlus()