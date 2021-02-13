import discord
import utils.ids as ids

async def activate(added_roles, after):
    guild = after.guild
    new_role = added_roles[0]
    blacklisted_roles = ids.elventus_space
    if "Elventus " in new_role.name and new_role.id not in blacklisted_roles:
        starter = discord.utils.get(guild.roles, id=ids.starter)
        top_starter = discord.utils.get(guild.roles, id=ids.top_starter)
        jungle_starter = discord.utils.get(guild.roles, id=ids.jungle_starter)
        mid_starter = discord.utils.get(guild.roles, id=ids.mid_starter)
        adc_starter = discord.utils.get(guild.roles, id=ids.adc_starter)
        support_starter = discord.utils.get(guild.roles, id=ids.support_starter)
        community = discord.utils.get(guild.roles, id=ids.community)
        top_community = discord.utils.get(guild.roles, id=ids.top_community)
        jungle_community = discord.utils.get(guild.roles, id=ids.jungle_community)
        mid_community = discord.utils.get(guild.roles, id=ids.mid_community)
        adc_community = discord.utils.get(guild.roles, id=ids.adc_community)
        support_community = discord.utils.get(guild.roles, id=ids.support_community)
        sub = discord.utils.get(guild.roles, id=ids.sub)
        top_sub = discord.utils.get(guild.roles, id=ids.top_sub)
        jungle_sub = discord.utils.get(guild.roles, id=ids.jungle_sub)
        mid_sub = discord.utils.get(guild.roles, id=ids.mid_sub)
        adc_sub = discord.utils.get(guild.roles, id=ids.adc_sub)
        support_sub = discord.utils.get(guild.roles, id=ids.support_sub)
        pairs = [(community,starter),(top_community,top_starter),(jungle_community,jungle_starter),(mid_community,mid_starter),(adc_community,adc_starter),(support_community,support_starter),(top_sub,top_starter),(jungle_sub,jungle_starter),(mid_sub,mid_starter),(adc_sub,adc_starter),(support_sub,support_starter)]
        member_roles = after.roles.copy()
        for pair in pairs:
            if pair[0] in member_roles and pair[1] not in member_roles:
                member_roles.remove(pair[0])
                member_roles.append(pair[1])
        if sub in member_roles:
            member_roles.remove(sub)
        await after.edit(roles=member_roles)

    else:
        return
    