import pyautogui
import logging
import time

from Helpers.BrowserHelpers import start_browser
from Helpers.BrowserHelpers import find_image
from Helpers.BrowserHelpers import wait_for_image
from Helpers.BrowserHelpers import click_location
from Helpers.BrowserHelpers import ping
from Helpers.BrowserHelpers import click_point
from Helpers.BrowserHelpers import wait_for_any_image_to_exist

from Configuration import CONFIG_USERNAME
from Configuration import CONFIG_PASSWORD
from Configuration import CONFIG_HEALTH_RUN
from Configuration import CONFIG_HEALTH_CLAIM

from enums.CasinoEnum import CasinoEnum

from time import sleep
from selenium import webdriver 
from selenium.webdriver.chrome.options import Options 
from selenium.webdriver.common.by import By


class Chumba:

    CONFIGURATION =  None

    def __init__(self, CONFIGURATION):
        print("Chumba initializing...")
        self.CONFIGURATION = CONFIGURATION

    def testChumbaClaim(self):
        print("Running Chumba claim function...")
        print(self.CONFIGURATION)

    async def getChumbaSCBalance(page):
        print("TODO getChumbaSCBalance SEEMS BROKEN!")
        return -1
        # return await page.evaluate('document.querySelector("div.counter.counter--SC").innerText')    

    async def claimChumba(self):
        name = CasinoEnum.CHUMBA.value
        base_path = "imgs/chumba/"
        # Use the functions
        browser, page = await start_browser("https://login.chumbacasino.com/")
        location = wait_for_image(base_path+"login.png", 50)
        email_location = find_image(base_path+"email.png")
        pass_location = find_image(base_path+"pass.png")
        if location:
            click_location(pass_location)
            #pyautogui.typewrite(self.CONFIGURATION[name][CONFIG_PASSWORD])
            pyautogui.typewrite(self.CONFIGURATION[CONFIG_PASSWORD])
            click_location(email_location)
            #pyautogui.typewrite(self.CONFIGURATION[name][CONFIG_USERNAME])
            pyautogui.typewrite(self.CONFIGURATION[CONFIG_USERNAME])
            click_location(location)
            
            claim_img_path = base_path+"claim2.png"
            noclaim_img_path = base_path+"noclaim.png"
            time.sleep(6)
            loaded_location, loaded_image = wait_for_any_image_to_exist([claim_img_path, noclaim_img_path], 50)
            
            
            if(loaded_image is claim_img_path):
                if CONFIG_HEALTH_RUN in self.CONFIGURATION:
                    ping(self.CONFIGURATION[CONFIG_HEALTH_RUN])
                else:
                    logging.warn(f"No health check run url defined for {name}")
                #Adjust for looking at the close button
                click_point(loaded_location.left+(loaded_location.width/2), loaded_location.top+(loaded_location.height/2))
                if CONFIG_HEALTH_CLAIM in self.CONFIGURATION:
                    ping(self.CONFIGURATION[CONFIG_HEALTH_CLAIM])
                else:
                    logging.warn(f"No health check claim url defined for {name}")
                balance = await self.getChumbaSCBalance(page)
                print(f"Current Chumba Balance is {balance}")
            elif(loaded_image is noclaim_img_path):
                print(f"No claim available right now!")
                if CONFIG_HEALTH_RUN in self.CONFIGURATION:
                    ping(self.CONFIGURATION[CONFIG_HEALTH_RUN])
                else:
                    logging.warn(f"No health check run url defined for {name}")
                #balance = await self.getChumbaSCBalance(page)
                #print(f"Current Chumba Balance is {balance}")
            else:
                # take a screenshot of the entire screen
                screenshot_name = "chumba_login_fail.png"
                pyautogui.screenshot(screenshot_name)
                print(f"Unable to login!! Screen saved to {screenshot_name}")
            
            # document.querySelector("").value = '';
            # document.querySelector("button[id='login_submit-button']").click(); //Error???
        else:
            print("ERROR Wasn't able to start up!! (Browser not on the main window?)")
            
        await browser.close()    

    async def claimChumba2(self):
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
        
        # getting GeekForGeeks webpage 
        driver.get('https://lobby.chumbacasino.com/')

        sleep(5)
        
        #Get username field
        XPATH_username='//*[@id="login_email-input"]'

        #get password field
        XPATH_password='//*[@id="login_password-input"]'

        #Fill in username
        driver.find_element(By.XPATH,XPATH_username).send_keys(self.CONFIGURATION[CONFIG_USERNAME])
        sleep(2)

        #Fill in password
        driver.find_element(By.XPATH,XPATH_password).send_keys(self.CONFIGURATION[CONFIG_PASSWORD])
        sleep(2)

        #Click to login
        button = '//*[@id="login_submit-button"]'
        driver.find_element(By.XPATH,button).click()
        sleep(5)

        #TODO: upon login in a new browser / incognito mode chumba asks to verify ID via SMS or Email... maybe need to find a way to intercept this


        #get current value, to compare later to make sure we actually claimed - otherwise send email / error that claim did not happen
        current_balance = driver.find_element(By.XPATH, '//*[@id="top-hud__currency-bar__sweeps-currency-amount"]/div/span/span').text

        #click claim button coins
        button = '//*[@id="daily-bonus__claim-btn"]'
        driver.find_element(By.XPATH,button).click()
        sleep(3)

        
        new_balance = driver.find_element(By.XPATH, '//*[@id="top-hud__currency-bar__sweeps-currency-amount"]/div/span/span').text


        if(current_balance == new_balance):
            print('Error claiming - old value and new value are the same')
            #TODO: send email or something

        
        # close browser after our manipulations 
        #driver.close() 