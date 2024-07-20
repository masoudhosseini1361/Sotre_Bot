import mysql.connector
from Config import *





#All Function for user table


def insert_user(cid ,user_date ,fullname= None , mobile_phone = None , national_code=None , adress= None ,username=None):
    conn=mysql.connector.connect(**db_config)
    cursor=conn.cursor()
    SQL_QURY="""INSERT IGNORE INTO user(cid , user_date,fullname, username , national_code, mobile_phone  , adress )
                VALUE(%s,%s,%s,%s,%s,%s,%s)
    """
    cursor.execute(SQL_QURY,(cid , user_date,fullname, username , national_code, mobile_phone  , adress))
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

def update_condition_user(cid,privilege =None ,is_block =None) :
    conn=mysql.connector.connect(**db_config)
    cursor=conn.cursor() 
    if  privilege != None : 
        SQL_QURY="""UPDATE user SET   privilege=%s WHERE cid=%s """
        cursor.execute(SQL_QURY,( privilege,cid ))
    elif is_block != None : 
        SQL_QURY="""UPDATE user SET   is_block=%s WHERE cid=%s """
        cursor.execute(SQL_QURY,(is_block,cid ))  
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

def update_show_category(name_category,show_category) :
    conn=mysql.connector.connect(**db_config)
    cursor=conn.cursor()
    SQL_QURY="""UPDATE category SET show_category=%s WHERE name_category=%s"""
    cursor.execute(SQL_QURY,(show_category ,name_category ))
    conn.commit()
    cursor.close()
    conn.close()
 

# All Function  For Kala  Table

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

def update_kala_with_buyinvoice(id , buy_price , count , m_size ,l_size ,xl_size ,xxl_size):
    conn=mysql.connector.connect(**db_config)
    cursor=conn.cursor()
    SQL_QURY="""UPDATE kala SET buy_price=%s , count= count+%s ,M=M +%s ,L = L + %s , XL = XL + %s , XXL = XXL + %s WHERE id=%s"""
    cursor.execute(SQL_QURY,(buy_price,count ,m_size ,l_size ,xl_size ,xxl_size,id))
    conn.commit()
    cursor.close() 
    conn.close()
    

def update_kala_with_saleinvoice(id , count , size ):
    conn=mysql.connector.connect(**db_config)
    cursor=conn.cursor()
    if size == 'm' :
        SQL_QURY="""UPDATE kala SET  count= count - %s ,M = M - %s  WHERE id=%s"""
    elif size == 'l' :
        SQL_QURY="""UPDATE kala SET  count= count - %s ,L = L - %s  WHERE id=%s"""    
    elif size == 'xl' :
        SQL_QURY="""UPDATE kala SET count= count - %s , XL = XL - %s  WHERE id=%s"""    
    elif size == 'xxl' :
        SQL_QURY="""UPDATE kala SET count= count - %s , XXL = XXL - %s WHERE id=%s"""            
    cursor.execute(SQL_QURY,(count ,count,id))
    conn.commit()
    cursor.close() 
    conn.close()    


def delete_kala(id):
    conn=mysql.connector.connect(**db_config)
    cursor=conn.cursor()
    SQL_QURY="""DELETE FROM kala  WHERE id=%s"""
    cursor.execute(SQL_QURY,(id , ))
    conn.commit()
    cursor.close()
    conn.close()

# All Function  For buy invoice  Table

def insert_buyinvoice(user_id,fullname,date_invoice):
    conn=mysql.connector.connect(**db_config)
    cursor=conn.cursor()
    SQL_QURY="""INSERT IGNORE INTO buy_invoice(user_id,fullname,date_invoice )
                VALUE(%s,%s,%s)
    """
    cursor.execute(SQL_QURY,(user_id,fullname,date_invoice))
    conn.commit()
    cursor.close()
    conn.close()

def insert_buy_rowinvoice(i_number,kala_id,kala_name,kala_price,count,total_row):
    conn=mysql.connector.connect(**db_config)
    cursor=conn.cursor()
    SQL_QURY="""INSERT IGNORE INTO buy_row(i_number,kala_id,kala_name,kala_price,count,total_row )
                VALUE(%s,%s,%s,%s,%s,%s)
    """
    cursor.execute(SQL_QURY,(i_number,kala_id,kala_name,kala_price,count,total_row))
    conn.commit()
    cursor.close()
    conn.close()

# All Function  For sale invoice  Table

def insert_sale_invoice(user_id,fullname,date_invoice):
    conn=mysql.connector.connect(**db_config)
    cursor=conn.cursor()
    SQL_QURY="""INSERT IGNORE INTO sale_invoice(user_id,fullname,date_invoice )
                VALUE(%s,%s,%s)
    """
    cursor.execute(SQL_QURY,(user_id,fullname,date_invoice))
    conn.commit()
    cursor.close()
    conn.close()

def insert_sale_rowinvoice(i_number,kala_id,kala_name,kala_price,count,total_row):
    conn=mysql.connector.connect(**db_config)
    cursor=conn.cursor()
    SQL_QURY="""INSERT IGNORE INTO sale_row(i_number,kala_id,kala_name,kala_price,count,total_row )
                VALUE(%s,%s,%s,%s,%s,%s)
    """
    cursor.execute(SQL_QURY,(i_number,kala_id,kala_name,kala_price,count,total_row))
    conn.commit()
    cursor.close()
    conn.close()


if __name__ == "__main__":
    pass
    # insert_sale_rowinvoice(i_number=2,kala_id=4,kala_name='xcxc',kala_price=216556,count=12,total_row=564165)
    # update_show_category(name_category='تی شرت',show_category='NO')
    # update_show_category(name_category='تی شرت',show_category='YES')
    # delete_kala(id=8)
    #insert_user(cid=342165313,step=1000 ,username='masoud216')
    #update_user(cid=87889742,fullname='masoud hosseini',national_code='0075239000',mobile_phone = '09125227989',adress='prozi street')
    #insert_category(name_category='شلوار',show_category='YES')
    # update_category(new_name_category='شلور' ,old_name_category='تی شرت' )
    #delete_category(name_category='شلوار')
    #insert_kala( kalaname='polo',name_category='تی شرت' ,kala_date='1403/03/27',image_file_id='d:\python\project\image.jpg', buy_price = 0 , sale_price=0 , count=0,m_size=0,l_size=0,xl_size=0,xxl_size=0)
    # edit_update_kala(id=2,kalaname='BURBERRY',image_file_id='D:\share\13189.jpg',sale_price=850000)
