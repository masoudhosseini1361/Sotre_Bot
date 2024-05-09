import mysql.connector


def insert_user(cid , fullname= None , mobile_phone = None , national_code=None , adress= None ,username=None):
    conn=mysql.connector.connect(user='root',password='mh0075239000',host='localhost',database='store')
    cursor=conn.cursor()
    SQL_QURY="""INSERT IGNORE INTO user(cid , fullname, username , national_code, mobile_phone  , adress )
                VALUE(%s,%s,%s,%s,%s,%s)
    """
    cursor.execute(SQL_QURY,(cid , fullname, username , national_code, mobile_phone  , adress))
    conn.commit()
    cursor.close()
    conn.close()




if __name__ == "__main__":
    pass
   #insert_user(cid=342165313,step=1000 ,username='masoud216')