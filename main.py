
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
show_kala=dict()
count_of_size =dict()           #count_of_size={cid:{m:count ,l: count,xl :count ,xxl :count}}
mid_cid=dict()                  #mid_cid={cid:mid,........}
cid_user=dict()                   #cid_user={cid:user of account cid}
buy_invoice_name=dict()             #id_user={cid:[id,fullname,cid]}
buy_invoice_kala=dict()            # buy_invoice_temp={cid: dict()}
temp_kala=dict()                #temp_kala={cid:temp dict}
shoping_cart=dict()             #shoping_cart={cid:{kalaid1:{size:qty , sale_price:price},kalaid2:{},....},...}
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
        'add_to_card':           'اضافه به سبد خرید  🛒',
        'user_profile' :         'مشخصات کاربری',
        'full_name':             'نام و نام خانوادگی' ,
        'mobile' :               'شماره موبایل' ,
        'personal_id'  :         'کد ملی' ,
        'adress' :               'آدرس',
        'send number':          'ارسال شماره موبایل',
        'kala' :                'کالا  📦',
        'admin_account':        'طرف حساب  👤',
        'invoice' :             'فاکتور  🧾',
        'buy_invoice':          'فاکتور خرید',
        'sale_invoice':         'فاکتور فروش',
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
        'add_factor':           'اضافه به فاکتور  ➕',
        'add_kala_infactor':    'اضافه کالا به فاکتور  ➕',
        'register_factor' :     ' ثبت فاکتور ✅',
             
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



#make function group kala

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
    markup.add(InlineKeyboardButton(button['register'],callback_data='group_add/sabt'),InlineKeyboardButton(button['cancel'],callback_data='group_add/cancel'))
    bot.edit_message_text(text['add_name_group'],cid,mid,reply_markup=markup)
    return


def inline_edit_group(cid , mid):
    if user_step[cid] ==2100 or user_step[cid] ==3100:
        if user_step[cid] == 2100 :
            user_step[cid] = 2110
        else :
            user_step[cid] = 3110 
    group_condition =text['group_condition']
    result=condition_category( name_category=category_oldname[cid] )
    show_category=result[0]['show_category']        
    markup=InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(category_oldname[cid],callback_data='group_edit/namecategory'))
    markup.add(InlineKeyboardButton(f'{group_condition} : {show_category}',callback_data=f'group_edit/showcategory={show_category}'))
    markup.add(InlineKeyboardButton(button['edit'],callback_data=f'group_edit/edit-{category_oldname[cid]}'))
    markup.add(InlineKeyboardButton(button['delete_group'],callback_data=f'group_edit/delete-{category_oldname[cid]}'))
    markup.add(InlineKeyboardButton(button['back'],callback_data=f'group_edit/back-{category_oldname[cid]}'))
    bot.edit_message_text(text['edit_name_group'],cid,mid,reply_markup=markup)
    return

def inline_change_group(cid , mid,condition=None):
    if user_step[cid] ==2100 or user_step[cid] ==3100:
        if user_step[cid] == 2100 :
            user_step[cid] = 2110
        else :
            user_step[cid] = 3110 
    markup=InlineKeyboardMarkup()
    if condition != None :
        
        if condition=='YES' :
            condition='NO'
        elif condition == 'NO':
            condition = 'YES'
        group_condition= text['group_condition']    
        markup.add(InlineKeyboardButton(f'{group_condition} : {condition}',callback_data=f'group_edit/showcategory={condition}'))
        markup.add(InlineKeyboardButton(button['register'],callback_data=f'group_edit/showcategory=sabt-{condition}'),InlineKeyboardButton(button['cancel'],callback_data='group_edit/cancel-condition={condition}'))
        bot.edit_message_text(text['register'],cid,mid,reply_markup=markup)
    
    
    else :        
        markup.add(InlineKeyboardButton(category_temp[cid][0],callback_data='group_edit/change-newname'))
        markup.add(InlineKeyboardButton(button['register'],callback_data='group_edit/sabt-newname'),InlineKeyboardButton(button['cancel'],callback_data='group_edit/cancel-newname'))
        bot.edit_message_text(text['change_name_group'],cid,mid,reply_markup=markup)
    return


#make fuction kala 

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




#make fuction admin account

def make_admin_account_inlinekeyboard(cid , mid=None) :
    markup =InlineKeyboardMarkup()
    if user_step[cid] == 2200 or user_step[cid] == 3200:
        markup.add(InlineKeyboardButton(button['search'],callback_data=f'adminaccount/search=search'))
        markup.add(InlineKeyboardButton(button['edit_account'],callback_data=f'adminaccount/edit=edit'))
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
    
    



#make function for buy invoice for admin & manger

def make_buy_invoice_inlinemarkup(cid,mid=None,result=None ,kala=None) :
    markup=InlineKeyboardMarkup()
    u_step=user_step[cid]
    # if mid == None :
    if user_step[cid] ==2310 or user_step[cid]==3310 :
        markup.add(InlineKeyboardButton(text['name_search'],callback_data='buyinvoice-searchname'))
        markup.add(InlineKeyboardButton(button['back'],callback_data=f'buyinvoice-back/{u_step}'))
        if mid == None :
            bot.send_message(cid,text['name_search1'],reply_markup=markup)
        else :
            bot.edit_message_text(text['name_search1'],cid,mid,reply_markup=markup)    
    elif (user_step[cid] ==2311 or user_step[cid]==3311) and result != None :
        for i in result :
            id=i['id']
            fullname=i['fullname']
            select_cid = i['cid']
            select=f'{id},{fullname},{select_cid}'
            markup.add(InlineKeyboardButton(fullname,callback_data=f'buyinvoice-choicename/{select}'))
        markup.add(InlineKeyboardButton(button['back'],callback_data=f'buyinvoice-back/{u_step}'))
        if mid == None :
            bot.send_message(cid,text['choice_name'],reply_markup=markup)
        else :
            bot.edit_message_text(text['choice_name'],cid,mid,reply_markup=markup)
    elif user_step[cid] == 2312 or user_step[cid]==3312 :
        markup.add(InlineKeyboardButton(text['search_kala'],callback_data='buyinvoice-searchkala'))
        markup.add(InlineKeyboardButton(text['enter_id'],callback_data='buyinvoice-enteridkala'))
        markup.add(InlineKeyboardButton(button['back'],callback_data=f'buyinvoice-back/{u_step}'))
        if mid == None :
            bot.send_message(cid,text['search_kala1'],reply_markup=markup)
        else :
            bot.edit_message_text(text['search_kala1'],cid,mid,reply_markup=markup) 
    elif (user_step[cid] ==2315 or user_step[cid]==3315 ) and kala == True :
        for i in result :
            id=i['id']
            kalaname=i['kalaname']
            select=f'کد کالا :{id}---- نام کالا :{kalaname}'
            markup.add(InlineKeyboardButton(select,callback_data=f'buyinvoice-choickala/{id}'))
        markup.add(InlineKeyboardButton(button['back'],callback_data=f'buyinvoice-back/{u_step}'))       
        if mid == None :
            bot.send_message(cid,text['choice_kala'],reply_markup=markup) 
        else :
            bot.edit_message_text(text['choice_kala'],cid,mid,reply_markup=markup)    
    
    elif (user_step[cid] ==2316 or user_step[cid]==3316 ) :
        temp1_kala=dict()
        if kala != None :
            id=kala
            kalaname =result[0]
            buy_price=result[1]
            m_size=result[7]
            l_size =result[8]
            xl_size =result[9]
            xxl_size=result[10]
            count=result[6]
            temp1_kala.update({'id':kala})
            temp1_kala.update({'kalaname':kalaname})
            temp1_kala.update({'buy_price':buy_price})
            temp1_kala.update({'m_size':m_size})
            temp1_kala.update({'l_size':l_size})
            temp1_kala.update({'xl_size':xl_size})
            temp1_kala.update({'xxl_size': xxl_size})
            temp1_kala.update({'count':count})
            temp_kala.update({cid:temp1_kala})
        else :
            temp1_kala=temp_kala[cid]
            id=temp1_kala['id']
            kalaname =temp1_kala['kalaname']
            buy_price=temp1_kala['buy_price']
            m_size=temp1_kala['m_size']
            l_size =temp1_kala['l_size']
            xl_size =temp1_kala['xl_size']
            xxl_size=temp1_kala['xxl_size']
            count=temp1_kala['count']   
        markup.add(InlineKeyboardButton(f'کد کالا :{id} ----نام کالا : {kalaname}',callback_data='buyinvoice-invoice/none'))
        markup.add(InlineKeyboardButton(f'M : {m_size}',callback_data='buyinvoice-invoice/msize'),
                   InlineKeyboardButton(f'L : {l_size}',callback_data='buyinvoice-invoice/lsize'))
        markup.add(InlineKeyboardButton(f'XL : {xl_size}',callback_data='buyinvoice-invoice/xlsize'),
                   InlineKeyboardButton(f'XXL : {xxl_size}',callback_data='buyinvoice-invoice/xxlsize'))
        markup.add(InlineKeyboardButton(f'جمع کل : {count}',callback_data='buyinvoice-invoice/none'),
                   InlineKeyboardButton(f'قیمت خرید : {buy_price}',callback_data='buyinvoice-invoice/buyprice'))
        markup.add(InlineKeyboardButton(button['add_factor'],callback_data=f'buyinvoice-invoice/addfactor'))
        markup.add(InlineKeyboardButton(button['back'],callback_data=f'buyinvoice-back/{u_step}'),
                   InlineKeyboardButton(button['cancel'],callback_data=f'buyinvoice-cancel'))
        if mid == None :
            bot.send_message(cid,text['enter_count_size'],reply_markup=markup) 
        else :
            bot.edit_message_text(text['enter_count_size'],cid,mid,reply_markup=markup) 
    
    elif user_step[cid] ==2317 or user_step[cid]==3317  :
        markup.add(InlineKeyboardButton(button['add_kala_infactor'],callback_data=f'buyinvoice-addfactor/addfactor'))    
        markup.add(InlineKeyboardButton(button['register_factor'],callback_data=f'buyinvoice-addfactor/sabt'))
        markup.add(InlineKeyboardButton(button['cancel'],callback_data=f'buyinvoice-cancel'))
        bot.edit_message_text(text['sabt_factor'],cid,mid,reply_markup=markup) 



def make_buy_menu_user(cid ,mid =None,number_kala=None):
    markup=InlineKeyboardMarkup()
    u_step=user_step[cid]
    if number_kala != None :
        temp=show_kala[cid]
    if user_step[cid] == 1100 :
        for i in category :
            if category[i] == 'YES':
               markup.add(InlineKeyboardButton(i,callback_data=f'buyuser-category/{i}'))
        markup.add(InlineKeyboardButton(button['back'],callback_data=f'buyuser-back/{u_step}'))
        if mid == None :
            bot.send_message(cid,text['choice_group'],reply_markup=markup)    
        else :
            bot.edit_message_text(text['choice_group'],cid,mid,reply_markup=markup)   
    elif user_step[cid] == 1110 :         
        image_file_id= temp[number_kala]['image_file_id'] 
        kala_name=temp[number_kala]['kalaname']
        kala_id = temp[number_kala]['id']
        sale_price=temp[number_kala]['sale_price']
        # print(count_of_size[cid])
        m_size =count_of_size[cid]['m']
        l_size = count_of_size[cid]['l']
        xl_size = count_of_size[cid]['xl']
        xxl_size = count_of_size[cid]['xxl']
        markup.add(InlineKeyboardButton('M : سایز',callback_data=f'buyuser-showkala/none'))
        markup.add(InlineKeyboardButton('➖',callback_data=f'buyuser-showkala/minus&m={number_kala}'),
                   InlineKeyboardButton(f'{m_size}',callback_data=f'buyuser-showkala/none'), 
                   InlineKeyboardButton('➕',callback_data=f'buyuser-showkala/plus&m={number_kala}')
                  )
        markup.add(InlineKeyboardButton('L : سایز',callback_data=f'buyuser-showkala/none'))
        markup.add(InlineKeyboardButton('➖',callback_data=f'buyuser-showkala/minus&l={number_kala}'),
                   InlineKeyboardButton(f'{l_size}',callback_data=f'buyuser-showkala/none'), 
                   InlineKeyboardButton('➕',callback_data=f'buyuser-showkala/plus&l={number_kala}')
                  )
        markup.add(InlineKeyboardButton(' سایز : XL ',callback_data=f'buyuser-showkala/none'))
        markup.add(InlineKeyboardButton('➖',callback_data=f'buyuser-showkala/minus&xl={number_kala}'),
                   InlineKeyboardButton(f'{xl_size}',callback_data=f'buyuser-showkala/none'), 
                   InlineKeyboardButton('➕  ',callback_data=f'buyuser-showkala/plus&xl={number_kala}')
                  )
        markup.add(InlineKeyboardButton(' سایز : XXL',callback_data=f'buyuser-showkala/none'))
        markup.add(InlineKeyboardButton('➖',callback_data=f'buyuser-showkala/minus&xxl={number_kala}'),
                   InlineKeyboardButton(f'{xxl_size}',callback_data=f'buyuser-showkala/none'), 
                   InlineKeyboardButton('➕',callback_data=f'buyuser-showkala/plus&xxl={number_kala}')
                  )
        markup.add(InlineKeyboardButton('  ⬅️ ',callback_data=f'buyuser-showkala/backward={number_kala}'),
                   InlineKeyboardButton('  ➡️  ',callback_data=f'buyuser-showkala/forward={number_kala}')
                  )
        markup.add(InlineKeyboardButton(button['add_to_card'],callback_data=f'buyuser-showkala/addtocard={number_kala}'))
        
        markup.add(InlineKeyboardButton(button['back'],callback_data=f'buyuser-back/{u_step}'),
                   InlineKeyboardButton(button['cancel'],callback_data=f'buyuser-showkala/cancel={u_step}')
                  )
        if user_step[cid]==1110 :
            user_step[cid]=1111
        bot.send_photo(cid,image_file_id,caption=f'کدکالا : {kala_id}---- نام کالا : {kala_name}---قیمت :{sale_price}',reply_markup=markup)
        
    elif user_step[cid] == 1111 :    
        image_file_id= temp[number_kala]['image_file_id'] 
        kala_name=temp[number_kala]['kalaname']
        kala_id = temp[number_kala]['id']
        sale_price=temp[number_kala]['sale_price']
        m_size =count_of_size[cid]['m']
        l_size = count_of_size[cid]['l']
        xl_size = count_of_size[cid]['xl']
        xxl_size = count_of_size[cid]['xxl']
        markup.add(InlineKeyboardButton('M : سایز',callback_data=f'buyuser-showkala/none'))
        markup.add(InlineKeyboardButton('➖',callback_data=f'buyuser-showkala/minus&m={number_kala}'),
                   InlineKeyboardButton(f'{m_size}',callback_data=f'buyuser-showkala/none'), 
                   InlineKeyboardButton('➕',callback_data=f'buyuser-showkala/plus&m={number_kala}')
                  )
        markup.add(InlineKeyboardButton('L : سایز',callback_data=f'buyuser-showkala/none'))
        markup.add(InlineKeyboardButton('➖',callback_data=f'buyuser-showkala/minus&l={number_kala}'),
                   InlineKeyboardButton(f'{l_size}',callback_data=f'buyuser-showkala/none'), 
                   InlineKeyboardButton('➕',callback_data=f'buyuser-showkala/plus&l={number_kala}')
                  )
        markup.add(InlineKeyboardButton(' سایز : XL ',callback_data=f'buyuser-showkala/none'))
        markup.add(InlineKeyboardButton('➖',callback_data=f'buyuser-showkala/minus&xl={number_kala}'),
                   InlineKeyboardButton(f'{xl_size}',callback_data=f'buyuser-showkala/none'), 
                   InlineKeyboardButton('➕  ',callback_data=f'buyuser-showkala/plus&xl={number_kala}')
                  )
        markup.add(InlineKeyboardButton(' سایز : XXL',callback_data=f'buyuser-showkala/none'))
        markup.add(InlineKeyboardButton('➖',callback_data=f'buyuser-showkala/minus&xxl={number_kala}'),
                   InlineKeyboardButton(f'{xxl_size}',callback_data=f'buyuser-showkala/none'), 
                   InlineKeyboardButton('➕',callback_data=f'buyuser-showkala/plus&xxl={number_kala}')
                  )
        markup.add(InlineKeyboardButton('  ⬅️ ',callback_data=f'buyuser-showkala/backward={number_kala}'),
                   InlineKeyboardButton('  ➡️  ',callback_data=f'buyuser-showkala/forward={number_kala}')
                  )
        markup.add(InlineKeyboardButton(button['add_to_card'],callback_data=f'buyuser-showkala/addtocard={number_kala}'))
        
        markup.add(InlineKeyboardButton(button['back'],callback_data=f'buyuser-back/{u_step}'),
                   InlineKeyboardButton(button['cancel'],callback_data=f'buyuser-showkala/cancel={u_step}')
                  )
        # bot.send_photo(cid,image_file_id,caption=f'کدکالا : {kala_id}---- نام کالا : {kala_name}---قیمت :{sale_price}',reply_markup=markup)
        bot.edit_message_caption(f'کدکالا : {kala_id}---- نام کالا : {kala_name}---قیمت :{sale_price}',cid,mid,reply_markup=markup)

    
    



#define the main  menu

def make_ReplyKeyboardMarkup(user_s=None):
    markup=ReplyKeyboardMarkup(resize_keyboard=True)
    if user_s >=3000 :
        if user_s  == 3000 :
            # main menu of manager
            markup.add(button['invoice'],button['admin_account'],button['kala'])
            markup.add(button['reports'],button['finacial_department'],button['admin'])
            return(markup)
            # kala menu on manger
        elif user_s ==3100 :
            markup.add(button['kala'],button['group'])
            markup.add(button['home'])
            return(markup)
            # account menu on manger
        elif user_s == 3200 :
            markup.add(button['home'])
            return(markup)
            # invoice menu on manger
        elif user_s == 3300 :
            markup.add(button['sale_invoice'],button['buy_invoice'])
            markup.add(button['home'])
            return(markup)
            #buy invoice menu on admin
        elif user_s == 3310 :
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
            # account menu on admin
        elif user_s == 2200 :
            markup.add(button['home'])
            return(markup)
            # invoice menu on admin
        elif user_s == 2300 :
            markup.add(button['sale_invoice'],button['buy_invoice'])
            markup.add(button['home'])
            return(markup)
            #buy invoice menu on admin    
        elif user_s == 2210 :
            markup.add(button['home'])
            return(markup)
        
    elif user_s >= 1000 and user_s <2000 :
        if user_s == 1000:
            # main menu on user
    
            markup.add(button['user_account'],button['buy'])
            markup.add(button['contact_to_me'],button['help'])
            return(markup)
            # buy invoice for user
        elif user_s == 1100 :
            markup.add(button['home'])
            return(markup)
        




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
                    category_temp.update({cid:[data,mid]})
                    category_oldname.update({cid:data})
                    inline_edit_group(cid , mid)
                elif data.startswith('showcategory') :
                    data = data.split('=')[-1]
                    if data == 'YES' or data == 'NO' :    
                        inline_change_group(cid , mid,condition=data)                                          
                    elif data.startswith('sabt') :   
                        data = data.split('-')[-1]
                        print(data) 
                        if user_step[cid] ==2110 :
                            user_step[cid] =2100
                        else :
                            user_step[cid]=3100  
                        update_show_category(name_category=category_oldname[cid],show_category=data)
                        bot.answer_callback_query(call_id, text['sabt'],show_alert=True)
                        bot.edit_message_reply_markup(cid, mid, reply_markup=None)          
                        category.update({category_oldname[cid]:data})
                        category_temp.pop(cid)
                        category_oldname.pop(cid)
                elif data.split('-')[0] =='edit' :
                    data= data.split('-')[0]
                    result =get_infokala_where_category(category_oldname[cid])
                    if len(result)== 0:
                        inline_change_group(cid , mid)
                    else :
                        markup=InlineKeyboardMarkup()
                        bot.answer_callback_query(call_id, text['no_delete_group'],show_alert=True,cache_time=3)                    
                elif data.split('-')[0] =='delete' :
                    if user_step[cid] ==2110 :
                        user_step[cid] =2100
                    else :
                        user_step[cid]=3100                    
                    data= data.split('-')[0]
                    result =get_infokala_where_category(category_oldname[cid])
                    if len(result)== 0:
                        delete_category(name_category=category_oldname[cid])
                        category.pop(category_oldname[cid])
                        category_temp.pop(cid)
                        category_oldname.pop(cid)
                        bot.edit_message_reply_markup(cid, mid, reply_markup=None)
                    else :
                        markup=InlineKeyboardMarkup()
                        bot.answer_callback_query(call_id, text['no_delete_group'],show_alert=True,cache_time=3)                    

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
                    if user_step[cid] ==3224.1 :
                        user_step[cid] =3224.2
                        make_edit_adminaccount_inline(cid ,mid=None,sabt=data)
                elif data.startswith('is_block') :
                    data=data.split('-')[-1]
                    if user_step[cid] ==3224.1  :
                        user_step[cid] =3224.2
                        make_edit_adminaccount_inline(cid ,mid=None,sabt=data)
                    elif user_step[cid] ==2224.1  :
                        user_step[cid] =2224.2
                        make_edit_adminaccount_inline(cid ,mid=None,sabt=data)    
                elif data.startswith('sabt') :
                    data=data.split('-')[-1]
                    cid_user_=cid_user[cid]
                    if data == 'ADMIN' :
                        user_cid.remove( cid_user_)
                        admin.append(cid_user_)
                        update_condition_user(cid=cid_user_,privilege = data)
                        bot.send_message(cid_user_,text['admin_condition'])
                        mid_cid.pop(cid)
                        cid_user.pop(cid)
                        user_step[cid_user_]=2000
                        bot.answer_callback_query(call_id, text['sabt'],show_alert=True)
                    elif data == 'USER' :
                        user_cid.append( cid_user_)
                        admin.remove(cid_user_)
                        update_condition_user(cid=cid_user_,privilege = data)
                        bot.send_message(cid_user_,text['user_condition1'])
                        mid_cid.pop(cid)
                        cid_user.pop(cid)
                        user_step[cid_user_]=1000
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
    elif data.startswith('buyinvoice'):
        if (user_step[cid] >=3300 and user_step[cid] <3400 ) or (user_step[cid] >=2300 and user_step[cid] <2400) :
            data = data.split('-')[-1]
            if data =='searchname':
                mid_cid.update({cid:mid})
                if user_step[cid] ==2310 :
                    user_step[cid] =2311
                elif  user_step[cid] ==3310 :
                    user_step[cid] = 3311
                bot.edit_message_text(text['name_search2'],cid,mid  , reply_markup=None)
            elif data.startswith('choicename') :
                data = data.split('/')[-1]
                #data= int(data)
                data=data.split(',')
                data[0]=int(data[0])
                data[2]=int(data[2])
                mid_cid.update({cid:mid})
                buy_invoice_name.update({cid:data})
                if user_step[cid] == 2311 :
                    user_step[cid] = 2312
                elif user_step[cid] == 3311 :
                    user_step[cid] = 3312    
                #select kala
                make_buy_invoice_inlinemarkup(cid,mid=mid)
            elif data.startswith('searchkala') :
                bot.edit_message_reply_markup(cid, mid, reply_markup=None) 
                if user_step[cid] == 2312 :
                    user_step[cid] = 2313
                elif user_step[cid] == 3312 :
                    user_step[cid] = 3313
                bot.send_message(cid,text['name_kala_search'])     
            elif data.startswith('enteridkala') :
                bot.edit_message_reply_markup(cid, mid, reply_markup=None) 
                if user_step[cid] == 2312 :
                    user_step[cid] = 2314
                elif user_step[cid] == 3312 :
                    user_step[cid] = 3314
                bot.send_message(cid,text['enter_id1'])
            elif data.startswith('choickala') :
                data =data.split('/')[-1]
                data=int(data)
                kala_select=kala[data]  
                if user_step[cid]==2315 :
                    user_step[cid] =2316
                elif user_step[cid]==3315 :
                    user_step[cid] =3316    
                make_buy_invoice_inlinemarkup(cid,mid=mid,result=kala_select,kala=data)    
            elif data.startswith('invoice') :
                data =data.split('/')[-1]
                mid_cid[cid] =mid
                if data == 'msize' :
                    if user_step[cid] == 2316 :
                        user_step[cid] =2316.1
                    elif user_step[cid] == 3316 :
                        user_step[cid] =3316.1 
                    bot.edit_message_reply_markup(cid, mid, reply_markup=None)
                    bot.send_message(cid,text['enter_count'])         
                elif  data == 'lsize' :
                    if user_step[cid] == 2316 :
                       user_step[cid] = 2316.2
                    elif user_step[cid] == 3316 :
                        user_step[cid] =3316.2 
                    bot.edit_message_reply_markup(cid, mid, reply_markup=None)
                    bot.send_message(cid,text['enter_count'])               
                elif  data == 'xlsize' :
                    if user_step[cid] == 2316 :
                        user_step[cid] = 2316.3
                    elif user_step[cid] == 3316 :
                        user_step[cid] =3316.3 
                    bot.edit_message_reply_markup(cid, mid, reply_markup=None)
                    bot.send_message(cid,text['enter_count'])                
                elif  data == 'xxlsize' :
                    if user_step[cid] == 2316 :
                        user_step[cid] = 2316.4
                    elif user_step[cid] == 3316 :
                        user_step[cid] =3316.4 
                    bot.edit_message_reply_markup(cid, mid, reply_markup=None)
                    bot.send_message(cid,text['enter_count'])    
                elif  data == 'buyprice' :
                    if user_step[cid] == 2316 :
                        user_step[cid] = 2316.5
                    elif user_step[cid] == 3316 :
                        user_step[cid] =3316.5 
                    bot.edit_message_reply_markup(cid, mid, reply_markup=None)
                    bot.send_message(cid,text['buy_price'])                       
                elif  data == 'addfactor' :
                    if user_step[cid] == 2316 :
                        user_step[cid] = 2317
                    elif user_step[cid] == 3316 :
                        user_step[cid] =3317
                    flag =0 
                    temp=dict()
                    temp1=dict()
                    if cid in buy_invoice_kala :
                        temp=buy_invoice_kala[cid]
                        row_number =len(temp) +1
                        temp1=temp_kala[cid]
                        for i in temp :
                            if temp[i]['id'] == temp1['id'] :
                                flag =1
                        if flag ==0 :        
                            temp.update({row_number :temp1})
                            buy_invoice_kala.update({cid:temp})
                        else :
                            bot.send_message(cid,text['reapat_kala'])    
                    else :
                        temp1=temp_kala[cid]
                        print(temp1)
                        temp.update({1 :temp1})
                        buy_invoice_kala.update({cid:temp})
                    temp_kala.pop(cid)        
                    make_buy_invoice_inlinemarkup(cid,mid=mid)    
            elif data.startswith('addfactor'):
                data =data.split('/')[-1]
                if data == 'addfactor' :
                    if user_step[cid] == 2317 :
                        user_step[cid] = 2312
                    elif user_step[cid] == 3317 :
                        user_step[cid] =3312
                    make_buy_invoice_inlinemarkup(cid,mid=mid)    
                elif data =='sabt' :
                    sum_total_price=0
                    sum_count = 0
                    invoice_name=[]
                    invoice_kala=dict()
                    today=date_today()
                    invoice_name = buy_invoice_name[cid]
                    invoice_name_cid = invoice_name[2]
                    insert_buyinvoice(user_id=invoice_name[0],fullname=invoice_name[1],date_invoice=today)
                    invoice_number=last_buyinvoice_id()
                    invoice_kala=buy_invoice_kala[cid]
                    for i in invoice_kala :
                        kala_id=invoice_kala[i]['id']
                        kala_name=invoice_kala[i]['kalaname']
                        kala_price=invoice_kala[i]['buy_price']
                        count=invoice_kala[i]['count']
                        m_size=invoice_kala[i]['m_size']
                        l_size=invoice_kala[i]['l_size']
                        xl_size=invoice_kala[i]['xl_size']
                        xxl_size=invoice_kala[i]['xxl_size']
                        total_row=kala_price * count
                        sum_total_price += total_row
                        sum_count += count
                        insert_rowinvoice(i_number=invoice_number , kala_id=kala_id , kala_name=kala_name , kala_price=kala_price , count=count,total_row=total_row)
                        update_kala_with_buyinvoice(id=kala_id , buy_price=kala_price , count=count , m_size=m_size ,l_size=l_size ,xl_size=xl_size ,xxl_size=xxl_size)
                    if user_step[cid] == 2317 :
                        user_step[cid] = 2300
                    elif user_step[cid] == 3317 :
                        user_step[cid] =3300 
                    message=f'طبق فاکتور شماره {invoice_number} در تاریخ {today} مبلغ {sum_total_price} و تعداد {sum_count} کالا از شما خریداری شد.      با تشکر'
                    bot.send_message(invoice_name_cid,message)
                    buy_invoice_kala.pop(cid)  
                    bot.edit_message_reply_markup(cid, mid, reply_markup=None)
                    bot.send_message(cid,text['select_menu'],reply_markup=make_ReplyKeyboardMarkup(user_step[cid]))
                    bot.answer_callback_query(call_id, text['sabt'],show_alert=True)            
            elif data.startswith('cancel'):
                if user_step[cid] == 3316 or user_step[cid] == 2316 :
                    if user_step[cid] == 2316 :
                        user_step[cid] = 2300
                    elif user_step[cid] == 3316 :
                        user_step[cid] = 3300    
                    if len(buy_invoice_kala.keys()) != 0 :
                        buy_invoice_kala.pop(cid)   
                    bot.edit_message_reply_markup(cid, mid, reply_markup=None)
                    bot.send_message(cid,text['select_menu'],reply_markup=make_ReplyKeyboardMarkup(user_step[cid]))                        
                elif user_step[cid] == 3317 or user_step[cid] == 2317 : 
                    if user_step[cid] == 2317 :
                        user_step[cid] = 2300
                    elif user_step[cid] == 3317 :
                        user_step[cid] = 3300    
                    if len(buy_invoice_kala.keys()) != 0 :
                        buy_invoice_kala.pop(cid) 
                    bot.edit_message_reply_markup(cid, mid, reply_markup=None)
                    bot.send_message(cid,text['select_menu'],reply_markup=make_ReplyKeyboardMarkup(user_step[cid]))                        
            elif data.startswith('back'):
                data = data.split('/')[-1]
                print(data)
                data =int(data)
                if data ==2310 :
                    user_step[cid] =2300
                    bot.edit_message_reply_markup(cid, mid, reply_markup=None)
                    bot.send_message(cid,text['select_menu'] , reply_markup=make_ReplyKeyboardMarkup(user_step[cid]))
                elif  data ==3310 :
                    user_step[cid] = 3300
                    bot.edit_message_reply_markup(cid, mid, reply_markup=None)
                    bot.send_message(cid,text['select_menu'] , reply_markup=make_ReplyKeyboardMarkup(user_step[cid]))  
                elif data ==2311 :
                    user_step[cid]=2310
                    make_buy_invoice_inlinemarkup(cid=cid,mid=mid)
                elif data ==3311:
                    user_step[cid]=3310
                    make_buy_invoice_inlinemarkup(cid=cid,mid=mid)
                elif data ==3312:
                    user_step[cid]=3310
                    make_buy_invoice_inlinemarkup(cid=cid,mid=mid)
                elif data ==2312:
                    user_step[cid]=231
                    make_buy_invoice_inlinemarkup(cid=cid,mid=mid)
                    
                elif data ==3315:
                    user_step[cid]=3312
                    make_buy_invoice_inlinemarkup(cid=cid,mid=mid)
                elif data ==2315:
                    user_step[cid]=2312
                    make_buy_invoice_inlinemarkup(cid=cid,mid=mid)
                elif data >=2316 and data <2317 :
                    user_step[cid]=2312
                    make_buy_invoice_inlinemarkup(cid=cid,mid=mid)
                elif data >= 3316 and data < 3317 :
                    user_step[cid]= 3312    
                    make_buy_invoice_inlinemarkup(cid=cid,mid=mid)
                            
        else :
            bot.edit_message_reply_markup(cid, mid, reply_markup=None)
    elif data.startswith('buyuser'):
        if user_step[cid] >=1100 and user_step[cid] <1200 :
            data = data.split('-')[-1]
            if data.startswith('category'):
                data = data.split('/')[-1]
                if data  in category :
                    temp=dict()
                    number=1
                    result = search_on_kala(name_category=data )
                    if len(result) !=0 :
                        for i in result :
                            if i['count'] != 0:
                                temp.update({number:i})
                                number +=1
                        if len(temp) !=0 :
                            show_kala.update({cid:temp})        
                            # print(show_kala)
                            temp=dict()
                            if show_kala[cid][1]['M'] !=0 :
                                temp.update({'m':0})
                            if show_kala[cid][1]['L'] !=0 :
                                temp.update({'l':0})
                            if show_kala[cid][1]['XL'] !=0 :
                                temp.update({'xl':0})
                            if show_kala[cid][1]['XXL'] !=0 :
                                temp.update({'xxl':0})
                            count_of_size.update({cid:temp})
                            if user_step[cid] ==1100 :
                                user_step[cid] =1110
                            bot.edit_message_reply_markup(cid,mid,reply_markup=None)    
                            make_buy_menu_user(cid=cid ,mid =mid,number_kala=1)
                        else :    
                            bot.answer_callback_query(call_id, text['no_kala'],show_alert=True)
                    else :
                      bot.answer_callback_query(call_id, text['no_kala'],show_alert=True)
            elif data.startswith('showkala'):
                data = data.split('/')[-1]
                if data.startswith('minus'):
                    data=data.split('&')[-1]
                    if data.startswith('m'):
                        data=data.split('=')[-1]
                        data =int(data)
                        if count_of_size[cid]['m'] > 0:
                            count_of_size[cid]['m'] -=1
                            make_buy_menu_user(cid=cid ,mid =mid,number_kala=data)
                    elif data.startswith('l'):
                        data=data.split('=')[-1]
                        data =int(data)
                        if count_of_size[cid]['l'] > 0:
                            count_of_size[cid]['l'] -=1
                            make_buy_menu_user(cid=cid ,mid =mid,number_kala=data)
                    elif data.startswith('xl'):
                        data=data.split('=')[-1]
                        data=int(data)
                        if count_of_size[cid]['xl'] > 0:
                            count_of_size[cid]['xl'] -=1
                            make_buy_menu_user(cid=cid ,mid =mid,number_kala=data)
                    elif data.startswith('xxl'):
                        data=data.split('=')[-1]
                        data =int(data)
                        if count_of_size[cid]['xxl'] > 0:
                            count_of_size[cid]['xxl'] -=1
                            make_buy_menu_user(cid=cid ,mid =mid,number_kala=data)     
                    
                    
                elif  data.startswith('plus'): 
                    # print(show_kala[cid])   
                    data=data.split('&')[-1]
                    if data.startswith('m'):
                        data=data.split('=')[-1]
                        data =int(data)
                        if show_kala[cid][data]['M'] > count_of_size[cid]['m'] :
                            count_of_size[cid]['m'] +=1
                            make_buy_menu_user(cid=cid ,mid =mid,number_kala=data)
                    elif data.startswith('l'):
                        data=data.split('=')[-1]
                        data =int(data)
                        if show_kala[cid][data]['L'] > count_of_size[cid]['l'] :
                            count_of_size[cid]['l'] +=1
                            make_buy_menu_user(cid=cid ,mid =mid,number_kala=data)
                    elif data.startswith('xl'):
                        data=data.split('=')[-1]
                        data =int(data)
                        if show_kala[cid][data]['XL'] > count_of_size[cid]['xl'] :
                            count_of_size[cid]['xl'] +=1
                            make_buy_menu_user(cid=cid ,mid =mid,number_kala=data)
                    elif data.startswith('xxl'):
                        data=data.split('=')[-1]
                        data =int(data)
                        print(show_kala[cid][data]['XXL'])
                        if show_kala[cid][data]['XXL'] > count_of_size[cid]['xxl'] :
                            count_of_size[cid]['xxl'] +=1  
                            make_buy_menu_user(cid=cid ,mid =mid,number_kala=data)                          
                    
                elif  data.startswith('backward'):    
                    data=data.split('=')[-1]
                    data=int(data)  
                    if data > 1 :
                        for i in count_of_size[cid] :
                            count_of_size[cid][i] =0 
                        data -=1
                        bot.delete_message(cid,mid)
                        if user_step[cid]==1111 :
                            user_step[cid]=1110    
                        make_buy_menu_user(cid=cid ,mid =mid,number_kala=data)                    
                    else:
                        bot.answer_callback_query(call_id,text['first_kala'],show_alert=True)    
                elif  data.startswith('forward'):    
                    data=data.split('=')[-1]
                    data=int(data)
                    if data < len(show_kala[cid]) :
                        for i in count_of_size[cid] :
                            count_of_size[cid][i] =0 
                        data +=1
                        bot.delete_message(cid,mid)                     
                        if user_step[cid]==1111 :
                            user_step[cid]=1110   
                        make_buy_menu_user(cid=cid ,mid =mid,number_kala=data)    
                    else:
                        bot.answer_callback_query(call_id,text['last_kala'],show_alert=True)                  
                elif  data.startswith('addtocard'): 
                    data= data.split('=')[-1]
                    data= int(data)   
                    flag =0
                    for i in count_of_size[cid] :
                        if count_of_size[cid][i] > 0 :
                            flag =1
                            break
                    if flag == 1 :
                        if cid in shoping_cart :
                            if show_kala[cid][data]['id'] in shoping_cart[cid] :
                                temp=dict()
                                for i  in shoping_cart[cid] :
                                    if i == show_kala[cid][data]['id'] :
                                        temp=shoping_cart[cid][i]
                                        if 'm' in temp :
                                            if count_of_size[cid]['m']>0 :
                                                temp['m'] += count_of_size[cid]['m']
                                        else :
                                            if count_of_size[cid]['m']>0 :
                                                temp.update({'m':count_of_size[cid]['m']}) 
                                        
                                        if 'l' in temp :
                                            if count_of_size[cid]['l']>0 :
                                                temp['l'] += count_of_size[cid]['l']
                                        else :
                                            if count_of_size[cid]['l']>0 :
                                                temp.update({'l':count_of_size[cid]['l']})
                                        
                                        if 'xl' in temp :
                                            if count_of_size[cid]['xl']>0 :
                                                temp['xl'] += count_of_size[cid]['xl']
                                        else :
                                            if count_of_size[cid]['xl']>0 :
                                                temp.update({'xl':count_of_size[cid]['xl']})               
                                        
                                        if 'xxl' in temp :
                                            if count_of_size[cid]['xxl']>0 :
                                                temp['xxl'] += count_of_size[cid]['xxl']
                                        else :
                                            if count_of_size[cid]['xxl']>0 :
                                                temp.update({'xxl':count_of_size[cid]['xxl']})    
                                        shoping_cart[cid].update({i: temp})
                                        print(shoping_cart)
                                    
                            else :
                                temp=dict()
                                kala_id = show_kala[cid][data]['id']
                                kala_name = show_kala[cid][data]['kalaname']
                                sale_price = show_kala[cid][data]['sale_price']
                                image_file_id=show_kala[cid][data]['image_file_id']
                                temp.update({'kala_name':kala_name})
                                temp.update({'sale_price':sale_price})
                                temp.update({'sale_price':sale_price})
                                temp.update({'image_file_id':image_file_id})
                                for i in count_of_size[cid] :
                                    if count_of_size[cid][i] != 0:
                                        temp.update({i:count_of_size[cid][i]})
                                shoping_cart[cid].update({kala_id: temp}) 
                                print(shoping_cart) 
                        else :
                            temp=dict()
                            kala_id = show_kala[cid][data]['id']
                            kala_name = show_kala[cid][data]['kalaname']
                            sale_price = show_kala[cid][data]['sale_price']
                            image_file_id=show_kala[cid][data]['image_file_id']
                            temp.update({'kala_name':kala_name})
                            temp.update({'sale_price':sale_price})
                            temp.update({'sale_price':sale_price})
                            temp.update({'image_file_id':image_file_id})
                            for i in count_of_size[cid] :
                                if count_of_size[cid][i] != 0:
                                    temp.update({i:count_of_size[cid][i]})
                            shoping_cart.update({cid:{kala_id:temp}})
                            print(shoping_cart)  
                        
                        bot.delete_message(cid,mid)
                        if user_step[cid] == 1111 :
                            user_step[cid] = 1100 
                        bot.answer_callback_query(call_id,text['add_to_cart'],show_alert=True)         
                        make_buy_menu_user(cid=cid)
                            
                    else :
                        if user_step[cid]==1110 :
                            user_step[cid]=1111
                        bot.answer_callback_query(call_id ,text['no_choice'],show_alert=True )   
                elif  data.startswith('cancel'):    
                    bot.delete_message(cid,mid)
                    if user_step[cid] ==1110 or user_step[cid] ==1111 :
                        user_step[cid]=1000
                    bot.send_message(cid,text['select_menu'],reply_markup=make_ReplyKeyboardMarkup(user_s=user_step[cid]))   
            elif data.startswith('back'):
                data = data.split('/')[-1]
                data=int (data)
                if user_step[cid] == 1100:
                    user_step[cid] =1000
                    bot.edit_message_reply_markup(cid, mid, reply_markup=None)
                    bot.send_message(cid,text['select_menu'],reply_markup=make_ReplyKeyboardMarkup(user_s=user_step[cid]))    
                if user_step[cid] > 1100 and user_step[cid] <1120 :
                    user_step[cid]=1100
                    bot.delete_message(cid,mid)
                    make_buy_menu_user(cid)
                    
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
            if cid in user_cid or cid in user_profile.keys() : return
            username = message.chat.username
            today=date_today()
            insert_user(cid=cid ,username=username,user_date=today)
            user_cid.append(cid)
            user_profile.update({cid:[None,None,None,username,None]})          

            bot.send_message(cid,text['select_menu'],reply_markup=make_ReplyKeyboardMarkup(user_step[cid]))
        
@bot.message_handler(commands=['main'])
def main_command(message) :
    cid=message.chat.id
    if cid in block_user : return
    if user_step[cid] <2000 :
        bot.send_message(cid,text['select_menu'],reply_markup=make_ReplyKeyboardMarkup(user_s=user_step[cid]))
    elif user_step[cid] >= 2000 and user_step[cid] <3000 :
        bot.send_message(cid,text['select_menu'],reply_markup=make_ReplyKeyboardMarkup(user_s=user_step[cid]))
    elif user_step[cid] >= 3000 :
        bot.send_message(cid,text['select_menu'],reply_markup=make_ReplyKeyboardMarkup(user_s=user_step[cid]))

 

@bot.message_handler(commands=['help'])
def help_func(message) :
    cid=message.chat.id
    if cid in block_user : return
    if user_step[cid] <2000 :
        bot.send_message(cid,text['help'])

#ReplyKeyboardMarkup
#make buy menu for user

@bot.message_handler(func=lambda message : message.text==button['buy'])
def button_buy(message) :
    cid=message.chat.id
    if cid in block_user :return
    if user_step[cid] >= 2000 :return
    # markup=ReplyKeyboardMarkup(resize_keyboard=True)
    # markup.add(button['shirt'],button['tshirt'])
    # markup.add(button['home'],button['pants'])
    user_step[cid]=1100
    make_buy_menu_user(cid)
    bot.send_message(cid,text['goto_home'],reply_markup=make_ReplyKeyboardMarkup(user_s=user_step[cid]))



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

#make help button for user
@bot.message_handler(func=lambda message : message.text==button['help'])
def help_func(message) :
    cid=message.chat.id
    if cid in block_user : return
    if user_step[cid] <2000 :
        bot.send_message(cid,text['help'])

#make kala menu for admin and manger
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
        
#make group menu  for admin and manger
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
    
# this account  menu for manager and admin
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


#this invoice menu in admin and manager
@bot.message_handler(func=lambda message : message.text==button['invoice'])
def invoice_func(message):
    cid=message.chat.id       
    if cid in block_user : return
    if user_step [cid] == 2000:
        user_step[cid] = 2300
    if user_step[cid] == 3000 :
        user_step[cid] = 3300     
    bot.send_message(cid,text['select_menu'],reply_markup=make_ReplyKeyboardMarkup(user_s=user_step[cid]))
    

# make buy invoice menu on admin and manager
@bot.message_handler(func=lambda message : message.text==button['buy_invoice'])
def buy_invoice_func(message):
    cid=message.chat.id       
    if cid in block_user : return
    if user_step [cid] == 2300:
        user_step[cid] = 2310
    if user_step[cid] == 3300 :
        user_step[cid] = 3310
    bot.send_message(cid,text['goto_home'],reply_markup=make_ReplyKeyboardMarkup(user_s=user_step[cid]))
    make_buy_invoice_inlinemarkup(cid)


# make home button for all 
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
        
        
# this account menu  for user       
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

# this account menu  for user 
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
  
# this account menu  for user  
@bot.message_handler(func=lambda message : message.text==button['full_name'])
def full_name_func(message):
    cid=message.chat.id
    if cid in block_user :return
    user_step[cid]=1251
    bot.send_message(cid,text['message_name'])    

# this account menu  for user 
@bot.message_handler(func=lambda message : message.text==button['personal_id'])
def personal_id_func(message):
    cid=message.chat.id
    if cid in block_user :return
    user_step[cid]=1252
    bot.send_message(cid,text['message_national_code'])      

# this account menu  for user 
@bot.message_handler(func=lambda message : message.text==button['mobile'])
def mobile_phone_func(message):
    cid=message.chat.id
    if cid in block_user :return
    markup=ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton(button['send number'], request_contact=True))
    user_step[cid]= 1253
    bot.send_message(cid, text['share_phone'], reply_markup=markup)
 


 
# this account menu  for user    
@bot.message_handler(func=lambda message : message.text==button['adress'])
def adress_func(message):
    cid=message.chat.id
    if cid in block_user :return
    user_step[cid]=1254
    bot.send_message(cid,text['adress_message'])      
     

# this account menu  for user        
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
    

# this account menu  for user 
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

        
# this account menu  for user 
@bot.message_handler(func=lambda message : message.text==button['contact_to_me'])
def contact_to_me_func(message):
    cid=message.chat.id
    if cid in block_user :return
    if user_step[cid] <2000 :
        bot.send_message(cid,text['call_admin'])


# this handler for take photo
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
        



# ALL MESSAGE INCOMING
@bot.message_handler(func=lambda message :True)
def message_func(message):
    print(message)
    cid=message.chat.id
    print(user_step[cid])
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
    elif user_step[cid] ==2311 or user_step[cid] ==3311 :
        m=message.text
        result = search_on_user(fullname=m)    
        if len(result) == 0 :
            if user_step[cid] == 2311 :
                user_step[cid] = 2310
            elif user_step[cid] == 3311:
                user_step[cid] = 3310                   
            bot.send_message(cid,text['not_exist'])
            make_buy_invoice_inlinemarkup(cid=cid)
        else :
            make_buy_invoice_inlinemarkup(cid=cid,result=result)
    elif (user_step[cid] >=3313 and user_step[cid] <=3314 ) or (user_step[cid] >=2213 and user_step[cid] <=2214) :  
        flag =1  
        m=message.text
        if user_step[cid] ==3313 or user_step[cid] ==2313 :    
            result = search_on_kala(kalaname=m )
        elif user_step[cid] ==3314 or user_step[cid] ==2314 :
            if m.isnumeric() :
                m=int(m)
                result = search_on_kala(id=m )
            else :
                flag =0
        if flag ==1 :        
            if len(result) ==0 :
                bot.send_message(cid,text['not_exist'])
                if user_step[cid]==3313 or user_step[cid] == 3314 :
                    user_step[cid]= 3312
                elif user_step[cid] ==2313 or user_step[cid] ==2314 :
                    user_step[cid] = 2312
                make_buy_invoice_inlinemarkup(cid=cid)      
            else :
                if user_step[cid]==3313 or user_step[cid] == 3314 :
                    user_step[cid]= 3315
                elif user_step[cid] ==2313 or user_step[cid] ==2314 :
                    user_step[cid] = 2315
                make_buy_invoice_inlinemarkup(cid=cid,result =result ,kala=True)          
        else :
            bot.send_message(cid,text['enter_corect'])                
    elif (user_step[cid] >=3316 and user_step[cid] <3317 ) or (user_step[cid] >=2316 and user_step[cid] <2317) :          
        m =message.text
        if m.isnumeric() :
            m=int(m)
            if user_step[cid] ==2316.1 or user_step[cid] == 3316.1 :
                m1=m-temp_kala[cid]['m_size']
                temp_kala[cid]['m_size']=m
                temp_kala[cid]['count'] = temp_kala[cid]['count'] + m1
                if user_step[cid] == 2316.1 :
                    user_step[cid] =2316
                elif user_step[cid] == 3316.1 :
                    user_step[cid] =3316                
            
            elif user_step[cid] ==2316.2 or user_step[cid] == 3316.2 :
                m1=m-temp_kala[cid]['l_size']
                temp_kala[cid]['l_size']=m
                temp_kala[cid]['count'] = temp_kala[cid]['count'] + m1
                if user_step[cid] == 2316.2 :
                    user_step[cid] =2316
                elif user_step[cid] == 3316.2 :
                    user_step[cid] =3316
            
            elif user_step[cid] ==2316.3 or user_step[cid] == 3316.3 :
                m1=m-temp_kala[cid]['xl_size']
                temp_kala[cid]['xl_size']=m
                temp_kala[cid]['count'] = temp_kala[cid]['count'] + m1
                if user_step[cid] == 2316.3 :
                    user_step[cid] =2316
                elif user_step[cid] == 3316.3 :
                    user_step[cid] =3316  
            
            elif user_step[cid] ==2316.4 or user_step[cid] == 3316.4 :
                m1=m-temp_kala[cid]['xxl_size']
                temp_kala[cid]['xxl_size']=m
                temp_kala[cid]['count'] = temp_kala[cid]['count'] + m1
                if user_step[cid] == 2316.4 :
                    user_step[cid] =2316
                elif user_step[cid] == 3316.4 :
                    user_step[cid] =3316        
            
            elif user_step[cid] ==2316.5 or user_step[cid] == 3316.5 :
                temp_kala[cid]['buy_price']=m
                if user_step[cid] == 2316.5 :
                    user_step[cid] =2316
                elif user_step[cid] == 3316.5 :
                    user_step[cid] =3316                    
            make_buy_invoice_inlinemarkup(cid=cid)             
        else :
            bot.send_message(cid,text['enter_corect'])
                
bot.infinity_polling()
temp_kala