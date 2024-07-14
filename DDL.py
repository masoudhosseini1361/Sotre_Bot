import mysql.connector
from Config import *

def create_database():
    conn=mysql.connector.connect(user=db_username,password=db_password,host=db_host)
    cursor=conn.cursor()
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
    cursor.close()
    conn.close()

def create_table_user():
    conn=mysql.connector.connect(**db_config)
    cursor=conn.cursor()
    SQL_QURY="""CREATE TABLE IF NOT EXISTS user(
        id              INT AUTO_INCREMENT NOT NULL PRIMARY KEY,
        cid             BIGINT NOT NULL ,
        fullname        VARCHAR(70),
        username        VARCHAR(32),
        national_code   CHAR(10),
        mobile_phone    VARCHAR(15),
        adress          VARCHAR(200),
        privilege       ENUM('USER','ADMIN') DEFAULT 'USER',
        is_block        ENUM('NO','YES') DEFAULT 'NO',
        user_date       varchar(10)
    )                   
    """
    cursor.execute(SQL_QURY)
    cursor.close()
    conn.close()

def create_table_category():
    conn=mysql.connector.connect(**db_config)
    cursor=conn.cursor()
    SQL_QURY="""CREATE TABLE IF NOT EXISTS category(
        name_category   VARCHAR(15) PRIMARY KEY NOT NULL ,
        show_category  ENUM('YES','NO') DEFAULT 'YES'
    )    
    """ 
    cursor.execute(SQL_QURY)
    cursor.close()
    conn.close()

# def create_table_category():
#     conn=mysql.connector.connect(**db_config)
#     cursor=conn.cursor()
#     SQL_QURY="""CREATE TABLE IF NOT EXISTS category(
#         name_english   VARCHAR(15) PRIMARY KEY NOT NULL ,
#         name_persian   VARCHAR(15),
#         show_category  ENUM('YES','NO') DEFAULT 'YES'
#     )    
#     """ 
#     cursor.execute(SQL_QURY)
#     cursor.close()
#     conn.close()



def create_table_kala():
    conn=mysql.connector.connect(**db_config)
    cursor=conn.cursor()
    SQL_QURY="""CREATE TABLE IF NOT EXISTS kala(
        id             INT AUTO_INCREMENT NOT NULL,
        kalaname       VARCHAR(50),
        buy_price      DOUBLE,
        sale_price     INT,
        name_category  VARCHAR(15),
        kala_date      VARCHAR(10) ,
        image_file_id  VARCHAR(200),
        count          SMALLINT (255) DEFAULT 0,
        M              SMALLINT (255) DEFAULT 0,
        L              SMALLINT (255) DEFAULT 0,
        XL             SMALLINT (255) DEFAULT 0,
        XXL            SMALLINT (255) DEFAULT 0,
        PRIMARY KEY(id),
        FOREIGN KEY (name_category) REFERENCES category (name_category)
    )
     """   
    cursor.execute(SQL_QURY)
    cursor.close()
    conn.close()


# def create_table_kala():
#     conn=mysql.connector.connect(**db_config)
#     cursor=conn.cursor()
#     SQL_QURY="""CREATE TABLE IF NOT EXISTS kala(
#         id             INT AUTO_INCREMENT NOT NULL,
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
#         PRIMARY KEY(id),
#         FOREIGN KEY (name_category) REFERENCES category (name_english)
#     )
#      """   
#     cursor.execute(SQL_QURY)
#     cursor.close()
#     conn.close()
    
    
def create_sale_invoice_table():
    conn=mysql.connector.connect(**db_config)
    cursor=conn.cursor()
    SQL_QURY="""CREATE TABLE IF NOT EXISTS sale_invoice(
        i_number            INT AUTO_INCREMENT NOT NULL ,
        user_id             INT,
        fullname            varchar(70),
        date_invoice        varchar(10),
        PRIMARY KEY(i_number),
        FOREIGN KEY (user_id) REFERENCES user (id)
    )
    """   
    cursor.execute(SQL_QURY)
    cursor.close()
    conn.close()
    
def create_sale_row_table():
    conn=mysql.connector.connect(**db_config)
    cursor=conn.cursor()
    SQL_QURY="""CREATE TABLE IF NOT EXISTS sale_row(
        i_number            INT ,
        kala_id             INT,
        kala_name           VARCHAR(50),
        kala_price          INT,
        count               SMALLINT(255),
        total_row           INT,
        FOREIGN KEY (i_number) REFERENCES sale_invoice(i_number),
        FOREIGN KEY (kala_id) REFERENCES kala (id)
    )
    """   
    cursor.execute(SQL_QURY)
    cursor.close()
    conn.close()
    


def create_buy_invoice_table():
    conn=mysql.connector.connect(**db_config)
    cursor=conn.cursor()
    SQL_QURY="""CREATE TABLE IF NOT EXISTS buy_invoice(
        i_number            INT AUTO_INCREMENT NOT NULL ,
        user_id             INT,
        fullname            varchar(70),
        date_invoice        varchar(10),
        PRIMARY KEY(i_number),
        FOREIGN KEY (user_id) REFERENCES user (id)
    )
    """   
    cursor.execute(SQL_QURY)
    cursor.close()
    conn.close()
    
def create_buy_row_table():
    conn=mysql.connector.connect(**db_config)
    cursor=conn.cursor()
    SQL_QURY="""CREATE TABLE IF NOT EXISTS buy_row(
        i_number            INT ,
        kala_id             INT,
        kala_name           VARCHAR(50),
        kala_price          INT,
        count               SMALLINT(255),
        total_row           INT,
        FOREIGN KEY (i_number) REFERENCES buy_invoice(i_number),
        FOREIGN KEY (kala_id) REFERENCES kala (id)
    )
    """   
    cursor.execute(SQL_QURY)
    cursor.close()
    conn.close()
    
                                        


        
    
if __name__ == "__main__" :
    create_database()
    create_table_user() 
    create_table_category()
    create_table_kala()
    create_sale_invoice_table()
    create_sale_row_table()
    create_buy_invoice_table()
    create_buy_row_table()