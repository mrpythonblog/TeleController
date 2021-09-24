from telegram.ext import Updater,CommandHandler,MessageHandler,Filters
import subprocess
from pyscreenshot import grab as grab_screenshot
from io import BytesIO
from telegram import ReplyKeyboardMarkup,ReplyKeyboardRemove
from pyautogui import alert
import sqlite3
import pyttsx3
import logging
import argparse
from os import listdir,startfile,system
from os import name as osName
from telegram.error import NetworkError
import sys
import time

def log(text):
    logging.critical(text)
    print(text)
    

arg_parser = argparse.ArgumentParser(description = "controll your system securely from telegram bots" ,
                                     epilog = "Enjoy it :)",
                                     usage = "%(prog)s [options]")

def runExecutable(name):
    if osName == "nt": # Windows
        startfile(executables_path + "\\" + name)
    
    
        
        
arg_parser.add_argument("-T", "--token" , metavar="TOKEN" , type=str  , help="Token of your telegram Bot")
arg_parser.add_argument("-P","--password",metavar="PASSWORD",type=str  , help="Password For your Bot !")
arg_parser.add_argument("-p" , "--proxy",metavar="IP:PORT" , help="use a socks5 proxy")

args = arg_parser.parse_args()

if args.token:
    TOKEN = args.token
else:
    TOKEN = input("TOKEN : ")

if args.password:
    password = args.password
else:
    password = input("Password : ")


executables_path = ".\\executables"


loggingFormat = "[%(asctime)s] %(message)s"
logging.basicConfig(level = logging.CRITICAL , filename="logs.log" , filemode="a",format = loggingFormat)

about_we = """
Site  :  https://mrpython.blog.ir
Channel : @mrpythonblog
Authors : Hossein Ahmadi - AmirHossein Mazaheri
Github : https://github.com/mrpythonblog/TeleController
"""
if args.proxy:
    proxy = {"proxy_url" : "socks5h://{}".format(args.proxy)}
    updater = Updater(TOKEN,use_context = True ,request_kwargs = proxy)
else:
    updater = Updater(TOKEN,use_context = True)




db = sqlite3.connect("database.db",check_same_thread=False)
c = db.cursor()
log("Connected to the database !")
c.execute("CREATE TABLE if not exists users(chat_id ,status)")
default_keyboard = [['screenshot' , 'TTS'],  ["open cmd" , "show message"] , ["executables" , "about we"] , ["LOG OUT"]]

executables = listdir(executables_path)
executables_keyboard = []
for i in executables:
    executables_keyboard.append([i])
executables_keyboard.append(["return"])


def sec(status,chat_id,c,db):
    c.execute("CREATE TABLE if not exists login(chat_id ,try)")
    tries = 1
    if status == "tries an incorrect Password":
        c.execute('SELECT * FROM login WHERE chat_id = {}'.format(int(chat_id)))
        result = c.fetchall()
        if len(result) >= 1:
            c.execute('SELECT try FROM login WHERE chat_id = {}'.format(int(chat_id)))
            result1=c.fetchall()
            result = list(result[0])
            try1 = result[1]
            try1 =try1 + 1
            c.execute('UPDATE login SET try = {} where chat_id = {}'.format(try1,chat_id))
            db.commit()
            if try1 >= 10:
                time1 = time.time()
                c.execute("INSERT INTO black_list(chat_id,time) VALUES({},{})".format(int(chat_id),time1))
                db.commit()
                c.execute("DELETE FROM login WHERE chat_id={};".format(int(chat_id)))
                db.commit()
        else:
            list1 = (chat_id,tries)
            c.execute("INSERT INTO login(chat_id,try) VALUES({}, {})".format(int(chat_id),tries))
            db.commit()
    elif status == "logged in":
        c.execute("DELETE FROM login WHERE chat_id={};".format(chat_id))
        db.commit()

def check_black_list(chat_id,c,db):
    c.execute("CREATE TABLE if not exists black_list(chat_id,time)")
    c.execute("select * from black_list where chat_id={}".format(chat_id))
    result5 = c.fetchall()
    # print(result5)
    if len(result5) == 1:
        return False
    else:
        return True


def checkChat_id(chat_id):
    c.execute("select * from users where chat_id=\"{}\"".format(chat_id))
    result = c.fetchall()
    if len(result) == 1:
        return True
    else:
        return False


def addUser(chat_id , status="idle"):
    log("Users {} logged in .".format(chat_id))
    c.execute("insert into users (chat_id , status) VALUES(\"{}\",\"{}\")".format(chat_id,status))
    db.commit()
    sec("logged in",chat_id,c,db)
    
def setStatus(chat_id , status):
    log("{}'s status Sets to {}".format(chat_id , status))
    c.execute("update users set status=\"{}\" where chat_id=\"{}\"".format(status,chat_id))
    db.commit()
    
def getStatus(chat_id):
    c.execute("select * from users where chat_id=\"{}\"".format(chat_id))
    result = c.fetchall()
    return result[0][1]



def start_method(update,context):
    chat_id = str(update.message.chat_id)
    log("{} has started the bot .".format(chat_id))
    if checkChat_id(chat_id): # this chat_id has logged in      
        message = """device connected!
    Please select the operation you want..."""
        reply_markup = ReplyKeyboardMarkup(default_keyboard,
                                           one_time_keyboard=True,
                                           resize_keyboard=True)
        update.message.reply_text(message, reply_markup=reply_markup)
    else:
        reply_markup = ReplyKeyboardRemove()
        update.message.reply_text("device connected !, Please Enter The Correct Password For Login", reply_markup=reply_markup)
    setStatus(chat_id , "idle")

def run_command(update,context,command = ""):

    chat_id = str(update.message.chat_id)
    
    if checkChat_id(chat_id):
        if command == "":
            command = ""
            for i in context.args:
                command += i+" "
        log("{} runs {}".format(chat_id , command))
        proc = subprocess.Popen(command,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,stdin=subprocess.PIPE)
        command_result = proc.stdout.read() + proc.stderr.read()
        context.bot.sendMessage(update.message.chat_id,command_result.decode())
    else:
        reply_markup = ReplyKeyboardRemove()
        update.message.reply_text("Please Login First .  Enter The Correct Password For Login", reply_markup=reply_markup)
       


def msgHandler(update , context):
    
    message = update.message.text
    chat_id = str(update.message.chat_id)
    
    if checkChat_id(chat_id):
        status = getStatus(chat_id)
    
        keyboard = [['return']]
       
        reply_markup = ReplyKeyboardMarkup(keyboard,
                                               one_time_keyboard=True,
                                               resize_keyboard=True)
        
        default_reply_markup = ReplyKeyboardMarkup(default_keyboard,
                                           one_time_keyboard=True,
                                           resize_keyboard=True)

        if status == "idle":
            if message == "about we":
                context.bot.sendMessage(chat_id , about_we)
            elif message == "screenshot":
                photo = grab_screenshot()
                photo_data = BytesIO()
                photo.save(photo_data , format="JPEG")
                photo_data.seek(0)
                context.bot.sendPhoto(chat_id , photo_data)
                log("{} grabbed a screenshot .".format(chat_id))

                setStatus(chat_id ,"idle")
                
            elif message == "TTS":
                setStatus(chat_id ,"wait_for_song")
                update.message.reply_text("plz select messeage!", reply_markup=reply_markup)
        
            elif message == "open cmd":
                try:
                    setStatus(chat_id ,"wait_for_command")
                    update.message.reply_text("Enter the command : ", reply_markup=reply_markup)
                except Exception as error:
                    print(error)
            elif message == "show message":
                setStatus(chat_id ,"wait_for_message")
                update.message.reply_text("Enter the message : ", reply_markup=reply_markup)
            elif message == "LOG OUT":
                reply_markup = ReplyKeyboardRemove()
                c.execute('Delete from users where chat_id=\"{}\"'.format(chat_id))
                db.commit() # log out
                log("{} Logged Out .".format(chat_id))
                update.message.reply_text("log out ! . enter password for login .", reply_markup=reply_markup)
                
            elif message == "executables":
                context.bot.sendMessage(chat_id , "warning : the bot just runs \"start <file>\" on windows and \"./<file>\" on linux .")
                executables_reply_markup = ReplyKeyboardMarkup(executables_keyboard,
                                           one_time_keyboard=True,
                                           resize_keyboard=True)
                
                update.message.reply_text("Select The Executable File to Execute :", reply_markup=executables_reply_markup)
                setStatus(chat_id , "wait_for_executable")
            
            else:
                context.bot.sendMessage(chat_id ,"wrong command !!!")

        else:
            if message == "return":
                update.message.reply_text("select Operation ...", reply_markup=default_reply_markup)
                setStatus(chat_id ,"idle")
            elif status == "wait_for_song":
                engine = pyttsx3.init() # For TTS
                engine.say(message)
                engine.runAndWait()
                log("{} Says {} using TTS".format(chat_id , message))
                update.message.reply_text("sound played !".format(message), reply_markup=default_reply_markup)
                setStatus(chat_id ,"idle")
            elif status == "wait_for_command":
                run_command(update,context , message)
                
            elif status == "wait_for_message":
                alert(title = "message for you" , text = message , timeout=5000)
                setStatus(chat_id ,"idle")
                log("{} alerts {}".format(chat_id , message))
                update.message.reply_text("message has shown !", reply_markup=default_reply_markup)
            elif status == "wait_for_executable":
                runExecutable(message)
                log("{} runs {} .".format(chat_id , message))
                setStatus(chat_id , "idle")
                update.message.reply_text("ok !", reply_markup=default_reply_markup)

                
    else:
        if check_black_list(chat_id,c,db) == True:
            if message == password:
                addUser(chat_id)
                start_method(update,context)
            else:
                reply_markup = ReplyKeyboardRemove()
                update.message.reply_text("Password Is Incorrect !", reply_markup=reply_markup)
                log("{} tries an incorrect Password".format(chat_id))
                sec("tries an incorrect Password",chat_id,c,db)
        else:
            c.execute("select time from black_list where chat_id={}".format(chat_id))
            result3 = c.fetchall()
            result3 = list(result3[0])
            time2 = time.time() - result3[0]
            
            if  time2 >= 30 :
                c.execute("DELETE FROM black_list WHERE chat_id={};".format(int(chat_id)))
            else:
                update.message.reply_text("try again in {}".format(30-int(time2)))

       
def showmessage_method(update , context):
    chat_id = str(update.message.chat_id)
    
    if checkChat_id(chat_id):
        if len(context.args) > 0:
            title = "message for you"
            message = ""
            for arg in context.args:
                message += arg + " "
            alert(text = message , title = title,timeout = 5000)
            log("{} alerts {}".format(chat_id , message))

        else:
            context.bot.sendMessage(update.message.chat_id , "Please Enter a valid Title and Text For Your Message")
        
    else:
        reply_markup = ReplyKeyboardRemove()
        update.message.reply_text("Please Login First .  Enter The Correct Password For Login", reply_markup=reply_markup)
        


updater.dispatcher.add_handler(CommandHandler("start",start_method))

updater.dispatcher.add_handler(CommandHandler("run",run_command))
updater.dispatcher.add_handler(CommandHandler("showmessage",showmessage_method))
updater.dispatcher.add_handler(MessageHandler(Filters.text,msgHandler))
try:
    updater.start_polling()
except NetworkError:
    print ("Network ERROR ! Connection Field ")
    sys.exit(1)
    
log("Server Started !")
