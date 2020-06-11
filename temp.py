def MakeNewShapeRD(self, existingPoints, allPoints):
    stop = False
    newShape = []
    tempPoints = list(allPoints)
    checkHorizontal = True
    counter = 0
    isFound = False
    firstX = 700
    firstY = 700
    SuspiciousX = []
    SuspiciousY = []
    z = 0

    currP = (firstX, firstY)

    if len(existingPoints) == 2:
        for EP in existingPoints:
            tempPoints.remove(EP)
        existingPoints.clear()

    if len(existingPoints) == 1:
        for EP in existingPoints:
            SuspiciousX.clear()
            counter = 0
            for T in tempPoints:
                if EP[0] == T[0]:
                    counter = counter + 1
            if counter % 2 != 0:
                for T in tempPoints:
                    if EP[0] == T[0]:
                        SuspiciousX.append(T)

            SuspiciousY.clear()
            counter = 0
            for T in tempPoints:
                if EP[1] == T[1]:
                    counter = counter + 1
            if counter % 2 != 0:
                for T in tempPoints:
                    if EP[1] == T[1]:
                        SuspiciousY.append(T)

            isRemoved = False

            if EP in SuspiciousX and EP in SuspiciousY:
                tempPoints.remove(EP)
                isRemoved = True
            elif EP in SuspiciousX:
                SuspiciousY.clear()
                SuspiciousX.remove(EP)

                for SU in SuspiciousX:
                    counter = 0
                    for T in tempPoints:
                        if SU[1] == T[1]:
                            counter = counter + 1
                    if counter % 2 != 0:
                        for T in tempPoints:
                            if SU[1] == T[1]:
                                SuspiciousY.append(T)

                if len(SuspiciousY) != 0:
                    SuspiciousY.sort()
                    z = int((len(SuspiciousY) - 1) / 2)
                    tempPoints.remove(SuspiciousY[z])
                    isRemoved = True

            elif EP in SuspiciousY:
                SuspiciousX.clear()
                SuspiciousY.remove(EP)

                for SU in SuspiciousY:
                    counter = 0
                    for T in tempPoints:
                        if SU[0] == T[0]:
                            counter = counter + 1
                    if counter % 2 != 0:
                        for T in tempPoints:
                            if SU[0] == T[0]:
                                SuspiciousX.append(T)

                if len(SuspiciousX) != 0:
                    SuspiciousX.sort()
                    z = int((len(SuspiciousX) - 1) / 2)
                    tempPoints.remove(SuspiciousX[z])
                    isRemoved = True

            if not isRemoved:
                tempPoints.remove(EP)

    # find corner point
    for p in tempPoints:
        if p[0] <= currP[0]:
            if p[1] <= currP[1]:
                currP = p

    newShape.append(currP)
    tempPoints.remove(currP)

    while len(tempPoints) > 0 and not stop:
        if checkHorizontal:
            # check right
            currP = (700, currP[1])
            isFound = False
            for p in tempPoints:
                if p[1] == currP[1]:
                    if newShape[-1][0] < p[0] < currP[0]:
                        isFound = True
                        checkHorizontal = False
                        currP = p
            # check left
            if not isFound:
                currP = (0, currP[1])
                for p in tempPoints:
                    if p[1] == currP[1]:
                        if newShape[-1][0] > p[0] > currP[0]:
                            currP = p
                            checkHorizontal = False
                            isFound = True
            if isFound:
                newShape.append(currP)
                tempPoints.remove(currP)

        if not checkHorizontal:
            currP = (currP[0], 700)
            isFound = False
            if len(tempPoints) > 0:
                # check down
                for p in tempPoints:
                    if p[0] == currP[0]:
                        if newShape[-1][1] < p[1] < currP[1]:
                            checkHorizontal = True
                            isFound = True
                            currP = p

                # check up
                if not isFound:
                    currP = (currP[0], 0)
                    for p in tempPoints:
                        if p[0] == currP[0]:
                            if newShape[-1][1] > p[1] > currP[1]:
                                currP = p
                                checkHorizontal = True
                                isFound = True
                if isFound:
                    newShape.append(currP)
                    tempPoints.remove(currP)

        counter = 0
        if len(tempPoints) == 0:
            for p in newShape:
                if p[0] == newShape[0][0]:
                    counter = counter + 1

        if not isFound or counter % 2 != 0:
            if newShape[0][0] == currP[0] and counter % 2 == 0:
                stop = True
            else:
                newShape.remove(newShape[-1])
                checkHorizontal = True
                tempPoints = list(newShape + tempPoints)
                newShape.clear()
                currP = tempPoints[0]
                newShape.append(currP)
                tempPoints.remove(tempPoints[0])
                counter = 0

    self.LinesProperties.clear()

    for i in range(len(newShape) - 1):
        if i % 2 == 0:
            if newShape[i][0] < newShape[i + 1][0]:
                self.LinesProperties.append(('x', newShape[i][1], newShape[i][0], newShape[i + 1][0]))
            else:
                self.LinesProperties.append(('x', newShape[i][1], newShape[i + 1][0], newShape[i][0],))
        else:
            if newShape[i][1] < newShape[i + 1][1]:
                self.LinesProperties.append(('y', newShape[i][0], newShape[i][1], newShape[i + 1][1]))
            else:
                self.LinesProperties.append(('y', newShape[i][0], newShape[i + 1][1], newShape[i][1]))

    if newShape[-1][1] < newShape[0][1]:
        self.LinesProperties.append(('y', newShape[-1][0], newShape[-1][1], newShape[0][1]))
    else:
        self.LinesProperties.append(('y', newShape[-1][0], newShape[0][1], newShape[-1][1]))

    allPoints = list(newShape)
    newShape.append(newShape[0])
    self.canvas.delete(self.MainLn)
    self.MainLn = self.canvas.create_polygon(newShape, fill='grey', width=1)

    return allPoints