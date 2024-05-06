import mysql.connector



def get_info_user() :
    conn=mysql.connector.connect(user='root',password='mh0075239000',host='localhost',database='store')
    cursor=conn.cursor(dictionary=True)
    SQL_QURY="""SELECT * FROM user"""
    cursor.execute(SQL_QURY)
    result=cursor.fetchall()
    conn.commit()
    cursor.close()
    conn.close()
    return result







if __name__ == "__main__" :    
   pass
"""  print(get_info_user())
    result =get_info_user()
    for i in result :
        print(i)
        print(i['cid'])
        """