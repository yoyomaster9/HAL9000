import discord
from discord.ext import commands
import config
import cogs

BOT_PREFIX = ('.')

bot = commands.Bot(command_prefix=BOT_PREFIX)
for x in commands.Cog.__subclasses__():
    bot.add_cog(x(bot))

@bot.event
async def on_message(message):
    # We do not want the bot to reply to itself
    if message.author == bot.user:
        return

    # Otherwise process command
    else:
        await bot.process_commands(message)

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name='Mathnasium@Home'))
    print('Logged in as ' + bot.user.name)
    print('---------------------')
    for g in bot.guilds:
        print('Logged into {}'.format(g))

bot.run(config.DiscordToken)
