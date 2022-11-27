import os
from typing import Optional

from dotenv import load_dotenv
load_dotenv()

import dateutil.parser
import json
import requests

import discord
from discord import app_commands

TOKEN = os.getenv("TOKEN")

class MyClient(discord.Client):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    # Don't need to sync command everytime.
    # Use when you make changes to slash command itself.
    # async def setup_hook(self) -> None:

    #     await self.tree.sync()
    #     print("Slash commands synced!")

intents = discord.Intents.default()
intents.members = True
intents.presences = True
client = MyClient(intents = intents)

# Event ~ 0 ~ on_ready
@client.event
async def on_ready():
    print('Bot is ready')


#Command ~ 0 ~ Ping
@client.tree.command()
async def ping(interaction: discord.Interaction):

    """Sends 'Pong' for no reason with latency (response time) in milliseconds"""

    await interaction.response.send_message(f"> Pong! (**Response Time** = {round(client.latency * 1000)}ms)")


#Command ~ 1 ~ Activity
@client.tree.command()
@app_commands.describe(member="The member you want to get the activity of; defaults to the user who uses the command")
async def activity(interaction: discord.Interaction, member: Optional[discord.Member] = None):

    """See wat a member doin 👀"""
    user = member or interaction.user
    member = user.guild.get_member(user.id)
    da_activity = next((activity for activity in member.activities), None)

    # Checking for user status (online, idle, etc...) and
    # storing relevant image to empty list called `status`.
    status = [] # Empty list of user status
  
    if str(member.status) == "online":
        status = "https://cdn.discordapp.com/emojis/1008781589871874118.webp?size=44&quality=lossless"
      
    elif str(member.status) == "idle":
        status = "https://cdn.discordapp.com/emojis/1008782182308909058.webp?size=96&quality=lossless"
      
    elif str(member.status) == "dnd":
        status = "https://cdn.discordapp.com/emojis/1008783135208644650.webp?size=96&quality=lossless"
      
    elif str(member.status) == "offline":
        status = "https://cdn.discordapp.com/emojis/1008784847306768484.webp?size=96&quality=lossless"

    else:
        status = "https://cdn.discordapp.com/emojis/1008830876534190170.webp?size=96&quality=lossless"

    # If user/member is not doing any activity,
    # then the following `if` statement will execute
    # otherwise it will be skipped.
    if da_activity is None:

        embed1 = discord.Embed(
            title="",
            description=
            f'You are not doin anything... *__stap it, get some help!__* <:happycheems:980237883527008298>'
        )
        embed1.set_author(name=f'{member.display_name}', icon_url=status)

        embed2 = discord.Embed(
            title="",
            description=
            f"**{member.display_name}** is doin nomthing.. (maybe watching some secrect sauce dat they don't wanna share?__<a:rickroll:933927394052567130>__) <:uhm:981696092179660801>"
        )
        embed2.set_author(name=f'{member.display_name}', icon_url=status)

        # Checking if member requested activity for themselves
        # or for another member, then send respectivily `embed1` and `embed2`
        if member == interaction.user:
            await interaction.response.send_message(embed=embed1)
            return
        else:
            await interaction.response.send_message(embed=embed2)
            return

    # Just comparing the activity type to add suffix to activity type in embed:
    # For example; if `activity.type.value == 2` (which means "Listening"
    # - see the Discord documentation: https://discord.com/developers/docs/game-sdk/activities#data-models-activitytype-enum)
    # then `doin_type` will be "to" & it will send "Listening to"
    doin_type = []

    # If acitivity type is "Listening", then
    # set `doin_type` value to "to".
    if da_activity.type.value == 2: # Listening
        doin_type = "to"

    # If acitivity type is "Custom", then
    # set `doin_type` value to "status/doin + [status_emoji]".
    elif da_activity.type.value == 4: # Custom

        if str(da_activity.emoji) == "None":
            doin_type = f"status/doin"
        else:
            doin_type = f"status/doin **{da_activity.emoji}**"

    # If acitivity type is "Competing", then
    # set `doin_type` value to "on".
    elif da_activity.type.value == 5: # Competing
        doin_type = "on"

    # If nothing is true above, then set `doin_type`
    # value to "~".
    else:
        doin_type = "~"

    # If acitivity type is "Playing", then
    # get activity details, status, large image, type
    # and store in empty lists.
    if str(da_activity.type.name) == "playing":
        ac_limg = [] # Activity large image
        ac_st = [] # Activity status
        ac_dt = [] # Activity details
        ac_type = [] # Activity type

        # If user have added a game manually as activity
        # then `member.activity.name` is "Game name" instead
        # of just "name". So, we checking if `member.activity.to_dict`
        # contains "Game name", then probably it will not have large image,
        # so just use the default image provided here, else get large image
        # using `member.activity.large_image_url`. Same for details, etc. (makes sense?)
        if "Game name" in str(da_activity.to_dict):
            ac_limg = "https://i.ibb.co/jbGRZrM/app-image.png"
            ac_st = "None / Couldn't get!"
            ac_dt = "None / Couldn't get!"
            ac_type = "Playing"
        else:
            ac_limg = da_activity.large_image_url
            ac_st = da_activity.state
            ac_dt = da_activity.details
            ac_type = da_activity.type.name.capitalize()

        # Getting activity timestamp & storing it in
        # an empty list "stamp".
        stamp = []

        # Not all acitivies will have start time and
        # it gives error and breaks whole code,
        # that's why doing `try - except` to pass any error
        # by just setting "stamp" value to "Couldn't get!"
        try:
            if str(da_activity.start) == "None":
                stamp = "Couldn't get!"
            
            else:
                # This one is like hack for me, I don't really
                # know WHY! Idk, but I tried getting timestamp
                # using `activity.start`, but it returns "None".
                # So, instead I used `activity._start`; which technically
                # returns activity start time in epochs, but with
                # extra 3 number in the end. So simply I'm storing
                # `activity._start` value in `stamp_raw` and than removing
                # last three number from it than adding the `stamp_raw`
                # value into Discord's Timestamp format for "Relative Time".
                # makes sense?
                if int(da_activity._start) != 0:
                    stamp_raw = f"{da_activity._start}"
                    stamp_ra = stamp_raw[:-3]
                    stamp = f"Started <t:{stamp_ra}:R>"
                else:
                    stamp = "Couldn't get!"
        except:
            stamp = "Couldn't get!"

        # Embed for "Playing" type activity (basically for games).
        embed = discord.Embed(title="", description=f"{ac_type} {doin_type} **{da_activity.name}**")
        embed.set_author(name=f'{member.display_name}', icon_url=status)
        embed.set_thumbnail(url=f"{ac_limg}")
        embed.add_field(name="State:", value=f"{ac_st}", inline=False)
        embed.add_field(name="Details:", value=f"{ac_dt}", inline=False)
        embed.add_field(name="Timestamp:", value=f"{stamp}")

    # If acitivity type is "Streaming", then
    # get activity details; platform, videoID (youtube only)
    # and store in empty lists.
    elif str(da_activity.type.name) == "streaming":
        platform = []
        videoID = []
        if "youtube" in str({da_activity.url}):
            platform = "YouTube"
            url = da_activity.url
            videoID = url.split("watch?v=")[1].split("&")[0] # spliting url to get video id, idk Google it xD
        else:
            platform = "Twitch"

        # Embed for "Streaming" type activity.
        embed = discord.Embed(title="", description = f"{da_activity.type.name.capitalize()} {doin_type} [**{da_activity.name}**]({da_activity.url})")
        embed.set_author(name=f'{member.display_name}', icon_url=status)
        embed.add_field(name="Platform:", value=f"{platform} - <:YouTube:1009145866197680159>", inline=False)
        embed.add_field(name="Details:", value=f"{da_activity.details}", inline=False)
        embed.set_image(url=f"https://img.youtube.com/vi/{videoID}/maxresdefault.jpg".format(videoID=videoID))

    # If acitivity type is "Listening", then
    # get activity details; song url, album art
    # and store in empty lists.
    elif str(da_activity.type.name) == "listening":
        songurl = []
        thumb = []

        # Please don't ask anything... 😶‍🌫️
        if str(da_activity.name) == "Spotify":
            songurl = f"https://open.spotify.com/track/{da_activity.track_id}"
            thumb = f"{da_activity.album_cover_url}"
        else:
            songurl = da_activity.url
            thumb = da_activity.large_image_url
        
        # Embed for "Listening" type activity.
        embed = discord.Embed(title="", description=f"{da_activity.type.name.capitalize()} {doin_type} **{da_activity.name}**")
        embed.set_author(name=f'{member.display_name}', icon_url=status)
        embed.add_field(name="Details:", value=f"[{da_activity._details}]({songurl}) by {da_activity._state}", inline=False)
        embed.set_thumbnail(url=f"{thumb}")

    # If user/member is not doing any activity,
    # then there can be a custom status, so this will
    # send that with emoji (if there's any).
    else:
        embed = discord.Embed(title="", description=f"{da_activity.type.name.capitalize()} {doin_type} **{da_activity.name}**")
        embed.set_author(name=f'{member.display_name}', icon_url=status)

    await interaction.response.send_message(embed=embed) # finally sending embed(s).


#Command ~ 2 ~ Spotify track currently listening to
# It's not dat hard... Don't say anything! 😶
@client.tree.command()
@app_commands.describe(member="The member you want to get the track from; defaults to the user who uses the command")
async def track(interaction: discord.Interaction, member: Optional[discord.Member] = None):

    """Show information about currently listening track on Spotify"""
    user = member or interaction.user
    member = user.guild.get_member(user.id)
    spotify_result = next((activity for activity in member.activities if isinstance(activity, discord.Spotify)), None)
    
    if spotify_result is None:
            if member == interaction.user:
                await interaction.response.send_message(f'You are not even listening to Spotify! <:happycheems:980237883527008298>')
                return
            else:
                await interaction.response.send_message(f'**{member.display_name}** is not listening to Spotify! <:uhm:981696092179660801>')
                return

    embed = discord.Embed(title=f'{spotify_result.title}', description="", url=f'https://open.spotify.com/track/{spotify_result.track_id}', color=spotify_result.color)
    embed.set_image(url=f"{spotify_result.album_cover_url}")
    # embed.set_thumbnail(url="https://i.ibb.co/R3qNYqc/spotify-logo-PNG3.png")
    embed.add_field(name="**Artist(s):**", value=f'{", ".join(spotify_result.artists)}', inline=False)
    embed.add_field(name="**Album:**", value=f'{spotify_result.album}', inline=False)
    embed.set_author(name=f'{member.display_name} is currently listening to:')
    embed.set_footer(text=f"Duration: {dateutil.parser.parse(str(spotify_result.duration)).strftime('%M:%S')}", icon_url="https://i.ibb.co/R3qNYqc/spotify-logo-PNG3.png")

    await interaction.response.send_message(embed=embed)


#Command ~ 3 ~ Lyrics?
@client.tree.command()
@app_commands.checks.cooldown(1, 120, key=lambda i: (i.guild_id)) # cooldown
@app_commands.describe(member="The member you want to get the track from; defaults to the user who uses the command")
async def lyrics(interaction: discord.Interaction, member: Optional[discord.Member] = None):

    """Get lyrics of Currently playing song on Spotify (1 lyrics every 2 minutes)"""
    user = member or interaction.user
    member = user.guild.get_member(user.id)
    spotify_result = next((activity for activity in member.activities if isinstance(activity, discord.Spotify)), None)
    
    if spotify_result is None:
            if member == interaction.user:
                await interaction.response.send_message(f'You are not even listening to Spotify! <:happycheems:980237883527008298>')
                return
            else:
                await interaction.response.send_message(f'**{member.display_name}** is not listening to Spotify! <:uhm:981696092179660801>')
                return

    Track = spotify_result.title # Song Name
    Artist = spotify_result.artist # Artist Name

    # Thanks to this guy on GitHub for simple API: https://github.com/asrvd
    # API GitHub page: https://github.com/asrvd/lyrist
    response = requests.get(f"https://lyrist.vercel.app/api/:{Track}/:{Artist}") # Fetching lyrics from api.
    lyrics_raw = response.json() # Converting fetched lyrics/data into JSON file.

    # Creating list of all keynames from "lyrics_raw"
    # json file than checking if certain keynames exists
    # in that list.
    keyname = list(lyrics_raw.keys())
    if "lyrics" in keyname:
        lyrics = lyrics_raw['lyrics'] # Getting the value of choosen key name (in this case "lyrics").
        source = lyrics_raw['source']

    elif "error" in keyname:
        lyrics = lyrics_raw['error'] # Getting the value of choosen key name (in this case "error").

    embed = discord.Embed(title=f'{spotify_result.title}', description=f"{lyrics}", url=f'https://open.spotify.com/track/{spotify_result.track_id}', color=spotify_result.color)
    embed.set_thumbnail(url=f"{spotify_result.album_cover_url}")
    embed.set_author(name=f'Lyrics of currently playing song:')
    embed.set_footer(text=f"Source: {source}", icon_url="https://i.ibb.co/R3qNYqc/spotify-logo-PNG3.png")

    await interaction.response.send_message(embed=embed)

# Lyrics command on cooldown error handler
@lyrics.error
async def on_test_error(interaction: discord.Interaction, error: app_commands.AppCommandError):
    if isinstance(error, app_commands.CommandOnCooldown):
        custom_error = str(error).replace("You are", "This command is")
        await interaction.response.send_message(str(custom_error), ephemeral=True)

client.run(TOKEN)
