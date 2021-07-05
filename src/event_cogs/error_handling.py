import discord
from discord.ext import commands

class ErrorHandling(commands.Cog):
  def __init__(self, bot):
    self.bot=bot
    self.name="ErrorHandling"

  @commands.Cog.listener()
  async def on_command_error(self, ctx, error):
    embed = discord.Embed(description=f"```{error}```", color=discord.Colour.dark_purple()).set_author(name="Bot Error")
    await ctx.send(embed=embed)

def setup(bot):
  bot.add_cog(ErrorHandling(bot))
