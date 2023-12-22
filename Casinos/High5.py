from Casinos.Casnio import Casino
from Helpers.BrowserHelpers import wait_for_image
from Helpers.BrowserHelpers import click_location
from Helpers.BrowserHelpers import report_failure

from enums.CasinoEnum import CasinoEnum

class High5(Casino):


    def __init__(self, CONFIGURATION):
        print("High5 initializing...")
        super().__init__(CONFIGURATION)

    def testHigh5Claim(self):
        print("Running High5 claim function...")
        print(self.CONFIGURATION)



    async def navigateToHigh5Claim(base_path, browser, page):
        # Is bonus_popup_open.png ?
        bonus_popup_open = wait_for_image(base_path+"bonus_popup_open.png", 20)
        if not bonus_popup_open:    
            # Open bonus_popup.png
            bonus_popup = wait_for_image(base_path+"bonus_popup.png", 20)
            if not bonus_popup:
                return report_failure("High 5 Claim Navigation", f"high_5_claim_bonus_popup_navigation_fail.png", f"Unable to open the bonus popup window!")
                
            click_location(bonus_popup)
            
            # Is bonus_popup_open.png now?
            bonus_popup_open_confirmation = wait_for_image(base_path+"bonus_popup_open.png", 20)
            if not bonus_popup_open_confirmation:    
                return report_failure("High 5 Claim Navigation", f"high_5_claim_bonus_popup_confirmation_fail.png", f"Unable to confirm the popup is open!")
            

    async def claimHigh5(self):
        return await super().genericClaim(
                name=CasinoEnum.HIGH5.value,
                base_path="imgs/high5/",
                base_url="https://club5.high5casino.com/gc",
                customNavigateToClaim=self.navigateToHigh5Claim
        )