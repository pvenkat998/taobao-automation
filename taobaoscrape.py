import urllib
from selenium import webdriver
import os
import requests
import hashlib
import io
from PIL import Image
from selenium.webdriver.support.ui import WebDriverWait
import pandas as pd 
brandname="brand abc"
itemname="item bbb"
def search_and_download():
    target_folder=os.path.join(brandname,itemname)
    if not os.path.exists(brandname):
        os.makedirs(brandname)    
    if not os.path.exists(target_folder):
        os.makedirs(target_folder)
    
    for elem in src:
        persist_image(target_folder,elem)

def persist_image(folder_path:str,url:str):
    try:
        image_content = requests.get(url).content

    except Exception as e:
        print(f"ERROR - Could not download {url} - {e}")
        print(1)

    try:
        image_file = io.BytesIO(image_content)
        image = Image.open(image_file).convert('RGB')
        file_path = os.path.join(folder_path,hashlib.sha1(image_content).hexdigest()[:10] + '.jpg')
        with open(file_path, 'wb') as f:
            image.save(f, "JPEG", quality=85)
        print(f"SUCCESS - saved {url} - as {file_path}")
    except Exception as e:
        print(2)
        print(f"ERROR - Could not save {url} - {e}")
data = pd.read_csv("input.csv")
data.head()
for i in range(len(data['url'])):
    print(data['url'][i])
    print(data['brand'][i])

driver = webdriver.Chrome()
#driver.get('home/denjo/Downloads/sns_automation/chromedriver')
#driver.get('https://item.taobao.com/item.htm?id=589892452897') 
for i in range(len(data['url'])):
    print(data['url'][i])
    brandname=(data['brand'][i])
    driver.get(data['url'][i])
  #  driver.get('https://item.taobao.com/item.htm?spm=a312a.7700824.w4004-22612662286.2.5f519e83O0WkbL&id=608274915235')

    wait = WebDriverWait(driver, 10)

    try:
        driver.find_elements_by_xpath('//*[@id="sufei-dialog-close"]')[0].click()
    except:
        print("no login dialogue1 IMPORTANTTT _____________")
    try:
        driver.find_elements_by_xpath('//*[@id="sufei-dialog-close"]')[0].click()
    except:
        print("no login dialogue2 IMPORTANTTT _____________")
    itemname=driver.find_elements_by_class_name('tb-main-title')[0].get_attribute('innerHTML')

    try:
        driver.find_elements_by_xpath('//*[@id="J_UlThumb"]/li[2]/div')[0].click()
    except:
        print('gg IMPORTANTTT _____________')
    src=list()

    for x in range(15):
        try:
            driver.find_elements_by_xpath('//*[@id="J_TbViewerThumb-'+str(x)+'"]')[0].click()
        except:
            print('gg2')
        print(x)
        try:
            src.append(driver.find_elements_by_xpath('//*[@id="tb-viewer-panel-'+str(x)+'"]/a')[0].get_attribute("href"))
        except:
            print('fail')

    #get link video
    #vidsrc=driver.find_elements_by_xpath('/html/head/link[12]')[0].get_attribute('href')
    vidsrc=driver.find_element_by_css_selector("*[rel='alternate']").get_attribute('href')
    print(vidsrc)
    driver.get(vidsrc)
    x=1
    while(x==1):
        try:
            driver.find_elements_by_xpath('/html/body/div[3]/div[1]/div[1]/div[1]/div[1]/img')[0].click()
            vidlnk=driver.find_elements_by_xpath('//*[@id="videoTag"]')[0].get_attribute('src') 
            print(vidlnk)
            x=0
        except:
            element = WebDriverWait(driver, 10)
            print("uh oh")
    #download image
    search_and_download()
    #download vid
    target_folder=os.path.join(brandname,itemname)
    urllib.request.urlretrieve(vidlnk, os.path.join(target_folder,'videoname.mp4'))
driver.quit() 