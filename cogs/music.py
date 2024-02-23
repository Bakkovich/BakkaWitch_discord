import traceback
from logging import DEBUG, getLogger
from os import getenv
from typing import TYPE_CHECKING, Any
import disnake
from bot import Alexbot
from disnake import Intents, Interaction, Member
from disnake.ext import commands

from mafic import NodePool, Player, Playlist, Track, TrackEndEvent

if TYPE_CHECKING:
    from disnake.abc import Connectable

getLogger("mafic").setLevel(DEBUG)

bot = Alexbot
class MyPlayer(Player[Alexbot]):
    def __init__(self, client: Alexbot, channel: disnake.VoiceChannel) -> None:
        super().__init__(client, channel)
        self.bot = bot
        # Mafic does not provide a queue system right now, low priority.
        self.queue: list[Track] = []


@bot.slash_command(dm_permission=False)
async def join(inter: disnake.GuildCommandInteraction):
    """Join your voice channel."""
    

    if not inter.author.voice or not inter.author.voice.channel:
        return await inter.response.send_message("You are not in a voice channel.")

    channel = inter.author.voice.channel

    # This apparently **must** only be `Client`.
    await channel.connect(cls=MyPlayer)  # pyright: ignore[reportGeneralTypeIssues]
    await inter.send(f"Joined {channel.mention}.")


@bot.slash_command(dm_permission=False)
async def play(inter: disnake.GuildCommandInteraction, query: str):
    """Play a song.

    query:
        The song to search or play.
    """
    

    if not inter.guild.voice_client:
        await join(inter)

    player: MyPlayer = (
        inter.guild.voice_client
    )  # pyright: ignore[reportGeneralTypeIssues]

    tracks = await player.fetch_tracks(query)
    if not tracks:
        return await inter.send("No tracks found.")

    if isinstance(tracks, Playlist):
        tracks = tracks.tracks
        if len(tracks) > 1:
            player.queue.extend(tracks[1:])
    
    track = tracks[0]
    

    await player.play(track)
        
    await inter.send(f"Playing [{track.title}]({track.uri})")

@bot.slash_command(description="Stop the music")
async def stop(inter:disnake.GuildCommandInteraction):
    try:
        await inter.guild.voice_client.disconnect()
        
        
        await inter.send("Disconnected.", ephemeral=True)
    except:
        await inter.send("Not disconnected.", ephemeral=True)
    try:
        await inter.guild.voice_client.cleanup()
    except:
        pass
@bot.listen()
async def on_track_end(event: TrackEndEvent):
    assert isinstance(event.player, MyPlayer)

    if event.player.queue:
        await event.player.play(event.player.queue.pop(0))


STATS = """```
Uptime: {uptime}
Memory: {used:.0f}MiB : {free:.0f}MiB / {allocated:.0f}MiB -- {reservable:.0f}MiB
CPU: {system_load:.2f}% : {lavalink_load:.2f}%
Players: {player_count}
Playing Players: {playing_player_count}
```"""

# Пока что отключил
# def setup(bot: commands.Bot):
#     bot.add_cog(MyPlayer(bot))
