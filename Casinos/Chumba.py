import pyautogui
import logging

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
            
            claim_img_path = base_path+"claim.png"
            noclaim_img_path = base_path+"noclaim.png"
            loaded_location, loaded_image = wait_for_any_image_to_exist([claim_img_path, noclaim_img_path], 50)
            
            
            if(loaded_image is claim_img_path):
                if CONFIG_HEALTH_RUN in self.CONFIGURATION:
                    ping(self.CONFIGURATION[CONFIG_HEALTH_RUN])
                else:
                    logging.warn(f"No health check run url defined for {name}")
                #Adjust for looking at the close button
                click_point(loaded_location.left+(loaded_location.width/2), loaded_location.top-45+(loaded_location.height/2))
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
                balance = await self.getChumbaSCBalance(page)
                print(f"Current Chumba Balance is {balance}")
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