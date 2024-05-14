import flet

class MessageBox(flet.AlertDialog):
    def __init__(self,
                 text,
                 text_color,
                 bgcolor,
                 height,
                 on_close_method,
                 ):
        super().__init__(
            content=flet.Column(
                controls=[
                    flet.Row(
                        controls=[
                            flet.IconButton(
                                icon=flet.icons.CLOSE,
                                icon_color=text_color,
                                style=flet.ButtonStyle(
                                    shape=flet.RoundedRectangleBorder(radius=8)
                                ),
                                on_click=on_close_method
                            )
                        ],
                        alignment=flet.MainAxisAlignment.END
                    ),
                    flet.Container(
                        content=flet.Text(
                            value=text,
                            color=text_color,
                            weight=flet.FontWeight.W_600
                        ),
                        padding=flet.padding.only(20,0,20,0)
                    )
                ],
                height=height
            ),
            bgcolor=bgcolor,
            modal=True,
            shape=flet.RoundedRectangleBorder(radius=8),
            content_padding=flet.padding.only(0,0,0,20)
        )