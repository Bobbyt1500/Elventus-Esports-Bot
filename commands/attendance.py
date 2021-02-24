import discord
import utils.ids as ids
import utils.ui

async def activate(message):
    guild = message.guild

    teams_category = discord.utils.get(guild.categories, id = ids.teams_category)
    attendance_channel = discord.utils.get(guild.text_channels, id = ids.attendance_channel)

    # Loop through voice channels creating embeds
    count = 0
    embed = utils.ui.new_embed_template()
    embed.title = "Attendance"
    for team_voice in teams_category.voice_channels:

        # If there are people in this channel
        if len(team_voice.members) != 0:
            # Build a string with all the members in the channel
            formatted_members_list = ""
            for member in team_voice.members:
                formatted_members_list += member.name + ","

            # Remove the last comma
            formatted_members_list = formatted_members_list[:-1]
        else:
            formatted_members_list = "None"

        embed.add_field(name=team_voice.name, value = formatted_members_list)
        count += 1

        # If there are 24 teams, make a new page
        if count == 24:
            await attendance_channel.send(embed=embed)
            embed = utils.ui.new_embed_template()
            embed.title = "Attendance"
            count = 0
    
    # Send last page if there is one
    if len(embed.fields) != 0:
        await attendance_channel.send(embed=embed)
