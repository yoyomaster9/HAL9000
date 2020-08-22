from discord.ext import commands
import config
from craps import game
import craps.config
import craps.bet
import pickle, os

class CrapsCog(commands.Cog):
    def __init__(self, bot):
        self.tables = {} # dict of tables, indexed by channel id
        if os.path.exists('tables.pickle'):
            with open('tables.pickle', 'rb') as file:
                self.tables = pickle.load(file)
        self.bot = bot
        self.saveTables()

    def update(self, ctx):
        if ctx.channel.id not in self.tables:
            raise Exception('No table created for channel {}'.format(ctx.channel.id))
        self.table = self.tables[ctx.channel.id]
        if ctx.author.name not in self.table.players:
            self.table.addPlayer(ctx.author.name)
        self.player = self.table.getPlayer(ctx.author.name)

    def saveTables(self):
        with open('tables.pickle', 'wb') as file:
            pickle.dump(self.tables, file)

    @commands.command()
    async def createTable(self, ctx):
        if ctx.channel.id in self.tables:
            await ctx.send('This channel already has a table!')
        else:
            self.tables[ctx.channel.id] = game.Table(ctx.channel.id)
            await ctx.send('Table created! Table bound to this channel.')
        self.saveTables()

    @commands.command()
    async def drop(self, ctx, amt):
        amt = int(amt)
        self.update(ctx)
        if amt > craps.config.MAXDROPSIZE:
            await ctx.send('You cannot drop more than ${:,}!'.format(craps.config.MAXDROPSIZE))
            return
        elif amt <= 0:
            await ctx.send('Invalid drop amout!')
            return
        self.player.bankroll += amt
        await ctx.send('{} now has ${:,}!'.format(self.player.name, self.player.bankroll))
        self.saveTables()

    @commands.command()
    async def walk(self, ctx):
        self.update(ctx)
        await ctx.send('{} left the table with ${:,}!'.format(self.player.name, self.player.bankroll))
        self.table.removePlayer(ctx.author.name)
        self.saveTables()

    @commands.command()
    async def bankroll(self, ctx):
        self.update(ctx)
        await ctx.send('{} has a bankroll of ${:,}!'.format(self.player.name, self.player.bankroll))

    @commands.command()
    async def roll(self, ctx):
        self.update(ctx)
        try:
            self.player.roll()
            msg = '{} rolled {}! '.format(ctx.author.name, self.table.dice)
            if self.table.puck.state == 'on':
                msg += 'The puck is on the {}.'.format(self.table.puck.point)
            elif self.table.puck.state == 'off':
                msg += 'The puck is off!'

            if [bet for bet in self.table.completedBets if bet.status == 'win'] != []:
                msg += '\nWe have some winners!\n```' + self.table.printBetsWon() + '```'

            if [bet for bet in self.table.completedBets if bet.status == 'loss'] != []:
                msg += '\nOh no! We have some losers!\n```' + self.table.printBetsLost() + '```'
            await ctx.send(msg)
        except game.ShooterError:
            await ctx.send('Wrong shooter! {} has the dice.'.format(self.table.shooter))
        self.saveTables()

    @commands.command()
    async def bet(self, ctx, *args):
        # *args will be tuple of all bets and wagers
        self.update(ctx)
        if len(args) % 2 != 0:
            raise Exception('Odd number of args!')
        l = [(args[i], args[i+1]) for i in range(0, len(args), 2)]
        for betType, wager in l:
            try:
                wager = int(wager)
                self.player.placeBet(betType, wager)
                await ctx.send('{} made a {} bet of ${}!'.format(self.player.name, betType, wager))
            except craps.bet.PlaceBetError as e:
                await ctx.send('Error! Bet cannot be placed.')
                await ctx.send(e.message)
        self.saveTables()

    @commands.command()
    async def bets(self, ctx):
        self.update(ctx)
        if self.table.bets == []:
            await ctx.send('There are no bets placed!')
        else:
            msg = '```\n' + self.table.printBets() + '\n```'
            await ctx.send(msg)

    @commands.command()
    async def puck(self, ctx):
        self.update(ctx)
        if self.table.puck.state == 'off':
            await ctx.send('The puck is off!')
        elif self.table.puck.state == 'on':
            await ctx.send('The puck is on {}!'.format(self.table.puck.point))

    @commands.command()
    async def players(self, ctx):
        self.update(ctx)
        if self.table.players != {}:
            await ctx.send('Here are the current players!')
            for name in self.table.players:
                player = self.table.getPlayer(name)
                await ctx.send('{}, Bankroll: ${:,}'.format(player, player.bankroll))
        else:
            await ctx.send('No players have joined the table!')

    @commands.command()
    async def clearShooter(self, ctx):
        self.update(ctx)
        self.table.shooter = None
        await ctx.send('Shooter cleared! Anyone can roll!')
        self.saveTables()

    @commands.command()
    async def resetTable(self, ctx):
        self.update(ctx)
        self.table.resetTable()
        await ctx.send('Resetting table!')
        self.saveTables()
