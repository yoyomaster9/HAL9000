from discord.ext import commands
import config
from craps import game
import craps.config

class CrapsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def drop(self, ctx, amt):
        amt = int(amt)
        if amt > craps.config.MAXDROPSIZE:
            await ctx.send('You cannot drop more than ${:,}!'.format(craps.config.MAXDROPSIZE))
            return
        player = game.table.getPlayer(ctx.author.name)
        player.bankroll += amt
        await ctx.send('{} now has ${:,}!'.format(player.name, player.bankroll))

    @commands.command()
    async def walk(self, ctx):
        player = game.table.getPlayer(ctx.author.name)
        await ctx.send('{} left the table with ${:,}!'.format(player.name, player.bankroll))
        game.table.removePlayer(ctx.author.name)

    @commands.command()
    async def bankroll(self, ctx):
        player = game.table.getPlayer(ctx.author.name)
        await ctx.send('{} has a bankroll of ${:,}!'.format(player.name, player.bankroll))

    @commands.command()
    async def roll(self, ctx):
        player = game.table.getPlayer(ctx.author.name)
        try:
            player.roll()
            await ctx.send('{} rolled {}!'.format(ctx.author.name, game.table.dice))
            for bet in game.table.completedBets:
                if bet.status == 'win':
                    msg = '{} won their {} bet of ${:,}!'.format(bet.player.name, bet.type, bet.amt)
                elif bet.status == 'loss':
                    msg = '{} lost their {} bet of ${:,}.'.format(bet.player.name, bet.type, bet.amt)
                await ctx.send(msg)

        except game.ShooterError:
            await ctx.send('Wrong shooter! {} has the dice.'.format(game.table.shooter))

    @commands.command()
    async def bet(self, ctx, betType, amt):
        try:
            amt = int(amt)
            player = game.table.getPlayer(ctx.author.name)
            bet = game.bet.getBet(betType)
            game.table.makeBet(player, bet, amt)
            await ctx.send('Bet made!')
        except game.BetBankrollError:
            await ctx.send('Bet size too large! Your bankroll is ${:,}.'.format(player.bankroll))

    @commands.command()
    async def bets(self, ctx):
        if game.table.bets != []:
            await ctx.send('Here are the current bets!')
            for bet in game.table.bets:
                await ctx.send(bet)
        else:
            await ctx.send('No bets have been made!')

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
            for player in game.table.players:
                player = game.table.players[player]
                await ctx.send('{}, Bankroll: ${:,}'.format(player, player.bankroll))
        else:
            await ctx.send('No players have joined the table!')
