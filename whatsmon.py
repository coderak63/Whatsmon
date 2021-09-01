import sys
sys.path.append("library/selenium")
sys.path.append("library/PIL")
sys.path.append("library/playsound")
from selenium import webdriver
from time import strftime,sleep
import datetime
from PIL import Image
import os
from playsound import playsound

from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import NoSuchElementException

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


from selenium.webdriver.common.keys import Keys  
from selenium.webdriver.chrome.options import Options  


chrome_options = Options()  
chrome_options.add_argument("--headless")  
chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3641.0 Safari/537.36") 


logo = """
***************************************************************************************
***************************************************************************************
$$\\      $$\\ $$\\                  $$\\               $$\\      $$\\                     
$$ | $\\  $$ |$$ |                 $$ |              $$$\\    $$$ |                    
$$ |$$$\\ $$ |$$$$$$$\\   $$$$$$\\ $$$$$$\\    $$$$$$$\\ $$$$\\  $$$$ | $$$$$$\\  $$$$$$$\\  
$$ $$ $$\\$$ |$$  __$$\\  \\____$$\\ _$$  _|  $$  _____|$$\\$$\\$$ $$ |$$  __$$\\ $$  __$$\\ 
$$$$  _$$$$ |$$ |  $$ | $$$$$$$ | $$ |    \\$$$$$$\\  $$ \\$$$  $$ |$$ /  $$ |$$ |  $$ |
$$$  / \\$$$ |$$ |  $$ |$$  __$$ | $$ |$$\\  \\____$$\\ $$ |\\$  /$$ |$$ |  $$ |$$ |  $$ |
$$  /   \\$$ |$$ |  $$ |\\$$$$$$$ | \\$$$$  |$$$$$$$  |$$ | \\_/ $$ |\\$$$$$$  |$$ |  $$ |
\\__/     \\__|\\__|  \\__| \\_______|  \\____/ \\_______/ \\__|     \\__| \\______/ \\__|  \\__|
***************************************************************************************
"""
print(logo)


print("Starting whatsMon.....")
driver = webdriver.Chrome(executable_path=r'chrome\\chromedriver.exe',options=chrome_options)
print("Generating QR Code.....")
driver.get("http://web.whatsapp.com")
"""
driver.save_screenshot('a.png')
print("saved screenshot")
"""


sleep(15)
qr_div = driver.find_element_by_xpath('/html/body/div[1]/div/div/div[2]/div[1]/div/div[2]/div').get_attribute('data-ref')
with open('QR\\qr_code.png', 'wb') as file:
    file.write(driver.find_element_by_xpath('/html/body/div[1]/div/div/div[2]/div[1]/div/div[2]/div/canvas').screenshot_as_png)   
image = Image.open('QR\\qr_code.png')
print("!!! QR code genereted successfully !!!")
image.show()


while True:
    try:
        qr_div2 = driver.find_element_by_xpath('/html/body/div[1]/div/div/div[2]/div[1]/div/div[2]/div').get_attribute('data-ref')
        if(qr_div2!=qr_div):
            qr_div=qr_div2
            with open('QR\\qr_code.png', 'wb') as file:
                file.write(driver.find_element_by_xpath('/html/body/div[1]/div/div/div[2]/div[1]/div/div[2]/div/canvas').screenshot_as_png)   
            image = Image.open('QR\\qr_code.png')
            print("!!! QR code genereted successfully !!!")
            image.show()
        sleep(1)
    except (NoSuchElementException, StaleElementReferenceException):
        os.system("taskkill /f /im Microsoft.Photos.exe")
        print("!!! Scan successful !!!\nLoging in.....")
        break


sleep(5)

chat = driver.find_element_by_xpath("/html/body/div[1]/div/div/div[3]/div/header/div[2]/div/span/div[2]/div")
chat.click()
sleep(2)

search = driver.find_element_by_xpath("/html/body/div[1]/div/div/div[2]/div[1]/span/div/span/div/div[1]/div/label/div/div[2]")
search.click()
sleep(2)

name = input("Please Enter exact Contact name saved in your Phone: ")
search.send_keys(name)
sleep(2)

print("Search Successful")

op = driver.find_element_by_xpath("/html/body/div[1]/div/div/div[2]/div[1]/span/div/span/div/div[2]/div[1]/div/div/div[2]/div/div")
op.click()
sleep(10)

name = driver.find_element_by_xpath("/html/body/div[1]/div/div/div[4]/div/header/div[2]/div[1]/div/span").text

print(".....Now tracking is live.....")
print("Name :  "+name)
print()
f=open('status_data\\'+name+'.txt','a+')
f.write("\nNew scannings, Date: "+str(datetime.datetime.today().strftime('%d/%m/%Y'))+"\n\n")
f.close()


while True:
    i=0
    try:
        status = driver.find_element_by_xpath('/html/body/div[1]/div/div/div[4]/div/header/div[2]/div[2]/span').text
        if(status=='online'):
            print(str(datetime.datetime.now())+" : "+status)
            f=open('status_data\\'+name+'.txt','a+')
            f.write(str(datetime.datetime.now())+" : "+status+"\n")
            f.close()
            playsound('sound\\alert.mp3')
        else:
            print(str(datetime.datetime.now())+" : "+"offline")
            f=open('status_data\\'+name+'.txt','a+')
            f.write(str(datetime.datetime.now())+" : "+"offline\n")
            f.close()
        i=1
    except (NoSuchElementException, StaleElementReferenceException):
        status = 'offline'
        print(str(datetime.datetime.now())+" : "+status)
        f=open('status_data\\'+name+'.txt','a+')
        f.write(str(datetime.datetime.now())+" : "+status+"\n")
        f.close()
        i=0
    
    
    
    while True:
        if i == 1:
            try:
                re_status = driver.find_element_by_xpath('/html/body/div[1]/div/div/div[4]/div/header/div[2]/div[2]/span').text
                if(status==re_status):
                    continue
                else:
                    break
            except (NoSuchElementException, StaleElementReferenceException):
                re_status = 'offline'
                break
        else:
            try:
                driver.find_element_by_xpath('/html/body/div[1]/div/div/div[4]/div/header/div[2]/div[2]/span').text
                break
            except (NoSuchElementException, StaleElementReferenceException):
                re_status = 'offline'
                continue
    sleep(1)

