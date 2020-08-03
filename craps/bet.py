class Bet:
    name = None
    def __init__(self, player, amt):
        self.player = player
        self.amt = amt

    def __str__(self):
        return '{} has a {} bet of ${}.'.format(self.player.name, self.type, self.amt)

    def __repr__(self):
        return 'Bet({}, {}, ${})'.format(self.player.name, self.type, self.amt)


class Passline(Bet):
    type = 'passline'
    def __init__(self, player, amt):
        if player.table.puck.state == 'on':
            raise PasslineError('Cannot make Passline bet if Puck is already on!')
        self.player = player
        self.amt = amt
        self.status = None
        self.winnings = 2*amt

    def check(self, table):
        if table.puck.state == 'off' and table.dice.sum in [7, 11]:
            self.status = 'win'

        elif table.puck.state == 'off' and table.dice.sum in [2, 3, 12]:
            self.status = 'loss'

        elif table.puck.state == 'on' and table.dice.sum == table.puck.point:
            self.status = 'win'

        elif table.puck.state == 'on' and table.dice.sum == 7:
            self.status = 'loss'

def getBet(str):
    for bet in Bet.__subclasses__():
        if bet.type == str:
            return bet



class Point(Bet):
    pass


class PasslineError(Exception):
    pass
