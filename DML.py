import mysql.connector
from Config import *





#All Function for user table


def insert_user(cid , fullname= None , mobile_phone = None , national_code=None , adress= None ,username=None):
    conn=mysql.connector.connect(**db_config)
    cursor=conn.cursor()
    SQL_QURY="""INSERT IGNORE INTO user(cid , fullname, username , national_code, mobile_phone  , adress )
                VALUE(%s,%s,%s,%s,%s,%s)
    """
    cursor.execute(SQL_QURY,(cid , fullname, username , national_code, mobile_phone  , adress))
    conn.commit()
    cursor.close()
    conn.close()

def update_user(cid , fullname , mobile_phone , national_code , adress ):
    conn=mysql.connector.connect(**db_config)
    cursor=conn.cursor()
    SQL_QURY="""UPDATE user SET  fullname = %s, national_code=%s, mobile_phone=%s  , adress=%s 
                WHERE cid=%s
    """
    cursor.execute(SQL_QURY,( fullname ,national_code, mobile_phone  , adress,cid ))
    conn.commit()
    cursor.close()
    conn.close()

#All function for category table

def insert_category(name_category ,show_category ):
    conn=mysql.connector.connect(**db_config)
    cursor=conn.cursor()
    SQL_QURY="""INSERT IGNORE INTO category(name_category ,show_category )
                VALUE(%s,%s)
    """
    cursor.execute(SQL_QURY,(name_category ,show_category))
    conn.commit()
    cursor.close()
    conn.close()


def update_category(new_name_category ,old_name_category ):
    conn=mysql.connector.connect(**db_config)
    cursor=conn.cursor()
    SQL_QURY="""UPDATE category SET name_category=%s WHERE name_category=%s"""
    cursor.execute(SQL_QURY,(new_name_category ,old_name_category))
    conn.commit()
    cursor.close()
    conn.close()

def delete_category(name_category):
    conn=mysql.connector.connect(**db_config)
    cursor=conn.cursor()
    SQL_QURY="""DELETE FROM category  WHERE name_category=%s"""
    cursor.execute(SQL_QURY,(name_category , ))
    conn.commit()
    cursor.close()
    conn.close()


if __name__ == "__main__":
    #pass
   #insert_user(cid=342165313,step=1000 ,username='masoud216')
   #update_user(cid=87889742,fullname='masoud hosseini',national_code='0075239000',mobile_phone = '09125227989',adress='prozi street')
   #insert_category(name_category='شلوار',show_category='YES')
   update_category(new_name_category='شلور' ,old_name_category='تی شرت' )
   #delete_category(name_category='شلوار')