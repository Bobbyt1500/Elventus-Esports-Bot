import discord
import utils.ids as ids

async def activate(guild):
    """
    Handles the auto creation and deletion of General Voice channels
    """
    voice_category = discord.utils.get(guild.categories, id=ids.voice_category)
    
    # [amount of channels, amount of channels with users]
    uncapped = [0,0]
    duo = [0,0]
    five = [0,0]

    for channel in voice_category.voice_channels:
        if channel.name == "Uncapped":
            if len(channel.members) > 0:
                uncapped[1] += 1
            uncapped[0] += 1
        elif channel.name == "Duo Queue":
            if len(channel.members) > 0:
                duo[1] += 1
            duo[0] += 1
        elif channel.name == "Five Queue":
            if len(channel.members) > 0:
                five[1] += 1
            five[0] += 1
    
    await update_channels(uncapped, "Uncapped", voice_category, 0, guild)
    await update_channels(duo, "Duo Queue", voice_category, 2, guild)
    await update_channels(five, "Five Queue", voice_category, 5, guild)

    
async def update_channels(channel_amounts, channel_name, voice_category, user_limit, guild):
    """
    Adds or removes a General Voice channel if needed
    """
    number_excess = channel_amounts[0] - channel_amounts[1]

    if number_excess == 0:
        new_vc = await voice_category.create_voice_channel(channel_name)

        everyone = discord.utils.get(guild.roles, id=ids.everyone)
        starter = discord.utils.get(guild.roles, id=ids.starter)
        community = discord.utils.get(guild.roles, id=ids.community)
    
        #VC set everyone no perms
        overwrite = discord.PermissionOverwrite()
        overwrite.view_channel = False
        overwrite.connect = False
        await new_vc.set_permissions(everyone, overwrite = overwrite)

        # VC set community and starter perms
        overwrite.view_channel = True
        overwrite.connect = True
        overwrite.speak = True
        await new_vc.set_permissions(starter, overwrite = overwrite)
        await new_vc.set_permissions(community, overwrite = overwrite)

        # VC set user limit
        position = get_new_position(channel_name, voice_category)
        await new_vc.edit(user_limit=user_limit,position=position)
    elif number_excess > 1:
        for channel in voice_category.voice_channels:
            if channel.name == channel_name and len(channel.members) == 0:
                await channel.delete()
                return

def get_new_position(channel_name, voice_category):
    """
    Returns the position of a new channel in the General Voice category based on the name
    """

    for channel in voice_category.channels:
        if channel.name == channel_name:
            return channel.position



    
