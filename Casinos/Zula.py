from Casinos.Casnio import Casino
from Helpers.BrowserHelpers import wait_for_image
from Helpers.BrowserHelpers import click_location
from Helpers.BrowserHelpers import report_failure



from enums.CasinoEnum import CasinoEnum

class Zula(Casino):

    def __init__(self, CONFIGURATION):
        print("Zula initializing...")
        super().__init__(CONFIGURATION)

    def testZulaClaim(self):
        print("Running Zula claim function...")
        print(self.CONFIGURATION)


    async def navigateToZulaClaim(base_path):
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

    async def claimZula(self):
        return await super().genericClaim(
                name=CasinoEnum.ZULA.value,
                base_path="imgs/zula/",
                base_url="https://www.zulacasino.com/",
                customNavigateToClaim=self.navigateToZulaClaim
        )