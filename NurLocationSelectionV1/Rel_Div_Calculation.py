import os.path

class RelDivCalc:
    def __init__(self):
        print("creating social Rel, spatial Rel, social Div, Spatial Div, Location index, and all results in file format. alpha beta, gamma not used, but later used for SocSpatial folder")
        self.alpha = 0.5
        self.beta = 0.5
        self.omega = 0.5

        self.baseFolder = "I:\\ExpDataUDI\\ExperimentFolder"
        self.datasetName = "Gowalla"

        self.operatingFolder = os.path.join(self.baseFolder, self.datasetName)
        self.outputFolder = os.path.join(self.operatingFolder, "ExpResult2")

obj = RelDivCalc()