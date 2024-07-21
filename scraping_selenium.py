from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

options = webdriver.ChromeOptions()

options.add_experimental_option('excludeSwitches', ['enable-logging']) # Here
options.add_argument("--headless=new")
options.add_argument('--blink-settings=imagesEnabled=false')
driver = webdriver.Chrome(options=options)
driver.implicitly_wait(0)
url_base = "https://polovniautomobili.com"
driver.get("https://www.polovniautomobili.com/auto-oglasi/pretraga?brand=&price_to=&year_from=&year_to=&showOldNew=all&submit_1=&without_price=1")

#driver.find_element(By.CLASS_NAME, 'btn_poll_no').click()

for _ in range(1):

    results = [driver.find_element(By.CLASS_NAME, 'ga-topSearch-paid-2')]
    results.append(driver.find_element(By.CLASS_NAME, 'ga-topSearch-paid-1'))
    results += driver.find_elements(By.CLASS_NAME, 'ga-title')
    
    next_page_url = driver.find_element(By.CLASS_NAME, 'js-pagination-next').get_dom_attribute('href')
    
    all_links = [res.get_dom_attribute('href') for res in results]

    prices = []
    
    for link in all_links:
        driver.get(url_base + link)
        try:
            cur_price = driver.find_element(By.CLASS_NAME, 'priceClassified').text
            print(cur_price)
        except:
            print('fucked ' + link)
            continue
        prices.append(cur_price)

    driver.get(url_base + next_page_url)

#print(results)
print(prices)
driver.quit()