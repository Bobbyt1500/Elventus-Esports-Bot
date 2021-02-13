import discord

def new_embed_template():
    elventus_color = discord.Color.from_rgb(2, 152, 222)
    embed = discord.Embed(color=elventus_color)
    embed.set_thumbnail(url="https://elventus.com/wp-content/uploads/2020/09/logo-elventus-white-all-1024x194.png")
    return embed