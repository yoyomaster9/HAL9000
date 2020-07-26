from discord.ext import commands
import config
import craps

class CrapsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def drop(self, ctx, amt):
        player = craps.getPlayer(ctx.author.id)
        player.bankroll += amt

    @commands.command()
    async def walk(self, ctx):
        # remove bankroll and return winnings
        pass

    @commands.command()
    async def bet(self, ctx, betType, amt):
        # places amt on betType
        # will need to convert betType (str) into Bet (class)
        pass

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
