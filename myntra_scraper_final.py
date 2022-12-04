import requests, json
from bs4 import BeautifulSoup
import bs4
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
import sys
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
import csv

product_links1 = []
product_links2 = []
binary = FirefoxBinary("C:/Program Files/Mozilla Firefox/firefox.exe")
driver = webdriver.Firefox(firefox_binary=binary)


def get_product_links(url):
    try:
        driver.get(url)
        elem = driver.find_element(By.CLASS_NAME, 'results-base')
        code = elem.get_attribute('innerHTML')        
        
    except Exception as e:
        print(e)
        exit()
        
    soup_res = bs4.BeautifulSoup(code, 'html.parser')    
    data = soup_res.find_all('li',{'class':'product-base'})
    for d in data:
        link = d.find('a')['href']
        product_links1.append(link)

def get_page_links(page_links):
    for url in page_links:
        get_product_links(url)

page_links=['https://www.myntra.com/shoes?p='+str(i) for i in range(1,5)]
t0 = time.time()
print("geckodriver is starting....")
get_page_links(page_links)
t1 = time.time()
print("Closing driver, please wait...")
driver.quit()
print("Links collected:", len(product_links1))

product_links2 = product_links1

for i in range(0,200):
    product_links2[i] = 'https://www.myntra.com/'+ product_links2[i]
    
headers = {'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36'}


productlinks = []
productlinks = product_links2

data= [('name', 'category', 'user_rating')]

for i in range(50, 100):
    s = requests.Session()
    res = s.get(productlinks[i], headers=headers)
    soup = BeautifulSoup(res.text,"lxml")
    script = None
    for s in soup.find_all(script):
        if 'pdpData' in s.text:
            script = s.get_text(strip=True)
            break
        
    a = json.loads(script[script.index('{'):])
    productname = (a['pdpData'])['name']
    productcategory = 'sneakers'
    if 'averageRating' not in ((a['pdpData'])['ratings']):
        productrating = 'Not Rated'
    else:
        productrating = ((a['pdpData'])['ratings'])['averageRating']
        
    data.append((productname, productcategory, productrating))
    

    
print('product_data is being stored in product_data.csv file. Please wait....')
f = open('product_data.csv', 'w+', newline ='')
with f:   
    write = csv.writer(f)
    write.writerows(data)
