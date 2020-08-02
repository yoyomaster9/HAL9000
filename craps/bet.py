class Bet:
    def __init__(self, player, amt):
        self.player = player
        self.amt = amt

    def sevenOut(self):
        # some bets will have this included
        pass

class Passline(Bet):
    def __init__(self, player, amt):
        # if puck.state == 'on':
        #     raise PasslineError('Cannot make Passline bet if Puck is already on!')
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




class Point(Bet):
    pass


class PasslineError(Exception):
    pass
