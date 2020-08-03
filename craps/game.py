import random
from craps import config
from craps import bet

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
        self.point = None
        self.state = 'off'

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
        self.players[userID].table = self

    def removePlayer(self, userID):
        for bet in self.getPlayer(userID).bets:
            self.bets.remove(bet)
        del self.players[userID]

    def roll(self, player):
        if self.shooter == None:
            self.shooter = player
        elif player != self.shooter:
            raise ShooterError('Wrong player rolling!')

        self.dice.roll()
        self.checkBets()

        if self.puck.state == 'off' and self.dice.sum in [4, 5, 6, 8, 9, 10]:
            self.puck.state = 'on'
            self.puck.point = self.dice.sum

        elif self.puck.state == 'on' and self.dice.sum in [7, self.puck.point]:
            self.puck.state = 'off'
            self.puck.point = None
            self.shooter = None

    def checkBets(self):
        for bet in self.bets:
            bet.check(self)
            if bet.status == 'win':
                bet.player.bankroll += bet.winnings
                self.bets.remove(bet)
            elif bet.status == 'loss':
                self.bets.remove(bet)

    def makeBet(self, player, bet, amt):
        b = bet(player, bet, amt)
        player.bets.append(b)
        table.bets.append(b)



class ShooterError(Exception):
    pass

table = Table()
