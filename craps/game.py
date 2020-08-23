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
        self.bets = {}

    def __repr__(self):
        return 'Player({})'.format(self.name)

    def roll(self):
        self.table.roll(self)

    def placeBet(self, betType, wager):

        wager = int(wager)
        if wager <= 0:
            raise Exception('Cannot place bets with negative amounts!')

        if self.bankroll < wager:
            raise bet.PlaceBetError('Bet too high! {}\'s bankroll is only ${}'.format(self.name, int(self.bankroll)))

        if betType in ['hard4', 'hard6', 'hard8', 'hard10']:
            betType, arg = betType[:4] + 'ways', int(betType[4:])
            b = bet.getBet(betType)(self, wager, arg)

        else:
            b = bet.getBet(betType)(self, wager)

        self.bankroll -= wager
        if b.type in self.bets:
            self.bets[b.type].wager += b.wager
        else:
            self.bets[b.type] = b

    def removeBet(self, betType):
        del self.bets[betType]

    def printBets(self):
        l = [[self.name, bet.type.title(), '$' + str(bet.wager)] for bet in self.bets.values()]
        l.insert(0, ['Player', 'Bet', 'Amount'])
        return util.col(l)

class Table:
    def __init__(self, channelID):
        self.channelID = channelID
        self.dice = Dice()
        self.puck = Puck()
        self.minBet = config.MINBET
        self.shooter = None
        self.players = {} # will be dict of players name:player(name)

    def bets(self):
        for player in self.players.values():
            return [bet for bet in player.bets.values()]

    def getPlayer(self, name): # returns player if exists, creates new otherwise
        if name not in self.players:
            raise PlayerNotFound('Player does not exist in table')
        else:
            return self.players[name]

    def addPlayer(self, name):
        if name in self.players:
            raise Exception('Player already exists!')
        self.players[name] = Player(name)
        self.players[name].table = self

    def removePlayer(self, name):
        if self.shooter == self.players[name]:
            self.shooter = None
        del self.players[name]

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
        for bet in self.bets():
            bet.check()
            if bet.status == 'win':
                bet.player.bankroll += bet.wager + bet.winnings
                self.completedBets.append(bet)
            elif bet.status == 'loss':
                self.completedBets.append(bet)

        for bet in self.completedBets:
            self.removeBet(bet)

    def removeBet(self, bet):
        del bet.player.bets[bet.type]

    def resetTable(self):
        self.__init__(self.channelID)

    def printBets(self):
        l = [[bet.player.name, bet.type.title(), '$' + str(bet.wager)] for bet in self.bets()]
        l.insert(0, ['Player', 'Bet', 'Wagered'])
        return util.col(l)

    def printBetsWon(self):
        l = [[bet.player.name, bet.type.title(), '$' + str(bet.wager), '$' + str(bet.winnings)] for bet in self.completedBets if bet.status == 'win']
        l.insert(0, ['Player', 'Bet', 'Wagered', 'Winnings'])
        return util.col(l)

    def printBetsLost(self):
        l = [[bet.player.name, bet.type.title(), '$' + str(bet.wager)] for bet in self.completedBets if bet.status == 'loss']
        l.insert(0, ['Player', 'Bet', 'Wagered'])
        return util.col(l)

    def printPlayers(self):
        l = [[player.name, '$' + str(player.bankroll)] for player in self.players.values()]
        l.insert(0, ['Player', 'Bankroll'])
        return util.col(l)





class PlayerNotFound(Exception):
    pass

class ShooterError(Exception):
    pass
