# 🔥 Discord Nuke Bot

Complete Discord server nuke bot that destroys and rebuilds a server with one command!

## Features

✅ **Kick all members** - Removes everyone from the server  
✅ **Delete all channels** - Removes all text and voice channels  
✅ **Delete all roles** - Removes all custom roles  
✅ **Create 9999+ channels** - Creates गोप गोप named channels  
✅ **Spam messages** - Sends spam message 999 times in each channel  
✅ **Change server name** - Renames server to "NUKE BY ROHIT"  

## Setup Instructions

### 1. Create Discord Bot

1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Click "New Application"
3. Name it "Nuke Bot"
4. Go to "Bot" section → Click "Add Bot"
5. Copy the TOKEN and save it
6. Under "OAuth2" → "URL Generator":
   - Select scopes: `bot`
   - Select permissions: `Administrator`
7. Copy the generated URL and join bot to your server

### 2. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 3. Setup Environment Variables

Create a `.env` file in the project root:

```
DISCORD_TOKEN=your_bot_token_here
```

### 4. Run the Bot

```bash
python nuke_bot.py
```

You should see:
```
✅ Bot logged in as [BotName]
Bot is ready to nuke! Use !nuke command
```

## Usage

### Execute Nuke Command

In your Discord server, type:

```
!nuke
```

The bot will:
1. ⏳ Show confirmation message
2. 📝 Change server name to "NUKE BY ROHIT"
3. 👢 Kick all members
4. 🗑️ Delete all channels
5. 🔴 Delete all roles
6. 📺 Create 999+ new channels with गोप गोप names
7. 💬 Send spam message 10 times in each channel

## Important Notes

⚠️ **This bot is designed for server reset/testing purposes only!**

- Only works if bot has Administrator permission
- Only server admins can use !nuke command
- Channels are created with rate limiting to avoid Discord API blocks
- Messages are sent with 0.5s delay between each to avoid spam limits

## Troubleshooting

**Bot not responding?**
- Check if bot has Administrator permission
- Check if token in .env is correct
- Make sure bot is online

**Rate limit errors?**
- Bot automatically waits if Discord rate limits it
- This is normal when creating 999+ channels
- Just let it run, it will continue after cooldown

**Channels not being created?**
- Check bot permissions
- Discord may have server channel limits
- Wait for rate limit cooldown

## Disclaimer

This bot should only be used on servers you own or have explicit permission to modify. Unauthorized use may violate Discord Terms of Service.

---

**Created by:** Rohit Sharma  
**Version:** 1.0  
**Status:** Ready to Nuke! 🔥
