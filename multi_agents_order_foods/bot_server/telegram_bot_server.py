import os
import telebot
from pydantic import BaseModel
import json
import asyncio
from dotenv import load_dotenv
import telebot.async_telebot


# Load environment variables
load_dotenv()

# Load menu data
def load_menu(menu_filepath):
    """Loads menu data from a JSON file"""
    with open(menu_filepath, "r") as f:
        menu = json.load(f)
    return menu


# Initialize Telegram bot
BOT_TOKEN = os.getenv("BOT_TOKEN")
# bot = telebot.TeleBot(BOT_TOKEN)
bot = telebot.async_telebot.AsyncTeleBot(BOT_TOKEN)

# Define a model for incoming webhook payloads
class UpdateModel(BaseModel):
    update_id: int
    message: dict = None
    edited_message: dict = None

# Bot command handlers
@bot.message_handler(commands=["start"])
async def start_handler(message):
    try:
        menu = load_menu("multi_agents_order_foods/menu_list/menu_oioi_fastfood.json")
        menu_str = "🍽️ *Menu*\n"
        for category in menu["menu"]:
            menu_str += f"\n*{category['category']}*\n"
            for item in category["items"]:
                menu_str += f"  - {item['icon']} {item['name']} - ${item['price']:.2f}\n"
        await bot.reply_to(message, f"Hello! I'm a food ordering bot from *OiOi Fastfood*. Here is the menu:", parse_mode="Markdown")
        await bot.send_message(message.chat.id, menu_str, parse_mode="Markdown")
        await bot.send_message(message.chat.id, "Please type the name of the item you want to order.")
        await bot.reply_to(message, str(message.chat.id))
    except Exception as e:
        await bot.reply_to(message, f"Error: {e}")


asyncio.run(bot.polling())