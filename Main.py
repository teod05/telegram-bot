from typing import Final
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import random

TOKEN: Final = '7734159270:AAGSwx0RZY4vVrhIiezeUiUvfO2F5-r6tLQ'
BOT_USERNAME: Final = '@PeaceUABot'

# Quote list
quotes = [
    "Success is the best revenge.",
    "Shoot for the stars, so if you fall you land on a cloud.",
    "Everything I'm not makes me everything I am.",
    "Love your haters—they're your biggest fans.",
    "If you're a Kanye West fan, you're not a fan of me; you're a fan of yourself.",
    "Nothing in life is promised except death.",
    "I refuse to follow the rules where society tries to control people with low self-esteem.",
    "For me to say I wasn't a genius I'd just be lying to you and to myself.",
    "My life is dope, and I do dope shit.",
    "I hate when I'm on a flight and I wake up with a water bottle next to me like oh great now I gotta be responsible for this water bottle.",
    "People always say that you can't please everybody. I think that's a cop-out.",
    "I am Warhol. I am the No. 1 most impactful artist of our generation.",
    "If you have the opportunity to play this game called life, you have to appreciate every moment.",
    "George Bush doesn't care about black people.",
    "They say your attitude determines your latitude.",
    "Success is the only option; failure is not.",
    "You can't be afraid to fail; it's the only way to succeed.",
    "The world is full of people who want to see you fail.",
    "Discipline is doing what you hate but doing it like you love it.",
    "The only way to get what you want is to work for it.",
    "Your mindset is everything; if you want something bad enough, you'll find a way to get it.",
    "You must be willing to put in the work that others won't.",
    "Life is hard; it's supposed to be hard.",
    "You are the sum of your habits; change them and change your life.",
    "When something is important enough, you do it even if the odds are not in your favor.",
    "I think it's possible for ordinary people to choose to be extraordinary.",
    "Some people don't like change, but you need to embrace change if the alternative is disaster.",
    "Failure is an option here. If things are not failing, you are not innovating enough.",
    "I could either watch it happen or be a part of it.",
    "Persistence is very important. You should not give up unless you are forced to give up.",
    "The first step is to establish that something is possible; then probability will occur.",
    "I think we should take the set of actions that are most likely to lead us toward a better future.",
    "Make America Great Again!",
    "Sometimes by losing a battle, you find a new way to win the war.",
    "I will be the greatest jobs president that God ever created.",
    "You have to think anyway, so why not think big?",
    "What separates the winners from the losers is how a person reacts to each new twist of fate.",
    "I don't like giving interviews because they're always misquoted or taken out of context.",
    "The point is that you can never be too greedy when it comes to winning!",
    "We're going to build a wall and Mexico is going to pay for it.",
    "The beauty of me is that I'm very rich.",
    "You have to show up in life, and if you don't show up, nothing happens.",
    "I think that I'm going to win.",
    "I'm not saying I'm going to change the world, but I'm going to change how people see it.",
    "If you're going to be thinking anyway, think big!",
    "The prettiest people do the ugliest things.",
    "You can't put a limit on anything.",
    "We will make America great again.",
    "Success isn't just about what you accomplish in your life; it's about what you inspire others to do.",
    "I'm always thinking about new ideas."
]

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Hello! Thanks for chatting with me')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('What you want gang?')

async def custom_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('This is a custom command!')

async def quote_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    quote = random.choice(quotes)
    await update.message.reply_text(quote)

def handle_response(text: str) -> str:
    processed: str = text.lower()

    if "hello" in processed:
        return 'Hey there'

    if "how are you" in processed:
        return "I'm doing well, thanks for asking! How about you?"

    if "i love you" in processed:
        return 'Benedict you are the BEST'

    return 'I do not understand what you wrote'

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
    text: str = update.message.text

    print(f'User ({update.message.chat.id}) in {message_type}: "{text}"')

    if message_type == 'group':
        if BOT_USERNAME in text:
            new_text: str = text.replace(BOT_USERNAME, '').strip()
            response: str = handle_response(new_text)
        else:
            return  # No response in groups unless mentioned
    else:
        response: str = handle_response(text)

    print('Bot:', response)
    await update.message.reply_text(response)

async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error {context.error}')

if __name__ == '__main__':
    print('Starting bot...')
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('custom', custom_command))
    app.add_handler(CommandHandler('quote', quote_command))  # New quote command

    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    app.add_error_handler(error)

    print('Polling')
    app.run_polling(poll_interval=3)