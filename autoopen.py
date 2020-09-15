
from selenium import webdriver 
import datetime
import time
from selenium.webdriver.common.keys import Keys
import schedule
import json
import os
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys



def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.dirname(__file__)
    return os.path.join(base_path, relative_path)


def job():
    # create webdriver object 

    driver = webdriver.Chrome(resource_path('./driver/chromedriver.exe'))
    actions = ActionChains(driver)

    # get google.co.in 
    with open('cred.json') as f:
        cred = json.load(f)
    driver.get("https://login.gitam.edu/") 
    id = driver.find_element_by_id("txtusername") 
    password = driver.find_element_by_id("password")
    id.send_keys(cred['id']) 
    password.send_keys(cred['password'])
    driver.find_element_by_id("Submit").click()
    driver.get("https://login.gitam.edu/route.aspx?id=GLEARN&type=S")

    table=driver.find_element_by_id("ContentPlaceHolder1_GridViewonline")
    row_count=len(table.find_elements_by_tag_name("tr"))+1
    rData = []
    for i in range(row_count):
        row = table.find_elements_by_xpath("//tr["+str(i)+"]/td/a/div/h6")
        
        for webElement in row :
            rData.append(webElement.text)
    currentClassRow=None
    for count,data in enumerate(rData):
        date_time_obj = datetime.datetime.strptime(data[7:18], '%d-%b-%Y')
        if date_time_obj.date()==datetime.date.today():
            currentHour=datetime.datetime.today().hour
            print(currentHour,int(data[27:29]))
            if currentHour%12==int(data[27:29]):
                currentClassRow=count
    print(currentClassRow)
    print(rData)
    #test 
    if currentClassRow==None:
        pass
    else:
        zoomLink=table.find_elements_by_xpath("//tr["+str(currentClassRow+1)+"]/td/a")[0].get_attribute('href')
        actions.send_keys(Keys.LEFT_CONTROL + 't')
        actions.perform()
        driver.get(zoomLink)
        time.sleep(1)
        actions.send_keys(Keys.ARROW_LEFT)
        actions.send_keys(Keys.RETURN)
        actions.perform()






schedule.every().hour.at(":00").do(job)
job()
while True:
    currentHour=datetime.datetime.today().hour
    if currentHour==4:
        print("terminating  Job .........")
        break
    schedule.run_pending()
    time.sleep(1)