import threading


class Enemy:
    EnemyX = 300
    EnemyY = 100
    stopMovement = False

    def __init__(self, frmEnemy, gb):
        self.EnemyV = frmEnemy
        self.EnemyV.place(width=16, height=16, x=self.EnemyX, y=self.EnemyY)
        self.GB = gb
        self.EnemySpeed = 0.02 + (self.GB.Lvl / 100)
        print(self.EnemySpeed)
        thread2 = threading.Thread(target=self.EnemyMove)
        thread2.start()

    def EnemyMove(self):

        EnemyDirection = 1

        while self.GB.Lives > 0 and not self.stopMovement:

            isHit = False
            if self.GB.Plr.isOutLine:

                LastLn = tuple(self.GB.Plr.getLastWhiteLine())
                if LastLn[0] != 'Finish':
                    if LastLn[0] == 'y':
                        if self.EnemyX + 7.7 < LastLn[1] < self.EnemyX + 8.3:
                            if LastLn[2] < self.EnemyY + 8 < LastLn[3]:
                                isHit = True
                                self.strike()
                    else:
                        if self.EnemyY + 7.7 < LastLn[1] < self.EnemyY + 8.3:
                            if LastLn[2] < self.EnemyX + 8 < LastLn[3]:
                                isHit = True
                                self.strike()

            if not isHit:
                for ln in self.GB.LinesPropertiesY:
                    if self.EnemyX + 7.7 < ln[1] < self.EnemyX + 8.3:
                        if ln[2] < self.EnemyY + 8 < ln[3]:
                            isHit = True

                            if not ln[4]:
                                if EnemyDirection == 1:
                                    EnemyDirection = 4
                                elif EnemyDirection == 2:
                                    EnemyDirection = 3
                                elif EnemyDirection == 3:
                                    EnemyDirection = 2
                                elif EnemyDirection == 4:
                                    EnemyDirection = 1
                                break
                            else:
                                self.strike()

            if not isHit:
                for ln in self.GB.LinesPropertiesX:
                    if self.EnemyY + 7.7 < ln[1] < self.EnemyY + 8.3:
                        if ln[2] < self.EnemyX + 8 < ln[3]:
                            if not ln[4]:
                                if EnemyDirection == 1:
                                    EnemyDirection = 2
                                elif EnemyDirection == 2:
                                    EnemyDirection = 1
                                elif EnemyDirection == 3:
                                    EnemyDirection = 4
                                elif EnemyDirection == 4:
                                    EnemyDirection = 3
                                break
                            else:
                                self.strike()

            self.EnemyV.place(x=self.EnemyX, y=self.EnemyY)

            if EnemyDirection in (1, 2):
                self.EnemyX = self.EnemyX + self.EnemySpeed
            else:
                self.EnemyX = self.EnemyX - self.EnemySpeed

            if EnemyDirection in (1, 4):
                self.EnemyY = self.EnemyY + self.EnemySpeed
            else:
                self.EnemyY = self.EnemyY - self.EnemySpeed

    def strike(self):
        # set lives -1

        # back to start point on firs white

        self.GB.Plr.stopPlayer = True

        # delete All WhiteLines in LinesProperties
        for ln in self.GB.LinesPropertiesX:
            if ln[4]:
                self.GB.LinesPropertiesX.remove(ln)

        for ln in self.GB.LinesPropertiesY:
            if ln[4]:
                self.GB.LinesPropertiesY.remove(ln)
