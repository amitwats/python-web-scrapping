import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import csv

CSV_FILE_NAME="file.csv"
URL='https://clutch.co/au/it-services/analytics'


# Once a page is opened
# gets all information from that page and writes it to the
# CSV file
def ProcessPage(driver):
    soup=BeautifulSoup(driver.page_source,"html.parser")
    cmpny_rows=soup.find_all('li', class_ = 'provider provider-row')
    with open(CSV_FILE_NAME,'a') as csv_file:
        csv_writer=csv.writer(csv_file)

        for cmpny_row in cmpny_rows:
            cmpny=cmpny_row.find('div', class_ = 'provider-info col-md-10')
            name=cmpny.div.div.h3.a.getText()
            tagline= cmpny.div.p.getText() 
            percentWork=cmpny.find('div',{'class':'chart-label hidden-xs'}).span.getText()
            peopleCount=cmpny.find('div',{'class':"col-md-3 provider-info__details"}).div.find_all('div')[2].span.getText()
            location=cmpny.find('div',{'class':"col-md-3 provider-info__details"}).div.find_all('div')[3].span.getText()
            url=cmpny_row.find('a', class_ = 'website-link__item')['href']
            csv_writer.writerow([name,tagline,percentWork,peopleCount,location,url])
            # review=cmpny_row.find('div', {'class':'rating-reviews'} ).span.getText()
    csv_file.close()

def main():
    driver = webdriver.Firefox()
    driver.implicitly_wait(30)
    driver.get(URL)

    #Header of the CSV file
    with open(CSV_FILE_NAME,'a') as csv_file:
        csv_writer=csv.writer(csv_file)
        csv_writer.writerow(["Company Name","Tagline","% - DS work","People Count",'Location','URL'])
    csv_file.close()

    # Loop through until the Next button stops appearing
    # The next button stops appearing on the last page
    while True:
        
        # If acknowledgement box present close it(by accepting cookies)
        # if this is not done it forms layer on top of the Navigation button
        # and prevents clicks
        try:
            cookie_btn=driver.find_element(By.ID, 'CybotCookiebotDialogBodyButtonAccept')#closing cookie reminder box
            cookie_btn.click()
        except:
            pass

        driver.implicitly_wait(30)
        

        ProcessPage(driver)
        next_button_list=[btn for btn in driver.find_elements(By.CLASS_NAME, 'page-link') if btn.text=="next"]
        if len(next_button_list)>0: # The next button exists and more pages can be traversed
            driver.implicitly_wait(30)
            next_button_list[0].click()
        else: # The next button does not exists and no more pages can be traversed
            break
    
    driver.close()



if __name__=="__main__" :
    main()

