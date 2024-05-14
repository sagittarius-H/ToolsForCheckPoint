import flet

class DatePicker(flet.Container):
    def __init__(self):
        super().__init__(
            content=flet.Row(
                controls=[
                    flet.TextField(
                        label="DD/MM/YY",
                        text_size=12,
                        read_only=True,
                        disabled=True,
                        width=110,
                        height=40,
                    ),
                    flet.Container(
                        content=flet.Icon(
                            name=flet.icons.CALENDAR_MONTH_ROUNDED,
                            color=flet.colors.BLACK
                        ),
                        ink=True,
                        ink_color="#c60c4e",
                        on_click=lambda e: print("Clickable with Ink clicked!"),
                        bgcolor="#efefef",
                        on_hover=DatePicker.on_hover_container,
                        border_radius=5,
                        height=40,
                        width=40,
                    )
                ]
            )
        )

    @staticmethod
    def on_hover_container(e):
        e.control.bgcolor = "#ef589e" if e.data == "true" else "#efefef"
        e.control.content.color = flet.colors.WHITE if e.data == "true" else flet.colors.BLACK
        e.control.update()