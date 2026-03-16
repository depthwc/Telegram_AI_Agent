A Telegram bot that connects to an AI API to answer questions and have conversations right in Telegram.

## Features

- **AI-Powered Responses**: Queries a local or remote AI model for intelligent answers
- **Smart Message Detection**: Works in private chats, group chats via mentions, and replies to bot messages
- **Context Awareness**: Maintains conversation context by referencing replied-to messages
- **Typing Indicators**: Shows typing status while processing queries
- **/ask Command**: Dedicated command to ask the AI questions

## Setup

1. Create a `.env` file with the following variables:
   - `url`: Your AI API endpoint
   - `api_key`: Authorization key for the AI API
   - `bot_api`: Your Telegram bot token
   - `model`: The AI model to use

2. Install dependencies:
   ```bash
   pip install pyTelegramBotAPI requests python-dotenv
   ```

3. Run the bot:
   ```bash
   python main.py
   ```