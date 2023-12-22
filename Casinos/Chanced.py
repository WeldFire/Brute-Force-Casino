
from Casinos.Casnio import Casino
from Helpers.BrowserHelpers import wait_for_image
from Helpers.BrowserHelpers import click_location
from Helpers.BrowserHelpers import report_failure



from enums.CasinoEnum import CasinoEnum

class Chanced(Casino):


    def __init__(self, CONFIGURATION):
        print("Chanced initializing...")
        super().__init__(CONFIGURATION)

    def testChancedClaim(self):
        print("Running Chanced claim function...")
        print(self.CONFIGURATION)

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
    
    async def claimChancedV2(self):
        return await super().genericClaim(
                name=CasinoEnum.CHANCED.value,
                base_path="imgs/chanced/",
                base_url="https://www.chanced.com",
                customNavigateToClaim=self.navigateToChancedClaim,
                claimAvailableClickOffset={'x':0, 'y':200}
            )