import flet as ft


def create_appbar(page, solitaire, settings, on_new_game, shop):

    def new_game_clicked(e):
        on_new_game(settings)

    def undo_move(e):
        if solitaire:
            solitaire.undo_last_move()

    def save_game(e):
        if solitaire:
            solitaire.save_game()

    def load_game(e):
        if solitaire:
            solitaire.load_game()

    def open_shop(e):
        if shop:
            shop.show()
        page.update()

    def tip_card(e):
        if solitaire:
            solitaire.tip_card()

    page.appbar = ft.AppBar(
        leading_width=30,
        bgcolor=ft.colors.SURFACE_VARIANT,
        actions=[
            ft.IconButton(ft.Icons.LIGHTBULB_OUTLINE_ROUNDED,
                          on_click=tip_card),
            ft.TextButton(text="New game", on_click=new_game_clicked),
            ft.TextButton(text="Save", on_click=save_game),
            ft.TextButton(text="Load", on_click=load_game),
            ft.IconButton(ft.Icons.SHOPPING_CART_OUTLINED, on_click=open_shop),
            ft.IconButton(ft.Icons.KEYBOARD_RETURN, on_click=undo_move),
        ],
    )
