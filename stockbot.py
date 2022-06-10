from telegram import Update
from telegram.ext import CommandHandler, Application
from telegram.ext import CallbackContext
from companies import COMPANIES
from decorators import PrintEventName
from pytz import timezone
import yfinance as yf
import datetime
from dotenv import load_dotenv
import os

load_dotenv()


def time_in_range(start, end, current):
    """Returns whether current is in the range [start, end]"""
    return start <= current <= end


@PrintEventName
async def start(update: Update, context: CallbackContext):
    print(time_in_range(datetime.time(7, 30), datetime.time(
        16, 0), datetime.datetime.now(timezone('US/Eastern')).time()))
    print(datetime.datetime.now(timezone('US/Eastern')).time())
    print(update.message.from_user)
    await update.message.reply_text("Hello")


@PrintEventName
async def update_user(context: CallbackContext):
    if (time_in_range(datetime.time(7, 30), datetime.time(16, 0), datetime.datetime.now(timezone('US/Eastern')).time())):
        tickers = yf.Tickers(
            ' '.join(list(COMPANIES.keys())))
        for company in COMPANIES.keys():
            ticker: yf.Ticker = tickers.tickers[company]
            COMPANIES[company].ask = ticker.history()['Close'][-1]
            COMPANIES[company].ma20 = ticker.history(period="20d")[
                'Close'].mean()
            COMPANIES[company].ma50 = ticker.history(period="50d")[
                'Close'].mean()
            if COMPANIES[company].ma20 > COMPANIES[company].ma50 and COMPANIES[company].ma20Passma50 == False:
                COMPANIES[company].ma20Passma50 = True
                await context.bot.send_message(chat_id=context.job.chat_id, text=f'{company} MA20 is higher than MA50')
            if COMPANIES[company].ma20 > COMPANIES[company].ask and COMPANIES[company].ma20PassAsk == False:
                COMPANIES[company].ma20PassAsk = True
                await context.bot.send_message(chat_id=context.job.chat_id, text=f'{company} MA20 is higher than ask')
            if COMPANIES[company].ma50 > COMPANIES[company].ask and COMPANIES[company].ma50PassAsk == False:
                COMPANIES[company].ma50PassAsk = True
                await context.bot.send_message(chat_id=context.job.chat_id, text=f'{company} MA50 is higher than ask')
            if COMPANIES[company].ma20Passma50 and COMPANIES[company].ma20 < COMPANIES[company].ma50:
                COMPANIES[company].ma20Passma50 = False
                await context.bot.send_message(chat_id=context.job.chat_id, text=f'{company} MA20 is lower than MA50')
            if COMPANIES[company].ma20PassAsk and COMPANIES[company].ma20 < COMPANIES[company].ask:
                COMPANIES[company].ma20PassAsk = False
                await context.bot.send_message(chat_id=context.job.chat_id, text=f'{company} MA20 is lower than ask')
            if COMPANIES[company].ma50PassAsk and COMPANIES[company].ma50 < COMPANIES[company].ask:
                COMPANIES[company].ma50PassAsk = False
                await context.bot.send_message(chat_id=context.job.chat_id, text=f'{company} MA50 is lower than ask')
    await context.bot.send_message(chat_id=context.job.chat_id, text=f'Hey {context.job.context}, finish round')


async def send_stock_update(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    name = update.effective_chat.full_name
    await context.bot.send_message(chat_id=chat_id, text='Setting a timer for 1 minute!')

    context.job_queue.run_repeating(
        update_user, interval=900, context=name, chat_id=chat_id)


application = Application.builder().token(
    os.environ.get("telegram-token")).build()

start_handler = CommandHandler('start', start)
stock_handler = CommandHandler('send_update', send_stock_update)

application.add_handler(start_handler)
application.add_handler(stock_handler)


print("Starting...")
application.run_polling()
print("Go idle")
application.idle()
