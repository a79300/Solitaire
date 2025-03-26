import flet as ft


class Slot(ft.Container):
    def __init__(self, solitaire, slot_type, top, left, border):
        super().__init__()
        self.solitaire = solitaire
        self.pile = []
        self.type = slot_type
        self.width = self.solitaire.settings.card_width
        self.height = self.solitaire.settings.card_height
        self.left = left
        self.top = top
        self.border_radius = ft.border_radius.all(6)
        self.border = border
        self.on_click = self.click

    def get_top_card(self):
        if len(self.pile) > 0:
            return self.pile[-1]

    def upper_card_top(self):
        if self.type == "tableau" and len(self.pile) > 1:
            return self.top + self.solitaire.card_offset * (len(self.pile) - 1)
        return self.top

    def click(self, e):
        if self.type == "stock" and self.solitaire.deck_passes_remaining > 1:
            self.solitaire.deck_passes_remaining -= 1
            self.solitaire.restart_stock()
