from email import message
import os
from numpy import byte
from telebot import TeleBot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton,KeyboardButton,ReplyKeyboardMarkup
from core.check import CheckDb
from requests import get as GET
from tools.cpanel import CPanelBasicAuth
from tools.smtp import SMTP

# objects
DB = CheckDb()
API_KEY = os.getenv("API_KEY")
bot = TeleBot("5517231574:AAHR2kpQ-lAXAp0Cf-ywX9AZfeF8n6YIk-k")

# variables
CHATID = {}


def choose_tool(var:str,file,message_id:str):
    if var == "cpanel":
        print("starting validating xD")
        sites = file.splitlines()
        try:
            organized_data = CPanelBasicAuth(sites).sorter()
            CPanelBasicAuth(organized_data,message_id,bot).multithreading()
        except Exception as e:
            print(e)
            bot.send_message(message_id,"File Wrong Patter")
        DB.delVar(message_id)
    elif var == "smtp":
        sites = file.splitlines()
        try:
            organized_data = SMTP(bot,message_id)
            organized_data.multithreading(sites)
        except Exception as e:
            print(e)
            bot.send_message(message_id,"File Wrong Patter")
        DB.delVar(message_id)
def gen_markup(message:object):
    message_id = message.chat.id
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(InlineKeyboardButton("Cpanel Checker", callback_data=f"cpanel,{message_id}"))
    markup.add(InlineKeyboardButton("SMTP Checker", callback_data=f"smtp,{message_id}"))
    markup.add(InlineKeyboardButton("Shell Checker", callback_data=f"shell,{message_id}"))

    print(markup)
    return markup


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    print(call.data)
    data = call.data.split(",")[0]
    id = call.data.split(",")[1]
    if data == "cpanel":
        bot.answer_callback_query(call.id, "Starting Cpanel Checker soon")
    elif data == "smtp":
        bot.answer_callback_query(call.id, "Starting SMTP Checker soon")
    elif data == "shell":
        bot.answer_callback_query(call.id, "Starting Shell Checker soon")
    DB.setVar(id,data)


@bot.message_handler(commands=["start","help"])
def menu(message):
    menu_ = """
/start          show menu

/buy            buy product
/bot            run the bot's tools

/info           further informations about the tool.
/credit         credit to developer
    """
    bot.send_message(message.chat.id,menu_)

@bot.message_handler(commands=["info"])
def info(message):
    bot.send_message(message.chat.id,"""Buying this bot will provide you:

 Spamming Tools:
  - CPanel Checker
  - Shell Checker
  - SMTP Checker 

 The tools are developed to validate fast asynchonorous validation.
 Your telegram will gain an infinite access to the bot. """)



@bot.message_handler(commands=["buy"])
def buyer(message):
    bot.send_message(message.chat.id,"""
Contact @georgeknowsit or @tools_designer if you are welling to pay for the bot.
Consider only Crypto Currencies accepted.

You may gain trial for the bot for only 30 minutes    
    """)


@bot.message_handler(commands=["trial"])
def trial(message):
    print("here")
    trial = DB.getFreeTrial(message.chat.id)
    if trial :bot.send_message(message.chat.id,"Trial have been successfully added for 15 Mins")
    else:bot.send_message(message.chat.id,"You can't make trial again, already done")



@bot.message_handler(content_types=["document"])
def files(file):
    bot.send_message(file.chat.id,"start validating")
    file_info = bot.get_file(file.document.file_id)
    downloaded_file = bot.download_file(file_info.file_path).decode("utf-8")
    try:
        var = DB.getVar(file.chat.id)
        bot.send_message(file.chat.id,f"validating on {var} tool")
        choose_tool(var,downloaded_file,file.chat.id)
    except Exception as e:
        bot.send_message(file.chat.id,"Wrong File Patter, We can't validate this file")


@bot.message_handler(commands=["bot"])
def tool_handler(message):
    bot.send_message(message.chat.id,"Checking Username in DATABASE")
    resp = DB.verify(message.chat.id)
    print(message.chat.id)
    if resp is True:
        bot.send_message(message.chat.id,"Choose a tool to go with",reply_markup=gen_markup(message))
    else:
        bot.send_message(message.chat.id,f"{message.chat.id}")
        bot.reply_to(message,"""we didn't find you in database.
for more info about the bot type /info.
if you are willing to buy bot use  /buy.
        
only crypto payment accepted.""")


bot.infinity_polling()