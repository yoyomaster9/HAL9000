from discord.ext import commands
import config
from craps import game
import craps.config
import craps.bet

class CrapsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def drop(self, ctx, amt):
        if ctx.author.name not in game.table.players:
            game.table.addPlayer(ctx.author.name)
        amt = int(amt)
        player = game.table.getPlayer(ctx.author.name)

        if amt > craps.config.MAXDROPSIZE:
            await ctx.send('You cannot drop more than ${:,}!'.format(craps.config.MAXDROPSIZE))
            return
        elif amt <= 0:
            await ctx.send('Invalid drop amout!')
            return
        player.bankroll += amt

        await ctx.send('{} now has ${:,}!'.format(player.name, player.bankroll))

    @commands.command()
    async def walk(self, ctx):
        if ctx.author.name not in game.table.players:
            game.table.addPlayer(ctx.author.name)
        player = game.table.getPlayer(ctx.author.name)
        await ctx.send('{} left the table with ${:,}!'.format(player.name, player.bankroll))
        game.table.removePlayer(ctx.author.name)

    @commands.command()
    async def bankroll(self, ctx):
        if ctx.author.name not in game.table.players:
            game.table.addPlayer(ctx.author.name)
        player = game.table.getPlayer(ctx.author.name)
        await ctx.send('{} has a bankroll of ${:,}!'.format(player.name, player.bankroll))


    @commands.command()
    async def roll(self, ctx):
        if ctx.author.name not in game.table.players:
            game.table.addPlayer(ctx.author.name)
        player = game.table.getPlayer(ctx.author.name)
        try:
            player.roll()
            msg = '{} rolled {}! '.format(ctx.author.name, game.table.dice)
            if game.table.puck.state == 'on':
                msg += 'The puck is on the {}.'.format(game.table.puck.point)
            elif game.table.puck.state == 'off':
                msg += 'The puck is off!'

            if [bet for bet in game.table.completedBets if bet.status == 'win'] != []:
                msg += '\nWe have some winners!\n```' + game.table.printBetsWon() + '```'

            if [bet for bet in game.table.completedBets if bet.status == 'loss'] != []:
                msg += '\nOh no! We have some losers!\n```' + game.table.printBetsLost() + '```'

            await ctx.send(msg)


        except game.ShooterError:
            await ctx.send('Wrong shooter! {} has the dice.'.format(game.table.shooter))

    @commands.command()
    async def bet(self, ctx, betType, wager):
        if ctx.author.name not in game.table.players:
            game.table.addPlayer(ctx.author.name)
        try:
            wager = int(wager)
            player = game.table.getPlayer(ctx.author.name)
            player.placeBet(betType, wager)
            await ctx.send('{} made a {} bet of ${}!'.format(player.name, betType, wager))

        except craps.bet.PlaceBetError as e:
            await ctx.send('Error! Bet cannot be placed.')
            await ctx.send(e.message)

    @commands.command()
    async def bets(self, ctx):
        msg = '```\n' + game.table.printBets() + '\n```'
        await ctx.send(msg)

    @commands.command()
    async def puck(self, ctx):
        if game.table.puck.state == 'off':
            await ctx.send('The puck is off!')
        elif game.table.puck.state == 'on':
            await ctx.send('The puck is on on {}!'.format(game.table.puck.point))

    @commands.command()
    async def players(self, ctx):
        if game.table.players != {}:
            await ctx.send('Here are the current players!')
            for name in game.table.players:
                player = game.table.getPlayer(name)
                await ctx.send('{}, Bankroll: ${:,}'.format(player, player.bankroll))
        else:
            await ctx.send('No players have joined the table!')

    @commands.command()
    async def changeShooter(self, ctx, other):
        player = game.table.getPlayer(other)
        game.table.shooter = player
        await ctx.send('Changing shooter to {}!'.format(player.name))

    @commands.command()
    async def resetTable(self, ctx):
        game.table.resetTable()
        await ctx.send('Resetting table!')
