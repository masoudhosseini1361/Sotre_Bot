
import telebot
import logging
import time
from jdatetime import date ,timedelta
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
category=dict()         #category={name_category :show_categroy=YES OR NO,...}
admin=[]     #admin=[cid admin]
block_user=[]        #block user = [cid block ,...]
user_cid=[]            #user_cid =[cid,cid,....]
user_step.update({manager[0]:3000})
full_name_temp=dict()        #full_name={cid :fulname,....}
national_code_temp= dict()   #national_code={cid :national_code ,....}
mobile_phone_temp =dict()    #mobile_phone={cid :mobile_phone,....}
adress_temp =dict()          #adress={cid:adress}
category_temp=dict()          #category_temp={cid :[name_category,mid]}
category_oldname=dict()        #category_oldname={cid:oldnamecategory,....}
kala=dict()                     #kala={id:[kalaname,buy_price,sale_price,name_category,kala_date,image_file_id,count,M,L,XL,XXL],.....}
kala_temp= dict()               #kala_temp ={cid={kalaname :name ,category:category,image_file_id :file_id ,sale_price:price,}}
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
result =get_info_category()
if len(result) !=0 :
    for i in result :
        category.update({i['name_category']:i['show_category']})
        
result =get_info_kala()
if len(result) !=0 :
    for i in result :
        kala.update({i['id']:[i['kalaname'],i['buy_price'],i['sale_price'],i['name_category'],i['kala_date'],i['image_file_id'],i['count'],i['M'],i['L'],i['XL'],i['XXL']]})


button= {
        'my_acount' :            'حساب کاربری من  👤',
        'help' :                 'راهنمای استفاده از بات',
        'buy'  :                 'خرید',
        'contact_to_me' :        'تماس با ما  📞' ,
        'back' :                 'بازگشت',
        'register' :             'ثبت  ✅',
        'cancel':                'کنسل  ❌',
        'shirt' :                'پیراهن',
        'tshirt' :               'تی شرت',
        'pants' :                'شلوار',
        'home' :                 'منوی اصلی  🏛️',
        'cart_basket' :          'سبد خرید  🛒' ,
        'user_profile' :         'مشخصات کاربری',
        'full_name':             'نام و نام خانوادگی' ,
        'mobile' :               'شماره موبایل' ,
        'personal_id'  :         'کد ملی' ,
        'adress' :               'آدرس',
        'send number':          'ارسال شماره موبایل',
        'kala' :                'کالا  📦',
        'invoice' :             'فاکتور  🧾',
        'admin' :               'ادمین  👨🏻‍💻',
        'finacial_department' : 'امور مالی  💰',
        'reports' :             'گزارشات  📊',
        'group':                'گروه  🗂️' ,       
        'add_group' :           'تعریف گروه جدید  ➕',
        'category_name':        'نام گروه',
        'edit':                 'اصلاح مشخصات  ✏️',
        'delete_kala':          'حذف کالا  🗑',
        'delete_group':         'حذف گروه  🗑',
        'add_kala':             'تعریف کالا جدید  ➕',
        'photo_image':          'ارسال عکس',
        'description':          'نام کالا',
        'sale_price' :          'قیمت فروش ',
        
        
        }

command= {  
          'start' :'شروع به کار رباط' ,
          'help'  :'راهنمایی استفاده از رباط',
          'main'  :'منوی اصلی برنامه',
         }

def get_user_step(cid):
    return user_step.setdefault(cid, 1000)

def creat_marrkup_button(step) :
    pass



bot = telebot.TeleBot(API_TOKEN, num_threads=therad_num)





# only used for console output
# this is then listener function
def listener(messages):
    """
    When new messages arrive TeleBot will call this function.
    """
    for m in messages:
        if m.content_type == 'text':
            # print the sent message to the console
            logging.info(str(m.chat.first_name) + " [" + str(m.chat.id) + "]: " + m.text)
bot.set_update_listener(listener)  # register listener


#function 

def date_today():
    today=date.today()
    today=today.strftime("%Y/%m/%d")
    return today

def make_inlinekeyboardMarkup_category(cid=None ,mid=None):
        markup=InlineKeyboardMarkup() 
        for i in category.keys():
             markup.add(InlineKeyboardButton(f'{i}',callback_data=f'group_edit/{i}'))
        inline_button=button['add_group']
        markup.add(InlineKeyboardButton(f'{inline_button}   ',callback_data='group_add/add'))
        markup.add(InlineKeyboardButton(button['cancel'],callback_data='group_add/cancel'))  
        if mid == None :
            bot.send_message(cid,text['add_group'],reply_markup=markup)  
        else: 
            bot.edit_message_text(text['add_group'],cid,mid,reply_markup=markup)

def inline_add_group(cid , mid):
    if user_step[cid] ==2100 or user_step[cid] ==3100:
        if user_step[cid] == 2100 :
            user_step[cid] = 2110
        else :
            user_step[cid] = 3110 
    markup=InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(category_temp[cid][0],callback_data='group_add/namecategory'))
    markup.add(InlineKeyboardButton(button['register'],callback_data='group_add/sabt'))
    markup.add(InlineKeyboardButton(button['cancel'],callback_data='group_add/cancel'))
    bot.edit_message_text(text['add_name_group'],cid,mid,reply_markup=markup)
    return


def inline_edit_group(cid , mid):
    if user_step[cid] ==2100 or user_step[cid] ==3100:
        if user_step[cid] == 2100 :
            user_step[cid] = 2110
        else :
            user_step[cid] = 3110 
    markup=InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(category_oldname[cid],callback_data='group_edit/namecategory'))
    markup.add(InlineKeyboardButton(button['edit'],callback_data=f'group_edit/edit-{category_oldname[cid]}'))
    markup.add(InlineKeyboardButton(button['delete_group'],callback_data=f'group_edit/delete-{category_oldname[cid]}'))
    markup.add(InlineKeyboardButton(button['back'],callback_data=f'group_edit/back-{category_oldname[cid]}'))
    bot.edit_message_text(text['edit_name_group'],cid,mid,reply_markup=markup)
    return

def inline_change_group(cid , mid):
    if user_step[cid] ==2100 or user_step[cid] ==3100:
        if user_step[cid] == 2100 :
            user_step[cid] = 2110
        else :
            user_step[cid] = 3110 
    markup=InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(category_temp[cid][0],callback_data='group_edit/change-newname'))
    markup.add(InlineKeyboardButton(button['register'],callback_data='group_edit/sabt-newname'))
    markup.add(InlineKeyboardButton(button['cancel'],callback_data='group_edit/cancel-newname'))
    bot.edit_message_text(text['change_name_group'],cid,mid,reply_markup=markup)
    return


def make_inlinekeyboardMarkup_kala(cid=None ,mid=None):
        markup=InlineKeyboardMarkup() 
        markup.add(InlineKeyboardButton(button['add_kala'],callback_data='kala_add/add'))
        markup.add(InlineKeyboardButton(button['edit'],callback_data='kala_edit/edit'))
        markup.add(InlineKeyboardButton(button['delete_kala'],callback_data='kala_delete/delete'))
        markup.add(InlineKeyboardButton(button['back'],callback_data='kala_back/back'))  
        if mid == None :
            bot.send_message(cid,text['add_kala'],reply_markup=markup)  
        else: 
            bot.edit_message_text(text['add_kala'],cid,mid,reply_markup=markup)
            
            
def show_inlinekeyboardMarkup_category(cid=None ,mid=None):
        markup=InlineKeyboardMarkup()
        if user_step[cid]==2121 or user_step[cid]==3121 :           
            for i in category.keys():
                markup.add(InlineKeyboardButton(f'{i}',callback_data=f'kala_add/{i}'))
            markup.add(InlineKeyboardButton(button['back'],callback_data='kala_add/back'))
            markup.add(InlineKeyboardButton(button['cancel'],callback_data='kala_add/cancel'))
        if user_step[cid]==2122 or user_step[cid]==3122 :           
            for i in category.keys():
                markup.add(InlineKeyboardButton(f'{i}',callback_data=f'kala_edit/{i}'))
            markup.add(InlineKeyboardButton(button['back'],callback_data='kala_edit/back'))
            markup.add(InlineKeyboardButton(button['cancel'],callback_data='kala_delete/cancel'))
        if user_step[cid]==2123 or user_step[cid]==3123 :           
            for i in category.keys():
                markup.add(InlineKeyboardButton(f'{i}',callback_data=f'kala_deldte/{i}'))
            markup.add(InlineKeyboardButton(button['back'],callback_data='kala_delete/back'))
            markup.add(InlineKeyboardButton(button['cancel'],callback_data='kala_delete/cancel'))
        bot.edit_message_text(text['choice_group'],cid,mid,reply_markup=markup)



# make ReplyKeyboardMarkup

def make_ReplyKeyboardMarkup(user_s=None):
    markup=ReplyKeyboardMarkup(resize_keyboard=True)
    if user_s >=3000 :
        if user_s  == 3000 :
            markup.add(button['admin'],button['invoice'],button['kala'])
            markup.add(button['reports'],button['finacial_department'])
            return(markup)
        elif user_s ==3100 :
            markup.add(button['kala'],button['group'])
            markup.add(button['home'])
            return(markup)
        
    elif user_s >=2000  and user_s < 3000 :
        if user_s == 2000 :
            markup.add(button['invoice'],button['kala'])
            markup.add(button['reports'],button['finacial_department'])
            return(markup)
        elif user_s ==2100 :
            markup.add(button['kala'],button['group'])
            markup.add(button['home'])
            return(markup)
        
    elif user_s >= 1000 and user_s <1000 :
        pass
    
    #kala_temp ={cid={kalaname :name ,category:category,image_file_id :file_id ,sale_price:price,}}
def  insert_kala_func(cid , mid = None ) :
    kala_cid=kala_temp[cid]
    markup=InlineKeyboardMarkup()
    category=kala_cid['category']
    category1=button['category_name']
    photo_image=button['photo_image']
    description=button['description']
    sale_price=button['sale_price']
    markup.add(InlineKeyboardButton(f'{category1} : {category}',callback_data='kala_add/none'))
    if 'image_file_id' in kala_cid.keys():
        markup.add(InlineKeyboardButton(f'{photo_image} : OK',callback_data='kala_add/imageid'))  
    else:
        markup.add(InlineKeyboardButton(f'{photo_image} : ',callback_data='kala_add/imageid'))  
        
    if 'kalaname' in  kala_cid.keys() :
        kala_name=kala_cid['kalaname']
        markup.add(InlineKeyboardButton(f'{description} : {kala_name}',callback_data='kala_add/kalaname'))  
    else :
         markup.add(InlineKeyboardButton(f'{description} : ',callback_data='kala_add/kalaname'))     
    if 'sale_price' in kala_cid.keys():
        price=kala_cid['sale_price'] 
        markup.add(InlineKeyboardButton(f'{sale_price} : {price}',callback_data='kala_add/saleprice'))  
    else :
        markup.add(InlineKeyboardButton(f'{sale_price} : ',callback_data='kala_add/saleprice'))
        
    markup.add(InlineKeyboardButton(button['register'],callback_data='kala_add/sabt'))
    markup.add(InlineKeyboardButton(button['cancel'],callback_data='kala_add/cancel'))        
    if mid == None :
        bot.send_message(cid,text['add_kala_detail'],reply_markup=markup)  
    else:    
        bot.edit_message_text(text['add_kala_detail'],cid,mid,reply_markup=markup)
        
        
           
# Inline QURY HANDLER

@bot.callback_query_handler(func=lambda call: True)
def call_back_handler(call):
    cid = call.message.chat.id
    data = call.data
    mid = call.message.message_id
    call_id = call.id
    print(f'cid: {cid}, data: {data}, mid: {mid}, id: {call_id}')
    # if call.message.date > time.time() + 10:
    #     bot.edit_message_reply_markup(cid, mid, reply_markup=None)
    if call.message.date < (time.time()-86400) :
        bot.edit_message_reply_markup(cid, mid, reply_markup=None)
    elif data.startswith('group'):
        data=data.split('_')[-1]
        if user_step[cid] ==3110 or user_step[cid] ==2110  :
            if data.startswith('add'): 
                data= data.split('/')[-1]               
                if data =='add' :
                    category_temp.setdefault(cid,[button['category_name'],mid]) 
                    inline_add_group(cid ,mid)
                elif data =='namecategory' :             
                    bot.send_message(cid,text['name_group'])
                elif data == 'sabt' :
                    if category_temp[cid][0]==button['category_name'] :
                        bot.send_message(cid,text['sabt_error'])
                    else:
                        if user_step[cid] ==2110 :
                            user_step[cid] =2100
                        else :
                            user_step[cid]=3100   
                        name_category =category_temp[cid][0]
                        insert_category(name_category=name_category,show_category='YES')
                        bot.answer_callback_query(call_id, text['sabt'])
                        bot.edit_message_reply_markup(cid, mid, reply_markup=None)
                        category.update({name_category:"YES"})
                        category_temp.pop(cid)
                elif data == 'cancel' :
                    if cid in category_temp.keys() :
                        category_temp.pop(cid)
                    if user_step[cid] ==2110  :
                        user_step[cid] =2100
                    elif user_step[cid]==3110 :
                        user_step[cid]=3100   
                    bot.edit_message_reply_markup(cid, mid, reply_markup=None)
            elif data.startswith('edit'):              
                data= data.split('/')[-1]
               # print(data,'in')
                if data in category.keys():
                    category_temp.update({cid:[data,mid]})
                    category_oldname.update({cid:data})
                    # print(data,'2')
                    inline_edit_group(cid , mid)
                elif data.split('-')[0] =='edit' :
                    data= data.split('-')[0]
                    inline_change_group(cid , mid)   
                elif data.split('-')[0] =='delete' :
                    if user_step[cid] ==2110 :
                        user_step[cid] =2100
                    else :
                        user_step[cid]=3100                    
                    data= data.split('-')[0]
                    # print (category_oldname[cid])
                    delete_category(name_category=category_oldname[cid])
                    category.pop(category_oldname[cid])
                    category_temp.pop(cid)
                    category_oldname.pop(cid)
                    bot.edit_message_reply_markup(cid, mid, reply_markup=None)
                elif data.split('-')[0] =='change' :
                    if user_step[cid] ==2110 :
                        user_step[cid] =2111
                    else :
                        user_step[cid]=3111                    
                    bot.send_message(cid,text['new_name_group'])
                elif data.split('-')[0] =='sabt' :
                    if category_temp[cid][0] in category.keys() :
                        bot.send_message(cid,text['sabt_error'])
                    else:
                        if user_step[cid] ==2110 :
                            user_step[cid] =2100
                        else :
                            user_step[cid]=3100   
                        new_name_category =category_temp[cid][0]
                        old_name_category=category_oldname[cid]
                        show_category=category[old_name_category]
                        update_category(new_name_category=new_name_category ,old_name_category=old_name_category)
                        bot.answer_callback_query(call_id, text['sabt'])
                        bot.edit_message_reply_markup(cid, mid, reply_markup=None)
                        category.pop(old_name_category)
                        category.update({new_name_category:show_category})
                        category_temp.pop(cid)
                        category_oldname.pop(cid)
                        
                elif data.split('-')[0] =='cancel' :
                    if cid in category_temp.keys() :
                        category_temp.pop(cid)
                        category_oldname.pop(cid)
                    if user_step[cid] ==2110 :
                        user_step[cid] =2100
                    else :
                        user_step[cid]=3100   
                    bot.edit_message_reply_markup(cid, mid, reply_markup=None)              
                elif data.split('-')[0]=='back':
                   make_inlinekeyboardMarkup_category(cid=cid ,mid=mid)   
            else :
                bot.answer_callback_query(call_id, text['no_data'])  
                bot.edit_message_reply_markup(cid, mid, reply_markup=None)    
        else :
            bot.edit_message_reply_markup(cid, mid, reply_markup=None)        
    elif data.startswith('kala'):
        if (user_step[cid] >=3120 and user_step[cid] <3130 ) or (user_step[cid] >=2120 and user_step[cid] <2130)  :
            data=data.split('_')[-1]
            if data.startswith('add') :   
                data=data.split('/')[-1]
                if data=='add':
                    if user_step[cid] == 2120 :
                        user_step[cid]= 2121
                    elif user_step[cid]== 3120 :
                        user_step[cid] = 3121    
                    show_inlinekeyboardMarkup_category(cid=cid ,mid=mid)
                elif data in category.keys():
                    kala_temp.update({cid:{'category':data}})
                    insert_kala_func(cid=cid , mid =mid)
                elif data == 'imageid' :
                    bot.edit_message_text(text['image_message'],cid,mid,reply_markup=None)  
                elif data =='kalaname' :
                    bot.edit_message_text(text['kala_message'],cid,mid,reply_markup=None) 
                elif data == 'saleprice' :
                    if user_step[cid] == 2121 :
                        user_step[cid]= 2121.1
                    elif user_step[cid]== 3121 :
                        user_step[cid] = 3121.1
                    bot.edit_message_text(text['price_message'],cid,mid,reply_markup=None)
                elif data =='sabt' :
                    kala_cid=kala_temp[cid]
                    if 'kalaname' not in kala_cid.keys() or  'image_file_id' not in kala_cid.keys() or 'sale_price' not in kala_cid.keys() :
                        bot.send_message(cid ,text['all_detail'])
                    else :
                        kalaname =kala_temp[cid]['kalaname']
                        name_category=kala_temp[cid]['category']
                        file_id=kala_temp[cid]['image_file_id']
                        sale_price=int( kala_temp[cid]['sale_price']) 
                        kala_date =date_today()
                        insert_kala( kalaname=kalaname,name_category=name_category ,kala_date=kala_date,image_file_id=file_id,sale_price=sale_price )
                        id =last_kala_id()
                        kala.update({id:[kalaname,0,sale_price,name_category,kala_date,file_id,0,0,0,0,0]})
                        bot.answer_callback_query(call_id, text['sabt'])
                        bot.edit_message_text(text['sabt_kala'],cid, mid, reply_markup=None)
                        kala_temp.pop(cid)
                        if user_step[cid] == 2121 :
                            user_step[cid]= 2100
                        elif user_step[cid]== 3121 :
                            user_step[cid] = 3100

                elif data =='cancel' :
                    kala_temp.pop(cid)
                    bot.edit_message_reply_markup(cid, mid, reply_markup=None)                    
                    if user_step[cid] ==2121 :
                        user_step[cid] =2100
                    elif user_step[cid] ==3121  :
                        user_step[cid]=3100   
                
                        
            elif data.startswith('edit'):
                data=data.split('/')[-1]        
                if data=='edit':
                    if user_step[cid] == 2120 :
                        user_step[cid]= 2122
                    elif user_step[cid]== 3120 :
                        user_step[cid] = 3122
                    show_inlinekeyboardMarkup_category(cid=cid ,mid=mid)
            elif data.startswith('delete'):
                data=data.split('/')[-1]
                if data =='delete':
                    if user_step[cid] == 2120 :
                            user_step[cid]= 2123
                    elif user_step[cid]== 3120 :
                        user_step[cid] = 3123
                    show_inlinekeyboardMarkup_category(cid=cid ,mid=mid)
            elif data.startswith('back'):
                data=data.split('/')[-1]
                if data=='back' :
                    if user_step[cid] == 2120 :
                            user_step[cid]= 2100
                    elif user_step[cid]== 3120 :
                        user_step[cid] = 3100 
                    bot.edit_message_reply_markup(cid, mid, reply_markup=None) 
            
        else :  
            bot.edit_message_reply_markup(cid, mid, reply_markup=None)
              
    else :
        bot.answer_callback_query(call_id, text['no_data'])  
        bot.edit_message_reply_markup(cid, mid, reply_markup=None)      








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
            bot.send_message(cid,text['select_menu'],reply_markup=make_ReplyKeyboardMarkup(user_s=user_step[cid]))
          
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
    elif user_step[cid] >= 2000 and user_step[cid] <3000 :
            pass
    elif user_step[cid] >= 3000 :
        bot.send_message(cid,text['select_menu'],reply_markup=make_ReplyKeyboardMarkup(user_s=user_step[cid]))
        

@bot.message_handler(commands=['help'])
def help_func(message) :
    cid=message.chat.id
    if cid in block_user : return
    if user_step[cid] <2000 :
        bot.send_message(cid,text['help'])

#ReplyKeyboardMarkup

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

@bot.message_handler(func=lambda message : message.text==button['kala'])
def kala_func(message) :
    cid=message.chat.id
    if cid in block_user : return
    if user_step[cid] >=2000 :
        if user_step[cid] == 2000 :
            user_step[cid] = 2100
            bot.send_message(cid,text['select_menu'],reply_markup=make_ReplyKeyboardMarkup(user_s=user_step[cid]))
        elif user_step[cid] == 2100 :
            user_step[cid] =2120
            make_inlinekeyboardMarkup_kala(cid=cid)            
        elif user_step[cid] == 3000:
            user_step[cid] = 3100
            bot.send_message(cid,text['select_menu'],reply_markup=make_ReplyKeyboardMarkup(user_s=user_step[cid]))
        elif user_step[cid] == 3100 :
            user_step[cid] = 3120
            make_inlinekeyboardMarkup_kala(cid=cid)       
        

@bot.message_handler(func=lambda message : message.text==button['group'])
def group_func(message) :
    cid=message.chat.id       
    if cid in block_user : return
    if user_step[cid] ==2100 or user_step[cid]==3100 :
        if user_step[cid] == 2100 :
            user_step[cid] = 2110
        else :
            user_step[cid] = 3110
        make_inlinekeyboardMarkup_category(cid=cid)   
    else :
        if 2110 <user_step[cid] < 2200 :
            user_step[cid] ==2100
        elif 3110 <user_step[cid] <3200 :
            user_step[cid] =3100 
        bot.send_message(cid,text['select_menu'],reply_markup=make_ReplyKeyboardMarkup(user_s=user_step[cid]))
    


@bot.message_handler(func=lambda message : message.text==button['home'])
def home_func(message):
    cid=message.chat.id
    print(user_step[cid])
    if cid in block_user :return
    if user_step[cid] <2000 :
        user_step[cid]=1000
        markup=ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(button['my_acount'],button['buy'])
        markup.add(button['contact_to_me'],button['help'])
        bot.send_message(cid,text['select_menu'],reply_markup=markup)
    elif user_step[cid] >=2000 and user_step[cid] <3000 :
            user_step[cid]=2000
            markup=ReplyKeyboardMarkup(resize_keyboard=True)
            markup.add(button['invoice'],button['kala'])
            markup.add(button['reports'],button['finacial_department'])

            bot.send_message(cid,text['select_menu'],reply_markup=markup)
    elif user_step[cid] >=3000 :
            user_step[cid]=3000
            markup=ReplyKeyboardMarkup(resize_keyboard=True)
            markup.add(button['admin'],button['invoice'],button['kala'])
            markup.add(button['reports'],button['finacial_department'])

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



@bot.message_handler(content_types=['photo'])
def photo_handler(message):
    cid =message.chat.id
    if cid in block_user: return
    if user_step[cid] == 2121 or user_step[cid] == 3121:
        file_id = message.photo[-1].file_id
        print (file_id)
        kala_cid=kala_temp[cid]
        kala_cid.update({'image_file_id' :file_id})
        kala_temp.update({cid : kala_cid})
        insert_kala_func(cid)




@bot.message_handler(func=lambda message :True)
def message_func(message):
    print(message)
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
    elif user_step[cid] ==3110 or user_step[cid] ==2110 :
        name_category=message.text
        mid=category_temp[cid][1]
        category_temp.update({cid:[name_category,mid]})
        inline_add_group(cid , mid)
    elif user_step[cid] ==3111 or user_step[cid] ==2111 :
        if user_step[cid]==2111:
            user_step[cid]=2110
        else:
            user_step[cid]=3110    
        name_category=message.text
        mid=category_temp[cid][1]
        category_temp.update({cid:[name_category,mid]})
        inline_change_group(cid , mid)
    elif user_step[cid] ==3121 or user_step[cid] ==2121 :
        kala_cid= kala_temp[cid]
        kala_name =message.text
        kala_cid.update({'kalaname' :kala_name})
        kala_temp.update({cid:kala_cid})
        insert_kala_func(cid)
    elif user_step[cid] ==3121.1 or user_step[cid] ==2121.1 :
        if user_step[cid] == 2121.1 :
            user_step[cid]= 2121
        elif user_step[cid]== 3121.1 :
            user_step[cid] = 3121
        kala_cid= kala_temp[cid]
        price =message.text
        kala_cid.update({'sale_price': price })
        kala_temp.update({cid:kala_cid})
        insert_kala_func(cid)

    
    
bot.infinity_polling()
