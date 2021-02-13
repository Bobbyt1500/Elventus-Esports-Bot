import discord
import utils.ids as ids
import utils.ui

ranks = ["Challenger","Grandmaster","Master","Diamond","Platinum","Gold","Silver","Bronze","Iron"]
positions = ["Top", "Jungle", "Mid", "Bot","Support"]

async def send_menus(message, general_dbinter):
    guild = message.guild
    server_access_channel = discord.utils.get(guild.channels, id=ids.server_access_channel)
    menu_ids = []
    
    # Create Ranks Menu
    rank_emojis = []
    embed = utils.ui.new_embed_template()
    embed.title = "Access the server (part 1):"
    embed.description = "React with your rank"

    for r in ranks:
        emoji = discord.utils.get(guild.emojis, name=r.lower())
        rank_emojis.append(emoji)
        embed.add_field(name=r,value=emoji)
    
    sent_message = await server_access_channel.send(embed=embed)
    menu_ids.append(sent_message.id)

    for e in rank_emojis:
        await sent_message.add_reaction(e)

    # Create positions menu
    position_emojis = []
    embed = utils.ui.new_embed_template()
    embed.title = "Access the server (part 2):"
    embed.description = "React with your role(s)"

    for p in positions:
        emoji = discord.utils.get(guild.emojis, name=p.lower())
        position_emojis.append(emoji)
        embed.add_field(name=p,value=emoji,inline=False)
    
    sent_message = await server_access_channel.send(embed=embed)
    menu_ids.append(sent_message.id)

    for e in position_emojis:
        await sent_message.add_reaction(e)

    # Create sub menu
    embed = utils.ui.new_embed_template()
    embed.title = "Become an Elventus Substitute 🔄?"
    embed.description = "Disclaimer: Subs may receive 5 pings a week or more but will find a team faster."
    
    sent_message = await server_access_channel.send(embed=embed)
    menu_ids.append(sent_message.id)

    await sent_message.add_reaction("❌")
    await sent_message.add_reaction("🔄")

    general_dbinter.replace_role_assign_ids(menu_ids)
    
    
async def invite_handler(payload, guilds):
    guild = discord.utils.get(guilds, id=ids.guild)
    emoji = payload.emoji.name

    # Call rank update handler if emoji was a rank
    rank_index = 0
    for r in ranks:
        if r.lower() == emoji:
            await update_rank(rank_index, guild, payload.member)
        rank_index += 1
    
    # Call position update handler if emoji was a position
    position_index = 0
    for p in positions:
        if p.lower() == emoji:
            await update_position(position_index, guild, payload.member)
        position_index += 1
    
    # Convert member to sub
    if emoji == "🔄":
        await convert_to_sub(payload.member, guild)
    # Convert sub to member
    if emoji == "❌":
        await convert_to_member(payload.member, guild)

async def convert_to_member(member, guild):
    roles_list = member.roles
    
    # Create an inverted mapping of positions
    sub_community_map = {}
    
    for key in ids.community_sub_map.keys():
        sub_community_map[ids.community_sub_map[key]] = key
    

    # Adjust roles
    roles_to_remove = []

    for role in roles_list:
        # Remove sub role
        if role.id == ids.sub:
            roles_to_remove.append(role)

        # Change community positions to sub positions
        if role.id in sub_community_map.keys():
            roles_to_remove.append(role)
            roles_list.append(discord.utils.get(guild.roles, id=sub_community_map[role.id]))
    
    for role in roles_to_remove:
        roles_list.remove(role)
    
    await member.edit(roles=roles_list)

async def convert_to_sub(member, guild):
    roles_list = member.roles

    # Make sure member has community role
    community = False
    for role in roles_list:
        if role.id == ids.community:
            community = True
    
    if not community:
        await member.send("Please fill out part 1 and part 2 before becoming a sub.")
        return
    
    # Adjust roles
    roles_to_remove = []

    for role in roles_list:
        # Add sub role
        if role.id == ids.community:
            roles_list.append(discord.utils.get(guild.roles, id=ids.sub))

        # Change community positions to sub positions
        if role.id in ids.community_sub_map.keys():
            roles_to_remove.append(role)
            roles_list.append(discord.utils.get(guild.roles, id=ids.community_sub_map[role.id]))
    
    for role in roles_to_remove:
        roles_list.remove(role)
    
    await member.edit(roles=roles_list)


async def update_rank(rank_index, guild, member):
    roles_list = member.roles
    
    community = False
    needs_community = False
    for role in roles_list:
        # Check if member has community
        if role.id == ids.community:
            community = True
        
        # Check if member needs community
        if role.id in ids.community_positions:
            needs_community = True

        # Remove old rank if applicable 
        if role.id in ids.ranks:
            roles_list.remove(role)

    # Add new rank
    new_rank_role = discord.utils.get(guild.roles, id=ids.ranks[rank_index])
    roles_list.append(new_rank_role)

    # Add community if needed
    if not community and needs_community:
        roles_list.append(discord.utils.get(guild.roles, id=ids.community))


    await member.edit(roles=roles_list)
    
    

async def update_position(position_index, guild, member):
    roles_list = member.roles

    
    sub = False
    needs_community = False
    community = False
    for role in roles_list:
        # Check if they already have community
        if role.id == ids.community:
            community = True
        
        # Check if they need community
        if role.id in ids.ranks:
            needs_community = True


        # Check if they need sub version of position roles
        if role.id == ids.sub:
            sub = True
    
    # Add new role
    if sub:
        new_position_role = discord.utils.get(guild.roles,id=ids.sub_positions[position_index])
    else:
        new_position_role = discord.utils.get(guild.roles,id=ids.community_positions[position_index])

    roles_list.append(new_position_role)

    # Remove any possible duplicates
    roles_list = list(set(roles_list))

    # Add community if needed
    if not sub and not community and needs_community:
        roles_list.append(discord.utils.get(guild.roles, id=ids.community))

    await member.edit(roles=roles_list)

async def remove_position(payload, guilds):
    guild = discord.utils.get(guilds, id=ids.guild)
    emoji = payload.emoji.name
    member = discord.utils.get(guild.members, id=payload.user_id)

    position_index = 0
    for p in positions:
        if p.lower() == emoji:
            break
        position_index += 1
    
    roles_list = member.roles

    for role in roles_list:
        if role.id == ids.community_positions[position_index] or role.id == ids.sub_positions[position_index]:
            roles_list.remove(role)
    
    await member.edit(roles=roles_list)

    



    

