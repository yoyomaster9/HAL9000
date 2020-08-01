import random
from craps import config

class Dice:
    def __init__(self):
        self.dice = (0, 0)
        self.sum = 0
    def roll(self):
        self.dice = (random.randint(1, 6), random.randint(1, 6))
        self.sum = sum(self.dice)
        return self.dice
    def __str__(self):
        return str(self.dice)
    def __repr__(self):
        return str(self.dice)
    def __eq__(self, other):
        return self.dice == other


class Puck:
    def __init__(self):
        self.point = 0
        # point can be {0, 4, 5, 6, 8, 9, 10}
        self.status = 'off'

        # Future rewrite - might not need self.status

class Player:
    def __init__(self, userID):
        self.userID = userID
        self.bankroll = 0
        self.bets = []


class Table:
    def __init__(self):
        self.dice = Dice()
        self.puck = Puck()
        self.minBet = config.MINBET
        self.shooter = None
        self.players = {} # will be dict of players userID:player(userID)
        self.bets = []

    def getPlayer(self, userID): # returns player if exists, creates new otherwise
        if userID not in self.players:
            self.addPlayer(userID)
        return self.players[userID]

    def addPlayer(self, userID):
        self.players[userID] = Player(userID)

    def removePlayer(self, userID):
        for bet in self.getPlayer(userID).bets:
            self.bets.remove(bet)
        del self.players[userID]

    def checkBets(self):
        for bet in self.bets:
            check = bet.check(self)
            if check == 'win':
                bet.player.bankroll += bet.winnings + bet.amt # give player original bet with winnings
                self.bets.remove(bet)
            elif check == 'loss':
                self.bets.remove(bet)

class Bet:
    def __init__(self, userID, checkfunction):
        self.userID = userID
        self.checkfunction = checkfunction
        self.payout = 0 # Maybe turn into function??

    def checkState(self, table):
        # will import table, and determine if the bet
        # is won, lost, or diesn't change
        self.checkfunction(table)
        # check funciton will return Win, Loss, or None




table = Table()
