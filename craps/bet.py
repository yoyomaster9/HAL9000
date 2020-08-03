class Bet:
    name = None
    def __init__(self, player, amt):
        self.player = player
        self.amt = amt

class Passline(Bet):
    name = 'Passline'
    def __init__(self, player, amt):
        if player.table.puck.state == 'on':
            raise PasslineError('Cannot make Passline bet if Puck is already on!')
        self.player = player
        self.amt = amt
        self.status = None
        self.winnings = 2*amt

    def check(self, table):
        if puck.state == 'off' and table.dice.sum in [7, 11]:
            self.status = 'win'

        elif puck.state == 'on' and table.dice.sum == table.puck.point:
            self.status = 'win'

        elif puck.state == 'on' and table.dice.sum == 7:
            self.status = 'loss'

def getBetClass(str):
    for betClass in Bet.__subclassses__():
        if betClass.name == str:
            return betClass



class Point(Bet):
    pass


class PasslineError(Exception):
    pass
