from pyrogram import Client, filters
from pyrogram.types import ChatMemberStatus
from config import API_ID, API_HASH, BOT_TOKEN
import database

app = Client("prgram_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# ========== START ==========
@app.on_message(filters.command("start") & filters.private)
def start(client, message):
    message.reply_text(
        "👋 Hello!\n\n"
        "➕ Mujhe apne group me add karo aur admin banao.\n\n"
        "Admin commands:\n"
        "/setchannel @channelname\n"
        "/forcejoin on\n"
        "/forcejoin off"
    )

# ========== SET CHANNEL ==========
@app.on_message(filters.command("setchannel") & filters.group)
def set_channel(client, message):
    if not message.from_user or not message.from_user.is_admin:
        return message.reply_text("❌ Sirf admin use kar sakta hai.")

    if len(message.command) < 2:
        return message.reply_text("Usage: /setchannel @channelname")

    channel = message.command[1]
    database.set_force_channel(message.chat.id, channel)
    message.reply_text(f"✅ Force join channel set: {channel}")

# ========== FORCEJOIN ON/OFF ==========
@app.on_message(filters.command("forcejoin") & filters.group)
def forcejoin_cmd(client, message):
    if not message.from_user or not message.from_user.is_admin:
        return message.reply_text("❌ Sirf admin use kar sakta hai.")

    if len(message.command) < 2:
        return message.reply_text("Usage: /forcejoin on/off")

    arg = message.command[1].lower()

    if arg == "on":
        database.set_force_join(message.chat.id, True)
        message.reply_text("✅ Force Join ENABLED")
    elif arg == "off":
        database.set_force_join(message.chat.id, False)
        message.reply_text("❌ Force Join DISABLED")
    else:
        message.reply_text("Usage: /forcejoin on/off")

# ========== MESSAGE CHECK ==========
@app.on_message(filters.group & filters.text)
def check_force_join(client, message):
    group = database.get_group(message.chat.id)

    if not group["force_join"]:
        return

    channel = group["force_channel"]
    if not channel:
        return

    try:
        member = client.get_chat_member(channel, message.from_user.id)
        if member.status in ["member", "administrator", "owner"]:
            return
    except:
        pass

    try:
        message.delete()
    except:
        pass

    message.reply_text(
        f"🚫 **Access Denied!**\n\n"
        f"👉 Pehle hamara channel join karo:\n"
        f"🔗 {channel}\n\n"
        "✅ Join karne ke baad yahan message bhejo."
    )

# ========== RUN ==========
print("Bot is running...")
app.run()
