import pyautogui
import time
import pytesseract
import subprocess
from pyppeteer import connect, launch
import asyncio
import requests
import logging
import re
from apscheduler.schedulers.background import BackgroundScheduler
from utils import get_active_window_title
from enum import Enum
import json
    
class RunSchedule(Enum):
  SixHours = 6
  EveryHour = 1
  All = 0


CONFIG_USERNAME="username"
CONFIG_PASSWORD="password"
CONFIG_HEALTH_RUN="health_check_successful_run"
CONFIG_HEALTH_CLAIM="health_check_successful_claim"

# logging.basicConfig(level=logging.DEBUG)
logging = logging.getLogger(__name__)


# browser_path = r'C:\\Program Files\\BraveSoftware\\Brave-Browser\\Application\\brave.exe'
# browser_title_fragment = " - Brave"
browser_path = r'C:\Users\Administrator\AppData\Local\Programs\Opera GX\launcher.exe'
browser_title_fragment = " - Opera"

# pytesseract.pytesseract.tesseract_cmd = r'<path_to_your_tesseract_executable>'

class MockBrowser:
    async def close(self):
        windowTitle = get_active_window_title()
        print("Browser Close Called! Title - " + windowTitle)
        
        if(browser_title_fragment in windowTitle):
            # pyautogui.hotkey('ctrl', 'w') # Close the tab
            pyautogui.hotkey('alt', 'f4')


async def start_browser(url):
    subprocess.Popen([browser_path, "--remote-debugging-port=9322", url], shell=True)
    # controlled_id=run_app([browser_path, "--remote-debugging-port=9322", url], True)
    # browser = await connect(browserURL='http://localhost:9322', defaultViewport={'width': 1366,'height': 768})
    # page = (await browser.pages())[-1]
    browser = MockBrowser()
    page = None
    return browser, page

def wait_for_any_image_to_exist(img_paths, max_tries=-1, delay=0.1):
    found_location = None
    found_image = None
    while max_tries != 0:
        for img_path in img_paths:
            location = find_image(img_path)
            
            if(location):
                return location, img_path
            
            time.sleep(delay)
            max_tries = max_tries - 1

    return found_location, found_image
    
def wait_for_image(img_path, max_tries=-1, delay=0.1, confidence=0.9):
    found_location = None
    while max_tries != 0:
        location = find_image(img_path, confidence)
        
        if(location):
            found_location = location
            break
        
        time.sleep(delay)
        max_tries = max_tries - 1

    return found_location

def click_location(location):
    x, y = location_to_point(location)
    click_point(x, y)

def location_to_point(location):
    x = location.left + (location.width/2)
    y = location.top + (location.height/2)
    return x, y

def click_point(x, y):
    pyautogui.moveTo(x, y)

    # Performs a left mouse click at the current mouse location
    pyautogui.click()


def find_image(image_file_path, confidence=0.9, minSearchTime=0):
    # Use image recognition to locate elements on the page
    location = pyautogui.locateOnScreen(image_file_path, minSearchTime, confidence=confidence)
    if location:
        print(f"Location of the image is: {location}")
    # else:
    #     print("Image not found!")
    return location

def read_text_from_location(location):
    # Use OCR to read text from images on the page
    im = pyautogui.screenshot(region=(location[0], location[1], location[2], location[3]))
    text = pytesseract.image_to_string(im)
    return text

def ping(url):
    try:
        requests.get(url, timeout=10)
    except requests.RequestException as e:
        # Log ping failure here...
        print("Ping failed: %s" % e)

async def getChumbaSCBalance(page):
    print("TODO getChumbaSCBalance SEEMS BROKEN!")
    return -1
    # return await page.evaluate('document.querySelector("div.counter.counter--SC").innerText')

async def claimChumba():
    name = "Chumba"
    base_path = "imgs/chumba/"
    # Use the functions
    browser, page = await start_browser("https://login.chumbacasino.com/")
    location = wait_for_image(base_path+"login.png", 50)
    email_location = find_image(base_path+"email.png")
    pass_location = find_image(base_path+"pass.png")
    if location:
        click_location(pass_location)
        pyautogui.typewrite(CONFIGURATION[name][CONFIG_PASSWORD])
        click_location(email_location)
        pyautogui.typewrite(CONFIGURATION[name][CONFIG_USERNAME])
        click_location(location)
        
        claim_img_path = base_path+"claim.png"
        noclaim_img_path = base_path+"noclaim.png"
        loaded_location, loaded_image = wait_for_any_image_to_exist([claim_img_path, noclaim_img_path], 50)
        
        
        if(loaded_image is claim_img_path):
            ping(CONFIGURATION[name][CONFIG_HEALTH_RUN])
            #Adjust for looking at the close button
            click_point(loaded_location.left+(loaded_location.width/2), loaded_location.top-45+(loaded_location.height/2))
            ping(CONFIGURATION[name][CONFIG_HEALTH_CLAIM])
            balance = await getChumbaSCBalance(page)
            print(f"Current Chumba Balance is {balance}")
        elif(loaded_image is noclaim_img_path):
            print(f"No claim available right now!")
            ping(CONFIGURATION[name][CONFIG_HEALTH_RUN])
            balance = await getChumbaSCBalance(page)
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


async def getPulszSCBalance(page):
    print("TODO getPulszSCBalance SEEMS BROKEN!")
    return -1
    # return await page.evaluate('document.querySelector("[data-test=\"header-sweepstakes-value\"]").innerText')

async def claimPulsz():
    name = "Pulsz"
    base_path = "imgs/pulsz/"
    # Use the functions
    browser, page = await start_browser("https://www.pulsz.com/login")
    time.sleep(3) # Login screen appears then goes away, need to convert this to the new method....
    location = wait_for_image(base_path+"login.png", 20)
    email_location = find_image(base_path+"email.png")
    pass_location = find_image(base_path+"pass.png")
    if location:
        click_location(pass_location)
        pyautogui.typewrite(CONFIGURATION[name][CONFIG_PASSWORD])
        click_location(email_location)
        pyautogui.typewrite(CONFIGURATION[name][CONFIG_USERNAME])
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
        ping(CONFIGURATION[name][CONFIG_HEALTH_RUN])
        click_location(loaded_location)
        ping(CONFIGURATION[name][CONFIG_HEALTH_CLAIM])
        balance = await getPulszSCBalance(page)
        print(f"Current Pulsz Balance is {balance}")
    elif(loaded_image is noclaim_img_path):
        print(f"No claim available right now!")
        ping(CONFIGURATION[name][CONFIG_HEALTH_RUN])
        balance = await getPulszSCBalance(page)
        print(f"Current Pulsz Balance is {balance}")
    else:
        # take a screenshot of the entire screen
        screenshot_name = "pulsz_login_fail.png"
        pyautogui.screenshot(screenshot_name)
        print(f"Unable to login!! Screen saved to {screenshot_name}")
        
    # await browser.close()

async def getChancedSCBalance(page):
    print("TODO getChancedSCBalance SEEMS BROKEN!")
    return -1
    # return await page.evaluate('document.querySelector("#headlessui-menu-button-1").innerText.split("\n")[0]')

async def navigateToChancedClaim(base_path, browser, page):
    # open_claim_model.png
    open_claim_model = wait_for_image(base_path+"open_claim_model.png")
    click_location(open_claim_model)
    
    # claim_model_open.png
    claim_model_open = wait_for_image(base_path+"claim_model_open.png")
    if not claim_model_open:
        return report_failure("Chanced Claim Navigation", f"chanced_claim_model_navigation_fail.png", f"Unable to ensure that the claim model was opened from the homepage!")
        
    # hourly_bonus_button.png
    hourly_bonus_button = wait_for_image(base_path+"hourly_bonus_button.png")
    click_location(hourly_bonus_button)
    
    # confirm_at_claim_page.png
    confirm_at_claim_page = wait_for_image(base_path+"confirm_at_claim_page.png")
    if not confirm_at_claim_page:
        return report_failure("Chanced Claim Navigation", f"chanced_claim_tab_navigation_fail.png", f"Unable to ensure that the claim model tab was switched correctly")
    
    # The numbers don't update immediately for some reason??
    time.sleep(3)
    
async def claimChancedV2():
    return await genericClaim(
            name="Chanced",
            base_path="imgs/chanced/",
            base_url="https://www.chanced.com",
            customNavigateToClaim=navigateToChancedClaim,
            claimAvailableClickOffset={'x':0, 'y':200}
        )

async def claimChanced():
    name = "Chanced"
    base_path = "imgs/chanced/"
    # Use the functions
    browser, page = await start_browser("https://www.chanced.com/?page=bonus^&tab=bank")
    location = wait_for_image(base_path+"login.png", 20, 0.1, 0.8)
    email_location = wait_for_image(base_path+"email.png", 20, 0.1, 0.8)
    pass_location = wait_for_image(base_path+"pass.png", 20, 0.1, 0.8)
    if location:
        click_location(pass_location)
        pyautogui.typewrite(CONFIGURATION[name][CONFIG_PASSWORD])
        click_location(email_location)
        pyautogui.typewrite(CONFIGURATION[name][CONFIG_USERNAME])
        location = wait_for_image(base_path+"login.png", 20, 0.1, 0.8)
        click_location(location)
        
        # document.querySelector("").value = '';
        # document.querySelector("button[id='login_submit-button']").click(); //Error???
    else:
        print("Doesn't look like we needed to log in")
    
    logged_in = wait_for_image(base_path+"logged-in.png", 20)
    if(logged_in):
        # await page.goto("https://www.chanced.com/affiliates/referred-users?page=bonus&tab=bank")
        # popup_img_path = base_path+"hourly-bonus-popup.png"
        
        # popup_location = wait_for_image(popup_img_path, 20)
        # if(popup_location):
        #     print("We can't claim hourly bonuses right now.... maybe one day")
        #     screenshot_name = "chanced_claim_hourly_bonus_popup_fail.png"
        #     pyautogui.screenshot(screenshot_name)
        #     print(f"Unable to login!! Screen saved to {screenshot_name}")
        #     return
        
        # time.sleep(3)
        
        claim_img_path = base_path+"claim.png"
        noclaim_img_path = base_path+"noclaim.png"
        loaded_location, loaded_image = wait_for_any_image_to_exist([claim_img_path, noclaim_img_path], 50)
        
        # Get the latest page object
        # page = (await browser.pages())[-1]
        
        if(loaded_image is claim_img_path):
            ping(CONFIGURATION[name][CONFIG_HEALTH_RUN])
            #Adjust for looking at the close button
            # click_point(loaded_location.left+(loaded_location.width/2), loaded_location.top-45+(loaded_location.height/2))
            click_location(loaded_location)
            confirm = wait_for_image(base_path+"confirm-claim.png", 20)
            if(confirm):
                click_location(confirm)    
                
                claimed = wait_for_image(base_path+"claimed.png", 20)
                if(claimed):
                    ping(CONFIGURATION[name][CONFIG_HEALTH_CLAIM])
                    balance = await getChancedSCBalance(page)
                    print(f"Current Chanced Balance is {balance}")
                else:
                    screenshot_name = "chanced_second_confirm_claim_fail.png"
                    pyautogui.screenshot(screenshot_name)
                    print(f"Unable to confirm claim!! Screen saved to {screenshot_name}")
            else:
                screenshot_name = "chanced_confirm_claim_fail.png"
                pyautogui.screenshot(screenshot_name)
                print(f"Unable to confirm claim!! Screen saved to {screenshot_name}")
                
        elif(loaded_image is noclaim_img_path):
            print(f"No claim available right now!")
            ping(CONFIGURATION[name][CONFIG_HEALTH_RUN])
            balance = await getChancedSCBalance(page)
            print(f"Current Chanced Balance is {balance}")
        else:
            # take a screenshot of the entire screen
            screenshot_name = "chanced_claim_fail.png"
            pyautogui.screenshot(screenshot_name)
            print(f"Unable to claim!! Screen saved to {screenshot_name}")
    else:
        # take a screenshot of the entire screen
        screenshot_name = "chanced_login_fail.png"
        pyautogui.screenshot(screenshot_name)
        print(f"Unable to login!! Screen saved to {screenshot_name}")
        
    # await browser.close()


async def getLuckylandSCBalance(page):
    print("TODO getLuckylandSCBalance DISABLED FOR NOW")
    return -1
    # return await page.evaluate('document.querySelector("#headlessui-menu-button-1").innerText.split("\n")[0]')

async def claimLuckylandslots():
    name = "Lucky Land"
    base_path = "imgs/luckyland/"
    # Use the functions
    browser, page = await start_browser("https://luckylandslots.com/loader")
    start_login_location = wait_for_image(base_path+"start-login.png", 20)
    
    if start_login_location:
        print("Looks like we need to login to lucky land!")
        click_location(start_login_location)
        login_button_location = wait_for_image(base_path+"login.png", 20, 0.1, 0.8)
        email_location = wait_for_image(base_path+"email.png", 20, 0.1, 0.8)
        pass_location = wait_for_image(base_path+"pass.png", 20, 0.1, 0.8)
        if login_button_location:
            click_location(pass_location)
            pyautogui.typewrite(CONFIGURATION[name][CONFIG_PASSWORD])
            click_location(email_location)
            pyautogui.typewrite(CONFIGURATION[name][CONFIG_USERNAME])
            location = wait_for_image(base_path+"login.png", 20, 0.1, 0.8)
            click_location(location)
            # document.querySelector("").value = '';
            # document.querySelector("button[id='login_submit-button']").click(); //Error???
        else:
            print("We can't login to lucky land for some reason :(")
            screenshot_name = "luckyland_login_fail.png"
            pyautogui.screenshot(screenshot_name)
            print(f"Unable to login!! Screen saved to {screenshot_name}")
            return
    else:
        print("Looks like we are already logged in to lucky land!")

    time.sleep(3) # Zzz don't like waiting this way, need to convert to other method
    
    claim_img_path = base_path+"claim.png"
    noclaim_img_path = base_path+"noclaim.png"
    loaded_location, loaded_image = wait_for_any_image_to_exist([claim_img_path, noclaim_img_path], 100)

    # Get the latest page object
    # page = (await browser.pages())[-1]

    if(loaded_image is claim_img_path):
        ping(CONFIGURATION[name][CONFIG_HEALTH_RUN])
        #Adjust for looking at the close button
        # click_point(loaded_location.left+(loaded_location.width/2), loaded_location.top-45+(loaded_location.height/2))
        click_location(loaded_location)
        # confirm = wait_for_image(base_path+"confirm-claim.png", 20)
        # if(confirm):
        #     click_location(confirm)    
            
        #     claimed = wait_for_image(base_path+"claimed.png", 20)
        #     if(claimed):
        ping(CONFIGURATION[name][CONFIG_HEALTH_CLAIM])
        balance = await getLuckylandSCBalance(page)
        print(f"Current lucky land Balance is {balance}")
        #     else:
        #         screenshot_name = "luckyland_second_confirm_claim_fail.png"
        #         pyautogui.screenshot(screenshot_name)
        #         print(f"Unable to confirm claim!! Screen saved to {screenshot_name}")
        # else:
        #     screenshot_name = "luckyland_confirm_claim_fail.png"
        #     pyautogui.screenshot(screenshot_name)
        #     print(f"Unable to confirm claim!! Screen saved to {screenshot_name}")
            
    elif(loaded_image is noclaim_img_path):
        print(f"No claim available right now!")
        ping(CONFIGURATION[name][CONFIG_HEALTH_RUN])
        balance = await getLuckylandSCBalance(page)
        print(f"Current luckyland Balance is {balance}")
    else:
        # take a screenshot of the entire screen
        screenshot_name = "luckyland_claim_fail.png"
        pyautogui.screenshot(screenshot_name)
        print(f"Unable to claim!! Screen saved to {screenshot_name}")
    
        
    # await browser.close()


async def getFortuneCoinsSCBalance(page):
    print("TODO getFortuneCoinsSCBalance DISABLED FOR NOW")
    return -1
    # return await page.evaluate('document.querySelector("#headlessui-menu-button-1").innerText.split("\n")[0]')

async def claimFortuneCoins():
    name = "Fortune Coins"
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
            
            pyautogui.typewrite(CONFIGURATION[name][CONFIG_PASSWORD])
            click_location(email_location)
            pyautogui.typewrite(CONFIGURATION[name][CONFIG_USERNAME])
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
        ping(CONFIGURATION[name][CONFIG_HEALTH_RUN])
        #Adjust for looking at the close button
        # click_point(loaded_location.left+(loaded_location.width/2), loaded_location.top-45+(loaded_location.height/2))
        click_location(loaded_location)
        # confirm = wait_for_image(base_path+"confirm-claim.png", 20)
        # if(confirm):
        #     click_location(confirm)    
            
        #     claimed = wait_for_image(base_path+"claimed.png", 20)
        #     if(claimed):
        ping(CONFIGURATION[name][CONFIG_HEALTH_CLAIM])
        balance = await getFortuneCoinsSCBalance(page)
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
        ping(CONFIGURATION[name][CONFIG_HEALTH_RUN])
        balance = await getFortuneCoinsSCBalance(page)
        print(f"Current fortune coins Balance is {balance}")
    else:
        # take a screenshot of the entire screen
        screenshot_name = "fortunecoins_claim_fail.png"
        pyautogui.screenshot(screenshot_name)
        print(f"Unable to claim!! Screen saved to {screenshot_name}")
    
        
    # await browser.close()

def load_configuration():
    # Open and load the JSON file
    with open('config.json', 'r') as file:
        map_var = json.load(file)
        
    # print(map_var)
    return map_var

def to_stub(s):
    s = s.lower() # make all characters lowercase
    s = re.sub(r'\W+', ' ', s) # replaces any non-alphanumeric character to a space
    s = s.replace(' ', '_') # replaces spaces with underscores
    return s

def report_failure(logging_prefix, screenshot_name, message):
    logging.error(f"{logging_prefix}{message}")
    pyautogui.screenshot(screenshot_name)
    logging.error(f"{logging_prefix}Saving debugging screenshot to {screenshot_name}")
    return False
    

# STEPS
# Webpage loaded
# Need to login/Logged in confirmation
# Email
# Password
# Login Button
# Logged in confirmation
# Claim Available/Not available
# Claim Button
# Claim Confirmation 
# REQUIRED FILES:
# - webpage-loaded.png - Determines if the initial load works (Visual Only)
# - login_required.png - Determines if you need to login (Visual Only)
# - login_not_required.png - Determines if you are already logged in (Visual Only)
# - start_login.png - Starts the login process, typically the 'login' button (Clicked)
# - pass_field.png - Password field (Clicked and Typed on)
# - email_field.png - Email/Username field (Clicked and Typed on)
# - submit_login.png - Button that will attempt to login with the provided credentials (Clicked)
# - claim_available.png - Determines if there is a claim available (Clicked)
# - noclaim_available.png - Determines if there is no claim currently available to claim right now (Visual Only)
# - claim_confirmation.png - Ensures that claim confirmations are clicked (Clicked)
# - claim_success.png - Indicator that the claim was successful (Visual Only)
async def genericClaim(name, base_path, base_url, customNavigateToClaim=None, claimAvailableClickOffset=None):
    username = CONFIGURATION[name][CONFIG_USERNAME]
    password = CONFIGURATION[name][CONFIG_PASSWORD]
    health_check_successful_run = CONFIGURATION[name][CONFIG_HEALTH_RUN]
    health_check_successful_claim = CONFIGURATION[name][CONFIG_HEALTH_CLAIM]
    
    name_stub = to_stub(name)
    logging_prefix = f"GenericClaim - {name} - "
    
    # Try to navigate to the webpage initially
    logging.debug(f"{logging_prefix}Trying to navigate to {base_url}")
    browser, page = await start_browser(base_url)
    webpage_loaded = wait_for_image(base_path+"webpage-loaded.png", 20)
    if not webpage_loaded:
        return report_failure(logging_prefix, f"{name_stub}_navigation_fail.png", f"Unable to load webpage of {name} for some reason!")
    logging.debug(f"{logging_prefix}Able to successfully navigate to {base_url}")
    
    # Are we logged in? or do we need to login now?
    logging.debug(f"{logging_prefix}Trying to detect if we need to login")
    
    login_required_path = base_path+"login_required.png"
    login_not_required_path = base_path+"login_not_required.png"
    _, login_check_image = wait_for_any_image_to_exist([login_required_path, login_not_required_path], 50)
    if (login_check_image is login_required_path):
        logging.debug(f"{logging_prefix}Login is required")
        
        logging.debug(f"{logging_prefix}Attempting to login")
        
        start_login_button = wait_for_image(base_path+"start_login.png", 20)
        if(not start_login_button):
            return report_failure(logging_prefix, f"{name_stub}_start_login_fail.png", f"Unable to find the login button to start the login process for some reason!")
            
        click_location(start_login_button)
        
        logging.debug(f"{logging_prefix}Attempting to find login elements")
        
        logging.debug(f"{logging_prefix}Attempting to fill password")
        pass_field_location = wait_for_image(base_path+"pass_field.png", 20, 0.1, 0.99)
        if(not pass_field_location):
            return report_failure(logging_prefix, f"{name_stub}_locate_password_field_fail.png", f"Unable to find the password field for some reason!")
        time.sleep(1)
        click_location(pass_field_location)
        pyautogui.typewrite(password)
        
        
        logging.debug(f"{logging_prefix}Attempting to fill username")
        email_field_location = wait_for_image(base_path+"email_field.png", 20, 0.1, 0.99)
        if(not email_field_location):
            return report_failure(logging_prefix, f"{name_stub}_locate_email_field_fail.png", f"Unable to find the email/username field for some reason!")
        click_location(email_field_location)
        pyautogui.typewrite(username)
        
        logging.debug(f"{logging_prefix}Attempting to submit login information")
        login_button_location = wait_for_image(base_path+"submit_login.png", 20, 0.1, 0.8)
        if(not login_button_location):
            return report_failure(logging_prefix, f"{name_stub}_locate_login_button_fail.png", f"Unable to find the login button for some reason!")
        click_location(login_button_location)
        
        logged_in = wait_for_image(login_not_required_path, 20)
        if(not logged_in):
            return report_failure(logging_prefix, f"{name_stub}_login_fail.png", f"Unable to login!")
    elif (login_check_image is login_not_required_path):
        logging.debug(f"{logging_prefix}Login is not required!")
    else:
        return report_failure(logging_prefix, f"{name_stub}_login_determination_fail.png", f"Unable to determine if we need to login to {name} for some reason!")
    
    logging.debug(f"{logging_prefix}Finished ensuring that we are logged in!")
    
    if(customNavigateToClaim is not None):
        logging.debug(f"{logging_prefix}A custom claim navigation was provided, so we will call it now")
        await customNavigateToClaim(base_path, browser, page)
        logging.debug(f"{logging_prefix}Finished calling custom claim navigation")
    
    # Determine if there is a Claim Available or not
    logging.debug(f"{logging_prefix}Trying to determine if there is a claim available!")
    
    claim_available_path = base_path+"claim_available.png"
    noclaim_available_path = base_path+"noclaim_available.png"
    claim_check_location, claim_check_image = wait_for_any_image_to_exist([claim_available_path, noclaim_available_path], 50)

    if(claim_check_image is claim_available_path):
        logging.debug(f"{logging_prefix}There is a claim available!")
        
        
        claim_check_locationX, claim_check_locationY = location_to_point(claim_check_location)
        if claimAvailableClickOffset:
            claim_check_locationX = claim_check_locationX + claimAvailableClickOffset['x']
            claim_check_locationY = claim_check_locationY + claimAvailableClickOffset['y']

        click_point(claim_check_locationX, claim_check_locationY)
        
        claim_confirmation_path = base_path+"claim_confirmation.png"
        claim_confirmation_location = wait_for_image(claim_confirmation_path, 20)
        if(not claim_confirmation_location):
            return report_failure(logging_prefix, f"{name_stub}_claim_confirmation_fail.png", f"Unable to find the claim confirmation for some reason!")
        
        click_location(claim_confirmation_location)
        
        claim_success_path = base_path+"claim_success.png"
        claim_success_location = wait_for_image(claim_success_path, 20)
        if(not claim_success_location):
            return report_failure(logging_prefix, f"{name_stub}_claim_success_fail.png", f"Unable to determine that the claim was finished successfully!")
        
        ping(health_check_successful_run)
        ping(health_check_successful_claim)
        
        logging.info(f"{logging_prefix}Finished successfully claiming!")
    elif(claim_check_image is noclaim_available_path):
        logging.debug(f"{logging_prefix}There is no claim available at this time")
        ping(health_check_successful_run)
    else:
        return report_failure(logging_prefix, f"{name_stub}_claim_determination_fail.png", f"Unable to determine if there was a claim available!")
    
    # TODO get the current balance here    
    
    # Finished, time to wrap up
    logging.debug(f"{logging_prefix}Finished checking claim, wrapping up")
    
    logging.debug(f"{logging_prefix}Attempting to close browser")
    await browser.close()



async def navigateToZulaClaim(base_path, browser, page):
    # close_modal.png
    close_modal = wait_for_image(base_path+"close_modal.png")
    if close_modal:
        click_location(close_modal)
    
    # coin_store.png
    coin_store = wait_for_image(base_path+"coin_store.png")
    click_location(coin_store)
        
    # confirm_at_claim_page.png
    confirm_at_claim_page = wait_for_image(base_path+"confirm_at_claim_page.png")
    if not confirm_at_claim_page:
        return report_failure("Zula Claim Navigation", f"zula_claim_tab_navigation_fail.png", f"Unable to ensure that we were able to open the claim model correctly")

async def claimZula():
    return await genericClaim(
            name="Zula",
            base_path="imgs/zula/",
            base_url="https://www.zulacasino.com/",
            customNavigateToClaim=navigateToZulaClaim
        )

async def claimFortuneCoinsV2():
    return await genericClaim(
            name="Fortune Coins",
            base_path="imgs/fortune/",
            base_url="https://www.fortunecoins.com/"
        )   


async def main(schedule = RunSchedule.All):
    ping("https://healthchecks.weldware.net/ping/08aab5ce-4bb7-4b3e-8e4c-01c7e0e08b75")
    try:        
        if(schedule == RunSchedule.All or schedule == RunSchedule.SixHours):
            await claimChumba()
            await claimPulsz()
            await claimLuckylandslots()
            await claimFortuneCoinsV2()
            await claimZula()
        
        if(schedule == RunSchedule.All or schedule == RunSchedule.EveryHour):
            await claimChancedV2()
    except KeyboardInterrupt:
        pass
        
def startup(schedule = RunSchedule.All):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        asyncio.run(main(schedule))
    except KeyboardInterrupt:
        pass


CONFIGURATION = load_configuration()

if __name__ ==  '__main__':
    startup()
    
    scheduler = BackgroundScheduler()
    scheduler.add_job(lambda schedule = RunSchedule.EveryHour: startup(schedule), 'interval', hours=1, minutes=2)
    scheduler.add_job(lambda schedule = RunSchedule.SixHours:  startup(schedule), 'interval', hours=6, minutes=2)
    
    scheduler.start()
    
    try:
        while 1:
            # Do nothing since blocking scheduler is brok.... zzzz
            time.sleep(0.1)
    except (KeyboardInterrupt, SystemExit):
        logging.warning('Got SIGTERM! Terminating...')
        scheduler.shutdown(wait=False)