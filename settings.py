import flet as ft


class Settings:
    def __init__(
        self,
        page,
        waste_size=1,
        deck_passes_allowed=1000,
        card_back=f"/images/card_back0.png",
    ):
        self.waste_size = waste_size
        self.deck_passes_allowed = deck_passes_allowed
        self.card_back = card_back
        self.card_width = 70
        self.card_height = 100
        self.card_offset = 100

        if page:
            width = page.width/7
            self.card_offset = round(width-(width*0.045),0)
            self.card_width = round(width-(width*0.105),0)
            self.card_height = round((self.card_width*100)/70,0)
            self.slot_offset = round(self.card_height*1.2)
