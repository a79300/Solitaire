import flet as ft
from layout import create_appbar
from settings import Settings
from solitaire import Solitaire
from shop import ShopOverlay


def main(page: ft.Page):

    solitaire = None
    shop = None

    def on_new_game(settings):
        nonlocal solitaire

        if len(page.controls) > 0:
            page.controls.pop()

        new_solitaire = Solitaire(page, settings, on_win)

        shop = ShopOverlay(
            page,
            settings,
            on_settings_applied=new_solitaire.update_card_back,
        )

        shop.top = -(shop.height * 0.135)
        shop.left = -(shop.width * 0.035)

        stack = ft.Stack(
            controls=[new_solitaire, shop],
            expand=True,
        )
        page.add(stack)

        create_appbar(page, new_solitaire, settings, on_new_game, shop)
        page.update()

    def on_win():
        page.add(
            ft.AlertDialog(
                title=ft.Text("YOU WIN!"),
                open=True,
                on_dismiss=lambda e: page.controls.pop(),
            )
        )
        page.update()

    settings = Settings(page)
    if not page.client_storage.contains_key(str("coins")):
        page.client_storage.set(str("coins"), 0)

    solitaire = Solitaire(page, settings, on_win)
    shop = ShopOverlay(
        page,
        settings,
        on_settings_applied=solitaire.update_card_back,
    )

    shop.top = -(shop.height * 0.135)
    shop.left = -(shop.width * 0.035)

    create_appbar(page, solitaire, settings, on_new_game, shop)

    stack = ft.Stack(
        controls=[solitaire, shop],
        expand=True,
    )
    page.add(stack)


ft.app(target=main, assets_dir="assets", view=ft.AppView.WEB_BROWSER)
