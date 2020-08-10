import craps.config

class Bet:
    name = None
    def __init__(self, player, amt):
        self.player = player
        self.table = player.table
        self.amt = amt
        self.status = None

    def __str__(self):
        return '{} has a {} bet of ${}.'.format(self.player.name, self.type, self.amt)

    def __repr__(self):
        return 'Bet({}, {}, ${})'.format(self.player.name, self.type, self.amt)


class Passline(Bet):
    type = 'passline'
    def __init__(self, player, amt):
        super().__init__(player, amt)
        if self.table.puck.state == 'on':
            raise PlaceBetError('Cannot make Passline bet if Puck is already on!')
        self.winnings = 2*amt

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
    def __init__(self, player, amt, number):
        super().__init__(player, amt)
        if self.table.puck.state == 'off':
            raise PlaceBetError('Cannot make odds bets when puck is off!')
        self.number = number
        self.type = 'odds' + str(self.number)
        self.winnings = amt * (6 / (6-abs(self.number - 7) ))


    def check(self):
        if self.table.dice.sum == self.number:
            self.status = 'win'

        elif self.table.dice.sum == 7:
            self.status = 'loss'

class Hardways(Bet):
    type = 'hardways'
    def __init__(self, player, amt, number):
        super().__init__(player, amt)
        self.number = number
        self.type = 'hard' + str(self.number)
        self.winnings = amt * (11 - abs(x-7))

    def check(self):
        if self.table.dice.sum == self.number and self.table.dice.dice1 == self.table.dice.dice2:
            self.status = 'win'

        elif self.table.dice.sum == self.number and self.table.dice.dice1 != self.table.dice.dice2:
            self.status = 'loss'

def getBet(str):
    for bet in Bet.__subclasses__():
        if bet.type == str:
            return bet


class PlaceBetError(Exception):
    def __init__(self, message):
        self.message = message
