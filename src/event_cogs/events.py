import discord
from discord.ext import commands

class Events(commands.Cog):
  def __init__(self, bot):
    self.bot=bot
    self.name="Events"

  @commands.Cog.listener()
  async def on_ready(self):
    print(f"-----------------------\nLOGGED IN\nUSERNAME - {self.bot.user.name}\nID - {self.bot.user.id}\nDEVELOPER[S] - Akins\nVERSION - v1.0.1\n-----------------------")

def setup(bot):
  bot.add_cog(Events(bot))
