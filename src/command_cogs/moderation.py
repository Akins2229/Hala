import discord
from discord.ext import commands
import asyncio

class Moderation(commands.Cog):
  def __init__(self, bot):
    self.bot=self
    self.name="Moderation"

  #ban command
  @commands.command(
    name="ban",
    brief="Bans a given member",
    description="Bans a given member for a given reason.",
    usage='<member> <reason: optional>'
    )
  @commands.has_permissions(ban_members=True)
  async def _ban(self, ctx, member: discord.Member, *, reason=None):
    """Bans a certain user"""
    if reason == None:
      reason = "No Reason Provided"
    await ctx.message.delete()
    await ctx.send(f"{member.display_name} has been banned in {ctx.guild}; Reason: {reason}")
    await member.send(f"You have been banned in {ctx.guild}; Reason: {reason}")
    await member.ban(reason=reason)

  #kick command
  @commands.command(
    name="kick",
    brief="Kicks a given member",
    description="Kicks a given member for a given reason.",
    usage='<member> <reason: optional>'
    )
  @commands.has_permissions(kick_members=True)
  async def _kick(self, ctx, member: discord.Member, *, reason=None):
    """Kicks a member"""
    if reason == None:
      reason = "No Reason Rrovided."
    await ctx.send(f"{member.display_name} has been banned from {ctx.guild}; Reason: {reason}")
    await member.send(f"You have been kicked from {ctx.guild}; Reason: {reason}")
    await member.kick(reason=reason)

	#mute command
  @commands.command(
    name="mute",
    brief='Mutes a member for a given duration',
    description="Mutes a member for a given duration, and reason.",
    usage='<member> <duration: [s (seconds), m (minutes), h (hours), d (days)]> <reason: optional>'
    )
  @commands.has_permissions(manage_messages=True)
  async def _mute(self, ctx, member: discord.Member, duration, *, reason=None):
    """Mutes a user for a specified amount of time in s (seconds), m (minutes), h (hours) or d (days)"""
    suffix = duration[-1]
    if suffix == 's':
      Duration = duration.replace(suffix, "")
      time = int(Duration)
    elif suffix == 'm':
      Duration = duration.replace(suffix, "")
      intDuration = int(Duration)
      time = intDuration*60
    elif suffix == 'h':      
      Duration = duration.replace(suffix, "")
      intDuration = int(Duration)
      time = intDuration*3600
    elif suffix == 'd':
      Duration = duration.replace(suffix, "")
      intDuration = int(Duration)
      time = intDuration*86400
    else:
      await ctx.send(f"{suffix} is not a valid duration option.")
    mutedRole = discord.utils.get(ctx.guild.roles, name="Muted")
    if not mutedRole:
      mutedRole = await ctx.guild.create_role(name="Muted")
      for channel in ctx.guild.channels:
        channel.set_permissions(mutedRole, read_messages=False, send_messages=False, read_message_history=False, speak=False)
    await member.add_role(mutedRole)
    await ctx.send(f"{member.display_name} has been muted in {ctx.guild}; Reason: {reason}; Duration: {duration}")
    await member.send(f"You have been muted in {ctx.guild}; Reason: {reason}; Duration: {duration}")
    await asyncio.sleep(time)
    await member.remove_role(mutedRole)
    await member.send(f"You are now unmuted in {ctx.guild}")

  #unmute command
  @commands.command(
    name="unmute",
    brief='Unmutes a given member',
    description="Unmutes a given member who has been muted indefinitely.",
    usage='<member>'
    )
  async def _unmute(self, ctx, member:discord.Member):
    mutedRole = discord.utils.get(ctx.guild.roles, name="Muted")
    if not mutedRole:
      await ctx.send(f"Member is not muted")
    else:
      await member.remove_role(mutedRole)
      await ctx.send("Member unmuted", delet_after=5)
      await member.send(f"You have now been unmuted in {ctx.guild}")

  #unban comman
  @commands.command(
    name="unban",
    brief="Unbans a given user.",
    description="Searches a list of banned users and attempts to unban a given user.",
    usage='<member>'
    )
  @commands.has_permissions(ban_members=True)
  async def _unban(self, ctx, member: discord.Member):
    """Unbans a given user"""
    bannedUsers = ctx.guild.bans()
    member_name, member_discriminator = member.split('#')
    for banEntry in bannedUsers:
      user = banEntry.user
      if (user.name, user.discriminator) == (member_name, member_discriminator):
        await ctx.guild.unban(user)
        await ctx.send(f"User has been unbanned")
        return

  #userinfo command
  @commands.command(
    name='userinfo',
    brief="Displays information about a given user.",
    description="Displays information about a given user or yourself if none is provided.",
    usage='<member: optional>'
    )
  async def _userinfo(self, ctx, *, member: discord.Member=None):
    """Displays information on a user"""
    if member == None:
      member = ctx.message.author
    roles = [role for role in member.roles if role != ctx.guild.default_role]
    embed = discord.Embed(color=member.color, timestamp=ctx.message.created_at)
    embed.set_author(name=f"User Info - {member}")
    embed.set_thumbnail(url=member.avatar_url)
    embed.set_footer (text=f"Requested by {ctx.author}")
    embed.add_field(name="ID", value=member.id)
    embed.add_field(name="Display Name", value=member.display_name)
    embed.add_field(name="Created at:", value=member.created_at.strftime("%a, %#d %B %Y, %I %M %p UTC"))
    embed.add_field(name="Joined at:", value=member.joined_at.strftime("%a, %#d %B %Y, %I %M %p UTC"))
    embed.add_field(name=f"(Roles, {len(roles)}", value=" ".join([role.mention for role in roles]))
    embed.add_field(name="Top Role:", value=member.top_role.mention)
    embed.add_field(name="Bot?", value=member.bot)
    await ctx.send(embed=embed)

  #avatar command  
  @commands.command(
    name='avatar',
    brief="Returns a users avatar.",
    description="Returns a users avatar or your own if none is provided.",
    usage='<member>'
    )
  async def _avatar(self, ctx, *, member: discord.Member=None):
    """Return a users avatar"""
    if member == None:
      member = ctx.message.author
    embed=discord.Embed(title=f"{member.name}'s Avatar", color=member.color, timestamp=ctx.message.created_at)
    embed.set_thumbnail(url=member.avatar_url)
    await ctx.send(embed=embed)

  #purge command
  @commands.command(
    name='purge',
    brief="Purges a given number of messages",
    description="Purges a given number of messages within your current channel.",
    usage='<amount>'
    )
  @commands.has_permissions(manage_messages=True)
  async def _purge(self, ctx, amount):
    """Will purge a given number of messages"""
    await ctx.message.delete()
    await ctx.send("Now purging...", delete_after=3)
    intLimit = int(amount)
    await asyncio.sleep(2)
    await ctx.channel.purge(limit=intLimit)

  #lockdown command
  @commands.command(
    name="lock",
    aliases=['lockdown', 'lock-down', 'ld'],
    brief="locks down the current channel.",
    description="Bars all members from accessing the channel unless they have a role specifically stating otherwise.",
    usage=''
    )
  @commands.has_permissions(administrator=True)
  async def _lockdown(self, ctx):
    """Will disallow most-all users the permissions to user a channel"""
    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=False)
    await ctx.send("The Channel has been Locked!")

  #unlock command
  @commands.command(
    name="unlock",
    brief="Unlocks a currently locked channel.",
    description="Unlocks the current channel given that it is currently locked.",
    usage=''
    )
  @commands.has_permissions(administrator=True)
  async def _unlock(self, ctx):
    """Will reallow those users to use the channel again"""
    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=True)
    await ctx.send("Channel has been unlocked")

class Actions():
  def __init__(self, ctx: commands.Context):
    self = self
    ctx = ctx

  async def action_mute(channel, member: discord.Member, duration, *, reason=None):
    """Mutes a user for a specified amount of time in s (seconds), m (minutes), h (hours) or d (days)"""
    suffix = duration[-1]
    if reason == None:
      reason = "Has collected 5 or more mutes."
    if suffix == 's':
      Duration = duration.replace(suffix, "")
      time = int(Duration)
    elif suffix == 'm':
      Duration = duration.replace(suffix, "")
      intDuration = int(Duration)
      time = intDuration*60
    elif suffix == 'h':      
      Duration = duration.replace(suffix, "")
      intDuration = int(Duration)
      time = intDuration*3600
    elif suffix == 'd':
      Duration = duration.replace(suffix, "")
      intDuration = int(Duration)
      time = intDuration*86400
    else:
      await channel.send(f"{suffix} is not a valid duration option.")
    mutedRole = discord.utils.get(channel.guild.roles, name="Muted")
    if not mutedRole:
      mutedRole = await channel.guild.create_role(name="Muted")
      for channel in channel.guild.channels:
        channel.set_permissions(mutedRole, read_messages=False, send_messages=False, read_message_history=False, speak=False)
    await member.add_role(mutedRole)
    await channel.send(f"{member.display_name} has been muted in {channel.guild}; Reason: {reason}; Duration: {duration}")
    await member.send(f"You have been muted in {channel.guild}; Reason: {reason}; Duration: {duration}")
    await asyncio.sleep(time)
    await member.remove_role(mutedRole)
    await member.send(f"You are now unmuted in {channel.guild}")

    async def action_kick(channel, member: discord.Member):
      await member.send(f"You have been kicked in {channel.guild} for collecting 10 or more warnings.")
      await member.kick(reason="collecting 10 or more warnings.")
      await channel.send(f"Member {member.display_name}, has been kicked for collecting 10 or more mutes.")

    async def action_ban(channel, member: discord.Member):
      await member.send(f"You have been banned in {channel.guild} for collecting 10 or more warnings.")
      await member.ban(reason="collecting 10 or more warnings.")
      await channel.send(f"Member {member.display_name}, has been banned for collecting 10 or more mutes.")


def setup(bot):
  bot.add_cog(Moderation(bot))
