import flet

class MessageBox(flet.AlertDialog):
    def __init__(self,
                 text,
                 text_color,
                 bgcolor,
                 height,
                 padding: flet.padding,
                 padding_content: flet.padding
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
                                on_click=MessageBox._on_close_box
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
                        padding=padding
                        # padding=flet.padding.only(20,0,20,0)
                    )
                ],
                height=height
            ),
            bgcolor=bgcolor,
            modal=True,
            shape=flet.RoundedRectangleBorder(radius=8),
            content_padding=padding_content,

        )
    @staticmethod
    def _on_close_box(e: flet.ControlEvent):
        # ControlEvent ссылается на IconButton. Он вложен в Row>Column>MessageBox
        e.control.parent.parent.parent.open = False
        e.page.update()
