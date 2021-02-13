import discord
import utils.ids as ids


async def activate(removed_roles, after):
    guild = after.guild
    removed_role = removed_roles[0]
    blacklisted_roles = ids.elventus_space
    for role in after.roles:
        if "Elventus " in role.name and role.id not in blacklisted_roles:
            return
    if "Elventus " in removed_role.name and removed_role.id not in blacklisted_roles:
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
        pairs = [(top_community,top_starter),(jungle_community,jungle_starter),(mid_community,mid_starter),(adc_community,adc_starter),(support_community,support_starter)]
        member_roles = after.roles.copy()
        for pair in pairs:
            if pair[1] in member_roles and pair[0] not in member_roles:
                member_roles.remove(pair[1])
                member_roles.append(pair[0])
        await after.edit(roles=member_roles)
        await after.send("Thanks for playing with " + removed_role.name + " if you could, please fill out this survey, it helps us to improve.  You can also use it to enroll in Elventus Vets, here you can find another team more quickly than a new recruit so that we can help you stay in circulation. Thanks again! https://forms.gle/if5DDwANvKADS6fH9")

    else:
        return