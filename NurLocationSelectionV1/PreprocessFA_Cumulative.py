import os.path

class CumulativeFAPreprocess:
    def __init__(self):
        print("Preprocessing Cumulative chart for Fast Approximation intuition")
        self.datasetName = "Flickr"  # Gowalla, Brightkite, Flickr, Yelp

        self.operatingFolder = os.path.join("I:\\ExpDataUDI\\ExperimentFolder", self.datasetName, "ExpResult2\\Results\\bin100\\FAIntuition")
        kList = [2, 4, 6, 8, 10]

        for k in kList:
            self.k = k # 2, 4, 6, 8, 10

            filePath = os.path.join(self.operatingFolder, "divideByTopScore_"+str(self.k)+".txt")
            with open(filePath) as f:
                content = f.readlines()
            content = [x.strip() for x in content]

            tempDict = {}
            for i in range(len(content)):
                splitArray = content[i].split("\t")
                if len(splitArray) > 3:
                    val1 = float(splitArray[0])
                    val2 = float(splitArray[1])
                    val3 = float(splitArray[2])
                    tempDict[i] = [val1, val2, val3]

            cumulativeCounter1 = 0
            cumulativeCounter12 = 0
            cumulativeCounter123 = 0

            for user in tempDict:
                if tempDict[user][0] == 1.0:
                    cumulativeCounter1 += 1
                if tempDict[user][0] == 1.0 or tempDict[user][1] == 1.0:
                    cumulativeCounter12 += 1
                if tempDict[user][0] == 1.0 or tempDict[user][1] == 1.0 or tempDict[user][2] == 1.0:
                    cumulativeCounter123 += 1
            outStr = str(round(cumulativeCounter1/len(tempDict),2)) + "\t"+ str(round(cumulativeCounter12/len(tempDict),2)) + "\t"+ str(round(cumulativeCounter123/len(tempDict),2))
            print("Result: ", outStr)

            self.createFile(os.path.join(self.operatingFolder, "divideByCumulative_" + str(self.k) +".txt"), outStr)

    def createFile(self, fileNameFullPath, contents):
        try:
            fw_fileName = open(fileNameFullPath, "w", encoding="utf8")
            fw_fileName.write(contents.__str__())
            fw_fileName.close()
        except KeyError:
            print("Error while creating file.. ", KeyError)
            pass

obj = CumulativeFAPreprocess()