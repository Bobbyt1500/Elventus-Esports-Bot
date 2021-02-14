import gspread
import os
import discord
import role_assign.role_assign as role_assign
import utils.ids as ids

async def update(guild):
    # Get spreadsheet data
    service_account = gspread.service_account(os.getenv("GOOGLE_CREDENTIALS"))
    spreadsheet = service_account.open_by_key(ids.applications_spread_key)
    worksheet = spreadsheet.get_worksheet(0)
    data = worksheet.get_all_values()

    lft_channel = discord.utils.get(guild.channels, id=ids.lft_channel)

    # Loop through data in reverse
    for i in range(len(data)-1, 0, -1):
        row = data[i]
        
        # Check for the timestamp * which means this cell has been seen before
        if row[0][-1] == "*":
            break

        # Mark this row as seen on the spreadsheet by adding a * to the timestamp
        worksheet.update_cell(i+1, 1, row[0] + "*")
        
        # Add roles for this person

        # Send message with reactions
        formatted_message = format_message(row, guild)
        sent = await lft_channel.send(formatted_message)
        await sent.add_reaction("👍")
        await sent.add_reaction("👎")
        await sent.add_reaction("❌")

def format_message(row, guild):
    name = row[1]
    discord_name = row[2]
    rank = row[6]
    position = row[7]
    op = row[9]

    # Get member mention if they are in the server
    disc_member = guild.get_member_named(discord_name)
    if disc_member != None:
        discord_name = disc_member.mention
    
    return "**Name:** " + name + " " + discord_name + " **Rank:** " + rank + " **Position:** " + position + " **OP.GG:** <" + op + ">"
        
async def add_roles(row):
    pass

            


    
