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

class FortuneCoins:

    CONFIGURATION =  None

    def __init__(self, CONFIGURATION):
        print("Fortune Coins initializing...")
        self.CONFIGURATION = CONFIGURATION

    def testFortuneCoinsClaim(self):
        print("Running Fortune Coins claim function...")
        print(self.CONFIGURATION)


    async def getFortuneCoinsSCBalance(page):
        print("TODO getFortuneCoinsSCBalance DISABLED FOR NOW")
        return -1
        # return await page.evaluate('document.querySelector("#headlessui-menu-button-1").innerText.split("\n")[0]')

    async def claimFortuneCoins(self):
        name = CasinoEnum.FORTUNECOINS.value
        base_path = "imgs/fortune/"
        # Use the functions
        browser, page = await start_browser("https://www.fortunecoins.com/")
        start_login_location = wait_for_image(base_path+"start-login.png", 20)
        
        if start_login_location:
            print("Looks like we need to login to fortune coins!")
            click_location(start_login_location)
            login_button_location = wait_for_image(base_path+"login.png", 20, 0.1, 0.8)
            email_location = wait_for_image(base_path+"email.png", 20, 0.1, 0.99)
            pass_location = wait_for_image(base_path+"pass.png", 20, 0.1, 0.99)
            if login_button_location:
                click_location(pass_location)
                
                pyautogui.typewrite(self.CONFIGURATION[CONFIG_PASSWORD])
                click_location(email_location)
                pyautogui.typewrite(self.CONFIGURATION[CONFIG_USERNAME])
                location = wait_for_image(base_path+"login.png", 20, 0.1, 0.8)
                click_location(location)
                
                # document.querySelector("").value = '';
                # document.querySelector("button[id='login_submit-button']").click(); //Error???
            else:
                print("We can't login to fortune coins for some reason :(")
                screenshot_name = "fortunecoins_login_fail.png"
                pyautogui.screenshot(screenshot_name)
                print(f"Unable to login!! Screen saved to {screenshot_name}")
                return
        else:
            print("Looks like we are already logged in to fortune coins!")

        claim_img_path = base_path+"claim.png"
        noclaim_img_path = base_path+"noclaim.png"
        loaded_location, loaded_image = wait_for_any_image_to_exist([claim_img_path, noclaim_img_path], 50)

        # Get the latest page object
        # page = (await browser.pages())[-1]

        if(loaded_image is claim_img_path):
            if CONFIG_HEALTH_RUN in self.CONFIGURATION:
                ping(self.CONFIGURATION[CONFIG_HEALTH_RUN])
            else:
                logging.warn(f"No health check run url defined for {name}")

            #Adjust for looking at the close button
            # click_point(loaded_location.left+(loaded_location.width/2), loaded_location.top-45+(loaded_location.height/2))
            click_location(loaded_location)
            # confirm = wait_for_image(base_path+"confirm-claim.png", 20)
            # if(confirm):
            #     click_location(confirm)    
                
            #     claimed = wait_for_image(base_path+"claimed.png", 20)
            #     if(claimed):

            if CONFIG_HEALTH_CLAIM in self.CONFIGURATION:
                ping(self.CONFIGURATION[CONFIG_HEALTH_CLAIM])
            else:
                logging.warn(f"No health check claim url defined for {name}")

            balance = await self.getFortuneCoinsSCBalance(page)
            print(f"Current fortune coins Balance is {balance}")
            #     else:
            #         screenshot_name = "fortunecoins_second_confirm_claim_fail.png"
            #         pyautogui.screenshot(screenshot_name)
            #         print(f"Unable to confirm claim!! Screen saved to {screenshot_name}")
            # else:
            #     screenshot_name = "fortunecoins_confirm_claim_fail.png"
            #     pyautogui.screenshot(screenshot_name)
            #     print(f"Unable to confirm claim!! Screen saved to {screenshot_name}")
                
        elif(loaded_image is noclaim_img_path):
            print(f"No claim available right now!")

            if CONFIG_HEALTH_RUN in self.CONFIGURATION:
                ping(self.CONFIGURATION[CONFIG_HEALTH_RUN])
            else:
                logging.warn(f"No health check run url defined for {name}")

            balance = await self.getFortuneCoinsSCBalance(page)
            print(f"Current fortune coins Balance is {balance}")
        else:
            # take a screenshot of the entire screen
            screenshot_name = "fortunecoins_claim_fail.png"
            pyautogui.screenshot(screenshot_name)
            print(f"Unable to claim!! Screen saved to {screenshot_name}")
        
            
        # await browser.close()