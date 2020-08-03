from discord.ext import commands
import config
from craps import game

class CrapsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def drop(self, ctx, amt):
        player = game.table.getPlayer(ctx.author.mention)
        player.bankroll += int(amt)
        await ctx.send('{} now has ${}!'.format(player.username, player.bankroll))

    @commands.command()
    async def walk(self, ctx):
        player = game.table.getPlayer(ctx.author.mention)
        await ctx.send('{} left the table with ${}!'.format(player.username, player.bankroll))
        game.table.removePlayer(ctx.author.id)

    @commands.command()
    async def bankroll(self, ctx):
        player = game.table.getPlayer(ctx.author.mention)
        await ctx.send('{} has a bankroll of ${}!'.format(player.username, player.bankroll))

    @commands.command()
    async def roll(self, ctx):
        player = game.table.getPlayer(ctx.author.mention)
        try:
            game.table.roll(player)
            await ctx.send('{} rolled {}!'.format(ctx.author.mention, game.table.dice))
            for bet in game.table.completedBets:
                if bet.status == 'win':
                    msg = '{} won their {} bet of {}!'.format(player.username, bet.type, bet.amt)
                elif bet.status == 'loss':
                    msg = '{} lost their {} bet of {}.'.format(player.username, bet.type, bet.amt)
                await ctx.send(msg)

        except game.ShooterError:
            await ctx.send('Wrong shooter! {} has the dice.'.format(player.username))

    @commands.command()
    async def bet(self, ctx, betType, amt):
        amt = int(amt)
        player = game.table.getPlayer(ctx.author.mention)
        bet = game.bet.getBet(betType)
        game.table.makeBet(player, bet, amt)
        await ctx.send('Bet made!')

    @commands.command()
    async def bets(self, ctx):
        await ctx.send('Here are the current bets!')
        for bet in game.table.bets:
            await ctx.send(bet)

    @commands.command()
    async def puck(self, ctx):
        if game.table.puck.state == 'off':
            await ctx.send('The puck is off!')
        elif game.table.puck.state == 'on':
            await ctx.send('The puck is on on {}!'.format(game.table.puck.point))

    @commands.command()
    async def minbet(self, ctx, amt):
        # sets the minimun bet size, likely admin use only
        pass

    @commands.command()
    async def betfor(self, ctx, other, bet, amt):
        # makes bet from ctx.author's wallet and payed to other
        pass
