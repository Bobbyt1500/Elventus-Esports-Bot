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
        if row[7][-1] == "*":
            break

        # Mark this row as seen on the spreadsheet by adding a * to the timestamp
        worksheet.update_cell(i+1, 8, row[7] + "*")
        
        # Add roles for this person
        await add_roles(row, guild)        

        # Send message with reactions
        formatted_message = format_message(row, guild)
        sent = await lft_channel.send(formatted_message)
        await sent.add_reaction("👍")
        await sent.add_reaction("👎")
        await sent.add_reaction("❌")

def format_message(row, guild):
    name = row[1]
    discord_name = row[0]
    rank = row[2]
    position = row[3]
    op = row[4]

    # Get member mention if they are in the server
    disc_member = guild.get_member_named(discord_name)
    if disc_member != None:
        discord_name = disc_member.mention
    
    return "**Name:** " + name + " " + discord_name + " **Rank:** " + rank + " **Position:** " + position + " **OP.GG:** <" + op + ">"
        
async def add_roles(row, guild):
    discord_name = row[0]
    rank = row[2]
    position = row[3]

    rank_indicies = {"Challenger":0,"Grandmaster":1,"Master":2,"D1":3,"D2":3,"D3":3,"D4":3,"P1":4,"P2":4,"P3":4,"P4":4,"G1":5,"G2":5,"G3":5,"G4":5,"S1":6,"S2":6,"S3":6,"S4":6}
    position_indicies = {"Top":0,"Jungle":1,"Mid":2,"ADC":3,"Support":4}

    disc_member = guild.get_member_named(discord_name)
    # Cannot assign roles if this person is not in the discord
    if disc_member == None:
        return
    
    # Use the role assign functions to assign roles to this member
    await role_assign.update_position(position_indicies[position], guild, disc_member)
    await role_assign.update_rank(rank_indicies[rank], guild, disc_member)

            


    
