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

#    id             INT AUTO_INCREMENT NOT NULL,
#         kalaname       VARCHAR(50),
#         buy_price      DOUBLE,
#         sale_price     INT,
#         name_category  VARCHAR(15),
#         kala_date      DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
#         image_file_id   VARCHAR(200),
#         count          SMALLINT (255) DEFAULT 0,
#         M              SMALLINT (255) DEFAULT 0,
#         L              SMALLINT (255) DEFAULT 0,
#         XL             SMALLINT (255) DEFAULT 0,
#         XXL            SMALLINT (255) DEFAULT 0,



# All Function  For Kala  Table


def insert_kala( kalaname,name_category ,kala_date,image_file_id,sale_price=0 , buy_price = 0 , count=0,m_size=0,l_size=0,xl_size=0,xxl_size=0):
    conn=mysql.connector.connect(**db_config)
    cursor=conn.cursor()
    SQL_QURY="""INSERT IGNORE INTO kala(kalaname, buy_price , sale_price , name_category , kala_date , image_file_id , count ,M ,L ,XL ,XXL )
                VALUE(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """
    cursor.execute(SQL_QURY,(kalaname, buy_price , sale_price ,name_category ,kala_date,image_file_id,count,m_size,l_size,xl_size,xxl_size))
    conn.commit()
    cursor.close()
    conn.close()

def edit_update_kala(id,kalaname,image_file_id,sale_price):
    conn=mysql.connector.connect(**db_config)
    cursor=conn.cursor()
    SQL_QURY="""UPDATE kala SET kalaname=%s ,sale_price=%s,image_file_id=%s WHERE id=%s"""
    cursor.execute(SQL_QURY,(kalaname,sale_price ,image_file_id,id))
    conn.commit()
    cursor.close()
    conn.close()


if __name__ == "__main__":
    pass
   #insert_user(cid=342165313,step=1000 ,username='masoud216')
   #update_user(cid=87889742,fullname='masoud hosseini',national_code='0075239000',mobile_phone = '09125227989',adress='prozi street')
   #insert_category(name_category='شلوار',show_category='YES')
  # update_category(new_name_category='شلور' ,old_name_category='تی شرت' )
   #delete_category(name_category='شلوار')
#    insert_kala( kalaname='polo',name_category='تی شرت' ,kala_date='1403/03/27',image_file_id='d:\python\project\image.jpg', buy_price = 0 , sale_price=0 , count=0,m_size=0,l_size=0,xl_size=0,xxl_size=0)
    # edit_update_kala(id=2,kalaname='BURBERRY',image_file_id='D:\share\13189.jpg',sale_price=850000)
