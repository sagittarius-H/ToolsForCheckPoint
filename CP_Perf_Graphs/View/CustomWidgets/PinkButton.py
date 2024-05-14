import flet

class PinkButton(flet.ElevatedButton):
    def __init__(self,
                 text,
                 height,
                 on_click_method=None,
                 width=None):
        super().__init__(
            text=text,
            width=width,
            height=height,
            style=flet.ButtonStyle(
                bgcolor={
                    flet.MaterialState.HOVERED: "#ff3d83",
                    flet.MaterialState.DEFAULT: "#efefef"
                },
                overlay_color={
                    flet.MaterialState.PRESSED: "#ba2b5e",
                },
                color={
                    flet.MaterialState.DEFAULT: flet.colors.BLACK,
                    flet.MaterialState.HOVERED: flet.colors.WHITE
                },
                shape=flet.RoundedRectangleBorder(radius=5)
            ),
            on_click=on_click_method
        )