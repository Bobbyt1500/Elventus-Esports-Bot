import discord
import utils.ids as ids


async def activate(message):
    if not message.channel.category:
        await message.channel.send("Not an acceptable channel for this command")
        return
    if "Anarchy" not in message.channel.category.name:
        await message.channel.send("Not an acceptable channel for this command")
        return
    guild = message.guild
    captain_role = discord.utils.get(guild.roles, id=ids.captain)
    accepted_ids = ids.admins
    if captain_role not in message.author.roles and message.author.id not in accepted_ids:
        await message.channel.send("You are not a captain")
        return
    
    await message.channel.delete()