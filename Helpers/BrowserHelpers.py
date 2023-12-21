import subprocess
import pyautogui
from utils import get_active_window_title
import time
import logging
import requests
import re
import os


browser_path = r"C:\\Users\\kenaw\\AppData\\Local\\Programs\\Opera GX\\launcher.exe"
browser_title_fragment = " - Opera"

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
    time.sleep(5) # Sleeping because Opera GX plays the dumb loading animation even though I turned it off.....
    return browser, page

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

def find_image(image_file_path, confidence=0.9, minSearchTime=0):
    # Use image recognition to locate elements on the page
    location = pyautogui.locateOnScreen(image_file_path, minSearchTime, confidence=confidence)
    if location:
        logging.debug(f"Location of the image is: {location}")
    # else:
    #     print("Image not found!")
    return location


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

def ping(url):
    try:
        requests.get(url, timeout=10)
    except requests.RequestException as e:
        # Log ping failure here...
        print("Ping failed: %s" % e)    

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


def report_failure(logging_prefix, screenshot_name, message):
    logging.error(f"{logging_prefix}{message}")
    pyautogui.screenshot(screenshot_name)
    logging.error(f"{logging_prefix}Saving debugging screenshot to {screenshot_name}")
    return False


def to_stub(s):
    s = s.lower() # make all characters lowercase
    s = re.sub(r'\W+', ' ', s) # replaces any non-alphanumeric character to a space
    s = s.replace(' ', '_') # replaces spaces with underscores
    return s