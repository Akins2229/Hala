import discord
from discord.ext import commands
from utils import Utils as utils

class Help(commands.Cog):
  def __init__(self, bot):
    self.bot=bot
    self.name="Help"
  
  @commands.command(
    name="help",
    brief="Shows this command",
    description="Will send a list of commands, and detailed descriptions of them to your current channel.",
    usage="<command: optional>"
    )
  async def _help(self, ctx, command_name=None):
    string = ''
    prefix = utils.get_prefix(self.bot, ctx.message)
    command_list = []
    for cog in self.bot.cogs:
      cog_object = self.bot.get_cog(cog)
      cog_string = f"\n{cog_object.name} category:\n"
      for command in cog_object.get_commands():
        if len(cog_object.get_commands()) < 1:
          string.replace(cog_string, '')
          break
        command_string = f"{command.name} - {command.brief}\n"
        cog_string+=command_string
        command_list.append(command.name)
      string+=cog_string
    if command_name is not None:
      if command_name in command_list:
        command_obj = self.bot.get_command(command_name)
        aliases = command_obj.aliases
        if len(aliases) < 1:
          aliases = ""
        string = f"\nNAME:\n{command_obj.name}{aliases}\n--------------\nDESCRIPTION:\n{command_obj.description}\n--------------\nUSAGE:\n{prefix}{command_obj.name}{aliases} {command_obj.usage}"
      else:
        return await ctx.send("That is not a valid command.")
    embed = discord.Embed(
      description=f"```{string}```",
      color = discord.Colour.dark_purple()
    ).set_author(
      name="Help Command"
      ).set_footer(
        text=f"For more information on a command do {prefix}help [command]"
      )
    await ctx.send(embed=embed)

def setup(bot):
  bot.add_cog(Help(bot))
