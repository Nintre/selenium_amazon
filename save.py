import pymysql
from my_selenium import setting


def save_data(item):
    db = pymysql.connect(host=setting.HOSTNAME, user=setting.USERNAME, password=setting.PASSWORD,
                         database=setting.DATABASE,
                         charset='utf8mb4', port=setting.PORT)
    cursor = db.cursor()
    try:
        product_sql = "insert into `parse_product`(`keywords`,`asin`,`title`,`image`,`stars`,`ratings`,`price`,`sponsored`,`best_seller_in`) values (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(product_sql, (item['keywords'], item['asin'],
                                     item['title'], item['image'],
                                     item['stars'], item['ratings'], item['price'],
                                     item['sponsored'], item['best_seller_in']))
        db.commit()
    except Exception as e:
        print("product_sql insert err:", e)
        db.rollback()