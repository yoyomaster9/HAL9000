import craps.config

class Bet:
    type = None
    def __init__(self, player, wager):
        self.player = player
        self.table = player.table
        self.wager = int(wager)
        self.status = None

    def __str__(self):
        return '{} has a {} bet of ${}.'.format(self.player.name, self.type, self.wager)

    def __repr__(self):
        return 'Bet({}, {}, ${})'.format(self.player.name, self.type, self.wager)


class Pass(Bet):
    type = 'pass'
    def __init__(self, player, wager):
        super().__init__(player, wager)
        if self.table.puck.state == 'on':
            raise PlaceBetError('Cannot make Pass bet if Puck is already on!')
        self.winnings = self.wager

    def check(self):
        if self.table.puck.state == 'off' and self.table.dice.sum in [7, 11]:
            self.status = 'win'

        elif self.table.puck.state == 'off' and self.table.dice.sum in [2, 3, 12]:
            self.status = 'loss'

        elif self.table.puck.state == 'on' and self.table.dice.sum == self.table.puck.point:
            self.status = 'win'

        elif self.table.puck.state == 'on' and self.table.dice.sum == 7:
            self.status = 'loss'


class Odds(Bet):
    type = 'odds'
    def __init__(self, player, wager):
        super().__init__(player, wager)
        if self.table.puck.state == 'off':
            raise PlaceBetError('Cannot make odds bets when puck is off!')
        if [bet for bet in self.player.bets if bet.type == 'passline'] == []:
            raise PlaceBetError('Cannot make odds bet without pass bet!')
        self.winnings = int(self.wager * (6 / (6-abs(self.table.puck.point - 7) )))

    def check(self):
        if self.table.dice.sum == self.table.puck.point:
            self.status = 'win'

        elif self.table.dice.sum == 7:
            self.status = 'loss'

class Hardways(Bet):
    type = 'hardways'
    def __init__(self, player, wager, number):
        super().__init__(player, wager)
        self.number = number
        self.type = 'hard' + str(self.number)
        self.winnings = int(self.wager * (11 - abs(self.number-7)) - self.wager)

    def check(self):
        if self.table.dice.sum == self.number and self.table.dice.dice[0] == self.table.dice.dice[1]:
            self.status = 'win'

        elif self.table.dice.sum == self.number and self.table.dice.dice[0] != self.table.dice.dice[1]:
            self.status = 'loss'

        elif self.table.dice.sum == 7:
            self.status = 'loss'

class Field(Bet):
    type = 'field'
    def __init__(self, player, wager):
        super().__init__(player, wager)

    def check(self):
        if self.table.dice.sum in [2, 12]:
            self.winnings = self.wager * 3
            self.status = 'win'

        elif self.table.dice.sum in [3, 4, 9, 10, 11]:
            self.winnings = self.wager
            self.status = 'win'

        elif self.table.dice.sum in [5, 6, 7, 8]:
            self.winnings = 0
            self.status = 'loss'

def getBet(str):
    for bet in Bet.__subclasses__():
        if bet.type == str:
            return bet


class PlaceBetError(Exception):
    def __init__(self, message):
        self.message = message
