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
    def __init__(self, username):
        self.username = username
        self.bankroll = 0
        self.bets = []

    def __repr__(self):
        return self.username

class Table:
    def __init__(self):
        self.dice = Dice()
        self.puck = Puck()
        self.minBet = config.MINBET
        self.shooter = None
        self.players = {} # will be dict of players username:player(username)
        self.bets = []

    def getPlayer(self, username): # returns player if exists, creates new otherwise
        if username not in self.players:
            self.addPlayer(username)
        return self.players[username]

    def addPlayer(self, username):
        self.players[username] = Player(username)
        self.players[username].table = self

    def removePlayer(self, username):
        for bet in self.getPlayer(username).bets:
            self.bets.remove(bet)
        del self.players[username]

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
            bet.check(self)
            if bet.status == 'win':
                bet.player.bankroll += bet.winnings
                self.completedBets.append(bet)
            elif bet.status == 'loss':
                self.completedBets.append(bet)

        for bet in self.completedBets:
            self.removeBet(bet)


    def makeBet(self, player, bet, amt):
        if player.bankroll > amt:
            b = bet(player, amt)
            player.bankroll -= amt
            player.bets.append(b)
            table.bets.append(b)

    def removeBet(self, bet):
        bet.player.bets.remove(bet)
        self.bets.remove(bet)



class ShooterError(Exception):
    pass

table = Table()
