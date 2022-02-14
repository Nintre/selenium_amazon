from my_selenium import save


def parse_title(driver, asin):
    title = ''
    try:
        title = driver.find_element_by_xpath('//div[@data-asin="{}"]//span[@class="a-size-medium a-color-base a-text-normal" or @class="a-size-base-plus a-color-base a-text-normal"]'.format(asin)).get_attribute('textContent')
    except Exception as e:
        print("parse_title err:", e)
    return title


def parse_image(driver, asin):
    image = ''
    try:
        image = driver.find_element_by_xpath('//div[@data-asin="{}"]//img[@class="s-image"]'.format(asin)).get_attribute('src')
    except Exception as e:
        print("parse_image err:", e)
    return image


def parse_stars(driver, asin):
    stars = ''
    try:
        stars = driver.find_element_by_xpath('//div[@data-asin="{}"]//span[@class="a-icon-alt"]'.format(asin)).get_attribute('textContent')
    except Exception as e:
        print("parse_stars err:", e)
    return stars


def parse_ratings(driver, asin):
    ratings = ''
    try:
        ratings = driver.find_element_by_xpath('//div[@data-asin="{}"]//span[@class="a-size-base s-underline-text"]'.format(asin)).get_attribute('textContent')
    except Exception as e:
        print("parse_ratings err:", e)
    return ratings


def parse_price(driver, asin):
    price = ''
    try:
        price = driver.find_element_by_xpath('//div[@data-asin="{}"]//div[@class="a-row a-size-base a-color-base"]//span[@class="a-offscreen"]'.format(asin)).get_attribute('textContent')
    except Exception as e:
        print("parse_price err:", e)
    return price


def parse_sponsored(driver, asin):
    sponsored = ''
    try:
        sponsored = driver.find_element_by_xpath('//div[@data-asin="{}"]//span[@class="s-label-popover-hover"]//span[@class="a-color-base"]'.format(asin)).get_attribute('textContent')
    except Exception as e:
        print("parse_sponsored err:", e)
    return sponsored


def parse_best_seller_in(driver, asin):
    best_seller_in = ''
    try:
        best_seller_in = driver.find_element_by_xpath('//div[@data-asin="{}"]//span[@id="{}-best-seller-supplementary"]'.format(asin, asin)).get_attribute('textContent').replace('in ', '')

    except Exception as e:
        print("best_seller_in err:", e)
    return best_seller_in


def parse_one_keywords(driver, keywords):
    product_list = driver.find_elements_by_xpath('//div[@class="s-main-slot s-result-list s-search-results sg-row"]/div[@data-asin]')
    # print(len(product_list))
    asin_list = []
    for asin in product_list:
        asin = asin.get_attribute('data-asin')
        if asin != '':
            asin_list.append(asin)
    print(asin_list)
    print(len(asin_list))

    for asin in asin_list:
        item = {}
        item['keywords'] = keywords
        item['asin'] = asin

        title = parse_title(driver, asin)
        item['title'] = title

        image = parse_image(driver, asin)
        item['image'] = image

        stars = parse_stars(driver, asin)
        item['stars'] = stars

        ratings = parse_ratings(driver, asin)
        item['ratings'] = ratings

        price = parse_price(driver, asin)
        item['price'] = price

        sponsored = parse_sponsored(driver, asin)
        item['sponsored'] = sponsored

        best_seller_in = parse_best_seller_in(driver, asin)
        item['best_seller_in'] = best_seller_in

        print(item)
        save.save_data(item)



