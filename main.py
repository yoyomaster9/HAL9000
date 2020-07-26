import discord
from discord.ext import commands
import config
import cogs
import random

BOT_PREFIX = ('.')

bot = commands.Bot(command_prefix=BOT_PREFIX)
for x in commands.Cog.__subclasses__():
    bot.add_cog(x(bot))

@bot.event
async def on_message(message):
    # We do not want the bot to reply to itself
    if message.author == bot.user:
        return

    if message.content[0] == BOT_PREFIX and random.random() < .01:
        await message.channel.send('I\'m sorry {}, I\'m afraid I can\'t do that.'.format(message.author.mention))

    # Otherwise process command
    else:
        await bot.process_commands(message)

@bot.event
async def on_ready():
    print('Logged in as ' + bot.user.name)
    print('---------------------')
    for g in bot.guilds:
        print('Logged into {}'.format(g))

bot.run(config.DiscordToken)
