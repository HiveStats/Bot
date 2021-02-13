import discord
import requests
import json
import os  # for heroku
import dbl
from discord.ext import commands

intents = discord.Intents(messages = True, guilds = True, reactions = True, members = True, presences = True)
client = commands.Bot(command_prefix = ['Hive!', 'hive!'], intents = intents)
client.remove_command("help")
dbl_client = dbl.DBLClient(client, "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6Ijc5NzQ5NzgyNzExODI4NDg2MCIsImJvdCI6dHJ1ZSwiaWF0IjoxNjEzMjQwNDE1fQ.JopXgJkPCcWxfhnE4qRrsupUEqVkP3p9F3hUKgxF4Jw", True)

@client.event
async def on_ready():
    print("Bot running on {0.user}!".format(client))
    await client.change_presence(activity=discord.Activity(name='for hive!help', type=3))


@client.command()
async def checkvote(ctx):
    support_server = client.get_guild("798959430162448404")
    await ctx.send("Checking...")
    has_ctx_user_voted = await dbl_client.get_user_vote(ctx.message.author.id)
    if has_ctx_user_voted:
        if ctx.message.author in support_server.members:
            ctx.send("You voted! You've been given the voter role in our server!")
            await ctx.message.author.add_roles(support_server.get_role("810218550425944064"))
        else:
            await ctx.send("You voted, but you're not in our support server! You should join! https://discord.com/invite/FpY5FUSFXq")
    else:
        await ctx.send("You didn't vote, please vote at https://top.gg/bot/797497827118284860/vote!")

@client.command()
async def asay(ctx, *, message):
    if ctx.message.author.id == 561492314862780427:
        await ctx.send("**Hive stats bot (unofficial)**\n```ahk\nMessage from an admin of this bot!\n\"" + message + "\"```")
    else:
        await ctx.send("Damn son! where'd you find this?")

@client.command(aliases=['sw'])
async def skywars(ctx, username):  # register command
    print("Connecting to api.playhive.com...")
    print("Requested Username: " + username)
    print("Requested Game: Skywars")
    json_data = requests.get("https://api.playhive.com/v0/game/all/sky/" + username)  # lookup player data
    print("Connected! Response status code: " + str(json_data.status_code))
    print("JSON: " + str(json_data.json()))  # print JSON in console
    data = json.loads(json_data.text)  # convert JSON to python dict
    print("Python dict:")
    print(data)  # print python dict to console
    print("Data type: " + str(type(data)))  # print data type to console (confirming if it is a dict)
    losses = data["played"] - data["victories"]  # calculate losses
    win_loss = (data["victories"] / data["played"]) * 100  # calculate win rate
    kdr = data["kills"] / losses  # calculate KDR
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
async def pvp(ctx, username):
    print("Connecting to api.playhive.com...")
    print("Requested Game: Total Kills")
    sg_json_data = requests.get("https://api.playhive.com/v0/game/all/sg/" + username)
    sw_json_data = requests.get("https://api.playhive.com/v0/game/all/sky/" + username)
    tw_json_data = requests.get("https://api.playhive.com/v0/game/all/wars/" + username)
    print("Connected! got all sg, sky and wars data for player!")
    sg_data = json.loads(sg_json_data.text)
    sw_data = json.loads(sw_json_data.text)
    tw_data = json.loads(tw_json_data.text)
    total_kills = sg_data['kills'] + sw_data['kills'] + tw_data['kills']
    sw_deaths = sw_data['played'] - sw_data['victories']
    sg_deaths = sg_data['played'] - sg_data['victories']
    total_deaths = sw_deaths + sg_deaths + tw_data['deaths']
    total_kdr = total_kills / total_deaths
    await ctx.send("**Whole-network PvP stats for " + username + "**\n```py\nKills: " + str(total_kills) + "\nDeaths: " + str(total_deaths) + "\nKDR: " + str(total_kdr) + "```\nStats for the entire Hive network.")

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

@pvp.error
async def pvp_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Usage: ```html\nhive!pvp <Username>\n```")

@client.command(aliases=['fb'])
async def feedback(ctx, *, message):
    owner = client.get_user(561492314862780427)
    await owner.send(ctx.author.name + "#" + str(ctx.author.discriminator) + "(" + str(ctx.author.id) + ")" " sent feedback: " + message)
    await ctx.send("**Hive stats bot (unofficial)**\n```ahk\nFeedback sent! Thanks!\n\"" + message + "\"\nPlease don\'t spam it!```")

@feedback.error
async def feedback_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Usage: ```html\nhive!feedback <Message>\n```")

@asay.error
async def asay_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Usage: ```html\nhive!asay <Message>\n```")

@client.command()
async def help(ctx):
    await ctx.send("**Hive stats bot (unofficial)**"
                   "```html\nPrefix: hive!\n\n"
                   "skywars <Username> - view a player's skywars stats\n"
                   "treasurewars <Username> - view a player's treasure wars stats\n"
                   "survivalgames <Username> - view a player's survival games stats\n"
                   "skywarsleaderboard - check the top 10 skywars players\n"
                   "treasurewarsleaderboard - check the top 10 treasure wars players\n"
                   "survivalgamesleaderboard - check the top 10 survival games players\n"
                   "pvp <Username> - check a player's whole network kills, deaths and KDR\n"
                   "help - view this\n"
                   "invite - add the bot to your server\n"
                   "botstats - check bot's stats\n"
                   "feedback <Message> - send me some feedback on what to add/change with the bot```\n"
                   "**YOU NEED TO USE \"username with spaces\" IF A USERNAME HAS SPACES IN IT!**\n"
                   "Need help? https://discord.gg/sWxV7WajhW\n"
                   "\nCheck out Anata, our partner bot! <https://bit.ly/3nL4SYG>")

client.run(os.environ['token'])
