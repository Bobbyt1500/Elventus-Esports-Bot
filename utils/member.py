import utils.ids as ids
import discord

def get_member_team(member):
    """
    Returns team emoji if member is on a team
    Returns None if member does not have a team
    """
    team_role = None
    for role in member.roles:
        if "Elventus " in role.name and role.id not in ids.elventus_space:
            team_role = role
            break
    
    if team_role is None:
        return None
    else:
        return team_role.name.split("Elventus ")[1]

def is_valid_captain(member, guild):
    captain_role = discord.utils.get(guild.roles, id=ids.captain)
    team = get_member_team(member)

    # If they are not a captain
    if captain_role not in member.roles:
        return False
    
    # If they do not have a team
    if team is None:
        return False
    
    return True