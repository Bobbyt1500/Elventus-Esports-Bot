import statistics
import discord
import utils.ids as ids

async def get_team_multi(team_category):
    """
    Returns multi link if found
    Returns None if not
    """
    records_channel = discord.utils.get(team_category.channels, name="records")
    message_history = await records_channel.history().flatten()

    for historic_message in message_history:
        split_message = historic_message.content.split()
        for word in split_message:
            if "na.op.gg" in word:
                return word
    
    # If no op.gg found
    return None

def get_team_category(guild, team_name):
    """
    Returns discord.py category object if found
    Returns None if not
    """
    for category in guild.categories:
        if "Elventus " in category.name:
            found_team_name = category.name.split("Elventus ")[1][:-2]
            if found_team_name == team_name:
                return category
    
    # If no matching category is found
    return None


def get_teams(guild):
    """
    Returns list of teams: (team_name, team_category)
    Example: ("Blue", discord.py_category)
    """
    teams = []
    for category in guild.categories:
        if "Elventus " in category.name:
            team_name = category.name.split("Elventus ")[1][:-2]
            teams.append((team_name, category))

    return teams

def get_team_captains(guild):
    """
    Returns dictionary mapping teams to team captains
    Example: "Blue" : discord.py_member
    """
    team_captains = {}

    # for each team
    for role in guild.roles:
        if "Elventus " in role.name and role.id not in ids.elventus_space:
            team_has_captain = False
            team = role.name.split("Elventus ")[1]

            # for each member on the team
            for member in role.members:
                for memberRole in member.roles:
                    # if they are a captain, add them to the list
                    if memberRole.id == ids.captain:
                        team_captains[team] = member
                        team_has_captain = True

            if team_has_captain is False:
                team_captains[team] = None

    return team_captains

def get_team_emojis(guild):
    """
    Returns a dictionary of team emojis
    """
    emojis = {}
    for category in guild.categories:
        if "Elventus " in category.name:
            team_name = category.name.split("Elventus ")[1][:-2]
            team_emoji = category.name[-1]
            emojis[team_name] = team_emoji
    
    return emojis



def get_team_ranks(guild):
    """
    Calculates and returns the average ranks of Elventus teams
    Returns dictionary mapping team names to rank strings
    Example: "Blue" : Diamond
    """
    ranks = {"Iron":0, "Bronze":1, "Silver":2, "Gold":3, "Platinum":4, "Diamond":5, "Master":6, "Grandmaster":7, "Challenger":8}
    team_ranks = {}

    # for each team
    for role in guild.roles:
        rank = None
        rank_found = False
        if "Elventus " in role.name and role.id not in ids.elventus_space:
            team = role.name.split("Elventus ")[1]

            # for each member on the team
            for member in role.members:
                ineligible_member = False
                for memberRole in member.roles:
                    # if they are a coach or sub, they don't count
                    if memberRole.id == ids.coach or memberRole.id == ids.sub:
                        ineligible_member = True
                        continue

                    if memberRole.name in ranks:
                        rank = memberRole.name

                if ineligible_member:
                    continue

                if rank is None:
                    continue

                if rank is not None:
                    rank_found = True
                    if team not in team_ranks.keys():
                        team_ranks[team] = [ranks[rank]]
                    else:
                        team_ranks[team].append(ranks[rank])

            if rank_found is False:
                team_ranks[team] = None

    ranks = ["Iron", "Bronze", "Silver", "Gold", "Platinum", "Diamond", "Master", "Grandmaster", "Challenger"]
    for team in team_ranks.keys():
        if team_ranks[team] is None:
            continue
        team_ranks[team] = ranks[round(statistics.mean(team_ranks[team]))]
    
    return team_ranks
