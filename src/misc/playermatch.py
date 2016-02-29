__author__ = 'jamie'


class Player(object):

    name = None
    dartsThrown = None
    oneDartAverage = None
    currentScore = None

    def __init__(self, name):
        self.name = name
        self.dartsThrown = 0
        self.oneDartAverage = 0
        self.currentScore = 0

    def addToScore(self, scoreToAdd):
        self.currentScore += scoreToAdd