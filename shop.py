import flet as ft


class ShopOverlay(ft.Stack):
    def __init__(self, page, settings, on_settings_applied):
        super().__init__()
        self.page = page
        self.settings = settings
        self.on_settings_applied = on_settings_applied
        self.visible = False
        self.width = self.page.width
        self.height = self.page.height
        self.coins = self.page.client_storage.get(str("coins"))
        self.card_prices = [0, 500, 2000, 9000]
        self.buyed_card_backs = [1, 0, 0, 0]
        self.padding_size = self.page.height*0.02

        if self.page.height > self.page.width:
            shop_card_width = self.page.width*0.8
            shop_card_height = self.page.width*0.8
            title_size = self.page.width*0.05
            title_padding = self.page.width*0.04
            self.padding_size = self.page.width*0.02
            self.card_back_width = self.settings.card_width
            self.card_back_height = self.settings.card_height*1.2
        else:
            shop_card_width = self.page.width*0.8
            shop_card_height = shop_card_width*0.5
            title_size = self.page.height*0.025
            title_padding = self.page.width*0.01
            self.padding_size = self.page.height*0.02
            self.card_back_width = self.settings.card_width*0.9
            self.card_back_height = self.settings.card_height*0.8


        self.overlay_bg = ft.Container(
            width=self.page.width,
            bgcolor=ft.colors.with_opacity(0.8, ft.colors.BLACK),
        )

        self.card_backs = []
        self.card_backs_row = self.generate_card_backs()

        self.coins_button = ft.TextButton(
            text=f"Current balance: {self.coins} coins",
            on_click=self.add_coins,
        )

        self.shop_card = ft.Card(
            content=ft.Container(
                width=shop_card_width,
                height=shop_card_height,
                padding=title_padding,
                content=ft.Column(
                    [
                        ft.Row(
                            [
                                ft.Text(
                                    "Card Back Shop", size=title_size, weight=ft.FontWeight.BOLD
                                ),
                                ft.IconButton(
                                    icon=ft.icons.CLOSE, on_click=self.close_shop
                                ),
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        ),
                        ft.Divider(),
                        ft.Text("Select a card back design:"),
                        self.card_backs_row,
                        ft.Container(
                            content=self.coins_button,
                            padding=ft.padding.only(top=self.padding_size),
                        ),
                    ],
                    spacing=self.page.width*0.03,
                ),
            ),
            elevation=self.padding_size,
        )

        self.shop_card.left = self.page.width*0.1
        self.shop_card.top = self.page.height*0.2

        self.controls = [self.overlay_bg, self.shop_card]

    def generate_card_backs(self):
        if not self.page.client_storage.contains_key(str("buyed_card_backs")):
            self.page.client_storage.set(str("buyed_card_backs"), [1, 0, 0, 0])

        self.buyed_card_backs = self.page.client_storage.get(str("buyed_card_backs"))
        card_backs_row = ft.Row(alignment=ft.MainAxisAlignment.CENTER)

        for i in range(4):
            is_locked = self.buyed_card_backs[i] == 0
            is_selected = self.settings.card_back == f"/images/card_back{i}.png"
            border = ft.border.all(3) if is_selected else None

            card_image = (
                f"/images/card_back{i}.png"
                if not is_locked
                else f"/images/card_back{i}_locked.png"
            )
            card_description = "Owned" if not is_locked else f"{self.card_prices[i]}c"

            card_back = ft.Container(
                width=self.card_back_width,
                height=self.card_back_height,
                content=ft.Column(
                    [
                        ft.Image(src=card_image),
                        ft.Text(card_description, text_align="center", size=self.page.width*0.02),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=self.page.width*0.01,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                border_radius=ft.border_radius.all(6),
                border=border,
                margin=self.padding_size,
                padding=self.padding_size,
                on_click=self.choose_card_design,
                data=i,
            )

            self.card_backs.append(card_back)
            card_backs_row.controls.append(card_back)

        self.selected_card = next(
            (card for card in self.card_backs if card.border is not None),
            self.card_backs[0],
        )

        return card_backs_row

    def choose_card_design(self, e):
        if self.buyed_card_backs[e.control.data] == 1:
            for card in self.card_backs:
                card.border = None

            e.control.border = ft.border.all(3)
            self.selected_card = e.control
        elif (
            self.buyed_card_backs[e.control.data] == 0
            and self.coins >= self.card_prices[e.control.data]
        ):
            self.coins -= self.card_prices[e.control.data]
            self.page.client_storage.set(str("coins"), self.coins)
            self.buyed_card_backs[e.control.data] = 1
            self.page.client_storage.set(str("buyed_card_backs"), self.buyed_card_backs)

            self.card_backs_row.controls.clear()
            self.card_backs_row = self.generate_card_backs()
            self.shop_card.content.content.controls[3] = self.card_backs_row

        self.settings.card_back = f"/images/card_back{self.selected_card.data}.png"
        self.on_settings_applied(self.settings)
        self.update_coins()

    def add_coins(self, e):
        self.coins += 1000
        self.page.client_storage.set(str("coins"), self.coins)
        self.update_coins()

    def close_shop(self, e=None):
        self.visible = False
        self.update()

    def update_coins(self):
        self.coins = self.page.client_storage.get(str("coins"))
        self.coins_button.text = f"Current balance: {self.coins} coins"
        self.update()

    def show(self):
        self.visible = True
        self.update_coins()