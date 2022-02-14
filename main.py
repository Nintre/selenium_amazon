import time
import multiprocessing
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities

from my_selenium import parse_product

# 15
keywords_list = ['phone', 'computer', 'tree', 'cat', 'dog', 'food', 'basketball', 'fishing', 'golf', 'hunting', 'gift', 'bag', 'football', 'ping pang', 'book']


def main():
    queue = multiprocessing.Manager().Queue()
    for keyword in keywords_list:
        queue.put(keyword)
        print('关键词:', keyword)

    print('queue 开始大小 %d' % queue.qsize())

    pool = multiprocessing.Pool(8)  # 异步进程池（非阻塞）
    for index in range(queue.qsize()):
        pool.apply_async(process_one, args=(queue,))
        # time.sleep(1)
    pool.close()
    pool.join()
    queue.join()


def process_one(in_queue):
    while in_queue.empty() is not True:
        keywords = in_queue.get()
        keywords_url = 'https://www.amazon.com/s?k=' + keywords

        chrome_options = webdriver.ChromeOptions()
        prefs = {'profile.managed_default_content_settings.images': 2}
        chrome_options.add_experimental_option('prefs', prefs)

        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument("disable-web-security")
        chrome_options.add_argument('disable-infobars')

        chrome_options.headless = True

        chrome_options.add_argument('User-Agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Safari/605.1.15"')
        chrome_options.add_argument('Accept-Language="en"')
        chrome_options.add_argument('Connection="keep-alive"')

        chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])

        driver = webdriver.Chrome("/users/hutaiyi/downloads/chromedriver", options=chrome_options)

        driver.get(keywords_url)

        postal = "10001"
        # print(driver.page_source)

        change_address(driver, postal)

        parse_product.parse_one_keywords(driver, keywords)

        driver.close()

        in_queue.task_done()


def change_address(driver, postal):
    while True:
        try:
            driver.find_element_by_id('glow-ingress-line1').click()
            time.sleep(1)
        except Exception as e:
            driver.refresh()
            time.sleep(1)
            continue
        try:
            driver.find_element_by_id("GLUXChangePostalCodeLink").click()
            time.sleep(1)
        except:
            pass
        try:
            driver.find_element_by_id('GLUXZipUpdateInput').send_keys(postal)
            time.sleep(1)
            break
        except Exception as NoSuchElementException:
            try:
                driver.find_element_by_id('GLUXZipUpdateInput_0').send_keys(postal.split('-')[0])
                time.sleep(1)
                driver.find_element_by_id('GLUXZipUpdateInput_1').send_keys(postal.split('-')[1])
                time.sleep(1)
                break
            except Exception as NoSuchElementException:
                driver.refresh()
                time.sleep(1)
                continue
        print("重新选择地址")
    driver.find_element_by_id('GLUXZipUpdate').click()
    time.sleep(1)
    driver.refresh()


if __name__ == "__main__":
    start = time.time()
    main()
    end = time.time()
    print((end - start))
