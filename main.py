
import telebot
import logging
import time
from telebot.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton
from DDL import *
from DQL import *
from DML import *
from BOTTOKEN import *



logging.basicConfig(filename='project.log', filemode='a', level=logging.INFO, format= f'%(asctime)s - %(levelname)s - %(message)s')
create_database()
create_table_user() 
create_table_category()
create_table_kala()
create_sale_invoice_table()
create_sale_row_table()

<<<<<<< HEAD
API_TOKEN =bottoken
=======
API_TOKEN = ' '
>>>>>>> 57a58806c4d6bf25757dcda6d3958b87c1678d0d

user_step=dict()     #user_step={ cid :step ,....}
user_profile=dict()     #user_data={cid : [firstname,lastname, mobile , code melli ,adress],....}
admin=[878897420]     #admin=[cid admin]
block_user=[]        #block user = [cid block admin,...]

button= {
        'my_acount' : 'حساب کاربری من',
        'help' :'راهنمای استفاده از بات',
        'buy'  :'خرید',
        'contact_to_me' : 'تماس با ما' ,
        'back' :'بازگشت',
        'shirt' : 'پیراهن',
        'tshirt' :'تی شرت',
        'pants' : 'شلوار',
        'home' : 'منوی اصلی',
        'cart_basket' : 'سبد خرید' ,
        'user_profile' :'مشخصات کاربری',
        'first_name':'نام' ,
        'last_name' :'نام خانوادگی' ,
        'mobile' : ' شماره موبایل' ,
        'personal_id' : 'کد ملی' ,
        'adress' : 'آدرس',
        }

command= {  
          'start' :'شروع به کار رباط' ,
          'help'  :'راهنمایی استفاده از رباط',
          'main'  :'منوی اصلی برنامه',
         }

def get_user_step(cid):
    return user_step.setdefault(cid, 1000)


bot = telebot.TeleBot(API_TOKEN, num_threads=10)




# only used for console output 
def listener(messages):
    """
    When new messages arrive TeleBot will call this function.
    """
    for m in messages:
        if m.content_type == 'text':
            # print the sent message to the console
            logging.info(str(m.chat.first_name) + " [" + str(m.chat.id) + "]: " + m.text)
bot.set_update_listener(listener)  # register listener

#Commands

@bot.message_handler(commands=['start'])
def command_start(message):
    cid=message.chat.id
    if cid in block_user : return
    if cid in admin :
        user_step.setdefault(cid,2000)
    else:
        bot.send_message(cid,"به بات خریداز فروشگاه خوش آمدید",reply_to_message_id=message.id)
        user_s=get_user_step(cid)
        if user_s ==1000 :
            if cid in block_user : return
            username = message.chat.username
            insert_user(cid=cid ,username=username,step=user_s)
            markup=ReplyKeyboardMarkup(resize_keyboard=True)
            markup.add(button['my_acount'],button['buy'])
            markup.add(button['contact_to_me'],button['help'])
            bot.send_message(cid,"لطقا از منوی زیر انتخاب کنید",reply_markup=markup)
        
@bot.message_handler(commands=['main'])
def main_command(message) :
    cid=message.chat.id
    if cid in block_user : return
    if user_step[cid] <2000 :
        markup=ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(button['my_acount'],button['buy'])
        markup.add(button['contact_to_me'],button['help'])
        bot.send_message(cid,"لطقا از منوی زیر انتخاب کنید",reply_markup=markup)

@bot.message_handler(commands=['help'])
def help_func(message) :
    cid=message.chat.id
    if cid in block_user : return
    if user_step[cid] <2000 :
        bot.send_message(cid,'راهنمای استفاده از برنامه\n 1- خرید \n بااستفاده از این منو  اول می توان دسته بندی را انتخاب کرد و بعد از ان از لیست کالای مورد نظر را انتخاب و به و سبد خرید اضافه کرد \n 2- حساب کاربری\n شامل دو زیر منو می باشد \n 2.1-سبد خرید\n شامل لسیت اجناس انتخابی که بعد از تایید مراحل واریز وجه و ارسال فاکتور انجام می شود\n 2.2-مشخصات کاربر\n برای تکمیل مشخصات کاربر که شامل :\n نام\n نام خانوادگی\n کد ملی\n شماره موبایل\n آدرس \n 3-راهنمای استفاده از برنامه\n 4- تماس با ما\n می توان به ادمین ها ارتباط برقرار کنید و پیغام دهید')

#text

@bot.message_handler(func=lambda message : message.text==button['buy'])
def button_buy(message) :
    cid=message.chat.id
    if cid in block_user :return
    if user_step[cid] >= 2000 :return
    markup=ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(button['shirt'],button['tshirt'])
    markup.add(button['home'],button['pants'])
    user_step[cid]=1100
    bot.send_message(cid,"از این تقسیم بندی یکی را انتخاب کنید",reply_markup=markup)

@bot.message_handler(func=lambda message : message.text==button['back'])
def back_func(message) :
    cid=message.chat.id
    if cid in block_user :return
    if user_step[cid]==1250:
        markup=ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(button['user_profile'],button['cart_basket'])
        markup.add(button['home'])
        user_step[cid]=1200
        bot.send_message(cid,'یکی از این گزینه هاراانتخاب کنید',reply_markup=markup)

@bot.message_handler(func=lambda message : message.text==button['help'])
def help_func(message) :
    cid=message.chat.id
    if cid in block_user : return
    if user_step[cid] <2000 :
        bot.send_message(cid,'راهنمای استفاده از برنامه\n 1- خرید \n بااستفاده از این منو  اول می توان دسته بندی را انتخاب کرد و بعد از ان از لیست کالای مورد نظر را انتخاب و به و سبد خرید اضافه کرد \n 2- حساب کاربری\n شامل دو زیر منو می باشد \n 2.1-سبد خرید\n شامل لسیت اجناس انتخابی که بعد از تایید مراحل واریز وجه و ارسال فاکتور انجام می شود\n 2.2-مشخصات کاربر\n برای تکمیل مشخصات کاربر که شامل :\n نام\n نام خانوادگی\n کد ملی\n شماره موبایل\n آدرس \n 3-راهنمای استفاده از برنامه\n 4- تماس با ما\n می توان به ادمین ها ارتباط برقرار کنید و پیغام دهید')

    
@bot.message_handler(func=lambda message : message.text==button['home'])
def home_func(message):
    cid=message.chat.id
    if cid in block_user :return
    if user_step[cid] <2000 :
        user_step[cid]=1000
        markup=ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(button['my_acount'],button['buy'])
        markup.add(button['contact_to_me'],button['help'])
        bot.send_message(cid,"لطقا از منوی زیر انتخاب کنید",reply_markup=markup)
        
       
@bot.message_handler(func=lambda message : message.text==button['my_acount'])
def button_buy(message) :
    cid=message.chat.id
    if cid in block_user :return
    if user_step[cid] >= 2000 :return
    markup=ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(button['user_profile'],button['cart_basket'])
    markup.add(button['home'])
    user_step[cid]=1200
    bot.send_message(cid,'یکی از این گزینه هاراانتخاب کنید',reply_markup=markup)

@bot.message_handler(func=lambda message : message.text==button['user_profile'])
def user_Profile_func(message):
    cid=message.chat.id
    if cid in block_user :return
    markup=ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(button['last_name'],button['first_name'])
    markup.add(button['mobile'],button['personal_id'])
    markup.add(button['back'],button['adress'])
    markup.add(button['home'])
    user_step[cid]=1250
    bot.send_message(cid,'هرگزینه را انتخاب و مشخصات مربوطه را وارد کنید\n لطفا فارسی وارد کنید',reply_markup=markup)    
  

@bot.message_handler(func=lambda message : message.text==button['contact_to_me'])
def contact_to_me_func(message):
    cid=message.chat.id
    if cid in block_user :return
    if user_step[cid] <2000 :
        bot.send_message(cid,"می توانید به ادمین زیر پیغام بدهید \n @masoud_hosseini216")






bot.infinity_polling()
