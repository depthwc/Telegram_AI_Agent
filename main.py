import os
import requests
import telebot
from dotenv import load_dotenv

load_dotenv(".env")

url = os.getenv("url")
api_key = os.getenv("api_key")
bot_api = os.getenv("bot_api")
model = os.getenv("model")

bot = telebot.TeleBot(bot_api)

bot_info = bot.get_me()

bot.set_my_commands([
    telebot.types.BotCommand("ask", "Ask the AI a question"),
])

def is_bot_mentioned(message):
    """Check if bot is mentioned via @username using Telegram entities (reliable in groups)."""
    if not message.entities:
        return False
    for entity in message.entities:
        if entity.type == "mention":
            mention = message.text[entity.offset: entity.offset + entity.length]
            if mention.lower() == f"@{bot_info.username.lower()}":
                return True
    return False


def query_ai(msgs):
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    response = requests.post(url, headers=headers, json={
        "model": model,
        "messages": msgs,
        "stream": False
    })
    return response.json()["choices"][0]["message"]["content"]


def build_and_reply(message, user_text):
    """Build message list with optional reply-context and query AI."""
    msgs = [{"role": "system", "content": "Answer short"}]

    # History: only from the message being replied to
    if message.reply_to_message and message.reply_to_message.text:
        if message.reply_to_message.from_user.id == bot_info.id:
            msgs.append({"role": "assistant", "content": message.reply_to_message.text})
        else:
            msgs.append({"role": "user", "content": message.reply_to_message.text})

    if user_text:
        msgs.append({"role": "user", "content": user_text})

    if len(msgs) <= 1:
        return  # Only system prompt, nothing to ask

    bot.send_chat_action(message.chat.id, 'typing')
    try:
        reply_content = query_ai(msgs)
        bot.reply_to(message, reply_content)
    except Exception as e:
        bot.reply_to(message, f"Error reaching local AI: {str(e)}")


# /ask and /call commands — work in groups even with privacy mode ON
@bot.message_handler(commands=["ask"])
def handle_ask_command(message):
    user_text = message.text.partition(" ")[2].strip()
    build_and_reply(message, user_text)


@bot.message_handler(func=lambda message: True)
def handle_message(message):
    if not message.text:
        return

    is_private = message.chat.type == "private"
    is_reply_to_bot = (
        message.reply_to_message is not None
        and message.reply_to_message.from_user is not None
        and message.reply_to_message.from_user.id == bot_info.id
    )
    mentioned = is_bot_mentioned(message)

    if not (is_private or is_reply_to_bot or mentioned):
        return

    user_text = message.text
    if mentioned:
        user_text = user_text.replace(f"@{bot_info.username}", "").strip()

    build_and_reply(message, user_text)


print(f"Bot @{bot_info.username} is polling... Press Ctrl+C to stop.")
bot.infinity_polling(timeout=30, long_polling_timeout=30)