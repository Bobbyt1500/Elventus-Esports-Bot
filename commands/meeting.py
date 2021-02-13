import discord
import utils.ids as ids


async def activate(message):
    accepted_ids = ids.admins
    if message.author.id not in accepted_ids: 
        await message.channel.send("Yargh Matey, ye don’t be lookin like the captain. Best be movin before ye walk the plank.")
        return

    team_category = discord.utils.get(message.guild.categories, id=ids.teams_category)
    channels = team_category.channels
    meeting_channel = discord.utils.get(message.guild.channels, id=ids.meeting_channel)

    for channel in channels:
        for member in channel.members:
            await member.move_to(meeting_channel)
    
    await message.add_reaction("✅")


