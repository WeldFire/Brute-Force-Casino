from Casinos.Casnio import Casino
from Helpers.BrowserHelpers import wait_for_image
from Helpers.BrowserHelpers import click_location
from Helpers.BrowserHelpers import report_failure



from enums.CasinoEnum import CasinoEnum


class Modo(Casino):

    def __init__(self, CONFIGURATION):
        print("Modo initializing...")
        super().__init__(CONFIGURATION)

    def testModoClaim(self):
        print("Running Modo claim function...")
        print(self.CONFIGURATION)

    async def claimModo():
        return await super().genericClaim(
                name=CasinoEnum.MODO.value,
                base_path="imgs/modo/",
                base_url="https://modo.us/lobby?value=APPROVED"
            )