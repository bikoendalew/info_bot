"""
Telegram Bot to list users and their information
"""

import json
import os
from datetime import datetime
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

# Load environment variables
load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
ADMIN_USER_ID = int(os.getenv("ADMIN_USER_ID", "0"))
USERS_FILE = "users_data.json"


# Utility functions
def load_users():
    """Load users from JSON file"""
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_users(users):
    """Save users to JSON file"""
    with open(USERS_FILE, "w", encoding="utf-8") as f:
        json.dump(users, f, indent=2, ensure_ascii=False)


def format_user_info(user_id, user_data):
    """Format user information for display"""
    return f"""
👤 **User Information**
├─ Account ID: `{user_id}`
├─ Username: @{user_data.get('username', 'Not set')}
├─ Name: {user_data.get('first_name', '')} {user_data.get('last_name', '')}
├─ Language: {user_data.get('language_code', 'Not set')}
├─ Premium: {'✅ Yes' if user_data.get('is_premium') else '❌ No'}
└─ Joined: {user_data.get('joined_date', 'Unknown')}
"""


def format_users_list(users):
    """Format all users as a list"""
    if not users:
        return "No users registered yet."

    message = "📊 **Registered Users List**\n\n"
    message += f"Total Users: {len(users)}\n\n"
    message += "```\n"
    message += f"{'ID':<15} | {'Username':<20} | {'Name':<25} | {'Lang'} | {'Premium'}\n"
    message += "-" * 85 + "\n"

    for user_id, user_data in users.items():
        username = user_data.get("username", "N/A")
        name = (
            f"{user_data.get('first_name', '')} {user_data.get('last_name', '')}"
        ).strip()
        lang = user_data.get("language_code", "N/A")
        premium = "✓" if user_data.get("is_premium") else "✗"

        # Truncate long values
        username = (username[:18] + "..") if len(username) > 20 else username
        name = (name[:23] + "..") if len(name) > 25 else name

        message += f"{user_id:<15} | {username:<20} | {name:<25} | {lang:<4} | {premium}\n"

    message += "```"
    return message


def format_users_detailed(users):
    """Format all users with detailed information"""
    if not users:
        return "No users registered yet."

    message = "📋 **Detailed Users List**\n\n"

    for user_id, user_data in users.items():
        message += format_user_info(user_id, user_data)
        message += "\n"

    return message


# Command handlers
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command"""
    user = update.effective_user
    users = load_users()

    # Store user information
    user_id = str(user.id)
    users[user_id] = {
        "id": user.id,
        "username": user.username or "Not set",
        "first_name": user.first_name or "",
        "last_name": user.last_name or "",
        "language_code": user.language_code or "Not set",
        "is_premium": user.is_premium,
        "joined_date": datetime.now().isoformat(),
    }
    save_users(users)

    welcome_message = f"""
Hello {user.first_name}! 👋

I'm a bot that tracks and lists user information. Here are my commands:

/start - Show this welcome message
/myinfo - Show your information
/list - Show all registered users (simple list)
/listdetail - Show all registered users (detailed view)
/stats - Show user statistics
/help - Show help message
"""
    await update.message.reply_text(welcome_message)


async def myinfo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show user's own information"""
    user = update.effective_user
    users = load_users()
    user_id = str(user.id)

    if user_id in users:
        user_data = users[user_id]
        message = "ℹ️ Your Information:\n" + format_user_info(user_id, user_data)
    else:
        message = "You are not registered yet. Use /start to register."

    await update.message.reply_text(message, parse_mode="Markdown")


async def list_users(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """List all registered users in simple format"""
    users = load_users()
    message = format_users_list(users)
    await update.message.reply_text(message, parse_mode="Markdown")


async def list_users_detailed(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """List all registered users in detailed format"""
    users = load_users()
    message = format_users_detailed(users)

    # Split message if too long (Telegram limit is 4096 characters)
    if len(message) > 4000:
        # Send first part
        await update.message.reply_text(
            message[:4000], parse_mode="Markdown"
        )
        # Send remaining parts
        remaining = message[4000:]
        while len(remaining) > 0:
            await update.message.reply_text(
                remaining[:4000], parse_mode="Markdown"
            )
            remaining = remaining[4000:]
    else:
        await update.message.reply_text(message, parse_mode="Markdown")


async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show user statistics"""
    users = load_users()

    if not users:
        await update.message.reply_text("No users registered yet.")
        return

    total_users = len(users)
    premium_users = sum(1 for u in users.values() if u.get("is_premium"))
    users_with_username = sum(
        1 for u in users.values() if u.get("username") and u.get("username") != "Not set"
    )

    stats_message = f"""
📈 **User Statistics**

├─ Total Users: {total_users}
├─ Premium Users: {premium_users} ({(premium_users/total_users*100):.1f}%)
├─ Users with Username: {users_with_username} ({(users_with_username/total_users*100):.1f}%)
└─ Data Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
    await update.message.reply_text(stats_message, parse_mode="Markdown")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show help message"""
    help_text = """
🤖 **User Info Bot - Help**

**Commands:**
/start - Register and see welcome message
/myinfo - View your user information
/list - View all users (simple format)
/listdetail - View all users (detailed format)
/stats - View user statistics
/help - Show this help message

**User Information Tracked:**
• Account ID - Your unique Telegram ID
• Username - Your Telegram username
• First Name & Last Name - Your profile name
• Language Code - Your Telegram language setting
• Premium Status - If you have Telegram Premium

**Note:**
User data is stored locally in JSON format.
"""
    await update.message.reply_text(help_text, parse_mode="Markdown")


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle regular messages"""
    message = update.message.text.lower()

    if message.startswith("/"):
        await update.message.reply_text(
            "Unknown command. Use /help to see available commands."
        )
    else:
        await update.message.reply_text(
            "I'm a bot that tracks user information. Use /help to see my commands."
        )


def main():
    """Main function to start the bot"""
    # Check if token is set
    if not TELEGRAM_BOT_TOKEN:
        print("Error: TELEGRAM_BOT_TOKEN not set in .env file")
        return

    # Create application
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    # Add command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("myinfo", myinfo))
    application.add_handler(CommandHandler("list", list_users))
    application.add_handler(CommandHandler("listdetail", list_users_detailed))
    application.add_handler(CommandHandler("stats", stats))
    application.add_handler(CommandHandler("help", help_command))

    # Add message handler for unknown commands
    application.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)
    )

    # Start bot
    print("🤖 Bot started. Press Ctrl+C to stop.")
    application.run_polling()


if __name__ == "__main__":
    main()
