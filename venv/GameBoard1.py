import ast
import json as json
import threading
import tkinter as tk
from tkinter import messagebox
from typing import Type

import requests
from PIL import Image, ImageTk
from Pixel import Pixel


class GameBoard:
    AllPoints = []
    PlayerCenter = ()
    size = 25, 25
    PosX = 3
    PosY = 3
    MovingDirection = '0'
    isSpacePressed = False
    AllowedFrames = []
    isOutLine = False
    LinesProperties = []
    FullShapeLines = ()
    localMaxMove = 608
    localMinMove = 3

    def MakeNewShape(self):
        stop = False
        newShape = []

        tempPoints = list(self.AllPoints)
        checkHorizontal = True
        counter = 0
        isFound = False
        firstX = 700
        firstY = 700

        currP = (firstX, firstY)

        # # find corner point
        # for p in tempPoints:
        #     if p[0] <= currP[0]:
        #         if p[1] <= currP[1]:
        #             currP = p

        currP = tempPoints[-1]

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

            if len(tempPoints) == 0:
                counter = 0
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

        self.AllPoints = list(newShape)
        newShape.append(newShape[0])
        self.canvas.delete(self.MainLn)
        self.MainLn = self.canvas.create_polygon(newShape, fill='grey', width=1)

    def getStopPointX(self, direction, startX, Y):
        if direction == '4':
            result = 0
            for ln in self.LinesProperties:
                if ln[0] == 'y':
                    if result < ln[1] < startX and (ln[2] < Y < ln[3] or ln[3] < Y < ln[2]):
                        result = ln[1] - 3
            return result

        elif direction == '6':
            result = 700
            for ln in self.LinesProperties:
                if ln[0] == 'y':
                    if result > ln[1] > startX and (ln[2] < Y < ln[3] or ln[3] < Y < ln[2]):
                        result = ln[1] - 3
            return result

    def getStopPointY(self, direction, startY, X):
        if direction == '8':
            result = 0
            for ln in self.LinesProperties:
                if ln[0] == 'x':
                    if result < ln[1] < startY and (ln[2] < X < ln[3] or ln[3] < X < ln[2]):
                        result = ln[1] - 3
            return result

        elif direction == '5':
            result = 700
            for ln in self.LinesProperties:
                if ln[0] == 'x':
                    if result > ln[1] > startY and (ln[2] < X < ln[3] or ln[3] < X < ln[2]):
                        result = ln[1] - 3
            return result

    def setLineProperties(self, OrgDirection, startP, finishP):

        if OrgDirection == '4':
            self.LinesProperties.append(('x', startP[1], finishP[0], startP[0]))
        elif OrgDirection == '6':
            self.LinesProperties.append(('x', startP[1], startP[0], finishP[0]))
        elif OrgDirection == '8':
            self.LinesProperties.append(('y', startP[0], finishP[1], startP[1]))
        elif OrgDirection == '5':
            self.LinesProperties.append(('y', startP[0], startP[1], finishP[1]))

    def isMoveOnLine(self, Direction, currX, currY):
        currX = currX + 3
        currY = currY + 3

        if Direction == '4':
            for ln in self.LinesProperties:
                if ln[0] == 'x':
                    if ln[1] == currY and ln[2] < currX <= ln[3]:
                        return ln[2] - 3
            return 0

        if Direction == '6':
            for ln in self.LinesProperties:
                if ln[0] == 'x':
                    if ln[1] == currY and ln[2] <= currX < ln[3]:
                        return ln[3]
            return 0

        if Direction == '8':
            for ln in self.LinesProperties:
                if ln[0] == 'y':
                    if ln[1] == currX and ln[2] < currY <= ln[3]:
                        return ln[2] - 3
            return 0

        if Direction == '5':
            for ln in self.LinesProperties:
                if ln[0] == 'y':
                    if ln[1] == currX and ln[2] <= currY < ln[3]:
                        return ln[3]
            return 0

    def isMoveIn(self, Direction, currX, currY):
        counter = 0
        currX = currX + 3
        currY = currY + 3

        if Direction == '4':
            for ln in self.LinesProperties:
                if ln[0] == 'y':
                    if ln[1] < currX and ln[2] <= currY <= ln[3]:
                        counter = counter + 1

        elif Direction == '6':
            for ln in self.LinesProperties:
                if ln[0] == 'y':
                    if ln[1] > currX and ln[2] <= currY <= ln[3]:
                        counter = counter + 1

        elif Direction == '8':
            for ln in self.LinesProperties:
                if ln[0] == 'x':
                    if ln[1] < currY and ln[2] <= currX <= ln[3]:
                        counter = counter + 1

        elif Direction == '5':
            for ln in self.LinesProperties:
                if ln[0] == 'x':
                    if ln[1] > currY and ln[2] <= currX <= ln[3]:
                        counter = counter + 1

        if counter % 2 == 0:
            return False
        else:
            return True

    def MovePlayer(self):
        tkLines = []
        tkFrames = []
        originalDirection = '0'
        localSize = 3
        startPoint = ()
        finishPoint = ()
        StopPoint = 0
        self.isOutLine = False
        isFirstLine = True

        while self.MovingDirection != '0':

            tempMovingTo = self.MovingDirection

            if self.isSpacePressed and not self.isOutLine:
                if not self.isMoveOnLine(tempMovingTo, self.PosX, self.PosY):
                    self.isOutLine = self.isMoveIn(tempMovingTo, self.PosX, self.PosY)

            if originalDirection != tempMovingTo and not self.isOutLine:
                nextEnablePoint = -1

            if originalDirection != tempMovingTo and self.isOutLine:
                tkWidth = 2
                tkHeight = 2
                StopPoint = 0
                tkFrame = tk.Frame(self.canvas, width=tkWidth, height=tkHeight, bg='#FFFFFF')
                tkFrame.place(x=self.PosX + localSize, y=self.PosY + localSize)
                tkFrames.append(tkFrame)

                t1 = (self.PosX + localSize, self.PosY + localSize)
                tkLines.append(t1)
                if t1 in self.AllPoints:
                    self.AllPoints.remove(t1)
                else:
                    self.AllPoints.append(t1)

                if isFirstLine:
                    isFirstLine = False
                    startPoint = (self.PosX + localSize, self.PosY + localSize)
                else:
                    finishPoint = (self.PosX + localSize, self.PosY + localSize)

                    self.setLineProperties(originalDirection, startPoint, finishPoint)

                    startPoint = finishPoint
                    finishPoint = tuple()

                originalDirection = tempMovingTo

            if tempMovingTo == '4':
                if not self.isOutLine:
                    if nextEnablePoint == -1:
                        nextEnablePoint = self.isMoveOnLine('4', self.PosX, self.PosY)
                else:
                    nextEnablePoint = -1

                if StopPoint == 0 and self.isOutLine:
                    StopPoint = self.getStopPointX('4', self.PosX + localSize, self.PosY + localSize)

                if (self.PosX <= nextEnablePoint and not self.isOutLine) or nextEnablePoint == 0 or (
                        self.PosX <= StopPoint and self.isOutLine):
                    self.MovingDirection = '0'
                    break

                temp = round((self.PosX - 0.01) * 100)
                temp = int(temp)
                self.PosX = float(temp / 100)

                self.Player.place(x=self.PosX)

                if self.isOutLine:
                    tkWidth = tkWidth + 0.01
                    tkFrame.place(x=self.PosX + localSize, width=tkWidth)

            elif tempMovingTo == '6':

                if not self.isOutLine:
                    if nextEnablePoint == -1:
                        nextEnablePoint = self.isMoveOnLine('6', self.PosX, self.PosY)
                else:
                    nextEnablePoint = -1

                if StopPoint == 0 and self.isOutLine:
                    StopPoint = self.getStopPointX('6', self.PosX + localSize, self.PosY + localSize)

                if (self.PosX >= nextEnablePoint and not self.isOutLine) or nextEnablePoint == 0 or (
                        self.PosX >= StopPoint and self.isOutLine):
                    self.MovingDirection = '0'
                    break

                temp = round((self.PosX + 0.01) * 100)
                temp = int(temp)
                self.PosX = float(temp / 100)

                self.Player.place(x=self.PosX)

                if self.isOutLine:
                    tkWidth = tkWidth + 0.01
                    tkFrame.place(width=tkWidth)

            elif tempMovingTo == '8':

                if not self.isOutLine:
                    if nextEnablePoint == -1:
                        nextEnablePoint = self.isMoveOnLine('8', self.PosX, self.PosY)
                else:
                    nextEnablePoint = -1

                if StopPoint == 0 and self.isOutLine:
                    StopPoint = self.getStopPointY('8', self.PosY + localSize, self.PosX + localSize)

                if (self.PosY <= nextEnablePoint and not self.isOutLine) or nextEnablePoint == 0 or (
                        self.PosY <= StopPoint and self.isOutLine):
                    self.MovingDirection = '0'
                    break
                temp = round((self.PosY - 0.01) * 100)
                temp = int(temp)
                self.PosY = float(temp / 100)

                self.Player.place(y=self.PosY)

                if self.isOutLine:
                    tkHeight = tkHeight + 0.01
                    tkFrame.place(y=self.PosY + localSize, height=tkHeight)

            elif tempMovingTo == '5':
                if not self.isOutLine:
                    if nextEnablePoint == -1:
                        nextEnablePoint = self.isMoveOnLine('5', self.PosX, self.PosY)
                else:
                    nextEnablePoint = -1

                if StopPoint == 0 and self.isOutLine:
                    StopPoint = self.getStopPointY('5', self.PosY + localSize, self.PosX + localSize)

                if (self.PosY >= nextEnablePoint and not self.isOutLine) or nextEnablePoint == 0 or (
                        self.PosY >= StopPoint and self.isOutLine):
                    self.MovingDirection = '0'
                    break

                temp = round((self.PosY + 0.01) * 100)
                temp = int(temp)
                self.PosY = float(temp / 100)

                self.Player.place(y=self.PosY)

                if self.isOutLine:
                    tkHeight = tkHeight + 0.01
                    tkFrame.place(height=tkHeight)

            finishPoint = (self.PosX + localSize, self.PosY + localSize)

        if len(finishPoint) > 0 and len(startPoint) > 0:

            self.setLineProperties(originalDirection, startPoint, finishPoint)

            startPoint = finishPoint
            finishPoint = tuple()

            t1 = (self.PosX + localSize, self.PosY + localSize)
            tkLines.append(t1)
            if t1 in self.AllPoints:
                self.AllPoints.remove(t1)
            else:
                self.AllPoints.append(t1)

            for frm in tkFrames:
                frm.pack_forget()
                frm.destroy()

            if len(tkLines) > 1:
                shapePoints = ()
                for point in tkLines:
                    shapePoints = shapePoints + point

                shapePoints = shapePoints + tkLines[0]

                self.MakeNewShape()

    def __init__(self, root):

        canvasWidth = 610
        canvasHeight = 610

        def setSpaceClick(event):
            self.isSpacePressed = True

        def MovePlayerThread(event):
            if event.char in ('4', '5', '6', '8'):
                if event.char == self.MovingDirection:
                    return
                else:
                    if self.MovingDirection != '0':
                        self.MovingDirection = event.char
                        return

                self.MovingDirection = event.char
                thread1 = threading.Thread(target=self.MovePlayer)
                thread1.start()

        def stopMovement(event):
            if self.MovingDirection == event.char and not self.isOutLine:
                self.MovingDirection = '0'

            if event.keycode == 32:
                self.isSpacePressed = False

        self.root = root
        self.root.title = 'Submarine War'

        self.canvas = tk.Canvas(self.root, width=canvasWidth, height=canvasHeight)
        self.canvas.bind("<Key>", MovePlayerThread)
        self.canvas.bind("<KeyRelease>", stopMovement)
        self.canvas.bind("<space>", setSpaceClick)
        self.canvas.pack()

        filename = 'PIC.JPG'
        img = tk.PhotoImage(file=r"Graphics/picpic.gif")
        self.canvas.create_image(img.width()/2, img.height()/2, image=img)

        self.MainLn = self.canvas.create_polygon(6, 6, 608, 6, 608, 608, 6, 608, 6, 6, fill='grey', width=1)

        self.LinesProperties.append(('y', 6, 6, 608))
        self.LinesProperties.append(('y', 608, 6, 608))
        self.LinesProperties.append(('x', 6, 6, 608))
        self.LinesProperties.append(('x', 608, 6, 608))

        p = (6, 6)
        self.AllPoints.append(p)
        p = (6, 608)
        self.AllPoints.append(p)
        p = (608, 608)
        self.AllPoints.append(p)
        p = (608, 6)
        self.AllPoints.append(p)

        self.MakeNewShape()

        self.Player = tk.Frame(self.canvas, bg='#FF0000')
        self.Player.place(width=8, height=8, x=3, y=3)

        self.canvas.focus_set()
        self.root.mainloop()
