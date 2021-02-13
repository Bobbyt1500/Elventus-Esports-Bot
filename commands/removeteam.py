import discord
import utils.ids as ids
import utils.team


async def activate(message, split_message, scrim_scheduler):
    if len(split_message) != 2:
        await message.channel.send("Please provide all parameters")
        return
    
    accepted_ids = ids.admins
    if message.author.id not in accepted_ids: 
        await message.channel.send("Not enough permissions")
        return

    guild = message.guild
    role_id = split_message[1][3:-1]

    role = discord.utils.get(guild.roles, id=int(role_id))
    team_name = role.name.split("Elventus ")[1]

    teams_category = utils.team.get_team_category(guild, team_name)

    # Remove the teams channels
    for category_channel in teams_category.channels:
        await category_channel.delete()
    await teams_category.delete()
    
    # Remove the teams role
    await role.delete()

    # Remove the team from the scrim scheduler
    await scrim_scheduler.remove_team(team_name)




