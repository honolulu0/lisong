import sqlite3
from sqlite3 import OperationalError

conn = sqlite3.connect('去重文件.sqlite3')
cur = conn.cursor()


def creat_db():
    try:
        sql = """create table listen_product
(
    id                  INTEGER not null
        primary key autoincrement,
    product_ID          varchar(255),
    product_title       varchar(255),
    product_store_ID    varchar(255),
    create_time datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
    product_platform    varchar(255),
    product_url         varchar(255),
    product_description varchar(255),
    product_store_url   varchar(255),
    constraint id_and_title_uniq
        unique (product_ID, product_title)
);
"""
        cur.execute(sql)
        sql = """create table listen_store
(
    id                 INTEGER not null
        primary key autoincrement,
    store_ID           varchar(255),
    store_title        varchar(255),
    store_crawl_time   varchar(255),
    store_platform     varchar(255),
    store_crawl_status varchar(255),
    store_enabled      bool    not null,
    store_url          varchar(255),
    store_description  varchar(255)
);
"""
        cur.execute(sql)
        print("create table success")
        return True
    except OperationalError as o:
        print(str(o))
        pass
        if str(o) == "table gas_price already exists":
            return True
        return False
    except Exception as e:
        print(e)
        return False
    finally:
        pass


def insert_url(product_store_ID, product_ID, product_title):
    insert_sql = f"""insert into listen_product(product_ID, product_title, product_store_ID) values('{product_ID}','{product_title}','{product_store_ID}')"""
    # print(insert_sql)
    try:
        cur.execute(insert_sql)
        conn.commit()
    except Exception as e:
        # print(e)
        conn.rollback()

        return False
    else:
        return True


def closed_db():
    cur.close()
    conn.close()
