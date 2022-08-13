import discord
import os

from webserver import keep_alive
from riotwatcher import LolWatcher, ApiError
from discord import Embed
from discord.utils import get
from discord.ext import commands

#riot API summoner
riotApiKey = "RGAPI-75475f20-b710-44d4-96ff-6ddd3fc0be65"
watcher = LolWatcher(riotApiKey)
platformRoutingValue = "NA1"
summonerName = ""

bot = commands.Bot(command_prefix = '*')

@bot.event
async def on_ready():
  print('{0.user} Online'.format(bot))

@bot.command()
async def start(context):
  await context.send('Thumbs up if ur playing 5s tonight!\nThumbs down if ur not playing :(')

@bot.command()
async def commands(context):
  helpEmbed=discord.Embed(title="Help", description="every command has a prefix of '*'", color=0x0000ff)
  helpEmbed.add_field(name="start", value="This command gets 10 people for 5v5!", inline=False)
  helpEmbed.add_field(name="team", value="This command creates team 1 and team 2. Type *team summonerName teamNumber role")
  helpEmbed.add_field(name="stats", value="This command can search up a summoner! Type *stats summonerName")
  await context.send(embed=helpEmbed)

#op.gg kind of thing here
  #shows tier and winrate
@bot.command()
async def stats(context, name):
  summonerName = str(name)
  embedVar=discord.Embed(title="Summoner Stats", color=0xFFFF00)
  try:
    summoner = watcher.summoner.by_name(platformRoutingValue, summonerName)
    stats = watcher.league.by_summoner(platformRoutingValue, summoner['id'])

    print(stats)
    print(len(stats))
  #check if the person has a flex rank or not
    if ('TFT' in stats[len(stats) - 1]['queueType']):
      tier = str(stats[len(stats) - 2]['tier'])
      rank = str(stats[len(stats) - 2]['rank'])
      lp = str(stats[len(stats) - 2]['leaguePoints'])
      wins = int(stats[len(stats) - 2]['wins'])
      losses = int(stats[len(stats) - 2]['losses'])
      wr = round(float(wins / (wins + losses)) * 100, 2)
      winrate = str(wr)
      sumTier = tier + " " + rank + " " + lp + "lp"
    elif ('FLEX' in stats[len(stats) - 1]['queueType']):
      tier = str(stats[len(stats) - 2]['tier'])
      rank = str(stats[len(stats) - 2]['rank'])
      lp = str(stats[len(stats) - 2]['leaguePoints'])
      wins = int(stats[len(stats) - 2]['wins'])
      losses = int(stats[len(stats) - 2]['losses'])
      wr = round(float(wins / (wins + losses)) * 100, 2)
      winrate = str(wr)
      sumTier = tier + " " + rank + " " + lp + "lp"
    else:
      tier = str(stats[len(stats) - 1]['tier'])
      rank = str(stats[len(stats) - 1]['rank'])
      lp = str(stats[len(stats) - 1]['leaguePoints'])
      wins = int(stats[len(stats) - 1]['wins'])
      losses = int(stats[len(stats) - 1]['losses'])
      wr = round(float(wins / (wins + losses)) * 100, 2)
      winrate = str(wr)
      sumTier = tier + " " + rank + " " + lp + "lp"
    
    embedVar.add_field(name="Summoner", value=summonerName, inline=False)
    embedVar.add_field(name="Tier", value=sumTier, inline=False)
    embedVar.add_field(name="Winrate", value=winrate, inline=False)
    await context.send(embed=embedVar)
  except ApiError as err:
    if err.response.status_code == 429:
        await context.send('We should retry in {} seconds.'.format(err.headers['Retry-After']))
    elif err.response.status_code == 404:
        await context.send('Summoner not found! If you have a space in your summoner name, type it without the space.')
    else:
      raise
  except IndexError:
    await context.send('This summoner is not ranked!')

#starting a 5v5 with the first 10 people who added a thumbs up emoji
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

rows, cols = 5, 2
global teamArr
global teamNum
global playerName
global lane
teamArr = [["Empty" for x in range(rows)] for y in range(cols)]
teamNum = ""
playerName = ""
lane = ""

@bot.command()
async def team(context, name: str, num: int, pos: str):
  teamEmbed = discord.Embed(title="Teams", color=0x6a0dad)
  playerName = name
  teamNum = num
  lane = pos

  #team1
  if (teamNum == 1):
    if (lane.casefold() == 'top'):
      teamArr[0][0] = playerName
    elif (lane.casefold() == 'jungle'):
      teamArr[0][1] = playerName
    elif (lane.casefold() == 'mid'):
      teamArr[0][2] = playerName
    elif (lane.casefold() == 'adc'):
      teamArr[0][3] = playerName
    elif (lane.casefold() == 'support'):
      teamArr[0][4] = playerName
  #team2
  elif (teamNum == 2):
    if (lane.casefold() == 'top'):
      teamArr[1][0] = playerName
    elif (lane.casefold() == 'jungle'):
      teamArr[1][1] = playerName
    elif (lane.casefold() == 'mid'):
      teamArr[1][2] = playerName
    elif (lane.casefold() == 'adc'):
      teamArr[1][3] = playerName
    elif (lane.casefold() == 'support'):
      teamArr[1][4] = playerName

  teamResult = str(teamArr[0][0]) + "\n" + str(teamArr[0][1]) + "\n" + str(teamArr[0][2]) + "\n" + str(teamArr[0][3]) + "\n" + str(teamArr[0][4])
  teamEmbed.add_field(name="Team 1", value=teamResult, inline=True)
  teamResult2 = str(teamArr[1][0]) + "\n" + str(teamArr[1][1]) + "\n" + str(teamArr[1][2]) + "\n" + str(teamArr[1][3]) + "\n" + str(teamArr[1][4])
  teamEmbed.add_field(name="Team 2", value=teamResult2, inline=True)

  await context.send(embed=teamEmbed)

@bot.command()
async def teamView(context):
  teamEmbed = discord.Embed(title="Teams", color=0x6a0dad)
  teamResult = str(teamArr[0][0]) + "\n" + str(teamArr[0][1]) + "\n" + str(teamArr[0][2]) + "\n" + str(teamArr[0][3]) + "\n" + str(teamArr[0][4])
  teamEmbed.add_field(name="Team 1", value=teamResult, inline=True)
  teamResult2 = str(teamArr[1][0]) + "\n" + str(teamArr[1][1]) + "\n" + str(teamArr[1][2]) + "\n" + str(teamArr[1][3]) + "\n" + str(teamArr[1][4])
  teamEmbed.add_field(name="Team 2", value=teamResult2, inline=True)
  await context.send(embed=teamEmbed)

@bot.command()
async def move(context, channel:discord.VoiceChannel):
  team1 = bot.get_channel({780236755030769674})
  team2 = bot.get_channel({780236792283529248})
  leagueoflegends = bot.get_channel({730320049302142991})
  team1_members = teamArr[0]
  team2_members = teamArr[1]
  
  for team1_members in leagueoflegends.members:
    await team1_members.move_to(team1)
  for team2_members in leagueoflegends.members:
    await team2_members.move_to(team2)
  

#keep the server running 24/7
keep_alive()
my_secret = os.environ['TOKEN']
bot.run(my_secret)

  
