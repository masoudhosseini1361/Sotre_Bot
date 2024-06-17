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



if __name__ == "__main__":
    # pass
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
    result=get_info_kala()
    print(result)
"""  print(get_info_user())
    result =get_info_user()
    for i in result :
        print(i)
        print(i['cid'])
        """
