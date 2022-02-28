from email import header
from tracemalloc import start
from telegram.ext import*
import csv

print('bot started....')
full_name=''
birth_date=''
phone=''
itme=0

def start (update,context):
    update.message.reply_text("مرحبا بك في مشروع قادرون")
    update.message.reply_text("/Exit")
    update.message.reply_text("/Apply")

def Aplly(update,context):
    global itme, full_name, birth_date, phone
    full_name=''
    birth_date=''
    phone=''
    itme=0
    update.message.reply_text("ادخل اسمك بالغة الانكليزية")

def Exit(update,context):
    update.message.reply_text("شكرا لك")

def handlmsg(update,context):
    print(update.message.text)
    global itme, full_name, birth_date, phone

    if itme == 0:
        full_name= update.message.text
        update.message.reply_text("عمرك")

    if itme ==1:
        birth_date=update.message.text
        update.message.reply_text("رقم هاتفك")

    if itme ==2:
        phone=update.message.text
        update.message.reply_text("تأكيد")
        print(full_name)
        print(birth_date)
        print(phone)
        update.message.reply_text("/submit")
        update.message.reply_text("/cancel")

    itme += 1

def save(update,context):
 header =['full name', 'birth date', 'phone']
 data = [full_name,birth_date, phone]
 with open('applica21.csv', 'a', encoding='utf-8', newline='') as f:
    writer= csv.writer(f)
    
    writer.writerow(data)

 f.close()
 update.message.reply_text("thank you")

def Cancel(update, context):
 update.message.reply_text("cancelled....")
 update.message.reply_text("/Apply")
 update.message.reply_text("/Exit")

def error(update, context):
    print(f'update {update} caused error{context.error}')

def main():
    updater= Updater('5197293301:AAHvfkzAllCFO5CBDjDTHm7nRE_1ZphUnTk', use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('Apply', Aplly))
    dp.add_handler(CommandHandler('Submit', save))
    dp.add_handler(CommandHandler('Cancel', Cancel))
    dp.add_handler(MessageHandler(Filters.text, handlmsg))
    dp.add_error_handler(error)
    updater.start_polling()
    updater.idle()

main()
