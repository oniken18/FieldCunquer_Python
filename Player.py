import tkinter as tk


class Player:
    PlayerSpeed = 0.02
    PosX = 3
    PosY = 3
    isSpacePressed = False
    MovingDirection = '0'
    isOutLine = False
    WhitePoint = (0, 0)
    stopPlayer = False
    LastLineStartP = (0, 0)

    def __init__(self, player, gb):
        self.Player = player
        self.Player.place(width=8, height=8, x=3, y=3)
        self.GB = gb

    def getLastWhiteLine(self):
        if self.MovingDirection == '4':
            return 'x', self.LastLineStartP[1], self.PosX, self.LastLineStartP[0], True
        if self.MovingDirection == '6':
            return 'x', self.LastLineStartP[1], self.LastLineStartP[0], self.PosX, True
        if self.MovingDirection == '8':
            return 'y', self.LastLineStartP[0], self.PosY, self.LastLineStartP[1], True
        if self.MovingDirection == '5':
            return 'y', self.LastLineStartP[0], self.LastLineStartP[1], self.PosY, True

        return 'Finish',0

    def setLineProperties(self, OrgDirection, startP, finishP):

        if OrgDirection == '4':
            self.GB.LinesPropertiesX.append(('x', startP[1], finishP[0], startP[0], True))
        elif OrgDirection == '6':
            self.GB.LinesPropertiesX.append(('x', startP[1], startP[0], finishP[0], True))
        elif OrgDirection == '8':
            self.GB.LinesPropertiesY.append(('y', startP[0], finishP[1], startP[1], True))
        elif OrgDirection == '5':
            self.GB.LinesPropertiesY.append(('y', startP[0], startP[1], finishP[1], True))

    def getStopPointX(self, direction, startX, Y):
        if direction == '4':
            result = (0, False)
            for ln in self.GB.LinesPropertiesY:
                if result[0] < ln[1] < startX and (ln[2] < Y < ln[3] or ln[3] < Y < ln[2]):
                    result = (ln[1] - 3, ln[4])
            return result

        elif direction == '6':
            result = (700, False)
            for ln in self.GB.LinesPropertiesY:
                if result[0] > ln[1] > startX and (ln[2] < Y < ln[3] or ln[3] < Y < ln[2]):
                    result = (ln[1] - 3, ln[4])
            return result

    def getStopPointY(self, direction, startY, X):
        if direction == '8':
            result = (0, False)
            for ln in self.GB.LinesPropertiesX:
                if result[0] < ln[1] < startY and (ln[2] < X < ln[3] or ln[3] < X < ln[2]):
                    result = (ln[1] - 3, ln[4])
            return result

        elif direction == '5':
            result = (700, False)
            for ln in self.GB.LinesPropertiesX:
                if result[0] > ln[1] > startY and (ln[2] < X < ln[3] or ln[3] < X < ln[2]):
                    result = (ln[1] - 3, ln[4])
            return result

    def isMoveOnLine(self, Direction, currX, currY):
        currX = currX + 3
        currY = currY + 3

        if Direction == '4':
            for ln in self.GB.LinesPropertiesX:
                if ln[1] == currY and ln[2] < currX <= ln[3]:
                    return ln[2] - 3
            return 0

        if Direction == '6':
            for ln in self.GB.LinesPropertiesX:
                if ln[1] == currY and ln[2] <= currX < ln[3]:
                    return ln[3]
            return 0

        if Direction == '8':
            for ln in self.GB.LinesPropertiesY:
                if ln[1] == currX and ln[2] < currY <= ln[3]:
                    return ln[2] - 3
            return 0

        if Direction == '5':
            for ln in self.GB.LinesPropertiesY:
                if ln[1] == currX and ln[2] <= currY < ln[3]:
                    return ln[3]
            return 0

    def isMoveIn(self, Direction, currX, currY):
        counter = 0
        currX = currX + 3
        currY = currY + 3

        if Direction == '4':
            for ln in self.GB.LinesPropertiesY:
                if ln[1] < currX and ln[2] <= currY <= ln[3]:
                    counter = counter + 1

        elif Direction == '6':
            for ln in self.GB.LinesPropertiesY:
                if ln[1] > currX and ln[2] <= currY <= ln[3]:
                    counter = counter + 1

        elif Direction == '8':
            for ln in self.GB.LinesPropertiesX:
                if ln[1] < currY and ln[2] <= currX <= ln[3]:
                    counter = counter + 1

        elif Direction == '5':
            for ln in self.GB.LinesPropertiesX:
                if ln[1] > currY and ln[2] <= currX <= ln[3]:
                    counter = counter + 1

        if counter % 2 == 0:
            return False
        else:
            return True

    def MovePlayer(self):
        tkLines = []
        tkFrames = []
        localAllPoints = []
        originalDirection = '0'
        localSize = 3
        startPoint = ()
        finishPoint = ()
        StopPoint = (0, False)
        self.isOutLine = False
        isFirstLine = True
        ExistingPoints = []
        AddedPoints = []

        localAllPoints = list(self.GB.AllPoints)

        while self.MovingDirection != '0':
            if self.stopPlayer:
                self.MovingDirection = '0'
                self.isOutLine = False
                self.PosX = self.WhitePoint[0] - 3
                self.PosY = self.WhitePoint[1] - 3
                self.GB.removeLive()
                self.Player.place(x=self.PosX, y=self.PosY)
                tkLines.clear()
                for frm in tkFrames:
                    frm.pack_forget()
                    frm.destroy()

                self.stopPlayer = False
                tkFrames.clear()

                for ln in self.GB.LinesPropertiesX:
                    if ln[4]:
                        self.GB.LinesPropertiesX.remove(ln)

                for ln in self.GB.LinesPropertiesY:
                    if ln[4]:
                        self.GB.LinesPropertiesY.remove(ln)

                return

            tempMovingTo = self.MovingDirection

            if originalDirection != tempMovingTo and self.isOutLine:
                if (originalDirection == '4' and tempMovingTo == '6') or (
                        originalDirection == '6' and tempMovingTo == '4'):
                    tempMovingTo = originalDirection

                if (originalDirection == '5' and tempMovingTo == '8') or (
                        originalDirection == '8' and tempMovingTo == '5'):
                    tempMovingTo = originalDirection

            if self.isSpacePressed and not self.isOutLine:
                if not self.isMoveOnLine(tempMovingTo, self.PosX, self.PosY):
                    self.isOutLine = self.isMoveIn(tempMovingTo, self.PosX, self.PosY)
                    if self.isOutLine:
                        self.WhitePoint = self.PosX + localSize, self.PosY + localSize

            if originalDirection != tempMovingTo and not self.isOutLine:
                nextEnablePoint = -1

            if originalDirection != tempMovingTo and self.isOutLine:
                tkWidth = 2
                tkHeight = 2
                StopPoint = (0, False)
                tkFrame = tk.Frame(self.GB.canvas, width=tkWidth, height=tkHeight, bg='#FFFFFF')
                tkFrame.place(x=self.PosX + localSize, y=self.PosY + localSize)
                tkFrames.append(tkFrame)

                t1 = (self.PosX + localSize, self.PosY + localSize, True)

                tkLines.append(t1)

                if t1 in localAllPoints:
                    ExistingPoints.append(t1)
                else:
                    localAllPoints.append(t1)

                AddedPoints.append(t1)

                if isFirstLine:
                    isFirstLine = False
                    startPoint = (self.PosX + localSize, self.PosY + localSize)
                else:
                    finishPoint = (self.PosX + localSize, self.PosY + localSize)

                    self.setLineProperties(originalDirection, startPoint, finishPoint)

                    startPoint = finishPoint
                    finishPoint = tuple()

                self.LastLineStartP = tuple(startPoint)
                originalDirection = tempMovingTo

            if tempMovingTo == '4':
                if not self.isOutLine:
                    if nextEnablePoint == -1:
                        nextEnablePoint = self.isMoveOnLine('4', self.PosX, self.PosY)
                else:
                    nextEnablePoint = -1

                if StopPoint[0] == 0 and self.isOutLine:
                    StopPoint = self.getStopPointX('4', self.PosX + localSize, self.PosY + localSize)

                if (self.PosX <= nextEnablePoint and not self.isOutLine) or nextEnablePoint == 0 or (
                        self.PosX <= StopPoint[0] and self.isOutLine):

                    if StopPoint[1]:
                        self.stopPlayer = True
                    else:
                        self.MovingDirection = '0'
                        break

                temp = round((self.PosX - self.PlayerSpeed) * 100)
                temp = int(temp)
                self.PosX = float(temp / 100)

                self.Player.place(x=self.PosX)

                if self.isOutLine:
                    tkWidth = tkWidth + self.PlayerSpeed
                    tkFrame.place(x=self.PosX + localSize, width=tkWidth)

            elif tempMovingTo == '6':

                if not self.isOutLine:
                    if nextEnablePoint == -1:
                        nextEnablePoint = self.isMoveOnLine('6', self.PosX, self.PosY)
                else:
                    nextEnablePoint = -1

                if StopPoint[0] == 0 and self.isOutLine:
                    StopPoint = self.getStopPointX('6', self.PosX + localSize, self.PosY + localSize)

                if (self.PosX >= nextEnablePoint and not self.isOutLine) or nextEnablePoint == 0 or (
                        self.PosX >= StopPoint[0] and self.isOutLine):
                    if StopPoint[1]:
                        self.stopPlayer = True
                    else:
                        self.MovingDirection = '0'
                        break

                temp = round((self.PosX + self.PlayerSpeed) * 100)
                temp = int(temp)
                self.PosX = float(temp / 100)

                self.Player.place(x=self.PosX)

                if self.isOutLine:
                    tkWidth = tkWidth + self.PlayerSpeed
                    tkFrame.place(width=tkWidth)

            elif tempMovingTo == '8':

                if not self.isOutLine:
                    if nextEnablePoint == -1:
                        nextEnablePoint = self.isMoveOnLine('8', self.PosX, self.PosY)
                else:
                    nextEnablePoint = -1

                if StopPoint[0] == 0 and self.isOutLine:
                    StopPoint = self.getStopPointY('8', self.PosY + localSize, self.PosX + localSize)

                if (self.PosY <= nextEnablePoint and not self.isOutLine) or nextEnablePoint == 0 or (
                        self.PosY <= StopPoint[0] and self.isOutLine):
                    if StopPoint[1]:
                        self.stopPlayer = True
                    else:
                        self.MovingDirection = '0'
                        break
                temp = round((self.PosY - self.PlayerSpeed) * 100)
                temp = int(temp)
                self.PosY = float(temp / 100)

                self.Player.place(y=self.PosY)

                if self.isOutLine:
                    tkHeight = tkHeight + self.PlayerSpeed
                    tkFrame.place(y=self.PosY + localSize, height=tkHeight)

            elif tempMovingTo == '5':
                if not self.isOutLine:
                    if nextEnablePoint == -1:
                        nextEnablePoint = self.isMoveOnLine('5', self.PosX, self.PosY)
                else:
                    nextEnablePoint = -1

                if StopPoint[0] == 0 and self.isOutLine:
                    StopPoint = self.getStopPointY('5', self.PosY + localSize, self.PosX + localSize)

                if (self.PosY >= nextEnablePoint and not self.isOutLine) or nextEnablePoint == 0 or (
                        self.PosY >= StopPoint[0] and self.isOutLine):
                    if StopPoint[1]:
                        self.stopPlayer = True
                    else:
                        self.MovingDirection = '0'
                        break

                temp = round((self.PosY + self.PlayerSpeed) * 100)
                temp = int(temp)
                self.PosY = float(temp / 100)

                self.Player.place(y=self.PosY)

                if self.isOutLine:
                    tkHeight = tkHeight + self.PlayerSpeed
                    tkFrame.place(height=tkHeight)

            finishPoint = (self.PosX + localSize, self.PosY + localSize)

        if len(finishPoint) > 0 and len(startPoint) > 0 and len(tkFrames) > 0:

            self.setLineProperties(originalDirection, startPoint, finishPoint)

            startPoint = finishPoint
            finishPoint = tuple()

            t1 = (self.PosX + localSize, self.PosY + localSize, True)
            tkLines.append(t1)

            if t1 in localAllPoints:
                ExistingPoints.append(t1)
            else:
                localAllPoints.append(t1)

            AddedPoints.append(t1)

            for frm in tkFrames:
                frm.pack_forget()
                frm.destroy()

            if len(tkLines) > 1:
                shapePoints = ()
                for point in tkLines:
                    shapePoints = shapePoints + point

                shapePoints = shapePoints + tkLines[0]

                self.GB.AllPoints = self.GB.Shp.MakeNewShapeRD(ExistingPoints, localAllPoints, AddedPoints)
                if self.GB.ShapeArea < 15000:
                    self.GB.NextLevel()
