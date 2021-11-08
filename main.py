print("Loading...")
from dotenv import load_dotenv
import discord
from discord.ext import commands
import json
import os
import sys
print(f"[DONE] Loaded Discord version `{discord.version_info}`!")
print("Fetching data from env file...")
load_dotenv()
token = os.getenv("token")
try:
    status = os.getenv("status")
    if status:
        print(f"[+] Got status `{status}` from .env!")
    else:
        print(f"[-] No status set, so booting without it")
except:
    print("[!] Tried to get status from .env file, failed")
if not token:
    print("Please give a token in your .env!")
    sys.exit(1)
print("Done! Loaded data from token.")
print("Loading intents & config...")

bot = commands.Bot(intents=discord.Intents.all(), command_prefix=".", fetch_offline_members=False, chunk_guilds_at_startup=False, case_insensitive=True, max_messages=100000, help_command=None)
print("[DONE] Intents loaded!")

print("Loading cogs...")
cogs = ['cogs.translate', 'cogs.admin', 'cogs.help']

for cog in cogs:
    try:
        bot.load_extension(cog)
        print(f"[+] {cog} loaded!")
    except Exception as x:
        print('[!] Failed to load cog {}\n{}: {}'.format(cog, type(x).__name__, x))
        sys.exit(1)

print("[DONE] Cogs loaded!")
print("Pre-flight checks complete, now taking off...")
print("""
  ##   #   # #    # #####    ##   #    # ##### ###### 
 #  #   # #  #    # #    #  #  #  ##   #   #   #      
#    #   #   #    # #    # #    # # #  #   #   #####  
######   #   #    # #    # ###### #  # #   #   #      
#    #   #   #    # #    # #    # #   ##   #   #      
#    #   #    ####  #####  #    # #    #   #   ######
""")


@bot.event
async def on_ready():
    command_names_list = []
    for x in bot.commands:
        command_names_list.append(x.name)
    print('Username: ' + bot.user.name)
    print('ID: ' + str(bot.user.id))
    if status:
        print(f"Using status: {status} from .env")
    else:
        print("Using status: none")
    print('-'*25)
    print(f"Started with commands:")
    for x in command_names_list:
        print(f"[+] `{x}`")
    print("\n")
    print("The bot has started and is ready!")
    try:
        import systemd.daemon
        systemd.daemon.notify('READY=1')
        print("[+] Notified systemd the process has started")
    except Exception as e:
        print(f"[!] Could notify systemd that the process has started: {e}")
    if status:
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=status))

bot.run(token)
