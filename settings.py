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