import discord
import os
from discord import Embed
from discord.utils import get
from discord.ext import commands

bot = commands.Bot(command_prefix = '*')

@bot.event
async def on_ready():
  print('{0.user} Online'.format(bot))

@bot.command()
async def start(context):
  await context.send('Thumbs up if ur playing 5s tonight!\nThumbs down if ur not playing :(')
#10명 뽑은사람들 티어랑 라인 알려주는 코맨드
#팀짜는 코맨드
#팀짜고나서 로스터 보여주는 코맨드
  
@bot.event
async def on_reaction_add(reaction, user):
  #only extract the reactions from the bot's message
  if reaction.message.author.id == bot.user.id:
    #if the emoji is thumbs up
    if reaction.emoji == '👍':
      await reaction.message.channel.send(f'{user.mention} is playing!')
    #if the emoji is thumbs down
    if reaction.emoji == '👎':
      await reaction.message.channel.send(f'{user.mention} is not playing :(')
    #if the reaction count reaches 10
    if len(reaction.message.reactions) == 10:
      await reaction.message.channel.send(f'We are ready to play! Form your teams.')
    #if the reaction count goes over 10, delete the reaction that the user put
    if len(reaction.message.reactions) > 10:
      await reaction.message.remove_reaction(reaction.emoji, user)
      await reaction.message.channel.send(f'We already have 10 people!')
                                          
        
my_secret = os.environ['TOKEN']
bot.run(my_secret)
  