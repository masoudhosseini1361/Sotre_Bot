
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
mid_cid=dict()                  #mid_cid={cid:mid,........}
cid_user=dict()                   #cid_user={cid:user of account cid}
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
        'user_account' :         'حساب کاربری من  👤',
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
        'admin_account':        'طرف حساب  👤',
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
        'search':               'جستجو  🔎',
        'add_account' :         'تعریف طرف حساب جدید  ➕',
        'edit_account':         'اصلاح وضیعت  ✏️',
        'delete_account':       'حذف طرف حساب  🗑', 
        'search_name':          'جستجو بر اساس نام',
        'search_nationalcode':  'جستجو براساس کد ملی',
        'search_mobile':        'جستجو بر اساس موبایل', 
              
        }

command= {  
          'start' :'شروع به کار رباط' ,
          'help'  :'راهنمایی استفاده از رباط',
          'main'  :'منوی اصلی برنامه',
         }

def get_user_step(cid):
    return user_step.setdefault(cid, 1000)




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
            markup.add(InlineKeyboardButton(button['back'],callback_data='kala_add/back'),InlineKeyboardButton(button['cancel'],callback_data='kala_add/cancel'))
        if user_step[cid]==2122 or user_step[cid]==3122 :           
            for i in category.keys():
                markup.add(InlineKeyboardButton(f'{i}',callback_data=f'kala_edit/{i}'))
            markup.add(InlineKeyboardButton(button['back'],callback_data='kala_edit/back'),InlineKeyboardButton(button['cancel'],callback_data='kala_edit/cancel'))
        if user_step[cid]==2123 or user_step[cid]==3123 :           
            for i in category.keys():
                markup.add(InlineKeyboardButton(f'{i}',callback_data=f'kala_delete/{i}'))
            markup.add(InlineKeyboardButton(button['back'],callback_data='kala_delete/back'),InlineKeyboardButton(button['cancel'],callback_data='kala_delete/cancel'))
        bot.edit_message_text(text['choice_group'],cid,mid,reply_markup=markup)

def make_admin_account_inlinekeyboard(cid , mid=None) :
    markup =InlineKeyboardMarkup()
    if user_step[cid] == 2200 or user_step[cid] == 3200:
        markup.add(InlineKeyboardButton(button['search'],callback_data=f'adminaccount/search=search'))
    #    markup.add(InlineKeyboardButton(button['add_account'],callback_data=f'adminaccount/add=add'))
        markup.add(InlineKeyboardButton(button['edit_account'],callback_data=f'adminaccount/edit=edit'))
    #    markup.add(InlineKeyboardButton(button['delete_account'],callback_data=f'adminaccount/delete=delete'))
        markup.add(InlineKeyboardButton(button['back'],callback_data=f'adminaccount/back=back'))
    if mid ==None :
        bot.send_message(cid,text['select_menu'],reply_markup=markup)  
    else :
        bot.edit_message_text(text['select_menu'],cid,mid,reply_markup=markup)
        
def make_search_inlinemarkup(cid, mid=None) :
    markup=InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(button['search_name'],callback_data=f'adminaccount/search=name'))    
    markup.add(InlineKeyboardButton(button['search_nationalcode'],callback_data=f'adminaccount/search=nationalcode'))    
    markup.add(InlineKeyboardButton(button['search_mobile'],callback_data=f'adminaccount/search=mobile'))    
    markup.add(InlineKeyboardButton(button['back'],callback_data=f'adminaccount/search=back'),InlineKeyboardButton(button['cancel'],callback_data=f'adminaccount/search=cancel'))
    if mid == None :
        bot.send_message(cid,text['search_account'],reply_markup=markup)
    else :    
        bot.edit_message_text(text['search_account'],cid,mid,reply_markup=markup)



def make_edit_adminaccount_inline(cid ,mid=None,result=None,cid_user_priv=None ,sabt=None) :
    markup=InlineKeyboardMarkup()
    if mid == None :
        mid=mid_cid[cid]
    if result ==None and (user_step[cid] == 3220 or user_step[cid]==2220):    
        markup.add(InlineKeyboardButton(button['search_name'],callback_data=f'adminaccount/edit=name'))    
        markup.add(InlineKeyboardButton(button['search_nationalcode'],callback_data=f'adminaccount/edit=nationalcode'))    
        markup.add(InlineKeyboardButton(button['search_mobile'],callback_data=f'adminaccount/edit=mobile'))    
        markup.add(InlineKeyboardButton(button['back'],callback_data=f'adminaccount/edit=back'),InlineKeyboardButton(button['cancel'],callback_data=f'adminaccount/edit=cancel'))   
        bot.edit_message_text(text['search_account'],cid,mid,reply_markup=markup)
    elif user_step[cid] == 3224 or user_step[cid]==2224 :
        for i in result:
            id=i['id']
            cid_user_= i['cid']
            fullname=i['fullname']
            username=i['username']
            national_code=i['national_code']
            mobile_phone=i['mobile_phone']
            adress=i['adress']
            privilege=i['privilege']
            is_block = i['is_block']
            user_date=i['user_date']
            markup.add(InlineKeyboardButton(f'نام : {fullname}--کد ملی :{national_code} --موبایل : {mobile_phone}',callback_data=f'adminaccount/edit={cid_user_}'))  
        markup.add(InlineKeyboardButton(button['back'],callback_data=f'adminaccount/edit=back'),InlineKeyboardButton(button['cancel'],callback_data=f'adminaccount/edit=cancel'))    
        bot.edit_message_text(text['select_switch'],cid,mid,reply_markup=markup)      
    
    elif user_step[cid] ==3224.1 :
        
        result =search_condition_on_user(cid=cid_user_priv)   
        print(result)
        result=result[0]
        fullname=result['fullname']
        privilege=result['privilege']
        if privilege =='USER' :
           n_privilege ='ADMIN'
        else : 
            n_privilege ='USER'
                
        is_block=result['is_block']
        if is_block == 'YES' :
            n_is_block= 'NO'
        else :
            n_is_block ='YES' 
        block_condition=text['block_condition']
        user_condition =text['user_condition']
        markup.add(InlineKeyboardButton(f'{fullname}',callback_data=f'adminaccount/edit=none'))  
        markup.add(InlineKeyboardButton(f'{user_condition} : {privilege} ',callback_data=f'adminaccount/edit=privilege-{n_privilege}'))
        markup.add(InlineKeyboardButton(f'{block_condition}  : {is_block}',callback_data=f'adminaccount/edit=is_block-{n_is_block}')) 
        markup.add(InlineKeyboardButton(button['cancel'],callback_data=f'adminaccount/edit=cancel'))
        bot.edit_message_text(text['change_condition'],cid,mid,reply_markup=markup) 
    
    elif user_step[cid] ==2224.1  :       
        result =search_condition_on_user(cid=cid_user_priv)
        fullname=result[0]['fullname']
        is_block=result[0]['is_block']
        if is_block == 'YES' :
            n_is_block= 'NO'
        else :
            n_is_block ='YES'
        block_condition=text['block_condition']
        user_condition =text['user_condition']
        markup.add(InlineKeyboardButton(f'{fullname}',callback_data=f'adminaccount/edit=none'))  
        markup.add(InlineKeyboardButton(f'{block_condition}  : {is_block}',callback_data=f'adminaccount/edit=is_block-{n_is_block}')) 
        markup.add(InlineKeyboardButton(button['cancel'],callback_data=f'adminaccount/edit=cancel'))
        bot.edit_message_text(text['change_condition'],cid,mid,reply_markup=markup) 
    
    elif user_step[cid] ==3224.2 :
        block_condition=text['block_condition']
        user_condition =text['user_condition']
        if sabt =='USER' :
            markup.add(InlineKeyboardButton(f'{user_condition}  : {sabt}',callback_data=f'adminaccount/edit=none'))         
        elif sabt =='ADMIN' :
            markup.add(InlineKeyboardButton(f'{user_condition}  : {sabt}',callback_data=f'adminaccount/edit=none'))
        elif sabt =='YES' :
            markup.add(InlineKeyboardButton(f'{block_condition} : {sabt}',callback_data=f'adminaccount/edit=none'))
        elif sabt =='NO' :
            markup.add(InlineKeyboardButton(f'{block_condition} : {sabt}' ,callback_data=f'adminaccount/edit=none'))        
        markup.add(InlineKeyboardButton(button['register'],callback_data=f'adminaccount/edit=sabt-{sabt}'),InlineKeyboardButton(button['cancel'],callback_data=f'adminaccount/edit=cancel'))    
        bot.edit_message_text(text['register'],cid,mid,reply_markup=markup)
    elif user_step[cid] ==2224.2 :
        block_condition=text['block_condition']
        if sabt =='YES' :
            markup.add(InlineKeyboardButton(f'{block_condition}: {sabt}',callback_data=f'adminaccount/edit=none'))
        elif sabt =='NO' :
            markup.add(InlineKeyboardButton(f'{block_condition} : {sabt}',callback_data=f'adminaccount/edit=none'))        
        markup.add(InlineKeyboardButton(button['register'],callback_data=f'adminaccount/edit=sabt-{sabt}'),InlineKeyboardButton(button['cancel'],callback_data=f'adminaccount/edit=cancel'))    
        bot.edit_message_text(text['register'],cid,mid,reply_markup=markup)
    
    


    
# make ReplyKeyboardMarkup


#define the main  menu

def make_ReplyKeyboardMarkup(user_s=None):
    markup=ReplyKeyboardMarkup(resize_keyboard=True)
    if user_s >=3000 :
        if user_s  == 3000 :
            # main menu of manager
            markup.add(button['invoice'],button['admin_account'],button['kala'])
            markup.add(button['reports'],button['finacial_department'],button['admin'])
            return(markup)
        elif user_s ==3100 :
            # kala menu on manger
            markup.add(button['kala'],button['group'])
            markup.add(button['home'])
            return(markup)
        elif user_s == 3200 :
            # account menu on manger
            markup.add(button['home'])
            return(markup)
        
    elif user_s >=2000  and user_s < 3000 :
        if user_s == 2000 :
            # main  menu of admin
            markup.add(button['invoice'],button['admin_account'],button['kala'])
            markup.add(button['reports'],button['finacial_department'])
            return(markup)
        elif user_s ==2100 :
            # kala menu on admin
            markup.add(button['kala'],button['group'])
            markup.add(button['home'])
            return(markup)
        elif user_s == 3200 :
            # account menu on admin
            markup.add(button['home'])
            return(markup)        
        
    elif user_s >= 1000 and user_s <2000 :
        if user_s == 1000:
            # main menu on user
    
            markup.add(button['user_account'],button['buy'])
            markup.add(button['contact_to_me'],button['help'])
            return(markup)
        
        



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


        
def edit_kala_func(cid ,mid=None,id=None,call_id=None):
    markup=InlineKeyboardMarkup()
    kala_cid=kala_temp[cid]
    category=kala_cid['category']
    category1=button['category_name']
    photo_image=button['photo_image']
    description=button['description']
    sale_price=button['sale_price']
    result =get_infokala_where_category(category)
    if len(result)== 0:
        bot.answer_callback_query(call_id, text['no_kala'],show_alert=True,cache_time=3)
        return
    if 'id' in kala_cid.keys():
        id=kala_cid['id']
    for i in result :
        if i['id'] ==id :
            kala_id=i['id']
            kalaname=i["kalaname"]
            sale_price1=i['sale_price']
            break

    
    if 'id' in kala_cid.keys() :
        markup.add(InlineKeyboardButton(f'{category1} : {category}',callback_data=f'kala_edit/id=none'))
        if 'image_file_id' in kala_cid.keys():
            markup.add(InlineKeyboardButton(f'{photo_image} : OK',callback_data=f'kala_edit/id=imageid'))  
        else:
            markup.add(InlineKeyboardButton(f'{photo_image} : ',callback_data=f'kala_edit/id=imageid'))  
            
        if 'kalaname' in  kala_cid.keys() :
            kala_name=kala_cid['kalaname']
            markup.add(InlineKeyboardButton(f'{description} : {kala_name}',callback_data=f'kala_edit/id=kalaname'))  
        else :
            markup.add(InlineKeyboardButton(f'{description} : {kalaname}',callback_data=f'kala_edit/id=kalaname'))     

        if 'sale_price' in kala_cid.keys():
            price=kala_cid['sale_price'] 
            markup.add(InlineKeyboardButton(f'{sale_price} : {price}',callback_data=f'kala_edit/id=saleprice'))  
        else :
            markup.add(InlineKeyboardButton(f'{sale_price} : {sale_price1}',callback_data=f'kala_edit/id=saleprice'))  
        markup.add(InlineKeyboardButton(button['register'],callback_data=f'kala_edit/id=sabt'))
        markup.add(InlineKeyboardButton(button['cancel'],callback_data=f'kala_edit/id=cancel'))
        if mid==None :
            bot.send_message(cid,text['change_kala1'],reply_markup=markup)
        else :
            bot.edit_message_text(text['change_kala1'],cid,mid,reply_markup=markup)
                   
    else :
       for i in result :
            kala_id=i['id']
            kalaname=i["kalaname"]
            description = f'کد کالا :{kala_id} ----نام کالا :{kalaname}'
            markup.add(InlineKeyboardButton(description,callback_data= f'kala_edit/id={kala_id}'))
       bot.edit_message_text(text['change_kala'],cid,mid,reply_markup=markup)     
        

def delete_kala_func(cid ,mid=None,id=None,call_id=None):
    kala_cid=kala_temp[cid]
    category=kala_cid['category']
    result =get_infokala_where_category(category)
    if len(result)== 0:
        bot.answer_callback_query(call_id, text['no_kala'],show_alert=True,cache_time=3)
        return
    if 'id' in kala_cid.keys():
        id=kala_cid['id']
    
    markup=InlineKeyboardMarkup()
    if 'id' in kala_cid.keys() :
       result =get_info_salrow_where_kala_id(kala_id=id)
       print(len(result))
       if len(result) == 0:
           kala_temp.pop(cid)
           kala.pop(id)
           delete_kala(id=id) 
           bot.edit_message_text(text['delete_kala'],cid,mid,reply_markup=None)
           bot.answer_callback_query(call_id, text['delete_kala1'],show_alert=True,cache_time=3)
       else :
           kala_temp.pop(cid)
           bot.edit_message_text(text['delete_kala'],cid,mid,reply_markup=None)
           bot.answer_callback_query(call_id, text['delete_kala2'],show_alert=True,cache_time=3) 
       if user_step[cid]==3123 :
           user_step[cid]=3100
       elif user_step[cid]==2123:
           user_step[cid]=2100                                                  
    else :
       for i in result :
            kala_id=i['id']
            kalaname=i["kalaname"]
            description = f'کد کالا :{kala_id} ----نام کالا :{kalaname}'
            markup.add(InlineKeyboardButton(description,callback_data= f'kala_delete/id={kala_id}'))
       markup.add(InlineKeyboardButton(button['back'],callback_data= f'kala_delete/id=back'),InlineKeyboardButton(button['cancel'],callback_data= f'kala_delete/id=cancel'))
       bot.edit_message_text(text['delete_kala'],cid,mid,reply_markup=markup)     


# Inline QURY HANDLER

@bot.callback_query_handler(func=lambda call: True)
def call_back_handler(call):
    cid = call.message.chat.id
    data = call.data
    mid = call.message.message_id
    call_id = call.id
    u_step=user_step[cid]
    print(f'cid: {cid}, data: {data}, mid: {mid}, id: {call_id},  user step:{u_step}')
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
                        bot.answer_callback_query(call_id, text['sabt'],show_alert=True,cache_time=3)
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
                    result =get_infokala_where_category(data)
                    if len(result)== 0:
                        category_temp.update({cid:[data,mid]})
                        category_oldname.update({cid:data})
                        # print(data,'2')
                        inline_edit_group(cid , mid)
                    else :
                        markup=InlineKeyboardMarkup()
                        bot.answer_callback_query(call_id, text['no_delete_group'],show_alert=True,cache_time=3)
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
                        bot.answer_callback_query(call_id, text['sabt'],show_alert=True,cache_time=3)
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
                bot.answer_callback_query(call_id, text['no_data'],cache_time=3)  
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
                        bot.answer_callback_query(call_id, text['sabt'],show_alert=True,cache_time=3)
                        bot.edit_message_text(text['sabt_kala'],cid, mid, reply_markup=None)
                        kala_temp.pop(cid)
                        if user_step[cid] == 2121 :
                            user_step[cid]= 2100
                        elif user_step[cid]== 3121 :
                            user_step[cid] = 3100
                elif data=='back':
                    if cid in kala_temp.keys():
                        kala_temp.pop(cid)
                        if user_step[cid]==3121 :
                            user_step[cid]= 3120
                        if user_step[cid]==2121 :
                            user_step[cid]= 2120
                    make_inlinekeyboardMarkup_kala(cid=cid ,mid=mid)
                elif data =='cancel' :
                    if cid in kala_temp.keys():
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
                elif data in category.keys():
                    kala_temp.update({cid:{'category':data}})
                    edit_kala_func(cid ,mid ,call_id=call_id)
                elif data.startswith('id') :
                    kala_cid=kala_temp[cid]
                    data=data.split('=')[-1]
                    if data.isnumeric()==True :
                        id=int(data)
                        kala_cid.update({'id':id})
                        kala_temp.update({cid:kala_cid})
                        edit_kala_func(cid ,mid,id=id)
                    else:
                        if data == 'imageid' :
                            bot.edit_message_text(text['image_message'],cid,mid,reply_markup=None)  
                        elif data =='kalaname' :
                            bot.edit_message_text(text['kala_message'],cid,mid,reply_markup=None) 
                        elif data == 'saleprice' :
                            if user_step[cid] == 2122 :
                                user_step[cid]= 2122.1
                            elif user_step[cid]== 3122 :
                                user_step[cid] = 3122.1
                            bot.edit_message_text(text['price_message'],cid,mid,reply_markup=None)
                        elif data =='sabt' :
                            kala_cid=kala_temp[cid]
                            id=kala_cid['id']
                            kalaname=kala[id][0]
                            buy_price=kala[id][1]
                            sale_price=kala[id][2]
                            name_category=kala[id][3]
                            kala_date=kala[id][4]  
                            image_file_id=kala[id][5]
                            count=kala[id][6]
                            m_size=kala[id][7]
                            l_size=kala[id][8]
                            xl_size=kala[id][9]
                            xxl_size=kala[id][10]                     
                            if 'kalaname'  in kala_cid.keys()  :
                                kalaname=kala_cid['kalaname']
                            if   'image_file_id' in kala_cid.keys() :
                               image_file_id= kala_cid['image_file_id']
                            if  'sale_price' in kala_cid.keys() :
                               sale_price=int(kala_cid['sale_price'])
                            edit_update_kala(id=id,kalaname=kalaname,image_file_id=image_file_id,sale_price=sale_price)   
                            kala.update({id:[kalaname,buy_price,sale_price,name_category,kala_date,image_file_id,count,m_size,l_size,xl_size,xxl_size]})
                            bot.answer_callback_query(call_id, text['sabt'],show_alert=True,cache_time=3)
                            bot.edit_message_text(text['sabt_kala'],cid, mid, reply_markup=None)
                            kala_temp.pop(cid)
                            if user_step[cid] == 2122 :
                                user_step[cid]= 2100
                            elif user_step[cid]== 3122 :
                                user_step[cid] = 3100

                        elif data=='back':
                            if cid in kala_temp.keys():
                                kala_temp.pop(cid)
                                if user_step[cid]==3122 :
                                    user_step[cid]= 3120
                                if user_step[cid]==2122 :
                                    user_step[cid]= 2120
                            make_inlinekeyboardMarkup_kala(cid=cid ,mid=mid)
                        elif data =='cancel' :
                            if cid in kala_temp.keys():
                                kala_temp.pop(cid)
                            bot.edit_message_reply_markup(cid, mid, reply_markup=None)                    
                            if user_step[cid] ==2122 :
                                user_step[cid] =2100
                            elif user_step[cid] ==3122  :
                                user_step[cid]=3100   
                elif data =='back' :
                    if cid in kala_temp.keys():
                        kala_temp.pop(cid)
                    bot.edit_message_reply_markup(cid, mid, reply_markup=None)                    
                    if user_step[cid] ==2122 :
                        user_step[cid] =2120
                    elif user_step[cid] ==3122  :
                        user_step[cid]=3120
                    make_inlinekeyboardMarkup_kala(cid,mid)
                elif data == 'cancel' :
                    if cid in kala_temp.keys():
                        kala_temp.pop(cid)
                    bot.edit_message_reply_markup(cid, mid, reply_markup=None)                    
                    if user_step[cid] ==2122 :
                        user_step[cid] =2100
                    elif user_step[cid] ==3122  :
                        user_step[cid]=3100                 

            elif data.startswith('delete'):
                data=data.split('/')[-1]
                if data =='delete':
                    if user_step[cid] == 2120 :
                            user_step[cid]= 2123
                    elif user_step[cid]== 3120 :
                        user_step[cid] = 3123
                    show_inlinekeyboardMarkup_category(cid=cid ,mid=mid)                    
                elif data in category.keys():
                    kala_temp.update({cid:{'category':data}})
                    delete_kala_func(cid ,mid ,call_id=call_id)
                elif data.startswith('id') :
                    kala_cid=kala_temp[cid]
                    data=data.split('=')[-1]
                    if data.isnumeric()==True :
                        id=int(data)
                        kala_cid.update({'id':id})
                        kala_temp.update({cid:kala_cid})
                        delete_kala_func(cid ,mid,id=id,call_id=call_id)
                    elif data=='back':
                        if cid in kala_temp.keys():
                            kala_temp.pop(cid)
                        show_inlinekeyboardMarkup_category(cid ,mid)    
                    elif data=='camcel':
                        if cid in kala_temp.keys():
                            kala_temp.pop(cid)
                        if user_step[cid] ==2123 :
                            user_step[cid] =2100
                        elif user_step[cid] ==3123  :
                            user_step[cid]=3100                        
                        bot.edit_message_reply_markup(cid, mid, reply_markup=None)                                                    
                elif data=='back':
                    # if cid in kala_temp.keys():
                    #     kala_temp.pop(cid)
                    if user_step[cid]==3123 :
                        user_step[cid]= 3120
                    if user_step[cid]==2123 :
                        user_step[cid]= 2120
                    make_inlinekeyboardMarkup_kala(cid=cid ,mid=mid)
                elif data =='cancel' :
                    if cid in kala_temp.keys():
                        kala_temp.pop(cid)
                    if user_step[cid] ==2123 :
                        user_step[cid] =2100
                    elif user_step[cid] ==3123  :
                        user_step[cid]=3100                        
                    bot.edit_message_reply_markup(cid, mid, reply_markup=None)                       
                
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
    
    elif data.startswith('adminaccount'):
        if (user_step[cid] >=3200 and user_step[cid] <3300 ) or (user_step[cid] >=2200 and user_step[cid] <2300)  :
            data=data.split('/')[-1]
            if data.startswith('search'):
                data=data.split('=')[-1]
                if data == 'search':
                    if user_step[cid]== 2200 :
                        user_step[cid] = 2210 
                    if user_step[cid]== 3200 :
                        user_step[cid] = 3210    
                    make_search_inlinemarkup(cid=cid, mid=mid) 
                elif data =='name':
                    if user_step[cid]== 2210 :
                        user_step[cid] = 2211 
                    if user_step[cid]== 3210 :
                        user_step[cid] = 3211                     
                    bot.edit_message_text(text['message_name'],cid, mid, reply_markup=None)  
                elif data =='nationalcode':
                    if user_step[cid]== 2210 :
                        user_step[cid] = 2212 
                    if user_step[cid]== 3210 :
                        user_step[cid] = 3212                     
                    bot.edit_message_text(text['message_national_code'],cid, mid, reply_markup=None)
                elif data =='mobile':
                    if user_step[cid]== 2210 :
                        user_step[cid] = 2213 
                    if user_step[cid]== 3210 :
                        user_step[cid] = 3213                     
                    bot.edit_message_text(text['enter_mobile'],cid, mid, reply_markup=None)
                elif data =='back':
                    if user_step[cid]== 2210 :
                        user_step[cid] = 2200 
                    if user_step[cid]== 3210 :
                        user_step[cid] = 3200                
                    make_admin_account_inlinekeyboard(cid , mid)
                elif data =='cancel':
                    if user_step[cid] == 3210:
                        user_step[cid]=3000
                    if user_step[cid]==2210 :
                        user_step[cid]= 2000
                    bot.edit_message_reply_markup(cid, mid, reply_markup=None)    
                    bot.send_message(cid,text['select_menu'],reply_markup=make_ReplyKeyboardMarkup(user_step[cid]))  
            # elif data.startswith('add'):
            #     data=data.split('=')[-1]                       
            #     if data == 'add' :
            #         pass
            elif data.startswith('edit'):
                data=data.split('=')[-1]    
                if data == 'edit' :
                    mid_cid.update({cid:mid})
                    if user_step[cid]== 2200 :
                          user_step[cid] = 2220 
                    if user_step[cid]== 3200 :
                        user_step[cid] = 3220
                    make_edit_adminaccount_inline(cid=cid,mid=mid)      
                elif data =='name':
                    if user_step[cid]== 2220 :
                        user_step[cid] = 2221 
                    if user_step[cid]== 3220 :
                        user_step[cid] = 3221                     
                    bot.edit_message_text(text['message_name'],cid, mid, reply_markup=None)  
                elif data =='nationalcode':
                    if user_step[cid]== 2220 :
                        user_step[cid] = 2222 
                    if user_step[cid]== 3220 :
                        user_step[cid] = 3222                     
                    bot.edit_message_text(text['message_national_code'],cid, mid, reply_markup=None)
                elif data =='mobile':
                    if user_step[cid]== 2220 :
                        user_step[cid] = 2223 
                    if user_step[cid]== 3220 :
                        user_step[cid] = 3223                     
                    bot.edit_message_text(text['enter_mobile'],cid, mid, reply_markup=None)
                elif data.isnumeric() == True :
                    data =int(data)
                    if user_step[cid]== 2224 :
                        user_step[cid] = 2224.1 
                    if user_step[cid]== 3224 :
                        user_step[cid] = 3224.1                    
                    cid_user.update({cid:data})
                    make_edit_adminaccount_inline(cid=cid,mid=mid,cid_user_priv=data)
                elif data.startswith('privilege') :
                    data=data.split('-')[-1]
                    print(data)
                    if user_step[cid] ==3224.1 :
                        user_step[cid] =3224.2
                        make_edit_adminaccount_inline(cid ,mid=None,sabt=data)
                elif data.startswith('is_block') :
                    data=data.split('-')[-1]
                    print(data)
                    if user_step[cid] ==3224.1  :
                        user_step[cid] =3224.2
                        make_edit_adminaccount_inline(cid ,mid=None,sabt=data)
                    elif user_step[cid] ==2224.1  :
                        user_step[cid] =2224.2
                        make_edit_adminaccount_inline(cid ,mid=None,sabt=data)    
                elif data.startswith('sabt') :
                    data=data.split('-')[-1]
                    cid_user_=cid_user[cid]
                    print(cid_user_)
                    if data == 'ADMIN' :
                        user_cid.remove( cid_user_)
                        admin.append(cid_user_)
                        update_condition_user(cid=cid_user_,privilege = data)
                        bot.send_message(cid_user_,text['admin_condition'])
                        print(mid_cid)
                        print(cid_user)
                        mid_cid.pop(cid)
                        cid_user.pop(cid)
                        user_step[cid_user_]=2000
                        print(call_id)
                        bot.answer_callback_query(call_id, text['sabt'],show_alert=True)
                    elif data == 'USER' :
                        user_cid.append( cid_user_)
                        admin.remove(cid_user_)
                        update_condition_user(cid=cid_user_,privilege = data)
                        bot.send_message(cid_user_,text['user_condition1'])
                        print(mid_cid)
                        print(cid_user)
                        mid_cid.pop(cid)
                        cid_user.pop(cid)
                        user_step[cid_user_]=1000
                        print(call_id)
                        bot.answer_callback_query(call_id, text['sabt'],show_alert=True)    

                    elif data == 'YES' :
                        block_user.append(cid_user_)
                        user_cid.remove(cid_user_)                        
                        update_condition_user(cid=cid_user_,is_block = data)
                        mid_cid.pop(cid)
                        cid_user.pop(cid)
                        bot.answer_callback_query(call_id, text['sabt'],show_alert=True,cache_time=3)        

                    elif data == 'NO' :
                        user_cid.append(cid_user_)
                        block_user.remove(cid_user_)
                        update_condition_user(cid=cid_user_,is_block = data)
                        mid_cid.pop(cid)
                        cid_user.pop(cid)
                        bot.answer_callback_query(call_id, text['sabt'],show_alert=True,cache_time=3)

                    if user_step[cid] ==3224.2:
                        user_step[cid] =3000
                    if user_step[cid] ==2224.2:
                        user_step[cid] =2000    
                    bot.edit_message_reply_markup(cid, mid, reply_markup=None)    
                    bot.send_message(cid,text['select_menu'],reply_markup=make_ReplyKeyboardMarkup(user_step[cid]))  
                            
                elif data =='none': 
                    pass
                elif data =='back':
                    if user_step[cid] == 2220 or user_step[cid] == 3220 :
                        if user_step[cid]== 2220 :
                            user_step[cid] = 2200 
                        if user_step[cid]== 3220 :
                            user_step[cid] = 3200                
                        make_admin_account_inlinekeyboard(cid , mid)
                    elif user_step[cid] == 2224 or user_step[cid] == 3224 :
                        if user_step[cid]== 2224 :
                            user_step[cid] = 2220 
                        if user_step[cid]== 3224 :
                            user_step[cid] = 3220                
                        make_edit_adminaccount_inline(cid , mid) 
                    elif user_step[cid] == 2224.1 or user_step[cid] == 3224.1 :
                        if user_step[cid]== 2224.1 :
                            user_step[cid] = 2224 
                        if user_step[cid]== 3224.1 :
                            user_step[cid] = 3224                
                        make_edit_adminaccount_inline(cid , mid)    
                elif data =='cancel':
                    if user_step[cid] >= 3220 and user_step[cid] < 3225 :
                        user_step[cid]=3000
                    if user_step[cid] >=2220 and user_step[cid] < 2225:
                        user_step[cid]= 2000
                    if cid in mid_cid.keys():
                        mid_cid.pop(cid)
                    if cid in cid_user.keys():
                        cid_user.pop(cid)    
                    bot.edit_message_reply_markup(cid, mid, reply_markup=None)    
                    bot.send_message(cid,text['select_menu'],reply_markup=make_ReplyKeyboardMarkup(user_step[cid]))  
            # elif data.startswith('delete'):
            #     data=data.split('=')[-1]            
            #     if data == 'delete' :
            #         pass
            elif data.startswith('back'):
                data=data.split('=')[-1]            
                if data == 'back' :
                    if user_step[cid] == 3200:
                        user_step[cid]=3000
                    if user_step[cid]==2200 :
                        user_step[cid]= 2000
                    bot.edit_message_reply_markup(cid, mid, reply_markup=None)    
                    bot.send_message(cid,text['select_menu'],reply_markup=make_ReplyKeyboardMarkup(user_step[cid]))  
                
        else :
            bot.edit_message_reply_markup(cid, mid, reply_markup=None)
              
    else :
        bot.answer_callback_query(call_id, text['no_data'],cache_time=5)  
        bot.edit_message_reply_markup(cid, mid, reply_markup=None)      








#Commands

@bot.message_handler(commands=['start'])
def command_start(message):
    cid=message.chat.id
    if cid in block_user : return
    if cid in admin :
        user_step.setdefault(cid,2000)
        bot.send_message(cid,text['select_menu'],reply_markup=make_ReplyKeyboardMarkup(user_s=user_step[cid]))
    elif cid in manager :
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

            bot.send_message(cid,text['select_menu'],reply_markup=make_ReplyKeyboardMarkup(user_step[cid]))
        
@bot.message_handler(commands=['main'])
def main_command(message) :
    cid=message.chat.id
    if cid in block_user : return
    if user_step[cid] <2000 :
        bot.send_message(cid,text['select_menu'],reply_markup=make_ReplyKeyboardMarkup(user_step[cid]))
    elif user_step[cid] >= 2000 and user_step[cid] <3000 :
        bot.send_message(cid,text['select_menu'],reply_markup=make_ReplyKeyboardMarkup(user_step[cid]))
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
    
# this account for manager adn admin
@bot.message_handler(func=lambda message : message.text==button['admin_account'])
def admin_account_func(message):
    cid=message.chat.id       
    if cid in block_user : return
    if user_step [cid] == 2000:
        user_step[cid] = 2200
    if user_step[cid] == 3000 :
        user_step[cid] = 3200 
    
    bot.send_message(cid,text['select_menu'],reply_markup=make_ReplyKeyboardMarkup(user_s=user_step[cid]))
    make_admin_account_inlinekeyboard(cid=cid)   





@bot.message_handler(func=lambda message : message.text==button['home'])
def home_func(message):
    cid=message.chat.id
    print(f'user step : {user_step[cid]}')
    if cid in block_user :return
    if user_step[cid] <2000 :
        user_step[cid]=1000
    elif user_step[cid] >=2000 and user_step[cid] <3000 :
            user_step[cid]=2000
    elif user_step[cid] >=3000 :
            user_step[cid]=3000
    bot.send_message(cid,text['select_menu'],reply_markup=make_ReplyKeyboardMarkup(user_step[cid]))
        
        
# this account for user       
@bot.message_handler(func=lambda message : message.text==button['user_account'])
def user_account_func(message) :
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
    elif user_step[cid] == 2122 or user_step[cid] == 3122:
        file_id = message.photo[-1].file_id
        print (file_id)
        kala_cid=kala_temp[cid]
        kala_cid.update({'image_file_id' :file_id})
        kala_temp.update({cid : kala_cid})
        edit_kala_func(cid)
        




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
        flag =0
        kala_cid= kala_temp[cid]
        result = get_field_kalaname()
        kala_name =message.text
        for i in result :
            if i['kalaname']== kala_name:
                flag =1
                break
        if flag == 0 :         
            kala_cid.update({'kalaname' :kala_name})
            kala_temp.update({cid:kala_cid})
            insert_kala_func(cid)
        else :
            bot.send_message(cid,text['repeat_namekala'])        
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
    elif user_step[cid] ==3122 or user_step[cid] ==2122 :
        flag =0
        kala_cid= kala_temp[cid]
        result = get_field_kalaname()
        kala_name =message.text
        for i in result :
            if i['kalaname']== kala_name:
                flag =1
                break
        if flag == 0 :         
            kala_cid.update({'kalaname' :kala_name})
            kala_temp.update({cid:kala_cid})
            edit_kala_func(cid)
        else :
            bot.send_message(cid,text['repeat_namekala'])        
    elif user_step[cid] ==3122.1 or user_step[cid] ==2122.1 :
        if user_step[cid] == 2122.1 :
            user_step[cid]= 2122
        elif user_step[cid]== 3122.1 :
            user_step[cid] = 3122
        kala_cid= kala_temp[cid]
        price =message.text
        kala_cid.update({'sale_price': price })
        kala_temp.update({cid:kala_cid})
        edit_kala_func(cid)
    elif (user_step[cid] >=3211 and user_step[cid] <=3213 ) or (user_step[cid] >=2211 and user_step[cid] <=2213) :
        flag =1
        m=message.text
        if user_step[cid] ==3211 or user_step[cid] ==2211 :    
            result = search_on_user(fullname=m)
        elif user_step[cid] ==3212 or user_step[cid] ==2212:
            if m.isnumeric() == True:               
                result = search_on_user(national_code=m)    
            else :
                flag = 0    
        elif user_step[cid] ==3213 or user_step[cid] ==2213:
            if m.isnumeric() == True:
                if m.startswith('0') or m.startswith('۰') :
                    m=m[1:]              
                    result = search_on_user(mobile_phone=m)    
            else :
                flag = 0    
        if flag ==1 :
                             
            if len(result) == 0 :
                bot.send_message(cid,text['not_exist'])
            else :
                for i in result:
                    id=i['id']
                    cid_user= i['cid']
                    fullname=i['fullname']
                    username=i['username']
                    national_code=i['national_code']
                    mobile_phone=i['mobile_phone']
                    adress=i['adress']
                    privilege=i['privilege']
                    is_block = i['is_block']
                    user_date=i['user_date']
                    desciptiom=f'آیدی : {id}\n CID : {cid_user} \n نام کامل : {fullname} \n نام کاربری تلگرام : {username} \n کد ملی : {national_code} \n شماره موبایل : {mobile_phone} \n  آدرس : {adress}  \n وضیعت : {privilege} \n وضیعت بلاک : {is_block} \n تاریخ ایجاد : {user_date}'
                    bot.send_message(cid,desciptiom)
            if user_step[cid] == 2211  or user_step[cid] == 2212 or user_step[cid] == 2213:
                user_step[cid] = 2210
            elif user_step[cid] == 3211 or user_step[cid] == 3212 or user_step[cid] == 3213:
                user_step[cid] = 3210    
            make_search_inlinemarkup(cid)        
        else :
            bot.send_message(cid,text['enter_corect'])
            
    elif (user_step[cid] >=3221 and user_step[cid] <=3223 ) or (user_step[cid] >=2221 and user_step[cid] <=2223) :
        flag =1
        m=message.text
        if user_step[cid] ==3221 or user_step[cid] ==2221 :    
            result = search_on_user(fullname=m)
        elif user_step[cid] ==3222 or user_step[cid] ==2222:
            if m.isnumeric() == True:               
                result = search_on_user(national_code=m)    
            else :
                flag = 0    
        elif user_step[cid] ==3223 or user_step[cid] ==2223:
            if m.isnumeric() == True:
                if m.startswith('0') or m.startswith('۰') :
                    m=m[1:]              
                    result = search_on_user(mobile_phone=m)    
            else :
                flag = 0    
        if flag ==1 :
                             
            if len(result) == 0 :
                if user_step[cid] == 2221  or user_step[cid] == 2222 or user_step[cid] == 2223:
                    user_step[cid] = 2220
                elif user_step[cid] == 3211 or user_step[cid] == 3212 or user_step[cid] == 3213:
                    user_step[cid] = 3220                   
                bot.send_message(cid,text['not_exist'])
                make_edit_adminaccount_inline(cid=cid)
            else :
                if user_step[cid] == 2221  or user_step[cid] == 2222 or user_step[cid] == 2223:
                    user_step[cid] = 2224
                elif user_step[cid] == 3221 or user_step[cid] == 3222 or user_step[cid] == 3223:
                    user_step[cid] = 3224   
                make_edit_adminaccount_inline(cid=cid,result=result)
        else :
            bot.send_message(cid,text['enter_corect'])            
    
bot.infinity_polling()
