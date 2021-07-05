import discord
from discord.ext import commands
from d20 import roll as diceroll

class Rolling(commands.Cog):
  def __init__(self, bot):
    self.bot=bot
    self.name="Rolling"

  @commands.command(
    name="roll",
    aliases=['dice', 'r'],
    brief="Rolls a dice using RPG format",
    description="Rolls a dice using the traditional RPG format. A guide can be found at https://en.wikipedia.org/wiki/Dice_notation",
    usage="<roll>"
    )
  async def _roll(self, ctx, roll=None):
    if roll == None:
      await ctx.send("You must provide a roll.")
      return
    rolls = diceroll(roll)
    rolls = str(rolls).replace('`', '')
    embed = discord.Embed(description=f"```{rolls}```", color=discord.Colour.dark_purple()).set_author(name=f"Roll Results - {ctx.message.author.display_name}")
    await ctx.send(embed=embed)

  @commands.command(
    name="stats",
    aliases=['stat', 'rs'],
    brief="Rolls basic stat rolls.",
    description="Rolls 6 4d6kh3 to fit traditional D&D 5e stat rolls.",
    usage=""
    )
  async def _stat(self, ctx,):
    embed = discord.Embed(description=f"```Stat Rolls```", color=discord.Colour.dark_purple()).set_author(name=f"Stat Roll Results - {ctx.message.author.display_name}")
    n = 6
    while n > 0:
      roll = diceroll('4d6kh3')
      rolls = str(roll).replace('`', '')
      embed.add_field(name=f"Stat - {roll.total}", value=f"{rolls}", inline=False)
      n = n-1
    await ctx.send(embed=embed)

def setup(bot):
  bot.add_cog(Rolling(bot))
