import flet

class TitledContainer(flet.Container):
    def __init__(self,
                 content,
                 title,
                 height=None,
                 width=None,
                 padding=20,
                 border_radius=5):
        super().__init__(
            content=flet.Stack(
                controls=[
                    flet.Container(
                        border=flet.border.all(1, flet.colors.GREY),
                        height=height,
                        width=width,
                        content=content,
                        padding=padding,
                        border_radius=border_radius,
                        top=10
                    ),
                    flet.Container(
                        content=flet.Text(" " + title + " "),
                        bgcolor=flet.colors.WHITE,
                        top=0,
                        left=20
                    )
                ]
            ),
            height=height + 10,
            margin=flet.margin.only(0, 10, 0, 0)
        )