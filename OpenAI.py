import os
import logging
from dotenv import load_dotenv
import telebot
from openai import OpenAI
import sqlite3
import json
from contextlib import closing

load_dotenv()

TELEGRAM_API_KEY = os.getenv("TELEGRAM_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY)
bot = telebot.TeleBot(TELEGRAM_API_KEY)

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s', filename='bot_messages.log')


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Hello! I'm a bot that uses OpenAI. Send me a message, and I'll respond.")


def get_db_connection():
    return sqlite3.connect('messages.db', check_same_thread=False)

@bot.message_handler(func=lambda message: True)

def handle_message(message):
    try:
        logging.info(f"User ID: {message.from_user.id}, Message: {message.text}")

        with closing(get_db_connection()) as conn:
            cursor = conn.cursor()
            # Check if user exists in the database and get chat history
            cursor.execute('SELECT message_history, token_spent FROM users WHERE chat_id = ?', (message.chat.id,))
            user = cursor.fetchone()
            print(user)

            if user:
                message_history, token_spent = user
                conversation = json.loads(message_history)
                print(conversation)
                if not conversation:
                    conversation = []
                conversation.append({"role": "user", "content": message.text})

            else:
                conversation = [
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": message.text}
                ]
                token_spent = 0

            # Get response from OpenAI using the conversation history
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=conversation
            )

            bot_response = response.choices[0].message.content
            conversation.append({"role": "assistant", "content": bot_response})

            # Update token usage (replace with actual token calculation if available)
            token_spent += response.usage.total_tokens if response.usage else len(message.text) + len(bot_response)

            # Update or insert user's record in the database
            cursor.execute('''
                INSERT OR REPLACE INTO users (chat_id, message_history, token_spent)
                VALUES (?, ?, ?)
            ''', (message.chat.id, json.dumps(conversation), token_spent))
            conn.commit()

        bot.reply_to(message, bot_response)
    except sqlite3.Error as e:
        logging.error(f"Database error: {str(e)}")
        bot.reply_to(message, "A database error occurred. Please try again later.")
    except OpenAI.error.OpenAIError as e:
        logging.error(f"OpenAI API error: {str(e)}")
        bot.reply_to(message, "An error occurred with the AI service. Please try again later.")
    except Exception as e:
        logging.error(f"Unexpected error: {str(e)}")
        bot.reply_to(message, "An unexpected error occurred. Please try again later.")

bot.polling()