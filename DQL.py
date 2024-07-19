import mysql.connector
from Config import *

#All Function for user table


def get_info_user() :
    conn=mysql.connector.connect(**db_config)
    cursor=conn.cursor(dictionary=True)
    SQL_QURY="""SELECT * FROM user"""
    cursor.execute(SQL_QURY)
    result=cursor.fetchall()
    cursor.close()
    conn.close()
    return result



def search_on_user(fullname=None ,national_code=None ,mobile_phone=None,cid=None) :
    conn=mysql.connector.connect(**db_config)
    cursor=conn.cursor(dictionary=True)
    if fullname != None :
        fullname =f'%{fullname}%'
        SQL_QURY="SELECT * FROM user WHERE fullname like %s"
        cursor.execute(SQL_QURY,(fullname,))
    elif national_code !=None:
        national_code=f'%{national_code}%'
        SQL_QURY="SELECT * FROM user WHERE national_code like %s"
        cursor.execute(SQL_QURY,(national_code,))
    elif  mobile_phone != None :
        mobile_phone=f'%{mobile_phone}%'
        SQL_QURY="SELECT * FROM user WHERE mobile_phone like %s"
        cursor.execute(SQL_QURY,(mobile_phone,))
    elif cid != None :
        SQL_QURY="SELECT fullname,national_code,mobile_phone,adress FROM user WHERE cid = %s"
        cursor.execute(SQL_QURY,(cid,))
    result=cursor.fetchall()
    cursor.close()
    conn.close()
    return result

def search_condition_on_user(cid) :
    conn=mysql.connector.connect(**db_config)
    cursor=conn.cursor(dictionary=True)
    SQL_QURY="""SELECT fullname,privilege,is_block FROM user WHERE cid = %s """
    cursor.execute(SQL_QURY,(cid,))
    result=cursor.fetchall()
    cursor.close()
    conn.close()
    return result        

def search_condition_on_user_by_cid(cid) :
    conn=mysql.connector.connect(**db_config)
    cursor=conn.cursor(dictionary=True)
    SQL_QURY="""SELECT id,fullname FROM user WHERE cid = %s """
    cursor.execute(SQL_QURY,(cid,))
    result=cursor.fetchall()
    cursor.close()
    conn.close()
    return result 



#All Function for category table


def get_info_category() :
    conn=mysql.connector.connect(**db_config)
    cursor=conn.cursor(dictionary=True)
    SQL_QURY="""SELECT * FROM category"""
    cursor.execute(SQL_QURY)
    result=cursor.fetchall()
    cursor.close()
    conn.close()
    return result


def condition_category( name_category ):
    conn=mysql.connector.connect(**db_config)
    cursor=conn.cursor(dictionary=True)
    SQL_QURY="""SELECT show_category FROM category  where  name_category = %s"""
    cursor.execute(SQL_QURY,(name_category,))
    result=cursor.fetchall()
    cursor.close()
    conn.close()
    return result

#All Function for kala table

def get_info_kala() :
    conn=mysql.connector.connect(**db_config)
    cursor=conn.cursor(dictionary=True)
    SQL_QURY="""SELECT * FROM kala"""
    cursor.execute(SQL_QURY)
    result=cursor.fetchall()
    cursor.close()
    conn.close()
    return result

def last_kala_id() :
    conn=mysql.connector.connect(**db_config)
    cursor=conn.cursor(dictionary=True)
    SQL_QURY="""SELECT id FROM kala ORDER BY id DESC LIMIT 1"""
    cursor.execute(SQL_QURY)
    result=cursor.fetchall()
    cursor.close()
    conn.close()
    result =result[0]['id']
    return result


def get_field_kalaname() :
    conn=mysql.connector.connect(**db_config)
    cursor=conn.cursor(dictionary=True)
    SQL_QURY="""SELECT  kalaname FROM kala """
    cursor.execute(SQL_QURY)
    result=cursor.fetchall()
    cursor.close()
    conn.close()
    return result
    
def get_infokala_where_category(category):
    conn=mysql.connector.connect(**db_config)
    cursor=conn.cursor(dictionary=True)
    SQL_QURY="SELECT id,kalaname,sale_price FROM kala WHERE name_category=%s"
    cursor.execute(SQL_QURY,(category,))
    result=cursor.fetchall()
    cursor.close()
    conn.close()
    return result


def search_on_kala(kalaname=None ,id=None ,name_category=None) :
    conn=mysql.connector.connect(**db_config)
    cursor=conn.cursor(dictionary=True)
    if kalaname != None :
        fullname =f'%{kalaname}%'
        SQL_QURY="SELECT * FROM kala WHERE kalaname like %s"
        cursor.execute(SQL_QURY,(fullname,))
    elif id !=None:
        SQL_QURY="SELECT * FROM kala WHERE id = %s"
        cursor.execute(SQL_QURY,(id,))
    elif name_category != None :
        SQL_QURY="SELECT * FROM kala WHERE name_category = %s"
        cursor.execute(SQL_QURY,(name_category,))     
    result=cursor.fetchall()
    cursor.close()
    conn.close()
    return result
    
def search_on_kala_by_size(id, m=None ,l=None ,xl=None,xxl=None) :
    conn=mysql.connector.connect(**db_config)
    cursor=conn.cursor(dictionary=True)
    if m != None :
        SQL_QURY="SELECT m FROM kala WHERE id=%s"
        cursor.execute(SQL_QURY,(id,))
    elif l !=None:
        SQL_QURY="SELECT l FROM kala WHERE id=%s"
        cursor.execute(SQL_QURY,(id,))
    elif xl != None :
        SQL_QURY="SELECT xl FROM kala WHERE id=%s"
        cursor.execute(SQL_QURY,(id,)) 
    elif xxl != None :
        SQL_QURY="SELECT xxl FROM kala WHERE id=%s"
        cursor.execute(SQL_QURY,(id,))       
    result=cursor.fetchall()
    cursor.close()
    conn.close()
    return result



#All Function for buy invoice table

def last_buyinvoice_id() :
    conn=mysql.connector.connect(**db_config)
    cursor=conn.cursor(dictionary=True)
    SQL_QURY="""SELECT i_number FROM buy_invoice ORDER BY i_number DESC LIMIT 1"""
    cursor.execute(SQL_QURY)
    result=cursor.fetchall()
    cursor.close()
    conn.close()
    result =result[0]['i_number']
    return result

def get_info_buyrow_where_kala_id(kala_id):
    conn=mysql.connector.connect(**db_config)
    cursor=conn.cursor(dictionary=True)
    SQL_QURY="SELECT i_number FROM buy_row WHERE kala_id=%s"
    cursor.execute(SQL_QURY,(kala_id,))
    result=cursor.fetchall()
    cursor.close()
    conn.close()
    return result






#All Function for sale_row table
def get_info_salerow_where_kala_id(kala_id):
    conn=mysql.connector.connect(**db_config)
    cursor=conn.cursor(dictionary=True)
    SQL_QURY="SELECT i_number FROM buy_row WHERE kala_id=%s"
    cursor.execute(SQL_QURY,(kala_id,))
    result=cursor.fetchall()
    cursor.close()
    conn.close()
    return result

def last_sale_invoice_id() :
    conn=mysql.connector.connect(**db_config)
    cursor=conn.cursor(dictionary=True)
    SQL_QURY="""SELECT i_number FROM sale_invoice ORDER BY i_number DESC LIMIT 1"""
    cursor.execute(SQL_QURY)
    result=cursor.fetchall()
    cursor.close()
    conn.close()
    result =result[0]['i_number']
    return result





if __name__ == "__main__":
    pass
    # print(search_on_user(cid=6944720842))
    # print(search_condition_on_user_by_cid(cid=6944720842))
    # print(search_on_kala(name_category='تی شرت' ))
    # print(search_on_kala(kalaname=None ,id=7 ))
    # print(condition_category( name_category='تی شرت' ))
    # result =search_condition_on_user(cid=6944720842)
    # result=result[0]
    # print(result)
    # print(search_condition_on_user(cid=6944720842))
    # print(search_on_user(fullname='حسینی'))
    # print(search_on_user(mobile_phone='522'))
    # print(search_on_user(national_code='239'))
    # # print (get_info_salrow_where_kala_id(kala_id=4))
    # print(get_infokala_where_category(category='تی شرت'))
    # print( get_field_kalaname())
    # resualt= get_info_category()
    # print(resualt)
    # if len (resualt) !=0 :
    #     for i in resualt :
    #         name_english =i['name_english']
    #         name_persian =i['name_persian']
    #         show_category = i['show_category']
    #         print (name_english,name_persian,show_category ,"\n")
    # else :
    #     print("zero")
    # result=get_info_kala()
    # print(result)
    # print(last_kala_id())
    
#   print(get_info_user())
    # result =get_info_user()
    # for i in result :
    #     print(i)
    #     print(i['cid'])
        
