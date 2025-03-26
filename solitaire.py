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

    def did_mount(self):
        self.create_slots()
        self.create_card_deck()
        self.deal_cards()

    def update_card_back(self, settings):
        self.settings.card_back = settings.card_back
        for card in self.cards:
            if not card.face_up:
                card.content.content.src = self.settings.card_back
        self.update()

    def create_slots(self):

        self.stock = Slot(solitaire=self,
                          slot_type="stock",
                          top=0,
                          left=0,
                          border=ft.border.all(1))

        self.waste = Slot(solitaire=self,
                          slot_type="waste",
                          top=0,
                          left=self.settings.card_offset,
                          border=None)

        self.foundation = []
        x = self.settings.card_offset * 3
        for i in range(4):
            self.foundation.append(
                Slot(
                    solitaire=self,
                    slot_type="foundation",
                    top=0,
                    left=x,
                    border=ft.border.all(1, "outline"),
                ))
            x += self.settings.card_offset

        self.tableau = []
        x = 0
        for i in range(7):
            self.tableau.append(
                Slot(
                    solitaire=self,
                    slot_type="tableau",
                    top=self.settings.slot_offset,
                    left=x,
                    border=None,
                ))
            x += self.settings.card_offset

        self.controls.append(self.stock)
        self.controls.append(self.waste)
        self.controls.extend(self.foundation)
        self.controls.extend(self.tableau)
        self.update()

    def create_card_deck(self):
        self.cards = []

        for suite in self.suites:
            for rank in self.ranks:
                file_name = f"/cards/{rank.name}_{suite.name}.svg"

                self.cards.append(Card(solitaire=self, suite=suite, rank=rank))

        random.shuffle(self.cards)
        self.controls.extend(self.cards)
        self.update()

    def deal_cards(self):
        card_index = 0
        first_slot = 0
        while card_index <= 27:
            for slot_index in range(first_slot, len(self.tableau)):
                self.cards[card_index].place(self.tableau[slot_index])
                card_index += 1
            first_slot += 1

        for number in range(len(self.tableau)):

            self.tableau[number].get_top_card().turn_face_up()

        for i in range(28, len(self.cards)):
            self.cards[i].place(self.stock)

    def move_on_top(self, cards_to_drag):
        for card in cards_to_drag:
            if card in self.controls:
                self.controls.remove(card)
            self.controls.append(card)
        self.update()

    def bounce_back(self, cards):
        i = 0
        for card in cards:
            card.top = self.current_top
            if card.slot.type == "tableau":
                card.top += i * self.card_offset
            card.left = self.current_left
            i += 1

    def restart_stock(self):
        cards_in_waste = self.waste.pile.copy()
        if cards_in_waste:
            self.record_move(cards_in_waste, self.waste, self.stock, True)

        self.waste.pile.reverse()
        while len(self.waste.pile) > 0:
            card = self.waste.pile[0]
            card.turn_face_down()
            card.place(self.stock)
        self.update()


    def check_foundation_rules(self, current_card, top_card=None):
        if top_card is not None:
            return (current_card.suite.name == top_card.suite.name
                    and current_card.rank.value - top_card.rank.value == 1)
        else:
            return current_card.rank.name == "Ace"

    def check_tableau_rules(self, current_card, top_card=None):
        if top_card is not None:
            return (current_card.suite.color != top_card.suite.color
                    and top_card.rank.value - current_card.rank.value == 1)
        else:
            return current_card.rank.name == "King"

    def check_if_you_won(self):
        cards_num = 0
        for slot in self.foundation:
            cards_num += len(slot.pile)
        if cards_num == 52:
            return True
        return False

    def record_move(self, cards, source_slot, destination_slot, was_face_up):

        move = {
            "cards": cards.copy() if isinstance(cards, list) else [cards],
            "source": source_slot,
            "destination": destination_slot,
            "was_face_up": was_face_up,
        }
        self.move_history.append(move)
        if was_face_up:
            self.coins += 25
            self.page.client_storage.set(str("coins"), self.coins)

    def undo_last_move(self):
        if not self.move_history:
            return

        last_move = self.move_history.pop()

        cards = last_move["cards"]
        source_slot = last_move["source"]
        destination_slot = last_move["destination"]
        was_face_up = last_move["was_face_up"]

        if source_slot.type == "stock" and destination_slot.type == "waste":
            self._undo_stock_to_waste(cards, source_slot, destination_slot)
        else:
            self._undo_move(cards, source_slot, destination_slot, was_face_up)
            if was_face_up:
                self.coins -= 30
                if self.coins < 0:
                    self.coins = 0
                self.page.client_storage.set(str("coins"), self.coins)

    def _undo_stock_to_waste(self, cards, source_slot, destination_slot):
        cards_to_return = []
        for _ in range(
                min(self.settings.waste_size, len(destination_slot.pile))):
            if destination_slot.pile:
                card = destination_slot.pile[-1]
                destination_slot.pile.remove(card)
                card.turn_face_down()
                card.slot = source_slot
                source_slot.pile.append(card)
                cards_to_return.append(card)

        for card in cards_to_return:
            card.top = source_slot.top
            card.left = source_slot.left

        self.update()

    def _undo_move(self, cards, source_slot, destination_slot, was_face_up):
        for card in cards:
            if card in destination_slot.pile:
                destination_slot.pile.remove(card)

            if was_face_up:
                card.turn_face_up()
            else:
                card.turn_face_down()

            card.slot = source_slot
            source_slot.pile.append(card)

            card.top = source_slot.top
            card.left = source_slot.left

        if source_slot.type == "tableau":
            self._adjust_tableau_cards(cards, source_slot)

        if destination_slot.type == "tableau" and len(
                destination_slot.pile) > 0:
            top_card = destination_slot.get_top_card()
            if not top_card.face_up:
                top_card.turn_face_up()

        all_affected_cards = source_slot.pile + destination_slot.pile
        self.move_on_top(all_affected_cards)
        self.update()

    def _adjust_tableau_cards(self, cards, source_slot):
        for i, card in enumerate(cards):
            card.top = source_slot.top + self.card_offset * (
                len(source_slot.pile) - len(cards) + i)


    def save_game(self):
        game_state = {
            "deck_passes_remaining": self.deck_passes_remaining,
            "slots": {
                "stock":
                self._get_slot_state(self.stock),
                "waste":
                self._get_slot_state(self.waste),
                "foundation":
                [self._get_slot_state(slot) for slot in self.foundation],
                "tableau":
                [self._get_slot_state(slot) for slot in self.tableau],
            },
        }

        self.page.client_storage.set("save", json.dumps(game_state))

    def _get_slot_state(self, slot):
        return {
            "pile": [{
                "suite": card.suite.name,
                "rank": card.rank.name,
                "face_up": card.face_up,
                "top": card.top,
                "left": card.left,
            } for card in slot.pile]
        }

    def create_card(self, suite, rank, face_up, slot):
        _suite = next(filter(lambda s: s.name == suite, self.suites))
        _rank = next(filter(lambda r: r.name == rank, self.ranks))
        card = Card(
            solitaire=self,
            suite=_suite,
            rank=_rank,
            face_up=face_up,
        )
        self.cards.append(card)
        card.place(slot)


    def load_game(self):
        try:
            if not self.loading:
                self.loading = True

                game_status = json.loads(self.page.client_storage.get("save"))
                self.controls = []
                self.deck_passes_remaining = game_status[
                    "deck_passes_remaining"]
                self.create_slots()

                self.cards = []
                all_cards_data = []

                stock = game_status["slots"]["stock"]["pile"]
                waste = game_status["slots"]["waste"]["pile"]
                foundation_slot = game_status["slots"]["foundation"]
                tableau_slot = game_status["slots"]["tableau"]

                all_cards_data.extend([(card, self.stock) for card in stock])
                all_cards_data.extend([(card, self.waste) for card in waste])

                for i, foundation_pile in enumerate(foundation_slot):
                    all_cards_data.extend([(card, self.foundation[i])
                                           for card in foundation_pile["pile"]
                                           ])

                for i, tableau_pile in enumerate(tableau_slot):
                    all_cards_data.extend([(card, self.tableau[i])
                                           for card in tableau_pile["pile"]])

                for card_data, slot in all_cards_data:
                    _suite = next(
                        filter(lambda s: s.name == card_data["suite"],
                               self.suites))
                    _rank = next(
                        filter(lambda r: r.name == card_data["rank"],
                               self.ranks))
                    card = Card(
                        solitaire=self,
                        suite=_suite,
                        rank=_rank,
                        face_up=card_data["face_up"],
                    )
                    self.cards.append(card)

                self.controls.extend(self.cards)

                for i, (card_data, slot) in enumerate(all_cards_data):
                    self.cards[i].place(slot)

                self.loading = False
                self.update()

        except Exception as e:
            self.loading = False
