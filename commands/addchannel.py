import discord
import utils.ids as ids


async def activate(message, split_message):
    if len(split_message) != 2:
        await message.channel.send("Incorrect parameters")
        return
    if not message.channel.category:
        await message.channel.send("Not an acceptable channel for this command")
        return
    if "Anarchy" not in message.channel.category.name:
        await message.channel.send("Not an acceptable channel for this command")
        return
    guild = message.guild
    global captain_role
    captain_role = discord.utils.get(guild.roles, id=ids.captain)
    accepted_ids = ids.admins
    if captain_role not in message.author.roles and message.author.id not in accepted_ids:
        await message.channel.send("You are not a captain")
        return
    
    category = message.channel.category
    global everyone
    global role
    role = None
    everyone = discord.utils.get(guild.roles, id=ids.everyone)
    emoji = category.name[-1]
    teams_category = discord.utils.get(guild.categories, id=ids.teams_category)
    for channel in teams_category.channels:
        if channel.name[0] == emoji:
            team_name = channel.name.split("Anarchy ")[1]
            for guild_role in guild.roles:
                if team_name in guild_role.name:
                    role = guild_role

    if role == None:
        await message.channel.send("Error grabbing team role")
        return
    
    new_channel = await category.create_text_channel(split_message[1])
    await set_new_text_channel_perms(new_channel)

async def set_new_text_channel_perms(channel, message_history = True):
    overwrite = discord.PermissionOverwrite()
    overwrite.view_channel = False
    await channel.set_permissions(everyone, overwrite=overwrite)
    overwrite.view_channel = True
    overwrite.send_messages = True
    overwrite.read_messages = True
    if message_history:
        overwrite.read_message_history = True
    await channel.set_permissions(role, overwrite=overwrite)
    overwrite = discord.PermissionOverwrite()
    overwrite.manage_channels = True
    await channel.set_permissions(captain_role, overwrite=overwrite)
    