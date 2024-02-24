from Casinos.Casnio import Casino
from Configuration import CONFIG_USERNAME
from Configuration import CONFIG_PASSWORD
from Configuration import CONFIG_HEALTH_RUN
from Configuration import CONFIG_HEALTH_CLAIM

from enums.CasinoEnum import CasinoEnum

from time import sleep
from selenium import webdriver 
from selenium.webdriver.chrome.options import Options 
from selenium.webdriver.common.by import By




class GlobalPoker(Casino):

    CONFIGURATION =  None

    def __init__(self, CONFIGURATION):
        print("Global Poker Initializing...")
        super().__init__(CONFIGURATION)


    async def claim(self):
        # instance of Options class allows 
        # us to configure Headless Chrome 
        options = webdriver.ChromeOptions()

        #if chrome is headless or not
        #options.add_argument('--headless')

        #keep chrome browser open
        options.add_experimental_option("detach", True)
        
        # this parameter tells Chrome that 
        # it should be run without UI (Headless) 
        options.headless = True
        
        # initializing webdriver for Chrome with our options 
        driver = webdriver.Chrome(options=options) 
        
        # getting global poker webpage 
        driver.get('https://play.globalpoker.com/')

        sleep(5)

        XPATH_username='//*[@id="1-email"]'
        XPATH_password='//*[@id="auth0-lock-container-1"]/div/div[2]/form/div/div/div/div[2]/div[2]/span/div/div/div/div/div/div/div/div/div[2]/div[3]/div[2]/div/div/input'
        driver.find_element(By.XPATH,XPATH_username).send_keys(self.CONFIGURATION[CONFIG_USERNAME])
        sleep(2)

        driver.find_element(By.XPATH,XPATH_password).send_keys(self.CONFIGURATION[CONFIG_PASSWORD])
        sleep(2)

        button = '//*[@id="auth0-lock-container-1"]/div/div[2]/form/div/div/div/button'
        driver.find_element(By.XPATH,button).click()
        sleep(5)


        #get current value, to compare later to make sure we actually claimed - otherwise send email / error that claim did not happen
        current_balance = driver.find_element(By.XPATH, '//*[@id="sc-balance-display"]/div/div/span[2]').text

        #click get coins
        button = '//*[@id="cashier-button"]'
        driver.find_element(By.XPATH,button).click()
        sleep(3)


        #Click all 7 tiles so we don't have to "guess" or keep track of which one is active
        for i in range(7):
            tile = '//*[@id="daily-bonus-'+str(i+1)+'"]'
            driver.find_element(By.XPATH,tile).click()
            sleep(1)

        
        new_balance = driver.find_element(By.XPATH, '//*[@id="sc-balance-display"]/div/div/span[2]').text


        if(current_balance == new_balance):
            print('Error claiming - old value and new value are the same')
            #TODO: send email or something
        
        # close browser after our manipulations 
        #driver.close() 