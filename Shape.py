from shapely.geometry import Point
from shapely.geometry.polygon import Polygon


class Shape:
    OldShape = [(6, 6), (608, 6), (608, 608), (6, 608)]
    firstX = 700
    firstY = 700
    isFound = True
    tempPoints = []
    newShape1 = []
    newShape2 = []
    currP = (0, 0)
    stop = False
    AllPoints = []

    def MakeNewShapeRD(self, existingPoints, allPoints, addedPoints):

        self.AllPoints = list(allPoints)
        self.tempPoints = list(allPoints)
        self.newShape1.clear()
        self.newShape2.clear()
        self.stop = False
        self.isFound = False

        if len(existingPoints) == 0:
            return list(self.Exist0())

        if len(existingPoints) == 1:
            return self.Exist1(existingPoints, addedPoints)

    def Exist0(self):
        counter = 0
        self.currP = self.tempPoints[-1]
        goOnX = True

        for ln in self.GB.LinesPropertiesX:
            if ln[1] == self.currP[1]:
                if ln[2] < self.currP[0] < ln[3]:
                    goOnX = False

        if not goOnX:
            self.tempPoints = list(self.AllPoints)

            self.newShape1.append(self.currP)

            while len(self.tempPoints) > 0 and not self.stop:
                self.isFound = False
                if not self.searchRight(self.newShape1):
                    self.searchLeft(self.newShape1)

                if self.isFound:
                    if self.currP == self.newShape1[0]:
                        break
                    else:
                        self.newShape1.append(self.currP)
                        self.tempPoints.remove(self.currP)

                self.isFound = False
                if len(self.tempPoints) > 0:
                    if not self.searchDown(self.newShape1):
                        self.searchUp(self.newShape1)

                    if self.isFound:
                        if self.currP == self.newShape1[0]:
                            break
                        else:
                            self.newShape1.append(self.currP)
                            self.tempPoints.remove(self.currP)

            self.tempPoints = list(self.AllPoints)
            self.currP = self.tempPoints[-1]

            self.newShape2.append(self.currP)

            while len(self.tempPoints) > 0 and not self.stop:
                self.isFound = False
                if not self.searchLeft(self.newShape2):
                    self.searchRight(self.newShape2)

                if self.isFound:
                    if self.currP == self.newShape2[0]:
                        break
                    else:
                        self.newShape2.append(self.currP)
                        self.tempPoints.remove(self.currP)

                self.isFound = False
                if len(self.tempPoints) > 0:
                    if not self.searchDown(self.newShape2):
                        self.searchUp(self.newShape2)

                    if self.isFound:
                        if self.currP == self.newShape2[0]:
                            break
                        else:
                            self.newShape2.append(self.currP)
                            self.tempPoints.remove(self.currP)

        else:  # Search up and then down

            self.tempPoints = list(self.AllPoints)
            self.newShape1.append(self.currP)

            while len(self.tempPoints) > 0 and not self.stop:
                self.isFound = False
                if not self.searchUp(self.newShape1):
                    self.searchDown(self.newShape1)

                if self.isFound:
                    if self.currP == self.newShape1[0]:
                        break
                    else:
                        self.newShape1.append(self.currP)
                        self.tempPoints.remove(self.currP)

                self.isFound = False
                if len(self.tempPoints) > 0:

                    if not self.searchRight(self.newShape1):
                        self.searchLeft(self.newShape1)

                    if self.isFound:
                        if self.currP == self.newShape1[0]:
                            break
                        else:
                            self.newShape1.append(self.currP)
                            self.tempPoints.remove(self.currP)

            self.tempPoints = list(self.AllPoints)
            self.currP = self.tempPoints[-1]
            self.newShape2.append(self.currP)

            while len(self.tempPoints) > 0 and not self.stop:
                self.isFound = False
                if not self.searchDown(self.newShape2):
                    self.searchUp(self.newShape2)

                if self.isFound:
                    if self.currP == self.newShape1[0]:
                        break
                    else:
                        self.newShape2.append(self.currP)
                        self.tempPoints.remove(self.currP)

                self.isFound = False
                if len(self.tempPoints) > 0:

                    if not self.searchRight(self.newShape2):
                        self.searchLeft(self.newShape2)

                    if self.isFound:
                        if self.currP == self.newShape1[0]:
                            break
                        else:
                            self.newShape2.append(self.currP)
                            self.tempPoints.remove(self.currP)

        tempShape = list(self.newShape1)
        pointNm = Point(self.GB.Enm.EnemyX + 8, self.GB.Enm.EnemyY + 8)
        polygon = Polygon(tempShape)

        if polygon.contains(pointNm):
            self.finishShape(self.newShape1)
            self.GB.ShapeArea = int(polygon.area)

            self.OldShape = list(self.newShape1)
            return self.newShape1
        else:
            polygon = Polygon(self.newShape2)
            self.GB.ShapeArea = int(polygon.area)

            self.finishShape(self.newShape2)
            self.OldShape = list(self.newShape2)

            return self.newShape2

    def Exist1(self, existingPoints, addedPoints):

        self.currP = existingPoints[0]
        self.tempPoints = list(self.AllPoints)

        goOnX = True
        if addedPoints[-1] == self.currP:
            if addedPoints[-1][0] == addedPoints[-2][0]:
                goOnX = False
        else:
            if addedPoints[0][0] == addedPoints[1][0]:
                goOnX = False

        if not goOnX:

            self.tempPoints = list(self.AllPoints)
            self.newShape1.append(self.currP)

            while len(self.tempPoints) > 0 and not self.stop:
                self.isFound = False
                if not self.searchRight(self.newShape1):
                    self.searchLeft(self.newShape1)

                if self.isFound:
                    if self.currP == self.newShape1[0]:
                        break
                    else:
                        self.newShape1.append(self.currP)
                        self.tempPoints.remove(self.currP)

                self.isFound = False
                if len(self.tempPoints) > 0:
                    if not self.searchDown(self.newShape1):
                        self.searchUp(self.newShape1)

                    if self.isFound:
                        if self.currP == self.newShape1[0]:
                            break
                        else:
                            self.newShape1.append(self.currP)
                            self.tempPoints.remove(self.currP)

            self.tempPoints = list(self.AllPoints)
            self.tempPoints.remove(existingPoints[0])

            if existingPoints[0] == addedPoints[0]:
                self.currP = addedPoints[-1]
            else:
                self.currP = addedPoints[0]

            self.newShape2.append(self.currP)

            while len(self.tempPoints) > 0 and not self.stop:
                self.isFound = False
                if not self.searchLeft(self.newShape2):
                    self.searchRight(self.newShape2)

                if self.isFound:
                    if self.currP == self.newShape2[0]:
                        break
                    else:
                        self.newShape2.append(self.currP)
                        self.tempPoints.remove(self.currP)
                else:

                    if len(self.newShape2) > 1:
                        if self.newShape2[-1] in self.tempPoints:
                            self.tempPoints.remove(self.newShape2[-1])
                        self.newShape2.remove(self.newShape2[-1])

                    self.currP = self.newShape2[-1]

                self.isFound = False
                if len(self.tempPoints) > 0:
                    if not self.searchDown(self.newShape2):
                        self.searchUp(self.newShape2)

                    if self.isFound:
                        if self.currP == self.newShape2[0]:
                            break
                        else:
                            self.newShape2.append(self.currP)
                            self.tempPoints.remove(self.currP)
                    else:
                        if len(self.newShape2) > 1:
                            if self.newShape2[-1] in self.tempPoints:
                                self.tempPoints.remove(self.newShape2[-1])
                            self.newShape2.remove(self.newShape2[-1])

                        self.currP = self.newShape2[-1]

        else:  # Search up and then down

            self.tempPoints = list(self.AllPoints)
            self.newShape1.append(self.currP)

            while len(self.tempPoints) > 0 and not self.stop:
                self.isFound = False
                if not self.searchUp(self.newShape1):
                    self.searchDown(self.newShape1)

                if self.isFound:
                    if self.currP == self.newShape1[0]:
                        break
                    else:
                        self.newShape1.append(self.currP)
                        self.tempPoints.remove(self.currP)

                self.isFound = False
                if len(self.tempPoints) > 0:
                    if not self.searchRight(self.newShape1):
                        self.searchLeft(self.newShape1)

                    if self.isFound:
                        if self.currP == self.newShape1[0]:
                            break
                        else:
                            self.newShape1.append(self.currP)
                            self.tempPoints.remove(self.currP)

            self.tempPoints = list(self.AllPoints)
            self.tempPoints.remove(existingPoints[0])
            if existingPoints[0] == addedPoints[0]:
                self.currP = addedPoints[-1]
            else:
                self.currP = addedPoints[0]

            self.newShape2.append(self.currP)

            while len(self.tempPoints) > 0 and not self.stop:
                self.isFound = False
                if not self.searchDown(self.newShape2):
                    self.searchUp(self.newShape2)

                if self.isFound:
                    if self.currP == self.newShape2[0]:
                        break
                    else:
                        self.newShape2.append(self.currP)
                        self.tempPoints.remove(self.currP)
                else:
                    if len(self.newShape2) > 1:
                        counter = 0
                        for tp in self.tempPoints:
                            if tp == self.newShape2[-1]:
                                self.tempPoints[counter] = (tp[0],tp[1],False)
                            counter = counter + 1
                        self.tempPoints.append((self.newShape2[-1][0],self.newShape2[-1][1],False))
                        self.newShape2.remove(self.newShape2[-1])

                    self.currP = self.newShape2[-1]

                self.isFound = False
                if len(self.tempPoints) > 0:

                    if not self.searchRight(self.newShape2):
                        self.searchLeft(self.newShape2)

                    if self.isFound:
                        if self.currP == self.newShape2[0]:
                            break
                        else:
                            self.newShape2.append(self.currP)
                            self.tempPoints.remove(self.currP)
                    else:
                        if len(self.newShape2) > 1:
                            counter = 0
                            for tp in self.tempPoints:
                                if tp == self.newShape2[-1]:
                                    self.tempPoints[counter] = (tp[0], tp[1], False)
                                counter = counter + 1
                            self.tempPoints.append((self.newShape2[-1][0], self.newShape2[-1][1], False))
                            self.newShape2.remove(self.newShape2[-1])
                        self.currP = self.newShape2[-1]

        tempShape = list(self.newShape1)

        pointNm = Point(self.GB.Enm.EnemyX + 8, self.GB.Enm.EnemyY + 8)
        polygon = Polygon(tempShape)

        if polygon.contains(pointNm):
            self.finishShape(self.newShape1)
            self.OldShape = list(self.newShape1)
            self.GB.ShapeArea = int(polygon.area)

            return self.newShape1
        else:
            polygon = Polygon(self.newShape2)
            self.GB.ShapeArea = int(polygon.area)

            self.finishShape(self.newShape2)
            self.OldShape = list(self.newShape2)
            return self.newShape2

    def searchRight(self, arrShape):
        GO = False
        self.currP = arrShape[-1]
        for ln in self.GB.LinesPropertiesX:
            if ln[1] == self.currP[1]:
                if ln[2] < self.currP[0] + 0.01 < ln[3]:
                    GO = True
        if not GO:
            return False

        # check right
        self.currP = (700, self.currP[1], False)
        for p in self.tempPoints:
            if p[1] == self.currP[1]:
                if arrShape[-1][0] < p[0] < self.currP[0]:
                    self.isFound = p[2]
                    self.currP = p

        return self.isFound

    def searchLeft(self, arrShape):
        self.currP = arrShape[-1]
        GO = False
        for ln in self.GB.LinesPropertiesX:
            if ln[1] == self.currP[1]:
                if ln[2] < self.currP[0] - 0.01 < ln[3]:
                    GO = True
        if not GO:
            return False

        # check left
        self.currP = (0, self.currP[1], False)
        for p in self.tempPoints:
            if p[1] == self.currP[1]:
                if arrShape[-1][0] > p[0] > self.currP[0]:
                    self.currP = p
                    self.isFound = p[2]

        return self.isFound

    def searchDown(self, arrShape):
        self.currP = arrShape[-1]
        GO = False
        for ln in self.GB.LinesPropertiesY:
            if ln[1] == self.currP[0]:
                if ln[2] < self.currP[1] + 0.01 < ln[3]:
                    GO = True
        if not GO:
            return False

        self.currP = (self.currP[0], 700, False)
        # check down
        for p in self.tempPoints:
            if p[0] == self.currP[0]:
                if arrShape[-1][1] < p[1] < self.currP[1]:
                    self.isFound = p[2]
                    self.currP = p
        return self.isFound

    def searchUp(self, arrShape):  # check up
        self.currP = arrShape[-1]
        GO = False
        for ln in self.GB.LinesPropertiesY:
            if ln[1] == self.currP[0]:
                if ln[2] < self.currP[1] - 0.01 < ln[3]:
                    GO = True
        if not GO:
            return False
        self.currP = (self.currP[0], 0,False)
        for p in self.tempPoints:
            if p[0] == self.currP[0]:
                if arrShape[-1][1] > p[1] > self.currP[1]:
                    self.currP = p
                    self.isFound = p[2]
        return self.isFound

    def FinishWhile(self, arrShape, finishWith):
        counter = 0
        isFinish = False

        if finishWith == 'x':
            if len(self.tempPoints) == 0:
                for p in arrShape:
                    if p[0] == arrShape[0][0]:
                        counter = counter + 1

            if not self.isFound or counter % 2 != 0:
                if arrShape[0][0] == self.currP[0] and counter % 2 == 0:
                    isFinish = True
        else:
            if len(self.tempPoints) == 0:
                for p in arrShape:
                    if p[1] == arrShape[0][1]:
                        counter = counter + 1

            if not self.isFound or counter % 2 != 0:
                if arrShape[0][1] == self.currP[1] and counter % 2 == 0:
                    isFinish = True

        if isFinish:
            self.stop = True
            return True
        else:
            if not self.isFound:
                self.currP = arrShape[0]
                self.tempPoints = list(self.AllPoints)
                self.tempPoints.remove(arrShape[-1])

            return False

    def finishShape(self, arrShape):

        self.GB.LinesPropertiesX.clear()
        self.GB.LinesPropertiesY.clear()

        for i in range(len(arrShape) - 1):
            if arrShape[i][0] != arrShape[i + 1][0]:
                if arrShape[i][0] < arrShape[i + 1][0]:
                    self.GB.LinesPropertiesX.append(('x', arrShape[i][1], arrShape[i][0], arrShape[i + 1][0], False))
                else:
                    self.GB.LinesPropertiesX.append(('x', arrShape[i][1], arrShape[i + 1][0], arrShape[i][0], False))
            else:
                if arrShape[i][1] < arrShape[i + 1][1]:
                    self.GB.LinesPropertiesY.append(('y', arrShape[i][0], arrShape[i][1], arrShape[i + 1][1], False))
                else:
                    self.GB.LinesPropertiesY.append(('y', arrShape[i][0], arrShape[i + 1][1], arrShape[i][1], False))

        if arrShape[-1][0] != arrShape[0][0]:
            if arrShape[-1][0] < arrShape[0][0]:
                self.GB.LinesPropertiesX.append(('x', arrShape[-1][1], arrShape[-1][0], arrShape[0][0], False))
            else:
                self.GB.LinesPropertiesX.append(('x', arrShape[-1][1], arrShape[0][0], arrShape[-1][0], False))
        else:
            if arrShape[-1][1] < arrShape[0][1]:
                self.GB.LinesPropertiesY.append(('y', arrShape[-1][0], arrShape[-1][1], arrShape[0][1], False))
            else:
                self.GB.LinesPropertiesY.append(('y', arrShape[-1][0], arrShape[0][1], arrShape[-1][1], False))

        allPoints = list(arrShape)
        arrShape.append(arrShape[0])
        self.GB.canvas.delete(self.MainLn)
        FinalShap = []
        for AS in arrShape:
            FinalShap.append((AS[0], AS[1]))
        self.MainLn = self.GB.canvas.create_polygon(FinalShap, fill='grey', width=1)

        return allPoints

    def __init__(self, mainLn, gb):

        self.MainLn = mainLn
        self.GB = gb

    def resetMainLn(self):
        self.MainLn = self.GB.canvas.create_polygon(6, 6, 608, 6, 608, 608, 6, 608, 6, 6, fill='grey', width=1)
