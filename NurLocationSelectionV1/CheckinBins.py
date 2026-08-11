import os.path
import NurTestingPycharm.UtilNur as Util
import ast


class CheckinBins:
    def __init__(self):
        print("Creating checkin bins 50, 100, 200, 500, 1000")

        self.baseFolder = "I:\\ExpDataUDI\\ExperimentFolder"
        self.datasetName = "Flickr"  # Gowalla, Flickr, Brightkite, Yelp
        bin50 = []
        bin100 = []
        bin200 = []
        bin500 = []
        bin1000 = []

        if self.datasetName == "Flickr": #Flickr, Yelp
            with open(os.path.join(self.baseFolder, self.datasetName, "NoOfCheckinListAndUniQ.txt")) as f:
                content = f.readlines()
            content = [x.strip() for x in content]

            strngTemp = ""
            for i in range(len(content)):
                splitArray = content[i].split("\t")
                if len(splitArray) > 1:
                    user = splitArray[0].strip()
                    noOfcheckins = int(splitArray[2].strip())
                    if noOfcheckins > 10 and noOfcheckins <= 50:
                        bin50.append(user)
                    if noOfcheckins > 50 and noOfcheckins <= 100:
                        bin100.append(user)
                    if noOfcheckins > 100 and noOfcheckins <= 200:
                        bin200.append(user)
                    if noOfcheckins > 200 and noOfcheckins <= 500:
                        bin500.append(user)
                    if noOfcheckins > 500 and noOfcheckins <= 1000:
                        bin1000.append(user)

            self.createFile(os.path.join(self.baseFolder, self.datasetName, "ExpResult2", "CheckinBins", "bin50.txt"), str(bin50))
            self.createFile(os.path.join(self.baseFolder, self.datasetName, "ExpResult2", "CheckinBins", "bin100.txt"), str(bin100))
            self.createFile(os.path.join(self.baseFolder, self.datasetName, "ExpResult2", "CheckinBins", "bin200.txt"), str(bin200))
            self.createFile(os.path.join(self.baseFolder, self.datasetName, "ExpResult2", "CheckinBins", "bin500.txt"), str(bin500))
            self.createFile(os.path.join(self.baseFolder, self.datasetName, "ExpResult2", "CheckinBins", "bin1000.txt"), str(bin1000))

            exit()
        # self.operatingFolder = os.path.join(self.baseFolder, self.datasetName)
        self.operatingFolder = os.path.join(self.baseFolder, self.datasetName)
        loadDict = Util.convert_String_Into_Dict2(self, self.operatingFolder, "userID_chkInNumber_location_Dict.txt")

        for user in loadDict.keys():
            noOfcheckins = int(loadDict[user])
            if noOfcheckins > 10 and noOfcheckins <=50:
                bin50.append(user)
            if noOfcheckins > 50 and noOfcheckins <= 100:
                bin100.append(user)
            if noOfcheckins > 100 and noOfcheckins <= 200:
                bin200.append(user)
            if noOfcheckins > 200 and noOfcheckins <= 500:
                bin500.append(user)
            if noOfcheckins > 500 and noOfcheckins <= 1000:
                bin1000.append(user)

        self.createFile(os.path.join(self.baseFolder, self.datasetName, "ExpResult2", "CheckinBins", "bin50.txt"), str(bin50))
        self.createFile(os.path.join(self.baseFolder, self.datasetName, "ExpResult2", "CheckinBins", "bin100.txt"), str(bin100))
        self.createFile(os.path.join(self.baseFolder, self.datasetName, "ExpResult2", "CheckinBins", "bin200.txt"), str(bin200))
        self.createFile(os.path.join(self.baseFolder, self.datasetName, "ExpResult2", "CheckinBins", "bin500.txt"), str(bin500))
        self.createFile(os.path.join(self.baseFolder, self.datasetName, "ExpResult2", "CheckinBins", "bin1000.txt"), str(bin1000))

    def createFile(self, fileNameFullPath, contents):
        try:
            fw_fileName = open(fileNameFullPath, "w", encoding="utf8")
            fw_fileName.write(contents.__str__())
            fw_fileName.close()
        except KeyError:
            print("Error while creating file.. ", KeyError)
            pass
obj = CheckinBins()