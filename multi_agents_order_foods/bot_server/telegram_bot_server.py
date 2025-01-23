import os
import telebot
from fastapi import FastAPI, Request
from pydantic import BaseModel
import json
from dotenv import load_dotenv


# Load environment variables
load_dotenv()

# Load menu data
def load_menu(menu_filepath):
    with open(menu_filepath, "r") as f:
        menu = json.load(f)
    return menu


# Initialize FastAPI app and Telegram bot
app = FastAPI()
BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)

# Define a model for incoming webhook payloads
class UpdateModel(BaseModel):
    update_id: int
    message: dict = None
    edited_message: dict = None

# Webhook route
@app.post("/webhook")
async def webhook(update: UpdateModel):
    try:
        # Process incomming Telegram update
        json_data = update.model_dump()
        bot.process_new_updates([telebot.types.Update.de_json(json_data)])
    except Exception as e:
        print(f"Error processing update: {e}")
    return {"ok": True}

# Bot command handler
@bot.message_handler(commands=["start"])
def start_handler(message):
    try:
        menu = load_menu("multi_agents_order_foods/menu_list/menu_oioi_fastfood.json")
        menu_str = "🍽️ *Menu*\n"
        for category in menu["menu"]:
            menu_str += f"\n*{category['category']}*\n"
            for item in category["items"]:
                menu_str += f"  - {item['icon']} {item['name']} - ${item['price']:.2f}\n"
        bot.reply_to(message, f"Hello! I'm a food ordering bot from *OiOi Fastfood*. Here is the menu:", parse_mode="Markdown")
        bot.send_message(message.chat.id, menu_str, parse_mode="Markdown")
        bot.send_message(message.chat.id, "Please type the name of the item you want to order.")
    except Exception as e:
        bot.reply_to(message, f"Error: {e}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("telegram_bot_server:app", host="0.0.0.0", port=8000, reload=True)