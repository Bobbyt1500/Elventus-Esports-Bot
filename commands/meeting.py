import discord
import utils.ids as ids


async def activate(message):
    accepted_ids = ids.admins
    if message.author.id not in accepted_ids: 
        await message.channel.send("You do not have enough permissions!")
        return

    channels = message.guild.voice_channels
    meeting_channel = discord.utils.get(message.guild.channels, id=ids.meeting_channel)

    # Move all members to the meeting channel
    for channel in channels:
        # Ignore meeting channel
        if channel == meeting_channel:
            return

        for member in channel.members:
            await member.move_to(meeting_channel)
    
    await message.add_reaction("✅")


