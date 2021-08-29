global wprize
wprize = None

from libs.custom_exceptions import UserAlreadyEnteredError, NoUsersEnteredError, WrongTimeFormatError
from discord_slash.utils.manage_commands import create_permission
from discord_slash.model import SlashCommandPermissionType
from discord_slash import SlashCommand
from discord.ext import commands
from datetime import datetime
import libs.parsetime as pt
from threading import Timer
import libs.database as db
from random import choice
from libs import poster
import discord
import asyncio

intents = discord.Intents().all()
client = commands.Bot(command_prefix="!", help_command=None, intents=intents)
slash = SlashCommand(client, sync_commands=True)
guild_ids = [869618049064525904]

print("Running")

async def get_lottery_result(wp):
    try:
        entries = db.get_all_values()
        winner = choice(entries)
        await poster.post_raffleended(client=client, guild_id=869618049064525904, member_id=881137802245472266, channel_name="lottery-posters", prize=wp, winner_id=winner)
    except NoUsersEnteredError:
        await poster.post_nowinnerended(client=client, guild_id=869618049064525904, member_id=881137802245472266, channel_name="lottery-posters", prize=wp)
    db.stop_raffle()
    db.remove_all()

def between_callback():
    client_loop = asyncio.new_event_loop()
    send_fut = asyncio.run_coroutine_threadsafe(get_lottery_result(), client_loop)
    # wait for the coroutine to finish
    send_fut.result()

@slash.slash(name="startraffle", description="This starts a raffle for a prize", guild_ids=guild_ids, permissions={
    869618049064525904: [
        create_permission(869618049064525904, SlashCommandPermissionType.ROLE, False),
        create_permission(881139338845499423, SlashCommandPermissionType.ROLE, True)
    ]})
async def startraffle(ctx, time, prize):
    timepresent = False
    wprize = prize
    if db.is_raffle_running() == "yes":
        await ctx.send("You already have a lottery running !")
    else:
        try:
            stime = pt.parse(time)
            db.start_raffle()
            await poster.post_rafflestarted(client=client, guild_id=869618049064525904, member_id=881137802245472266, channel_name="lottery-posters", prize=wprize, timeduration=time)
            await ctx.send("Done!")
            await asyncio.sleep(float(stime))
            await get_lottery_result(wprize)
        except WrongTimeFormatError:
            await ctx.send("Listen, you have one option. 1s is 1 second, 1m is 1 minute, 1h is 1 hour, 1d is 1 day and 1w is 1 week.")

@slash.slash(name="joinraffle", description="Joins a raffle", guild_ids=guild_ids, permissions={
    869618049064525904: [
        create_permission(869618049064525904, SlashCommandPermissionType.ROLE, False),
        create_permission(881169369206505492, SlashCommandPermissionType.ROLE, True),
        create_permission(881139338845499423, SlashCommandPermissionType.ROLE, True)
    ]})
async def joinraffle(ctx):
    entry = ctx.author.id
    if db.is_raffle_running() == "yes":
        try:
            db.add_user_to_raffle(str(entry))
            channel = discord.utils.get(client.get_guild(869618049064525904).text_channels, name="join-lottery")
            await channel.send(f"<@{entry}> has entered the lottery !")
            await ctx.send(f"<@{entry}> has entered the lottery !")
        except UserAlreadyEnteredError:
            await ctx.send("You already entered ! Wait for the next one")
    else:
        await ctx.send("Dude, wait for a lottery to start !")

@slash.slash(name="removeraffle", description="This removes the raffle", guild_ids=guild_ids, permissions={
    869618049064525904: [
        create_permission(869618049064525904, SlashCommandPermissionType.ROLE, False),
        create_permission(881139338845499423, SlashCommandPermissionType.ROLE, True)
    ]})
async def removeraffle(ctx):
    if db.is_raffle_running() == "yes":
        db.stop_raffle()
        db.remove_all()
        await ctx.send("Removed raffle")
    else:
        await ctx.send("Raffle not even started !")

@slash.slash(name="rafflestatus", description="The name speaks for it self", guild_ids=guild_ids)
async def lottery_status(ctx):
    await ctx.send(db.is_raffle_running())

@client.event
async def on_ready():
    print("Ready")

@client.event
async def on_message(ctx):
    pass

client.run(str(open(".env","r").read().replace("\n","")))