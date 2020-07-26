from discord.ext import commands
import config
import json, aiohttp

class Utilties(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(description = 'Checks to see if the bot is responsive',
                    help = 'Responds with Pong!',
                    brief = 'Responds with Pong!')
    async def ping(self, ctx):
        await ctx.send('Pong! {}ms'.format(round(self.bot.latency*1000, 1)))

    @commands.command(brief = 'Logs out of all servers. ADMIN ONLY',
                    description  = 'Logs out of all servers.\nONLY FOR ADMIN USE!')
    async def logout(self, ctx):
        if ctx.author.id == config.adminID:
            await ctx.send('Logging out!!')
            await self.bot.logout()
        else:
            await ctx.send('You\'re not an admin!')

    @commands.command(description = 'Returns information on the bot.',
                    brief = 'Returns information on the bot.')
    async def about(self, ctx):
        with open('resources/about.txt', 'r') as file:
            s = ''.join(file.readlines())
            await ctx.send(s)

    @commands.command(description = 'Returns current price of ETH in USD',
                    brief = 'Returns current price of ETH in USD')
    async def eth(self, ctx):
        url = 'https://min-api.cryptocompare.com/data/pricemulti?fsyms=ETH&tsyms=USD&api_key=' + str(config.EthereumAPIKey)
        async with aiohttp.ClientSession() as session:
            raw_response = await session.get(url)
            response = await raw_response.text()
            response = json.loads(response)
            msg = 'Ethereum Price: ${:.2f}'.format(response['ETH']['USD'])
        await ctx.send(msg)

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        await ctx.send('I\'m sorry {}, I\'m afraid I can\'t do that.'.format(ctx.author.mention))
