import os
import pyautogui
import time
import logging


from Helpers.BrowserHelpers import to_stub
from Helpers.BrowserHelpers import start_browser
from Helpers.BrowserHelpers import wait_for_image
from Helpers.BrowserHelpers import report_failure
from Helpers.BrowserHelpers import wait_for_any_image_to_exist
from Helpers.BrowserHelpers import click_location
from Helpers.BrowserHelpers import location_to_point
from Helpers.BrowserHelpers import click_point
from Helpers.BrowserHelpers import ping


from Configuration import CONFIG_USERNAME
from Configuration import CONFIG_PASSWORD
from Configuration import CONFIG_HEALTH_RUN
from Configuration import CONFIG_HEALTH_CLAIM


class Casino:


    CONFIGURATION =  None

    def __init__(self, CONFIGURATION):
        print("Casino initializing...")
        self.CONFIGURATION = CONFIGURATION
        print(self.CONFIGURATION)

    async def genericClaim(self, name, base_path, base_url, customNavigateToClaim=None, claimAvailableClickOffset=None):
        username = self.CONFIGURATION[CONFIG_USERNAME]
        password = self.CONFIGURATION[CONFIG_PASSWORD]
        health_check_successful_run = self.CONFIGURATION[CONFIG_HEALTH_RUN]
        health_check_successful_claim = self.CONFIGURATION[CONFIG_HEALTH_CLAIM]
        
        name_stub = to_stub(name)
        logging_prefix = f"GenericClaim - {name} - "
        
        # Try to navigate to the webpage initially
        logging.info(f"{logging_prefix}Trying to navigate to {base_url}")
        browser, page = await start_browser(base_url)
        webpage_loaded = wait_for_image(base_path+"webpage-loaded.png", 100)
        if not webpage_loaded:
            return report_failure(logging_prefix, f"{name_stub}_navigation_fail.png", f"Unable to load webpage of {name} for some reason!")
        logging.info(f"{logging_prefix}Able to successfully navigate to {base_url}")
        
        # Are we logged in? or do we need to login now?
        logging.info(f"{logging_prefix}Trying to detect if we need to login")
        
        login_required_path = base_path+"login_required.png"
        login_not_required_path = base_path+"login_not_required.png"
        _, login_check_image = wait_for_any_image_to_exist([login_required_path, login_not_required_path], 50)
        if (login_check_image is login_required_path):
            logging.info(f"{logging_prefix}Login is required")
            
            logging.info(f"{logging_prefix}Attempting to login")
            
            start_login_button = wait_for_image(base_path+"start_login.png", 20)
            if(not start_login_button):
                return report_failure(logging_prefix, f"{name_stub}_start_login_fail.png", f"Unable to find the login button to start the login process for some reason!")
                
            click_location(start_login_button)
            
            # OPTIONAL - Try to find login selector if it was defined
            login_selection_image = base_path+"login_selection.png"
            if os.path.isfile(login_selection_image):
                logging.info(f"{logging_prefix}Attempting to find login selection element")
                
                login_selection_button = wait_for_image(login_selection_image, 20)
                if(not login_selection_button):
                    return report_failure(logging_prefix, f"{name_stub}_select_login_type_fail.png", f"Unable to find the login selection button provided for some reason!")
                    
                click_location(login_selection_button)
            
            logging.info(f"{logging_prefix}Attempting to find login elements")
            
            logging.info(f"{logging_prefix}Attempting to fill password")
            pass_field_location = wait_for_image(base_path+"pass_field.png", 20, 0.1, 0.99)
            if(not pass_field_location):
                return report_failure(logging_prefix, f"{name_stub}_locate_password_field_fail.png", f"Unable to find the password field for some reason!")
            time.sleep(1)
            click_location(pass_field_location)
            pyautogui.typewrite(password)
            
            
            logging.info(f"{logging_prefix}Attempting to fill username")
            email_field_location = wait_for_image(base_path+"email_field.png", 20, 0.1, 0.99)
            if(not email_field_location):
                return report_failure(logging_prefix, f"{name_stub}_locate_email_field_fail.png", f"Unable to find the email/username field for some reason!")
            click_location(email_field_location)
            pyautogui.typewrite(username)
            
            logging.info(f"{logging_prefix}Attempting to submit login information")
            login_button_location = wait_for_image(base_path+"submit_login.png", 20, 0.1, 0.8)
            if(not login_button_location):
                return report_failure(logging_prefix, f"{name_stub}_locate_login_button_fail.png", f"Unable to find the login button for some reason!")
            click_location(login_button_location)
            
            logged_in = wait_for_image(login_not_required_path, 20)
            if(not logged_in):
                return report_failure(logging_prefix, f"{name_stub}_login_fail.png", f"Unable to login!")
        elif (login_check_image is login_not_required_path):
            logging.info(f"{logging_prefix}Login is not required!")
        else:
            return report_failure(logging_prefix, f"{name_stub}_login_determination_fail.png", f"Unable to determine if we need to login to {name} for some reason!")
        
        logging.info(f"{logging_prefix}Finished ensuring that we are logged in!")
        
        if(customNavigateToClaim is not None):
            logging.info(f"{logging_prefix}A custom claim navigation was provided, so we will call it now")
            await customNavigateToClaim(base_path, browser, page)
            logging.info(f"{logging_prefix}Finished calling custom claim navigation")
        
        # Determine if there is a Claim Available or not
        logging.info(f"{logging_prefix}Trying to determine if there is a claim available!")
        
        claim_available_path = base_path+"claim_available.png"
        noclaim_available_path = base_path+"noclaim_available.png"
        claim_check_location, claim_check_image = wait_for_any_image_to_exist([claim_available_path, noclaim_available_path], 50)

        if(claim_check_image is claim_available_path):
            logging.info(f"{logging_prefix}There is a claim available!")
            
            
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
            
            if(health_check_successful_run):
                ping(health_check_successful_run)
            else:
                logging.warn(f"No health check run url defined for {name}")

            if(health_check_successful_claim):
                ping(health_check_successful_claim)
            else:
                logging.warn(f"No health check claim url defined for {name}")

            logging.info(f"{logging_prefix}Finished successfully claiming!")
        elif(claim_check_image is noclaim_available_path):
            logging.info(f"{logging_prefix}There is no claim available at this time")
            if(health_check_successful_run):
                ping(health_check_successful_run)
            else:
                logging.warn(f"No health check run url defined for {name}")
        else:
            return report_failure(logging_prefix, f"{name_stub}_claim_determination_fail.png", f"Unable to determine if there was a claim available!")
        
        # TODO get the current balance here    
        
        # Finished, time to wrap up
        logging.info(f"{logging_prefix}Finished checking claim, wrapping up")
        
        logging.info(f"{logging_prefix}Attempting to close browser")
        await browser.close()


