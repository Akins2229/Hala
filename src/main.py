import discord, os
from discord.ext import commands
from replit import db
from utils import Utils as utils

token = db['token']

bot = commands.Bot(
  command_prefix=utils.get_prefix,
  description="A simple D&D Discord bot.",
  case_insensitive=True,
  intents=discord.Intents.all(),
  help_command=None
  )

command_cogs = ['command_cogs.help_command', 'command_cogs.characters', 'command_cogs.bot_commands', 'command_cogs.rolling', 'command_cogs.music', 'command_cogs.moderation']
event_cogs = ['event_cogs.error_handling', 'event_cogs.events']

if __name__ == '__main__':
  for cog in command_cogs:
    bot.load_extension(cog)
  for cog in event_cogs:
    bot.load_extension(cog)

bot.run(token)
