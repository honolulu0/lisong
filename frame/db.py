import time

from frame.my_sqllite import insert_url

now_time = time.strftime("%Y-%m-%d", time.localtime())


def save_db(shop_name, product_id, title):
    print(shop_name, product_id, title)
    if insert_url(shop_name, product_id, title):
        with open(f"{now_time}采集记录.txt", "a+") as f:  # 设置文件对象
            f.write(f'{shop_name}\t{product_id}\t{title}\n')
        return True
