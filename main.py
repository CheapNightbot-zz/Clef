import os
from typing import Optional

from dotenv import load_dotenv
load_dotenv()
import dateutil.parser

import discord
from discord import app_commands

TOKEN = os.getenv("TOKEN")

class MyClient(discord.Client):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self) -> None:

        await self.tree.sync()
        print("Slash commands synced!")

intents = discord.Intents.default()
intents.members = True
intents.presences = True
client = MyClient(intents = intents)

# Even ~ 1 ~ on_ready
@client.event
async def on_ready():
    print('Bot is ready')


#Command ~ 1 ~ Ping
@client.tree.command()
async def ping(interaction: discord.Interaction):

    """Sends 'Pong' for no reason with latency (response time) in milliseconds"""

    await interaction.response.send_message(f"> Pong! (**Response Time** = {round(client.latency * 1000)}ms)")


#Command ~ 3 ~ Activity
@client.tree.command()
async def activity(interaction: discord.Interaction, member: Optional[discord.Member] = None):

    """See wat a member doin"""
    user = member or interaction.user
    member = user.guild.get_member(user.id)
    da_activity = next((activity for activity in member.activities), None)

    status = []
  
    if str(member.status) == "online":
        status = "https://cdn.discordapp.com/emojis/1008781589871874118.webp?size=44&quality=lossless"  #<:online:1008781589871874118>
      
    elif str(member.status) == "idle":
        status = "https://cdn.discordapp.com/emojis/1008782182308909058.webp?size=96&quality=lossless"  #<:idle:1008782182308909058>
      
    elif str(member.status) == "dnd":
        status = "https://cdn.discordapp.com/emojis/1008783135208644650.webp?size=96&quality=lossless"  #<:dnd:1008783135208644650>
      
    elif str(member.status) == "offline":
        status = "https://cdn.discordapp.com/emojis/1008784847306768484.webp?size=96&quality=lossless"  #<:invisible:1008784847306768484>

    else:
        status = "https://cdn.discordapp.com/emojis/1008830876534190170.webp?size=96&quality=lossless"  #<:streaming:1008830876534190170>

    if da_activity is None:

        embed1 = discord.Embed(
            title="",
            description=
            f'You are not doin anything... *__stap it, get some help!__* <:what_1:885289872032694353>'
        )
        embed1.set_author(name=f'{member.display_name}', icon_url=status)

        embed2 = discord.Embed(
            title="",
            description=
            f"**{member.display_name}** is doin nomthing.. (maybe watching some secrect sauce dat they don't wanna share?__<a:rickroll:933927394052567130>__) <:uhm:981696092179660801>"
        )
        embed2.set_author(name=f'{member.display_name}', icon_url=status)

        if member == interaction.user:
            await interaction.response.send_message(embed=embed1)
            return
        else:
            await interaction.response.send_message(embed=embed2)
            return

    doin = []
    if da_activity.type.value == 2:
        doin = "to"
    elif da_activity.type.value == 4:
        if str(da_activity.emoji) == "None":
            doin = f"status/doin"
        else:
            doin = f"status/doin **{da_activity.emoji}**"
    elif da_activity.type.value == 5:
        doin = "on"
    else:
        doin = "~"

    if str(da_activity.type.name) == "playing":
        ac_limg = []
        ac_st = []
        ac_dt = []
        g_type = []

        if "Game name" in str(da_activity.to_dict):
            ac_limg = "https://i.ibb.co/jbGRZrM/app-image.png"
        else:
            ac_limg = da_activity.large_image_url

        if "Game name" in str(da_activity.to_dict):
            ac_st = "None / Couldn't get!"
        else:
            ac_st = da_activity.state

        if "Game name" in str(da_activity.to_dict):
            ac_dt = "None / Couldn't get!"
        else:
            ac_dt = da_activity.details

        if "Game name" in str(da_activity.to_dict):
            g_type = "Playing"
        else:
            g_type = da_activity.type.name.capitalize()

        stamp = []
        if str(da_activity.start) == "None":
            stamp = "Couldn't get!"
        
        else:
            if int(da_activity._start) != 0:
                stamp_raw = f"{da_activity._start}"
                stamp_ra = stamp_raw[:-3]
                stamp = f"Started <t:{stamp_ra}:R>"
            else:
                stamp = "Couldn't get!"

        embed = discord.Embed(title="", description=f"{g_type} {doin} **{da_activity.name}**")
        embed.set_author(name=f'{member.display_name}', icon_url=status)
        embed.set_thumbnail(url=f"{ac_limg}")
        embed.add_field(name="State:", value=f"{ac_st}", inline=False)
        embed.add_field(name="Details:", value=f"{ac_dt}", inline=False)
        embed.add_field(name="Timestamp:", value=f"{stamp}")

    elif str(da_activity.type.name) == "streaming":
        platform = []
        videoID = []
        if "youtube" in str({da_activity.url}):
            platform = "YouTube"  #<:YouTube:1009145866197680159>
            url = da_activity.url
            videoID = url.split("watch?v=")[1].split("&")[0]
        else:
            platform = "Twitch"  #<:Twitch:1009145863429435522>
        embed = discord.Embed(
            title="",
            description=
            f"{da_activity.type.name.capitalize()} {doin} [**{da_activity.name}**]({da_activity.url})"
        )
        embed.set_author(name=f'{member.display_name}', icon_url=status)
        embed.add_field(name="Platform:", value=f"{platform} - <:YouTube:1009145866197680159>", inline=False)
        embed.add_field(name="Details:", value=f"{da_activity.details}", inline=False)
        embed.set_image(url=f"https://img.youtube.com/vi/{videoID}/maxresdefault.jpg".format(videoID=videoID))

    elif str(da_activity.type.name) == "listening":
        songurl = []
        thumb = []
        if str(da_activity.name) == "Spotify":
            songurl = f"https://open.spotify.com/track/{da_activity.track_id}"
            thumb = "https://cdn-icons.flaticon.com/png/512/2585/premium/2585161.png?token=exp=1661109514~hmac=0e40686fc50875d90b3e5d4edaf4d271"
        else:
            songurl = da_activity.url
            thumb = da_activity.large_image_url
        embed = discord.Embed(
            title="",
            description=
            f"{da_activity.type.name.capitalize()} {doin} **{da_activity.name}**"
        )
        embed.set_author(name=f'{member.display_name}', icon_url=status)
        embed.add_field(
            name="Details:",
            value=
            f"[{da_activity._details}]({songurl}) by {da_activity._state}",
            inline=False)
        embed.set_thumbnail(url=f"{thumb}")

    else:
        embed = discord.Embed(
            title="",
            description=
            f"{da_activity.type.name.capitalize()} {doin} **{da_activity.name}**"
        )
        embed.set_author(name=f'{member.display_name}', icon_url=status)

    await interaction.response.send_message(embed=embed)


#Command ~ 4 ~ Spotify track currently listening to
@client.tree.command()
async def track(interaction: discord.Interaction, member: Optional[discord.Member] = None):

    """Show information about currently listening track on Spotify"""
    user = member or interaction.user
    member = user.guild.get_member(user.id)
    spotify_result = next((activity for activity in member.activities if isinstance(activity, discord.Spotify)), None)
    
    if spotify_result is None:
            if member == interaction.user:
                await interaction.response.send_message(f'You are not even listening to Spotify! <:what_1:885289872032694353>')
                return
            else:
                await interaction.response.send_message(f'**{member.display_name}** is not listening to Spotify! <:uhm:981696092179660801>')
                return

    embed = discord.Embed(
        title=f'{spotify_result.title}',
        description="",
        url=f'https://open.spotify.com/track/{spotify_result.track_id}',
        color=spotify_result.color
    )

    embed.set_image(url=f"{spotify_result.album_cover_url}")
    # embed.set_thumbnail(url="https://i.ibb.co/R3qNYqc/spotify-logo-PNG3.png")
    embed.add_field(
        name="**Artist(s):**",
        value=f'{", ".join(spotify_result.artists)}',
        inline=False
    )
    embed.add_field(
        name="**Album:**",
        value=f'{spotify_result.album}',
        inline=False
    )
    embed.set_author(name=f'{member.display_name} is currently listening to:')
    embed.set_footer(text=f"Duration: {dateutil.parser.parse(str(spotify_result.duration)).strftime('%M:%S')}", icon_url="https://i.ibb.co/R3qNYqc/spotify-logo-PNG3.png")

    await interaction.response.send_message(embed=embed)


#Command ~ 5 ~ Lyrics?
@client.tree.command()
async def lyrics(interaction: discord.Interaction):

    """Get lyrics of any song [CURRENTLY NOT AVAILABLE]"""

    await interaction.response.send_message("**__CURRENTLY NOT AVAILABLE__**")


client.run(TOKEN)
