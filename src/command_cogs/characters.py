import discord, os
from discord.ext import commands
from replit import db
from d20 import roll

class Characters(commands.Cog):
  def __init__(self, bot):
    self.bot=bot
    self.name="Characters"

  @commands.command(
    name="register",
    aliases=['register-character', 'reg', 'rc', 'create-character'],
    brief="Registers a character with the given information.",
    description="Registers a character given the ability scores, hit points, spell list, currency, and equipment.",
    usage=f"<name> [attach: utopiumsheet file created with the create-file command"
    )
  async def register_character(self, ctx, name):
    if str(ctx.author.id) not in db:
      db[str(ctx.author.id)] = {}
    if name in db[str(ctx.author.id)]:
      return await ctx.send("```A character is already registered with this ID```")
    db[str(ctx.author.id)][name] = {}
    message = ctx.message
    if str(message.attachments) == "[]":
      return await ctx.send("```You did not attach a character sheet file.```")
    else:
      split_v1 = str(message.attachments).split("filename='")[1]
      filename = str(split_v1).split("' ")[0]
      if filename.endswith(".utopiumsheet"):
        await message.attachments[0].save(fp="player_data/character_sheets/{}".format(filename))
        await ctx.send("```Character successfully registered```")
        file_path = os.path.join('player_data/character_sheets', filename)
        with open(file_path, 'r+') as f:
          content = f.read()
        new_content = content.split('; ')
        scores = new_content[0]
        hp = new_content[1]
        spell_list = new_content[2]
        currency = new_content[3]
        equipment = new_content[4]
        new_scores = scores.split('! ')
        new_spell_list = spell_list.split('! ')
        new_equipment = equipment.split('! ')
        db[str(ctx.author.id)][name]['scores'] = {}
        db[str(ctx.author.id)][name]['scores']['con'] = int(new_scores[0])
        db[str(ctx.author.id)][name]['scores']['dex'] = int(new_scores[1])
        db[str(ctx.author.id)][name]['scores']['str'] = int(new_scores[2])
        db[str(ctx.author.id)][name]['scores']['int'] = int(new_scores[3])
        db[str(ctx.author.id)][name]['scores']['wis'] = int(new_scores[4])
        db[str(ctx.author.id)][name]['scores']['cha'] = int(new_scores[5])
        db[str(ctx.author.id)][name]['hp'] = hp
        db[str(ctx.author.id)][name]['spells'] = new_spell_list
        db[str(ctx.author.id)][name]['currency'] = currency
        db[str(ctx.author.id)][name]['equipment'] = new_equipment
      else:
        return await ctx.send("```That is not a valid .utopiumsheet file```")

  @commands.command(
    name="createfile",
    aliases=["cf", 'create-file', 'create_file'],
    brief="Creates utopiumsheet file",
    description="Will create a utopiumsheet file with a given name and further given information.",
    usage ="<name> [answer further promopts]"
  )
  async def create_file(self, ctx, name):
    string = ''
    scores = await ctx.send("```Please input your ability scores in the following order [constitution, dexterity, strength, intelligence, wisdom, charisma] seperated by a comma. If you do not yet have scores, you may instead say \"roll\" and have them assigned randomly. You have 2 minutes to respond.```")
    message_one = await self.bot.wait_for('message', check=lambda message: message.channel == scores.channel and message.author == ctx.author, timeout=190)
    if message_one.content == 'roll':
      scores_string = f"{roll('4d6kh3').total}, {roll('4d6kh3').total}, {roll('4d6kh3').total}, {roll('4d6kh3').total}, {roll('4d6kh3').total}, {roll('4d6kh3').total}".replace(', ', '! ')
    else:
      scores_string = message_one.content
    scores_string.replace(", ", '! ')
    string+=scores_string+"; "
    hp = await ctx.send("```Please input your hit points. You have 2 minutes.```")
    message_two = await self.bot.wait_for('message', check=lambda message: message.channel == hp.channel and message.author == ctx.author, timeout=190)
    string+=message_two.content+'; '
    spells = await ctx.send("```Please list your spells seperated by a comma. If you have none simply say 'None'. You have 2 minutes.```")
    message_three = await self.bot.wait_for('message', check=lambda message: message.channel == spells.channel and message.author == ctx.author, timeout=190)
    string+=message_three.content.replace(', ', '! ')+'; '
    currency = await ctx.send("```Please say how much currency you have below. If you have none simply say 'None'. You have 2 minutes.```")
    message_four = await self.bot.wait_for('message', check=lambda message: message.channel == currency.channel and message.author == ctx.author, timeout=190)
    string+=message_four.content+'; '
    equipment = await ctx.send("```Please list your equipment below seperated by a comma. If you have none simply say 'None'. You have 2 minutes.```")
    message_five = await self.bot.wait_for('message', check=lambda message: message.channel == equipment.channel and message.author == ctx.author, timeout=190)
    string+=message_five.content.replace(', ', '! ')
    with open(f'{name}.utopiumsheet', 'w') as f:
      f.write(string)
    await ctx.send(embed=discord.Embed(
      description=f"```{string.replace(', ', '! ')}```",
      color=discord.Colour.dark_purple()
    ).set_author(
      name="Character File Created"
    ), file=discord.File(
      f'{name}.utopiumsheet'
      ))
    os.remove(f"{name}.utopiumsheet")

  @commands.command(
    name="update",
    aliases=['update-characeter', 'uc', 'u'],
    brief="Updates a given character",
    description="Will update a given character with a new sheet (which can be created using the create-file command. Note: Character must already exist.",
    usage="<name> [attach new file]"
  )
  async def update_character(self, ctx, name):
    if str(ctx.author.id) not in db:
      return await ctx.send("```You don't have any characters registered.```")
    if name not in db[str(ctx.author.id)]:
      return await ctx.send("```You do not have a character registered with this name.```")
    message = ctx.message
    if str(message.attachments) == "[]":
      return await ctx.send("```You did not attach a character sheet file.```")
    else:
      split_v1 = str(message.attachments).split("filename='")[1]
      filename = str(split_v1).split("' ")[0]
      if filename.endswith(".utopiumsheet"):
        await message.attachments[0].save(fp="player_data/character_sheets/{}".format(filename))
        await ctx.send(embed=discord.Embed(description="```Character registered```", color=discord.Colour.dark_purple()))
        file_path = os.path.join('player_data/character_sheets', filename)
        with open(file_path, 'r+') as f:
          content = f.read()
        new_content = content.split('; ')
        scores = new_content[0]
        hp = new_content[1]
        spell_list = new_content[2]
        currency = new_content[3]
        equipment = new_content[4]
        new_scores = scores.split('! ')
        new_spell_list = spell_list.split('! ')
        new_equipment = equipment.split('! ')
        del db[str(ctx.author.id)][name]
        db[str(ctx.author.id)][name] = {}
        db[str(ctx.author.id)][name]['scores'] = {}
        db[str(ctx.author.id)][name]['scores']['con'] = int(new_scores[0])
        db[str(ctx.author.id)][name]['scores']['dex'] = int(new_scores[1])
        db[str(ctx.author.id)][name]['scores']['str'] = int(new_scores[2])
        db[str(ctx.author.id)][name]['scores']['int'] = int(new_scores[3])
        db[str(ctx.author.id)][name]['scores']['wis'] = int(new_scores[4])
        db[str(ctx.author.id)][name]['scores']['cha'] = int(new_scores[5])
        db[str(ctx.author.id)][name]['hp'] = int(hp)
        db[str(ctx.author.id)][name]['spells'] = new_spell_list
        db[str(ctx.author.id)][name]['currency'] = int(currency)
        db[str(ctx.author.id)][name]['equipment'] = new_equipment
      else:
        return await ctx.send("That is not a valid .utopiumsheet file")

  @commands.command(
    name="delete",
    aliases=['del', 'dc', 'delete_character', 'delete-character'],
    brief="Deletes a character",
    description="Deletes a character",
    usage="<name>"
  )
  async def create_character(self, ctx, name):
    if name not in db[str(ctx.author.id)]:
      return await ctx.send("You do not have a character registered under this name.")
    del db[str(ctx.author.id)][name]
    await ctx.send("Character deleted.")

  @commands.command(
    name="get-character",
    aliases=['get', 'gc','getcharacter'],
    brief="Returns information about a character.",
    description="Returns information about a given character.",
    usage='<name> <member: optional>')
  async def get_character(self, ctx, name, member: discord.Member=None):
    if member == None:
      member = ctx.author
    if name not in db[str(member.id)]:
      return await ctx.send("The given member does not have a character registered under that name.")
    await ctx.send(
      embed=discord.Embed(
        description=f"```\n-----------------\nNAME\n-----------------\n{name}\n-----------------\nAbility Scores\n-----------------\nConstitution - {db[str(member.id)][name]['scores']['con']}\nDexterity - {db[str(member.id)][name]['scores']['dex']}\nStrength - {db[str(member.id)][name]['scores']['str']}\nIntelligence - {db[str(member.id)][name]['scores']['int']}\nWisdom - {db[str(member.id)][name]['scores']['wis']}\nCharisma - {db[str(member.id)][name]['scores']['cha']}\n-----------------\nHit Points\n-----------------\n{db[str(member.id)][name]['hp']}\n-----------------\nSpells\n-----------------\n{db[str(member.id)][name]['spells'].value}\n-----------------\nCurrency\n-----------------\n{db[str(member.id)][name]['currency']}\n-----------------\nequipment\n-----------------\n{db[str(member.id)][name]['equipment'].value}```",
        color=discord.Colour.dark_purple()
      )
    )

  @commands.command(
    name="list-characters",
    aliases=['lc', 'listcharacters'],
    brief="displays a list of characters for a member.",
    description="Will return a list of all of the characters registered under a user.",
    usage="<member: optional>"
  )
  async def list_characters(self, ctx, member: discord.Member=None):
    if member == None:
      member = ctx.author
    if str(member.id) not in db:
      return await ctx.send("```That user does not have any characters registered under then```")
    await ctx.send(
      embed=discord.Embed(
        description=f"```{db[str(member.id)]}```",
        color=discord.Colour.dark_purple()
      )
    )

def setup(bot):
  bot.add_cog(Characters(bot))
