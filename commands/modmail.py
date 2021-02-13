import discord
import utils.ids as ids

async def activate(message, guilds):
    if message.author.id == ids.bot_id:
        return
    guild = discord.utils.get(guilds, id=ids.guild)
    modmail = discord.utils.get(guild.channels, id=ids.modmail_channel)

    embed = discord.Embed(title=message.author.name + "#"+message.author.discriminator)
    embed.add_field(name="Question:",value=message.content)

    await modmail.send(embed=embed)
    await message.channel.send("Question sent to Staff and Moderators")

