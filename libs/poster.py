import discord
import random

async def post_rafflestarted(client, guild_id, member_id, channel_name: str, prize: str, timeduration: str):
    member = client.get_guild(guild_id).get_member(member_id)
    channel = discord.utils.get(client.get_guild(guild_id).text_channels, name=channel_name)
    embed=discord.Embed(title="Lottery Started", description=str(f"To enter, run /join in raffle-enteries channel !"))
    embed.colour = discord.Colour.from_rgb(random.randint(0,255),random.randint(0,255),random.randint(0,255))
    embed.set_author(name=str(member.name), icon_url=str(member.avatar_url))
    #embed.set_thumbnail(url="https://media.discordapp.net/attachments/872709016088883240/876357345926586388/R_3.png?width=427&height=427")
    embed.add_field(name=f"Prize: ", value=str(prize), inline=False)
    embed.add_field(name="Raffle ends in: ", value=str(timeduration), inline=False)
    embed.set_footer(text=str("Made by RushanNotOfficial#1146"))
    await channel.send("@everyone", embed=embed)
    return embed

async def post_raffleended(client, guild_id, member_id, channel_name: str, prize: str, winner_id):
    winner = client.get_guild(guild_id).get_member(winner_id)
    member = client.get_guild(guild_id).get_member(member_id)
    channel = discord.utils.get(client.get_guild(guild_id).text_channels, name=channel_name)
    embed=discord.Embed(title="Lottery has ended", description=str(f"Make sure to enter next time !"))
    embed.colour = discord.Colour.from_rgb(random.randint(0,255),random.randint(0,255),random.randint(0,255))
    embed.set_author(name=str(member.name), icon_url=str(member.avatar_url))
    #embed.set_thumbnail(url="https://media.discordapp.net/attachments/872709016088883240/876357345926586388/R_3.png?width=427&height=427")
    embed.add_field(name=f"Prize: ", value=str(prize), inline=False)
    embed.add_field(name="Winner: ", value=str(f"<@{winner_id}>"), inline=False)
    embed.set_footer(text=str("Made by RushanNotOfficial#1146"))
    await channel.send("@everyone", embed=embed)
    return embed

async def post_nowinnerended(client, guild_id, member_id, channel_name: str, prize: str):
    #winner = client.get_guild(guild_id).get_member(winner_id)
    member = client.get_guild(guild_id).get_member(member_id)
    channel = discord.utils.get(client.get_guild(guild_id).text_channels, name=channel_name)
    embed=discord.Embed(title="Lottery has ended", description=str(f"Make sure to enter next time !"))
    embed.colour = discord.Colour.from_rgb(random.randint(0,255),random.randint(0,255),random.randint(0,255))
    embed.set_author(name=str(member.name), icon_url=str(member.avatar_url))
    #embed.set_thumbnail(url="https://media.discordapp.net/attachments/872709016088883240/876357345926586388/R_3.png?width=427&height=427")
    embed.add_field(name=f"Prize: ", value=str(prize), inline=False)
    embed.add_field(name="Winner: ", value=str(f"No one entered lol"), inline=False)
    embed.set_footer(text=str("Made by RushanNotOfficial#1146"))
    await channel.send("@everyone", embed=embed)
    return embed