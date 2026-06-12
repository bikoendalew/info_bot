# Telegram User Info Bot

A simple Telegram bot that tracks and displays user information including Account ID, username, names, language code, and premium status.

## Features

- ✅ Track user information automatically on /start
- ✅ Display user's own information
- ✅ List all registered users
- ✅ View detailed user information
- ✅ User statistics
- ✅ Persistent data storage (JSON)

## Requirements

- Python 3.8+
- python-telegram-bot library
- python-dotenv

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Create Bot on Telegram

1. Open Telegram and search for `@BotFather`
2. Use `/newbot` command to create a new bot
3. Copy your bot token

### 3. Configure Environment Variables

Create a `.env` file in the project root:

```bash
cp .env.example .env
```

Edit `.env` and add:
```
TELEGRAM_BOT_TOKEN=your_bot_token_here
ADMIN_USER_ID=your_user_id_here
```

### 4. Run the Bot

```bash
python bot.py
```

## Commands

- `/start` - Register and view welcome message
- `/myinfo` - View your user information
- `/list` - View all registered users (simple format)
- `/listdetail` - View all registered users (detailed format)
- `/stats` - View user statistics
- `/help` - Show help message

## User Information Tracked

The bot collects and displays the following information:

- **Account ID** (`id`) - Unique Telegram user ID (e.g., 123456789)
- **Username** (`@username`) - Telegram handle (if set)
- **First Name & Last Name** - User's profile name
- **Language Code** (e.g., `en`, `am`) - Telegram language preference
- **Premium Status** (`is_premium`) - Whether user has Telegram Premium

## Data Storage

User data is stored in `users_data.json` in JSON format. Example:

```json
{
  "123456789": {
    "id": 123456789,
    "username": "john_doe",
    "first_name": "John",
    "last_name": "Doe",
    "language_code": "en",
    "is_premium": true,
    "joined_date": "2024-01-15T10:30:45.123456"
  }
}
```

## Project Structure

```
info_bot/
├── bot.py                 # Main bot script
├── requirements.txt       # Python dependencies
├── .env.example          # Example environment variables
├── .gitignore            # Git ignore rules
├── README.md             # This file
└── users_data.json       # User data (auto-generated)
```

## License

MIT License

## Support

For issues or questions, please check the Telegram Bot API documentation:
https://core.telegram.org/bots/api
