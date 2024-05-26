
import telebot
import logging
import time
from telebot.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton
from DDL import *
from DQL import *
from DML import *
from Config import *
from TEXT import *




logging.basicConfig(filename=logfile, filemode='a', level=logging.INFO, format= f'%(asctime)s - %(levelname)s - %(message)s')
create_database()
create_table_user() 
create_table_category()
create_table_kala()
create_sale_invoice_table()
create_sale_row_table()

API_TOKEN =bottoken

user_step=dict()     #user_step={ cid :step ,....}
user_profile=dict()     #user_data={cid : [fullname, mobile phone, national code ,username ,adress],....}
admin=[]     #admin=[cid admin]
block_user=[]        #block user = [cid block ,...]
user_cid=[]            #user_cid =[cid,cid,....]
user_step.update({manager[0]:3000})
full_name_temp=dict()        #full_name={cid :fulname,....}
national_code_temp= dict()   #national_code{cid :national_code ,....}
mobile_phone_temp =dict()    #mobile_phone {cid :mobile_phone,....}
adress_temp =dict()          #adress{cid:adress}
result = get_info_user()

for i in result:
    if i['is_block']=='YES' :
        block_user.append(i['cid'])
        user_profile.update({i['cid']:[i['fullname'],i['mobile_phone'],i['national_code'],i['username'],i['adress']]})
        user_step.setdefault(i['cid'],1000)
    elif i['privilege'] =='USER' :
        user_cid.append(i['cid'])
        user_profile.update({i['cid']:[i['fullname'],i['mobile_phone'],i['national_code'],i['username'],i['adress']]})
        user_step.setdefault(i['cid'],1000)
    else :
        admin.append(i['cid'])
        user_profile.update({i['cid']:[i['fullname'],i['mobile_phone'],i['national_code'],i['username'],i['adress']]})
        user_step.setdefault(i['cid'],2000)
            
button= {
        'my_acount' :            'حساب کاربری من',
        'help' :                 'راهنمای استفاده از بات',
        'buy'  :                 'خرید',
        'contact_to_me' :        'تماس با ما' ,
        'back' :                 'بازگشت',
        'register' :             'ثبت',
        'shirt' :                'پیراهن',
        'tshirt' :               'تی شرت',
        'pants' :                'شلوار',
        'home' :                 'منوی اصلی',
        'cart_basket' :          'سبد خرید' ,
        'user_profile' :         'مشخصات کاربری',
        'full_name':             'نام و نام خانوادگی' ,
        'mobile' :               'شماره موبایل' ,
        'personal_id'  :         'کد ملی' ,
        'adress' :               'آدرس',
        'send number':          'ارسال شماره موبایل',
        'kala' :                'کالا',
        'invoice' :             'فاکتور',
        'admin' :               'ادمین',
        'finacial_department' : 'امور مالی',
        'reports' :             'گزارشات'
        }

command= {  
          'start' :'شروع به کار رباط' ,
          'help'  :'راهنمایی استفاده از رباط',
          'main'  :'منوی اصلی برنامه',
         }

def get_user_step(cid):
    return user_step.setdefault(cid, 1000)

def creat_marrkup(step) :
    pass



bot = telebot.TeleBot(API_TOKEN, num_threads=therad_num)





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
    if cid in manager :
        user_s=get_user_step(cid)
        if user_s ==3000 :
            if cid in block_user : return
            markup=ReplyKeyboardMarkup(resize_keyboard=True)
            markup.add(button['kala'],button['invoice'],button['admin'])
            markup.add(button['finacial_department'],button['reports'])
            bot.send_message(cid,text['select_menu'],reply_markup=markup)
          
    else:
        bot.send_message(cid,text['welcome'],reply_to_message_id=message.id)
        user_s=get_user_step(cid)
        if user_s ==1000 :
            if cid in block_user : return
            if cid in user_cid : return
            username = message.chat.username
            insert_user(cid=cid ,username=username)
            user_cid.append(cid)
            user_profile.update({cid:[None,None,None,username,None]})          
            markup=ReplyKeyboardMarkup(resize_keyboard=True)
            markup.add(button['my_acount'],button['buy'])
            markup.add(button['contact_to_me'],button['help'])
            bot.send_message(cid,text['select_menu'],reply_markup=markup)
        
@bot.message_handler(commands=['main'])
def main_command(message) :
    cid=message.chat.id
    if cid in block_user : return
    if user_step[cid] <2000 :
        markup=ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(button['my_acount'],button['buy'])
        markup.add(button['contact_to_me'],button['help'])
        bot.send_message(cid,text['select_menu'],reply_markup=markup)

@bot.message_handler(commands=['help'])
def help_func(message) :
    cid=message.chat.id
    if cid in block_user : return
    if user_step[cid] <2000 :
        bot.send_message(cid,text['help'])

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
    bot.send_message(cid,text['select_breakdown'],reply_markup=markup)

@bot.message_handler(func=lambda message : message.text==button['back'])
def back_func(message) :
    cid=message.chat.id
    if cid in block_user :return
    if user_step[cid]==1250:
        markup=ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(button['user_profile'],button['cart_basket'])
        markup.add(button['home'])
        user_step[cid]=1200
        bot.send_message(cid,text['select_switch'],reply_markup=markup)

@bot.message_handler(func=lambda message : message.text==button['help'])
def help_func(message) :
    cid=message.chat.id
    if cid in block_user : return
    if user_step[cid] <2000 :
        bot.send_message(cid,text['help'])

    
@bot.message_handler(func=lambda message : message.text==button['home'])
def home_func(message):
    cid=message.chat.id
    if cid in block_user :return
    if user_step[cid] <2000 :
        user_step[cid]=1000
        markup=ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(button['my_acount'],button['buy'])
        markup.add(button['contact_to_me'],button['help'])
        bot.send_message(cid,text['select_menu'],reply_markup=markup)
        
       
@bot.message_handler(func=lambda message : message.text==button['my_acount'])
def button_buy(message) :
    cid=message.chat.id
    if cid in block_user :return
    if user_step[cid] >= 2000 :return
    markup=ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(button['user_profile'],button['cart_basket'])
    markup.add(button['home'])
    user_step[cid]=1200
    bot.send_message(cid,text['select_switch'],reply_markup=markup)

@bot.message_handler(func=lambda message : message.text==button['user_profile'])
def user_Profile_func(message):
    cid=message.chat.id
    if cid in block_user :return
    markup=ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(button['personal_id'],button['full_name'])
    markup.add(button['adress'],button['mobile'])
    markup.add(button['back'],button['register'])
    markup.add(button['home'])
    user_step[cid]=1250
    bot.send_message(cid,text['add_personal'],reply_markup=markup)    
  
 
@bot.message_handler(func=lambda message : message.text==button['full_name'])
def full_name_func(message):
    cid=message.chat.id
    if cid in block_user :return
    user_step[cid]=1251
    bot.send_message(cid,text['message_name'])    

@bot.message_handler(func=lambda message : message.text==button['personal_id'])
def personal_id_func(message):
    cid=message.chat.id
    if cid in block_user :return
    user_step[cid]=1252
    bot.send_message(cid,text['message_national_code'])      


@bot.message_handler(func=lambda message : message.text==button['mobile'])
def mobile_phone_func(message):
    cid=message.chat.id
    if cid in block_user :return
    markup=ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton(button['send number'], request_contact=True))
    user_step[cid]= 1253
    bot.send_message(cid, text['share_phone'], reply_markup=markup)
    
@bot.message_handler(func=lambda message : message.text==button['adress'])
def adress_func(message):
    cid=message.chat.id
    if cid in block_user :return
    user_step[cid]=1254
    bot.send_message(cid,text['adress_message'])      
     
       
@bot.message_handler(content_types= ['contact'])
def contact_handler(message):
    cid=message.chat.id
    if cid in block_user :return
    if user_step[cid] == 1253 :
        phone_number = message.contact.phone_number
        user_id = message.contact.user_id
        if cid == user_id :
            mobile_phone_temp.update({cid:phone_number})
            markup=ReplyKeyboardMarkup(resize_keyboard=True)
            markup.add(button['personal_id'],button['full_name'])
            markup.add(button['adress'],button['mobile'])
            markup.add(button['back'],button['register'])
            markup.add(button['home'])
            user_step[cid]=1250
            bot.send_message(cid,text['ok'],reply_markup=markup)    
        else :
            user_step[cid]=1250
            markup=ReplyKeyboardMarkup(resize_keyboard=True)
            markup.add(KeyboardButton(button['send number'], request_contact=True))
            user_step[cid]= 1253
            bot.send_message(cid,text['mobile_error'], reply_markup=markup)   
    

@bot.message_handler(func=lambda message : message.text==button['register'])
def register_account_func(message):
    cid=message.chat.id
    if cid in block_user :return
    if cid in full_name_temp :
        if cid in national_code_temp :
            if cid in mobile_phone_temp :
                if cid in adress_temp :
                     #user_data={cid : [fullname, mobile phone, national code ,username ,adress],....}
                    user=user_profile.get(cid)
                    user[0]=full_name_temp.get(cid)
                    user[1]=mobile_phone_temp.get(cid)
                    user[2]=national_code_temp.get(cid)
                    user[4]=adress_temp.get(cid)
                    user_profile.update({cid:user})
                    update_user(cid =cid , fullname=user[0] , mobile_phone=user[1] , national_code=user[2] , adress=user[4] )
                    full_name_temp.pop(cid)
                    mobile_phone_temp.pop(cid)
                    national_code_temp.pop(cid)
                    adress_temp.pop(cid)
                    bot.send_message(cid,text['sabt'])
                    markup=ReplyKeyboardMarkup(resize_keyboard=True)
                    markup.add(button['user_profile'],button['cart_basket'])
                    markup.add(button['home'])
                    user_step[cid]=1200
                    bot.send_message(cid,text['select_switch'],reply_markup=markup)
                else :
                    user_step[cid]=1254
                    bot.send_message(cid,text['adress_message'])      
            else :
                markup=ReplyKeyboardMarkup(resize_keyboard=True)
                markup.add(KeyboardButton(button['send number'], request_contact=True))
                user_step[cid]= 1253
                bot.send_message(cid, text['share_phone'], reply_markup=markup)                
        else :
            user_step[cid]=1252
            bot.send_message(cid,text['message_national_code'])              
    else :
        user_step[cid]=1251
        bot.send_message(cid,text['message_name'])              

        

@bot.message_handler(func=lambda message : message.text==button['contact_to_me'])
def contact_to_me_func(message):
    cid=message.chat.id
    if cid in block_user :return
    if user_step[cid] <2000 :
        bot.send_message(cid,text['call_admin'])



@bot.message_handler(func=lambda message :True)
def message_func(message):
    cid=message.chat.id
    if cid in block_user :return
    if user_step[cid]==1251 :
        full_name =message.text
        full_name_temp.update({cid:full_name})
        markup=ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(button['personal_id'],button['full_name'])
        markup.add(button['adress'],button['mobile'])
        markup.add(button['back'],button['register'])
        markup.add(button['home'])
        user_step[cid]=1250
        bot.send_message(cid,text['ok'],reply_markup=markup) 
    elif user_step[cid] == 1252 :
        national_code= message.text
        if national_code.isnumeric() == True :
            if  len(national_code) ==10 :
                national_code_temp.update({cid:national_code})
                markup=ReplyKeyboardMarkup(resize_keyboard=True)
                markup.add(button['personal_id'],button['full_name'])
                markup.add(button['adress'],button['mobile'])
                markup.add(button['back'],button['register'])
                markup.add(button['home'])
                user_step[cid]=1250
                bot.send_message(cid,text['ok'],reply_markup=markup)    
            else :
                bot.send_message(cid,text['national_Error2'])
        else :
            bot.send_message(cid,text['national_Error1'])
    elif user_step[cid] ==1254 :
        adress_text=message.text
        adress_temp.update({cid:adress_text})
        markup=ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(button['personal_id'],button['full_name'])
        markup.add(button['adress'],button['mobile'])
        markup.add(button['back'],button['register'])
        markup.add(button['home'])
        user_step[cid]=1250
        bot.send_message(cid,text['ok'],reply_markup=markup)    
        

bot.infinity_polling()
