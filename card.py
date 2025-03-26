import flet as ft


class Card(ft.GestureDetector):
    def __init__(self, solitaire, suite, rank, face_up=False):
        super().__init__()
        self.solitaire = solitaire
        self.suite = suite
        self.rank = rank
        self.face_up = face_up
        self.slot = None

        self.mouse_cursor = ft.MouseCursor.MOVE
        self.drag_interval = 5
        self.on_pan_update = self.drag
        self.on_pan_start = self.start_drag
        self.on_pan_end = self.drop
        self.on_tap = self.click
        self.on_double_tap = self.doubleclick
        self.content = ft.Container(
            width=self.solitaire.settings.card_width,
            height=self.solitaire.settings.card_height,
            border_radius=ft.border_radius.all(6),
            content=ft.Image(src=self.solitaire.settings.card_back),
        )

        if self.face_up:
            self.turn_face_up()

    def turn_face_up(self):
        self.face_up = True
        self.content.content.src = (
            f"/images/cards/{self.rank.name}_{self.suite.name}.svg"
        )
        self.solitaire.update()

    def turn_face_down(self):
        self.face_up = False
        self.content.content.src = self.solitaire.settings.card_back
        self.solitaire.update()

    def can_be_moved(self):
        if (self.face_up and self.slot.type != "waste") or ( self.slot.type == "waste" and len(self.solitaire.waste.pile) - 1 == self.solitaire.waste.pile.index(self)):
            return True
        return False

    def start_drag(self, e: ft.DragStartEvent):
        if self.can_be_moved():
            cards_to_drag = self.get_cards_to_move()
            self.solitaire.move_on_top(cards_to_drag)
            self.solitaire.current_top = e.control.top
            self.solitaire.current_left = e.control.left
            self.solitaire.update()

    def drag(self, e: ft.DragUpdateEvent):
        if self.can_be_moved():
            i = 0
            for card in self.get_cards_to_move():
                card.top = max(0, self.top + e.delta_y)
                if card.slot.type == "tableau":
                    card.top += i * self.solitaire.card_offset
                card.left = max(0, self.left + e.delta_x)
                i += 1
            self.solitaire.update()

    def drop(self, e: ft.DragEndEvent):
        if self.can_be_moved():
            cards_to_drag = self.get_cards_to_move()
            slots = self.solitaire.tableau + self.solitaire.foundation

            for slot in slots:
                if (
                    abs(self.top - slot.upper_card_top()) < 40
                    and abs(self.left - slot.left) < 40
                ):
                    if (
                        slot.type == "tableau"
                        and self.solitaire.check_tableau_rules(
                            self, slot.get_top_card()
                        )
                    ) or (
                        slot.type == "foundation"
                        and len(cards_to_drag) == 1
                        and self.solitaire.check_foundation_rules(
                            self, slot.get_top_card()
                        )
                    ):

                        old_slot = self.slot

                        self.solitaire.record_move(
                            cards_to_drag, old_slot, slot, self.face_up
                        )

                        for card in cards_to_drag:
                            card.place(slot)

                        if len(old_slot.pile) > 0 and old_slot.type == "tableau":
                            old_slot.get_top_card().turn_face_up()
                        self.solitaire.update()

                        return

            self.clear_cards_border()
            self.solitaire.bounce_back(cards_to_drag)
            self.solitaire.update()

    def doubleclick(self, e):
        if self.slot.type in ("waste", "tableau") and self.face_up:
            self.solitaire.move_on_top([self])
            old_slot = self.slot
            for slot in self.solitaire.foundation:
                if self.solitaire.check_foundation_rules(self, slot.get_top_card()):
                    self.solitaire.record_move([self], old_slot, slot, self.face_up)

                    self.place(slot)
                    self.clear_cards_border()
                    self.solitaire.update()
                    return

    def click(self, e):
        if self.slot.type == "stock":
            cards_to_draw = min(
                self.solitaire.settings.waste_size, len(self.solitaire.stock.pile)
            )
            if cards_to_draw > 0:
                cards_to_record = self.solitaire.stock.pile[-cards_to_draw:]
                self.solitaire.record_move(
                    cards_to_record, self.solitaire.stock, self.solitaire.waste, False
                )

                for i in range(
                    min(self.solitaire.settings.waste_size, len(self.solitaire.stock.pile))
                ):
                    top_card = self.solitaire.stock.pile[-1]

                    top_card.place(self.solitaire.waste)
                    top_card.turn_face_up()
            else:
                self.solitaire.restart_stock()
                
            self.solitaire.update()

        if self.slot.type == "tableau":
            if self.face_up == False and len(
                self.slot.pile
            ) - 1 == self.slot.pile.index(self):
                self.solitaire.record_move([self], self.slot, self.slot, False)
                self.turn_face_up()

    def place(self, slot):
        self.top = slot.top
        self.left = slot.left
        if slot.type == "tableau":
            self.top += self.solitaire.card_offset * len(slot.pile)

        if self.slot is not None:
            self.slot.pile.remove(self)

        self.slot = slot

        slot.pile.append(self)
        self.solitaire.move_on_top([self])
        if self.solitaire.check_if_you_won():
            self.solitaire.on_win()
        self.clear_cards_border()
        self.solitaire.update()

    def get_cards_to_move(self):
        if self.slot is not None:
            return self.slot.pile[self.slot.pile.index(self):]

        return [self]

    def highlight_cards(self, card1, card2):
        self.highlight_cards_color1(card1)
        self.highlight_cards_color2(card2)
    
    def highlight_cards_color1(self, card):
        color1 = "yellow"
        card.content.border = ft.border.all(3, color1)
        self.solitaire.update()
    
    def highlight_cards_color2(self, card):
        color2 = "green"
        try:
            card.content.border = ft.border.all(3, color2)
        except:
            card.border = ft.border.all(3, color2)
        finally:
            self.solitaire.update()

    def clear_cards_border(self):
        self.solitaire.stock.border = ft.border.all(1)

        for tableau in self.solitaire.tableau:
            tableau.border = None
        
        for foundation in self.solitaire.foundation:
            foundation.border = ft.border.all(1, "outline")

        for card in self.solitaire.cards:
            card.content.border = None
        self.solitaire.update()
