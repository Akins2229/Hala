import os
from replit import db

class Utils():
  def __init__(self):
    self=self

  def get_prefix(bot, message):
    if str(message.guild.id) in db:
      prefix = db[str(message.guild.id)]
    else:
      prefix = 'dnd!'
    return prefix
