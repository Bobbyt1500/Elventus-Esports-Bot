import discord 
import utils.ids as ids
import utils.member

async def add_teammate(message, split_message):
    guild = message.guild
    captain = message.author

    # If they are not a valid captain
    if not utils.member.is_valid_captain(captain, guild):
        await message.channel.send("You do not have the permissions to do this")
        return

    teammate_id = int(split_message[1][3:-1])
    teammate = guild.get_member(teammate_id)

    # If teammate is not found
    if teammate is None:
        await message.channel.send("That person is not found")
        return
    
    teammate_team = utils.member.get_member_team(teammate)

    # If teammate is on a team
    if teammate_team != None:
        await message.channel.send("That person is already on a team")
        return
    
    team = utils.member.get_member_team(captain)
    team_role = discord.utils.get(guild.roles, name="Elventus " + team)

    # Add the role to the new teammate
    role_list = teammate.roles
    role_list.append(team_role)
    await teammate.edit(roles=role_list)



async def remove_teammate(message, split_message):
    guild = message.guild
    captain = message.author
    
    # If they are not a valid captain
    if not utils.member.is_valid_captain(captain, guild):
        await message.channel.send("You do not have the permissions to do this")
        return

    teammate_id = int(split_message[1][3:-1])
    teammate = guild.get_member(teammate_id)

    # If teammate is not found
    if teammate is None:
        await message.channel.send("That person is not found")
        return
    
    captain_team = utils.member.get_member_team(captain)
    teammate_team = utils.member.get_member_team(teammate)

    # If teammate is on a team
    if teammate_team != captain_team:
        await message.channel.send("That person is not on your team")
        return
    
    team_role = discord.utils.get(guild.roles, name="Elventus " + captain_team)

    # Remove the role from the teammate
    role_list = teammate.roles
    role_list.remove(team_role)
    await teammate.edit(roles=role_list)