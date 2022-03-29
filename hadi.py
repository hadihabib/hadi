from cgitb import text
from fileinput import close
import imp
from tkinter import Text
from unittest.mock import call
from numpy import ones_like
from telegram.ext import *
from telegram import *
import requests,json
import telegram
import pandas as pd

import csv
from openpyxl import Workbook



TOKEN = "5137905230:AAFnc7m78VR6Ria5IdAnho2BW1xPZ0vwBRw"
data = []
dash_key = [['Name','birthday','address','Phone','qualification','University','college','specialization']]

dat = json.load(open('users.json','r'))
enter="مشروع يهدف إلى إحداث نقلة نوعية في مفهوم التعليم العالي والبحث العلمي من خلال الانتقال من التلقين النظري إلى التطبيق العملي وتحقيق الربط الفعال بين الجامعة والمجتمع عملياً وفق أسس علمية بما يسهم في تعزيز الاقتصاد الوطني والمساهمة في عملية البناء."


def start(update, context):     
    update.message.reply_text(enter)
    if update.message.chat.type == 'private':
        user = str(update.message.chat.id)
        if user not in data['users']:
            data['users'].append(user)
            if user not in data['Name']:
                data['Name'][user] = ""
            if user not in data['birthday']:
                data['birthday'][user] = ""
            if user not in data['Phone']:
                data['Phone'][user] = ""
            if user not in data['address']:
                data['address'][user] = ""
            if user not in data['qualification']:
                data['qualification'][user] = ""
            if user not in data['University']:
                data['University'][user] = ""
            if user not in data['college']:
                data['college'][user] = ""
            if user not in data['specialization']:
                data['specialization'][user] = ""
            data['process'][user] = "Name"
            json.dump(data,open('users.json','w'))
            reply_markup = telegram.ReplyKeyboardMarkup([[telegram.KeyboardButton("أريد الانضمام")]],resize_keyboard=True,one_time_keyboard=True)
            update.message.reply_text(enter, reply_markup=reply_markup)
            

        else:
            reply_markup = telegram.ReplyKeyboardMarkup([[telegram.KeyboardButton("خيارات")]],resize_keyboard=True,one_time_keyboard=True)
            update.message.reply_text("لقد قمت بادخال بيانتك مسبقا  ", reply_markup=reply_markup)

def one (update: Update, context: CallbackContext): 
    
    json.dump(data,open('users.json','w'))
    update.message.reply_text("الاسم الثلاثي")

def Restat (update: Update, context: CallbackContext):   

            user = str(update.message.chat.id)
            data["users"].remove(user)
            reply_markup = telegram.ReplyKeyboardMarkup([[telegram.KeyboardButton("تعديل")]],resize_keyboard=True,one_time_keyboard=True)
            update.message.reply_text("....",reply_markup=reply_markup)



def extra(update, context):
    if update.message.chat.type == 'private':
        user = str(update.message.chat.id)
        if data["process"][user] == 'Name':
            data['Name'][user] = update.message.text
            data['process'][user] = 'birthday'
            json.dump(data,open('users.json','w'))
            update.message.reply_text("تاريخ الميلاد")
        elif data["process"][user] == 'birthday':
            data['birthday'][user] = update.message.text
            data['process'][user] = 'address'
            json.dump(data,open('users.json','w'))
            update.message.reply_text("العنوان")
        elif data["process"][user] == 'address':
            data['address'][user] = update.message.text
            data['process'][user] = "Phone"
            json.dump(data,open('users.json','w'))
            update.message.reply_text("رقم الهاتف")
        elif data["process"][user] == 'Phone':
            data['Phone'][user] = update.message.text
            data['process'][user] = "qualification"
            json.dump(data,open('users.json','w'))
            reply_markup = telegram.ReplyKeyboardMarkup(
                [
                    [telegram.KeyboardButton("ثانوية عامة")],[telegram.KeyboardButton("معهد متوسط")]
                    ,[telegram.KeyboardButton("إجازة جامعية")],[telegram.KeyboardButton("دبلوم")],
                    [telegram.KeyboardButton("ماجستير")],[telegram.KeyboardButton("دكتوراه")]

                ],
                resize_keyboard=True,one_time_keyboard=True)
            update.message.reply_text("المؤهل العلمي",reply_markup=reply_markup)
            
        elif data["process"][user] == 'qualification':
            data['qualification'][user] = update.message.text
            data['process'][user] = "University"
            json.dump(data,open('users.json','w'))
            update.message.reply_text("الجامعة")    
        elif data["process"][user] == 'University':
            data['University'][user] = update.message.text
            data['process'][user] = "college"
            json.dump(data,open('users.json','w'))
            update.message.reply_text("الكلية")
        elif data["process"][user] == 'college':
            data['college'][user] = update.message.text
            data['process'][user] = "specialization"
            json.dump(data,open('users.json','w'))
            update.message.reply_text("الاختصاص")
        elif data["process"][user] == 'specialization':
            data['specialization'][user] = update.message.text
            data['process'][user] = "finished"
            json.dump(data,open('users.json','w',encoding='utf-8'))
            reply_markup = telegram.ReplyKeyboardMarkup([[telegram.KeyboardButton("خيارات"),telegram.KeyboardButton("تأكيد")]],resize_keyboard=True,one_time_keyboard=True)
            update.message.reply_text(text="هل تريد تأكيد البيانات", reply_markup=reply_markup)


def save(update: Update, context: CallbackContext):  
            print("dsfs") 
       
            with open('users.csv','w', encoding="utf-8") as f:
             f.write("username,Name ,birthday,address,Phone,qualification,University,college,specialization\n")
             for u in data['users']:
                d = "{},{},{},{},{},{},{},{},{}\n".format(u,data['Name'][u],data['birthday'][u],data['address'][u],data['Phone'][u],data['qualification'][u],data['University'][u],data['college'][u],data['specialization'][u])
                f.write(d)
            f.close()
            
            wb = Workbook()
            ws=wb.active
            with open('users.csv','r') as f:
                for row in csv.reader(f):
                    ws.append(row)
            wb.save('users.xlsx')
            f.close()
            context.bot.send_document(chat_id=844534481, document=open( 'users.xlsx', 'rb'))


if __name__ == '__main__':
    data = json.load(open('users.json','r'))
    updater = Updater(TOKEN,use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start",start))
    dp.add_handler(MessageHandler(Filters.text("تأكيد"),save))
    dp.add_handler(MessageHandler(Filters.text("تعديل"),start))
    dp.add_handler(MessageHandler(Filters.text("خيارات"),Restat))
    dp.add_handler(MessageHandler(Filters.text("أريد الانضمام"),one))
    dp.add_handler(MessageHandler(Filters.text,extra))
    updater.start_polling()
    print("Bot Started")
    updater.idle()
