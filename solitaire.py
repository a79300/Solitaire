from card import Card
from slot import Slot
import random
import json
import flet as ft


class Suite:

    def __init__(self, suite_name, suite_color):
        self.name = suite_name
        self.color = suite_color


class Rank:

    def __init__(self, card_name, card_value):
        self.name = card_name
        self.value = card_value


class Solitaire(ft.Stack):

    def __init__(self, page, settings, on_win):
        super().__init__()
        self.current_top = 0
        self.current_left = 0
        self.card_offset = 20
        self.page = page
        self.settings = settings
        self.deck_passes_remaining = int(self.settings.deck_passes_allowed)
        self.controls = []
        self.on_win = on_win
        self.coins = self.page.client_storage.get(str("coins"))
        self.move_history = []
        self.suites = [
            Suite("hearts", "RED"),
            Suite("diamonds", "RED"),
            Suite("clubs", "BLACK"),
            Suite("spades", "BLACK"),
        ]
        self.loading = False

        self.ranks = [
            Rank("Ace", 1),
            Rank("2", 2),
            Rank("3", 3),
            Rank("4", 4),
            Rank("5", 5),
            Rank("6", 6),
            Rank("7", 7),
            Rank("8", 8),
            Rank("9", 9),
            Rank("10", 10),
            Rank("Jack", 11),
            Rank("Queen", 12),
            Rank("King", 13),
        ]