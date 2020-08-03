from discord.ext import commands
import config
from craps import game

class CrapsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def drop(self, ctx, amt):
        player = game.table.getPlayer(ctx.author.id)
        player.bankroll += int(amt)
        await ctx.send('{} now has ${}!'.format(ctx.author.mention, player.bankroll))

    @commands.command()
    async def walk(self, ctx):
        player = game.table.getPlayer(ctx.author.id)
        await ctx.send('{} left the table with ${}!'.format(ctx.author.mention, player.bankroll))
        game.table.removePlayer(ctx.author.id)

    @commands.command()
    async def roll(self, ctx):
        player = game.table.getPlayer(ctx.author.id)
        if player == game.table.shooter or game.table.shooter == None:
            game.table.dice.roll()
            await ctx.send('{} rolled {}!'.format(ctx.author.mention, game.table.dice))
            game.table.shooter = player
        else:
            user = self.bot.get_user(game.table.shooter.userID)
            await ctx.send('{} is the shooter!'.format(user.mention))

        game.table.checkBets()
        # post any updates to bets here

    @commands.command()
    async def bet(self, ctx, betType, amt):
        amt = int(amt)
        player = game.table.getPlayer(ctx.author.id)
        bet = game.bet.getBet(betType)
        game.table.makeBet(player, bet, amt)

    @commands.command()
    async def minbet(self, ctx, amt):
        # sets the minimun bet size, likely admin use only
        pass

    @commands.command()
    async def betfor(self, ctx, other, bet, amt):
        # makes bet from ctx.author's wallet and payed to other
        pass

    @commands.command()
    async def puck(self, ctx):
        # returns the state of the puck
        pass
