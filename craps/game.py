import random
from craps import config, bet, util

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
    def __init__(self, name):
        self.name = name
        self.bankroll = 0
        self.bets = []

    def __repr__(self):
        return self.name

    def roll(self):
        self.table.roll(self)

    def placeBet(self, betType, amt):

        if self.bankroll < amt:
            raise bet.PlaceBetError('Bet too high! {}\'s bankroll is only ${:2f}'.format(self.name, self.bankroll))

        if betType in ['hard4', 'hard6', 'hard8', 'hard10']:
            betType, arg = betType[:4] + 'ways', int(betType[4:])
            b = bet.getBet(betType)(self, amt, arg)

        else:
            b = bet.getBet(betType)(self, amt)

        self.bankroll -= amt
        self.bets.append(b)
        self.table.bets.append(b)

    def printBets(self):
        l = [[bet.player.name.title(), bet.type.title(), '$' + str(bet.amt)] for bet in self.bets]
        l.insert(0, ['Player', 'Bet', 'Amount'])
        return util.col(l)


class Table:
    def __init__(self):
        self.dice = Dice()
        self.puck = Puck()
        self.minBet = config.MINBET
        self.shooter = None
        self.players = {} # will be dict of players name:player(name)
        self.bets = []

    def getPlayer(self, name): # returns player if exists, creates new otherwise
        if name not in self.players:
            raise PlayerNotFound('Player does not exist in table')
        else:
            return self.players[name]

    def addPlayer(self, name):
        self.players[name] = Player(name)
        self.players[name].table = self

    def removePlayer(self, name):
        for bet in self.getPlayer(name).bets:
            self.bets.remove(bet)
        del self.players[name]
        if self.shooter.name == name:
            self.shooter = None

    def roll(self, player):
        self.completedBets = [] # completedBets will be list of bets that won/lost
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
            bet.check()
            if bet.status == 'win':
                bet.player.bankroll += bet.amt + bet.winnings
                self.completedBets.append(bet)
            elif bet.status == 'loss':
                self.completedBets.append(bet)

        for bet in self.completedBets:
            self.removeBet(bet)

    def removeBet(self, bet):
        bet.player.bets.remove(bet)
        self.bets.remove(bet)

    def resetTable(self):
        self.__init__()

    def printBets(self):
        l = [[bet.player.name.title(), bet.type.title(), '$' + str(bet.amt)] for bet in self.bets]
        l.insert(0, ['Player', 'Bet', 'Wagered'])
        return util.col(l)

    def printBetsWon(self):
        l = [[bet.player.name.title(), bet.type.title(), '$' + str(bet.amt), '$' + str(bet.winnings)] for bet in self.completedBets if bet.status == 'win']
        l.insert(0, ['Player', 'Bet', 'Wagered', 'Winnings'])
        return util.col(l)

    def printBetsLost(self):
        l = [[bet.player.name.title(), bet.type.title(), '$' + str(bet.amt)] for bet in self.completedBets if bet.status == 'loss']
        l.insert(0, ['Player', 'Bet', 'Wagered'])
        return util.col(l)

class PlayerNotFound(Exception):
    pass

class ShooterError(Exception):
    pass

table = Table()
