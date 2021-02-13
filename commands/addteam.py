import discord
import utils.ids as ids


async def activate(message, split_message, scrim_scheduler):
    if len(split_message) != 3:
        await message.channel.send("Please provide all parameters")
        return

    emoji = split_message[2]
    if len(emoji) != 1:
        await message.channel.send("Not a valid emoji")
        return
    
    guild = message.guild
    new_team_name = split_message[1]

    #Roles
    captain = discord.utils.get(guild.roles, id=ids.captain)
    roster_manager = discord.utils.get(guild.roles, id=ids.roster_manager)
    everyone = discord.utils.get(guild.roles, id=ids.everyone)

    # Make sure user trying to run command has permissions
    accepted_ids = ids.admins
    if message.author.id not in accepted_ids and roster_manager not in message.author.roles: 
        await message.channel.send("Not enough permissions")
        return

    # Create new team role
    new_team_role = await guild.create_role(name="Elventus " + new_team_name, hoist=True, mentionable = True)

    # Create private category
    new_category = await guild.create_category(new_team_role.name + " " + emoji)

    chat = await new_category.create_text_channel("chat")
    records = await new_category.create_text_channel("records")
    pickban = await new_category.create_text_channel("pickban")
    agenda = await new_category.create_text_channel("agenda")
    vc = await new_category.create_voice_channel("voice-chat")

    #VC set everyone no perms
    overwrite = discord.PermissionOverwrite()
    overwrite.view_channel = False
    overwrite.connect = False
    await vc.set_permissions(everyone, overwrite = overwrite)

    # VC set extra captain perms
    overwrite = discord.PermissionOverwrite()
    overwrite.move_members = True
    await vc.set_permissions(captain, overwrite=overwrite)

    # VC set role perms
    overwrite = discord.PermissionOverwrite()
    overwrite.connect = True
    overwrite.view_channel = True
    await vc.set_permissions(new_team_role, overwrite=overwrite)


    # Set chat perms
    await set_new_text_channel_perms(chat, everyone, new_team_role)

    # Set records perms
    await set_new_text_channel_perms(records, everyone, new_team_role)

    # Set pickban perms
    await set_new_text_channel_perms(pickban, everyone, new_team_role)

    # Set agenda perms
    await set_new_text_channel_perms(agenda, everyone, new_team_role)

    # Set up scrim scheduler for new team
    await scrim_scheduler.add_team(new_team_name, new_category)

async def set_new_text_channel_perms(channel, everyone, role):
    # Set perms for @everyone
    overwrite = discord.PermissionOverwrite()
    overwrite.view_channel = False
    await channel.set_permissions(everyone, overwrite=overwrite)
    # Set perms for team role
    overwrite.view_channel = True
    overwrite.send_messages = True
    overwrite.read_messages = True
    overwrite.read_message_history = True
    await channel.set_permissions(role, overwrite=overwrite)