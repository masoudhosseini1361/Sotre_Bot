import mysql.connector


def create_database():
    conn=mysql.connector.connect(user='root',password='mh0075239000',host='localhost')
    cursor=conn.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS store")
    cursor.close()
    conn.close()

def create_table_user():
    conn=mysql.connector.connect(user='root',password='mh0075239000',host='localhost',database='store')
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
        user_date       DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP     
    )                   
    """
    cursor.execute(SQL_QURY)
    cursor.close()
    conn.close()

def create_table_category():
    conn=mysql.connector.connect(user='root',password='mh0075239000',host='localhost',database='store')
    cursor=conn.cursor()
    SQL_QURY="""CREATE TABLE IF NOT EXISTS category(
        name_english   VARCHAR(15) PRIMARY KEY NOT NULL ,
        name_persian   VARCHAR(15),
        show_category  ENUM('YES','NO') DEFAULT 'YES'
    )    
    """ 
    cursor.execute(SQL_QURY)
    cursor.close()
    conn.close()



def create_table_kala():
    conn=mysql.connector.connect(user='root',password='mh0075239000',host='localhost',database='store')
    cursor=conn.cursor()
    SQL_QURY="""CREATE TABLE IF NOT EXISTS kala(
        id             INT AUTO_INCREMENT NOT NULL,
        kalaname       VARCHAR(50),
        buy_price      DOUBLE,
        sale_price     INT,
        name_category  VARCHAR(15),
        kala_date      DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
        image_file_id   VARCHAR(200),
        count          SMALLINT (255) DEFAULT 0,
        M              SMALLINT (255) DEFAULT 0,
        L              SMALLINT (255) DEFAULT 0,
        XL             SMALLINT (255) DEFAULT 0,
        XXL            SMALLINT (255) DEFAULT 0,
        PRIMARY KEY(id),
        FOREIGN KEY (name_category) REFERENCES category (name_english)
    )
     """   
    cursor.execute(SQL_QURY)
    cursor.close()
    conn.close()
    
    
def create_sale_invoice_table():
    conn=mysql.connector.connect(user='root',password='mh0075239000',host='localhost',database='store')
    cursor=conn.cursor()
    SQL_QURY="""CREATE TABLE IF NOT EXISTS sale_invoice(
        i_number            INT AUTO_INCREMENT NOT NULL ,
        user_id             INT,
        date_invoice        DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
        PRIMARY KEY(i_number),
        FOREIGN KEY (user_id) REFERENCES user (id)
    )
    """   
    cursor.execute(SQL_QURY)
    cursor.close()
    conn.close()
    
def create_sale_row_table():
    conn=mysql.connector.connect(user='root',password='mh0075239000',host='localhost',database='store')
    cursor=conn.cursor()
    SQL_QURY="""CREATE TABLE IF NOT EXISTS sale_row(
        i_number            INT ,
        kala_id             INT,
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
    

        
    
if __name__ == "__main__" :
    pass


"""    create_database()
    create_table_user() 
    create_table_category()
    create_table_kala()
    create_sale_invoice_table()
    create_sale_row_table()"""