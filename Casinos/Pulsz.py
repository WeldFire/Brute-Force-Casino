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


class Pulsz:

    CONFIGURATION =  None

    def __init__(self, CONFIGURATION):
        print("Pulsz initializing...")
        self.CONFIGURATION = CONFIGURATION

    def testPulszClaim(self):
        print("Running Pulsz claim function...")
        print(self.CONFIGURATION)


    async def getPulszSCBalance(page):
        print("TODO getPulszSCBalance SEEMS BROKEN!")
        return -1
        # return await page.evaluate('document.querySelector("[data-test=\"header-sweepstakes-value\"]").innerText')

    async def claimPulsz(self):
        name = CasinoEnum.PULSZ.value
        base_path = "imgs/pulsz/"
        # Use the functions
        browser, page = await start_browser("https://www.pulsz.com/login")
        time.sleep(3) # Login screen appears then goes away, need to convert this to the new method....
        location = wait_for_image(base_path+"login.png", 20)
        email_location = find_image(base_path+"email.png")
        pass_location = find_image(base_path+"pass.png")
        if location:
            click_location(pass_location)
            pyautogui.typewrite(self.CONFIGURATION[name][CONFIG_PASSWORD])
            click_location(email_location)
            pyautogui.typewrite(self.CONFIGURATION[name][CONFIG_USERNAME])
            click_location(location)
            
            # document.querySelector("").value = '';
            # document.querySelector("button[id='login_submit-button']").click(); //Error???
        else:
            print("Doesn't look like we needed to log in")
        
        time.sleep(1)
        
        claim_img_path = base_path+"claim.png"
        noclaim_img_path = base_path+"noclaim.png"
        loaded_location, loaded_image = wait_for_any_image_to_exist([claim_img_path, noclaim_img_path], 50)
        
        if(loaded_image is claim_img_path):
            if CONFIG_HEALTH_RUN in self.CONFIGURATION:
                ping(self.CONFIGURATION[CONFIG_HEALTH_RUN])
            else:
                logging.warn(f"No health check run url defined for {name}")

            click_location(loaded_location)

            if CONFIG_HEALTH_CLAIM in self.CONFIGURATION:
                ping(self.CONFIGURATION[CONFIG_HEALTH_CLAIM])
            else:
                logging.warn(f"No health check claim url defined for {name}")
            balance = await self.getPulszSCBalance(page)
            print(f"Current Pulsz Balance is {balance}")
        elif(loaded_image is noclaim_img_path):
            print(f"No claim available right now!")

            if CONFIG_HEALTH_RUN in self.CONFIGURATION:
                ping(self.CONFIGURATION[CONFIG_HEALTH_RUN])
            else:
                logging.warn(f"No health check run url defined for {name}")

            balance = await self.getPulszSCBalance(page)
            print(f"Current Pulsz Balance is {balance}")
        else:
            # take a screenshot of the entire screen
            screenshot_name = "pulsz_login_fail.png"
            pyautogui.screenshot(screenshot_name)
            print(f"Unable to login!! Screen saved to {screenshot_name}")
            
        # await browser.close()