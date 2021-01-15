import discord
import requests
import json
import os # for heroku
from discord.ext import commands

intents = discord.Intents(messages = True, guilds = True, reactions = True, members = True, presences = True)
client = commands.Bot(command_prefix = 'hive!', intents = intents)
client.remove_command("help")

@client.event
async def on_ready():
    print("Bot running on {0.user}!".format(client))
    await client.change_presence(activity=discord.Activity(name='for hive!help', type=3))

@client.command(aliases=['sw'])
async def skywars(ctx, username): # register command
    print("Connecting to api.playhive.com...")
    print("Requested Username: " + username)
    print("Requested Game: Skywars")
    json_data = requests.get("https://api.playhive.com/v0/game/all/sky/" + username) # lookup player data
    print("Connected! Response status code: " + str(json_data.status_code))
    print("JSON: " + str(json_data.json())) # print JSON in console
    data = json.loads(json_data.text) # convert JSON to python dict
    print("Python dict:")
    print(data) # print python dict to console
    print("Data type: " + str(type(data))) # print data type to console (confirming if it is a dict)
    losses = data["played"] - data["victories"] # calculate losses
    win_loss = (data["victories"] / data["played"]) * 100 # calculate win rate
    kdr = data["kills"] / losses # calculate KDR
    await ctx.send("**Skywars stats for " + username + "**\n```py\nXP: " + str(data["xp"]) + "\nWins: " + str(data["victories"]) + "\nLosses: " + str(losses) + "\nPlayed: " + str(data["played"]) + "\nWin rate: " + (str(win_loss)) + "%" + "\nKills: " + str(data["kills"]) + "\nKDR: " + str(kdr) + "```")


@client.command(aliases=['tw'])
async def treasurewars(ctx, username):
    print("Connecting to api.playhive.com...")
    print("Requested Username: " + username)
    print("Requested Game: Treasure Wars")
    json_data = requests.get("https://api.playhive.com/v0/game/all/wars/" + username)
    print("Connected! Response status code: " + str(json_data.status_code))
    print("JSON: " + str(json_data.json()))
    data = json.loads(json_data.text)
    print("Python dict:")
    print(data)
    print("Data type: " + str(type(data)))
    losses = data["played"] - data["victories"]
    win_loss = (data["victories"] / data["played"]) * 100
    kdr = data["kills"] / data["deaths"]
    await ctx.send("**Treasure Wars stats for " + username + "**\n```py\nXP: " + str(data["xp"]) + "\nWins: " + str(data["victories"]) + "\nLosses: " + str(losses) + "\nPlayed: " + str(data["played"]) + "\nWin rate: " + (str(win_loss)) + "%" + "\nKills: " + str(data["kills"]) + "\nFinal Kills: " + str(data["final_kills"]) + "\nTreasures Destroyed: " + str(data["treasure_destroyed"]) + "\nKDR: " + str(kdr)+ "```")

@client.command(aliases=['sg'])
async def survivalgames(ctx, username):
    print("Connecting to api.playhive.com...")
    print("Requested Username: " + username)
    print("Requested Game: Survival Games")
    json_data = requests.get("https://api.playhive.com/v0/game/all/sg/" + username)
    print("Connected! Response status code: " + str(json_data.status_code))
    print("JSON: " + str(json_data.json()))
    data = json.loads(json_data.text)
    print("Python dict:")
    print(data)
    print("Data type: " + str(type(data)))
    losses = data["played"] - data["victories"]
    win_loss = (data["victories"] / data["played"]) * 100
    kdr = data["kills"] / losses
    await ctx.send("**Survival Games stats for " + username + "**\n```py\nXP: " + str(data["xp"]) + "\nWins: " + str(data["victories"]) + "\nLosses: " + str(losses) + "\nPlayed: " + str(data["played"]) + "\nWin rate: " + (str(win_loss)) + "%" + "\nKills: " + str(data["kills"]) + "\nKDR: " + str(kdr) + "```")

@client.command(aliases=['swlb'])
async def skywarsleaderboard(ctx):
    print("Connecting to api.playhive.com...")
    print("Requested Game: Skywars Leaderboard")
    json_data = requests.get("https://api.playhive.com/v0/game/all/sky")
    print("Connected! Response status code: "  + str(json_data.status_code))
    print("JSON: " + str(json_data.json()))
    data = json.loads(json_data.text) # should return a list
    print("Python:")
    print(data)
    print("Data type: " + str(type(data)))
    await ctx.send("**Skywars Leaderboard**\n```ahk\n"
                   "#1 " + data[0]['username'] + "(" + str(data[0]['victories']) + " Wins)"
                   + "\n#2 " + data[1]['username'] + "(" + str(data[1]['victories']) + " Wins)"
                   + "\n#3 " + data[2]['username'] + "(" + str(data[2]['victories']) + " Wins)"
                   + "\n#4 " + data[3]['username'] + "(" + str(data[3]['victories']) + " Wins)"
                   + "\n#5 " + data[4]['username'] + "(" + str(data[4]['victories']) + " Wins)"
                   + "\n#6 " + data[5]['username'] + "(" + str(data[5]['victories']) + " Wins)"
                   + "\n#7 " + data[6]['username'] + "(" + str(data[6]['victories']) + " Wins)"
                   + "\n#8 " + data[7]['username'] + "(" + str(data[7]['victories']) + " Wins)"
                   + "\n#9 " + data[8]['username'] + "(" + str(data[8]['victories']) + " Wins)"
                   + "\n#10 " + data[9]['username'] + "(" + str(data[9]['victories']) + " Wins)```")

@client.command(aliases=['twlb'])
async def treasurewarsleaderboard(ctx):
    print("Connecting to api.playhive.com...")
    print("Requested Game: Treasure Wars Leaderboard")
    json_data = requests.get("https://api.playhive.com/v0/game/all/wars")
    print("Connected! Response status code: " + str(json_data.status_code))
    print("JSON: " + str(json_data.json()))
    data = json.loads(json_data.text) # should return a list
    print("Python:")
    print(data)
    print("Data type: " + str(type(data)))
    await ctx.send("**Treasure Wars Leaderboard**\n```ahk\n"
                   "#1 " + data[0]['username'] + "(" + str(data[0]['victories']) + " Wins)"
                   + "\n#2 " + data[1]['username'] + "(" + str(data[1]['victories']) + " Wins)"
                   + "\n#3 " + data[2]['username'] + "(" + str(data[2]['victories']) + " Wins)"
                   + "\n#4 " + data[3]['username'] + "(" + str(data[3]['victories']) + " Wins)"
                   + "\n#5 " + data[4]['username'] + "(" + str(data[4]['victories']) + " Wins)"
                   + "\n#6 " + data[5]['username'] + "(" + str(data[5]['victories']) + " Wins)"
                   + "\n#7 " + data[6]['username'] + "(" + str(data[6]['victories']) + " Wins)"
                   + "\n#8 " + data[7]['username'] + "(" + str(data[7]['victories']) + " Wins)"
                   + "\n#9 " + data[8]['username'] + "(" + str(data[8]['victories']) + " Wins)"
                   + "\n#10 " + data[9]['username'] + "(" + str(data[9]['victories']) + " Wins)```")

@client.command(aliases=['sglb'])
async def survivalgamesleaderboard(ctx):
    print("Connecting to api.playhive.com...")
    print("Requested Game: Survival Games Leaderboard")
    json_data = requests.get("https://api.playhive.com/v0/game/all/sg")
    print("Connected! Response status code: " + str(json_data.status_code))
    print("JSON: " + str(json_data.json()))
    data = json.loads(json_data.text) # should return a list
    print("Python:")
    print(data)
    print("Data type: " + str(type(data)))
    await ctx.send("**Survival Games Leaderboard**\n```ahk\n"
                   "#1 " + data[0]['username'] + "(" + str(data[0]['victories']) + " Wins)"
                   + "\n#2 " + data[1]['username'] + "(" + str(data[1]['victories']) + " Wins)"
                   + "\n#3 " + data[2]['username'] + "(" + str(data[2]['victories']) + " Wins)"
                   + "\n#4 " + data[3]['username'] + "(" + str(data[3]['victories']) + " Wins)"
                   + "\n#5 " + data[4]['username'] + "(" + str(data[4]['victories']) + " Wins)"
                   + "\n#6 " + data[5]['username'] + "(" + str(data[5]['victories']) + " Wins)"
                   + "\n#7 " + data[6]['username'] + "(" + str(data[6]['victories']) + " Wins)"
                   + "\n#8 " + data[7]['username'] + "(" + str(data[7]['victories']) + " Wins)"
                   + "\n#9 " + data[8]['username'] + "(" + str(data[8]['victories']) + " Wins)"
                   + "\n#10 " + data[9]['username'] + "(" + str(data[9]['victories']) + " Wins)```")

@client.command()
async def botstats(ctx):
    await ctx.send("Bot is in " + str(len(client.guilds)) + " servers!")

@survivalgames.error
async def skywars_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Usage: ```html\nhive!survivalgames <Username>\n```")

@skywars.error
async def skywars_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Usage: ```html\nhive!skywars <Username>\n```")

@treasurewars.error
async def treasurewars_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Usage: ```html\nhive!treasurewars <Username>\n```")

@client.command()
async def invite(ctx):
    await ctx.send("**Hive stats bot (unofficial)**\nAdd to your server: "
                   "https://discord.com/api/oauth2/authorize?client_id=797497827118284860&permissions=8&scope=bot")

@client.command(aliases=['fb'])
async def feedback(ctx, *, message):
    owner = client.get_user(561492314862780427)
    channel = owner.create_dm
    owner.send(ctx.author.mention + " sent feedback: " + message)

@client.command()
async def help(ctx):
    await ctx.send("**Hive stats bot (unofficial)**"
                   "```html\nPrefix: hive!\n\n"
                   "skywars <Username> - view a player's skywars stats\n"
                   "treasurewars <Username> - view a player's treasure wars stats\n"
                   "survivalgames <Username> - view a player's survival games stats\n"
                   "skywarsleaderboard - check the top 10 skywars players (Beta)\n"
                   "help - view this\n"
                   "invite - add the bot to your server\n"
                   "botstats - check bot's stats```\n"
                   "**YOU NEED TO USE \"username with spaces\" IF A USERNAME HAS SPACES IN IT!**\n"
                   "Need help? https://discord.gg/sWxV7WajhW\n"
                   "\nCheck out Anata, our partner bot! <https://bit.ly/3nL4SYG>")

client.run(os.environ['token'])
