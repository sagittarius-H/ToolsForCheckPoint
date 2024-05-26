import flet
import CustomEvents.Event as Event
import View.CustomWidgets.DatePickerPopup as DatePickerPopup


class DatePickerForm(flet.Container):
    def __init__(self, popup_calendar: DatePickerPopup, button_status=False):
        # Объект календаря для выбора даты
        self.popup_calendar = popup_calendar
        # Активная ли кнопка для открытия календаря
        self.button_status = button_status
        # Выбранная в календаре дата
        self.date = None
        super().__init__(
            content=flet.Row(
                controls=[
                    # Отображаем выбранную дату
                    flet.TextField(
                        label="DD/MM/YY",
                        text_size=12,
                        read_only=True,
                        disabled=True,
                        width=110,
                        height=40
                    ),
                    # Кнопка иконка с bgcolor и hover color - выбор даты
                    flet.Container(
                        content=flet.Icon(
                            name=flet.icons.CALENDAR_MONTH_ROUNDED,
                            color=DatePickerForm._set_icon_color_according_status(button_status)
                        ),
                        ink=True,
                        ink_color="#c60c4e",
                        on_click=self._on_click_button_container,
                        bgcolor="#efefef",
                        on_hover=DatePickerForm._on_hover_button_container,
                        border_radius=5,
                        height=40,
                        width=40,
                        disabled=not button_status
                    )
                ]
            )
        )

    # Метод для активации/деактивации кнопки выбора даты
    def set_button_status(self, value: bool):
        self.button_status = value
        self.content.controls[1].content.color = DatePickerForm._set_icon_color_according_status(value)
        self.content.controls[1].disabled = not value

    # Метод для отображения выбранной даты в TextField
    def set_specific_date(self, date: str):
        self.date = date
        self.content.controls[0].value = date
        self.content.controls[0].disabled = False
        Event.Event("unset_accident_visibility")

    # При неправильно выбранной дате можно задать состояние ошибки
    def set_accident_visibility(self):
        self.content.controls[0].border_color = flet.colors.RED
        self.content.controls[0].color = flet.colors.RED
        self.content.controls[0].label_style = flet.TextStyle(
            color=flet.colors.RED
        )
        self.content.controls[0].border = flet.InputBorder.OUTLINE
        self.content.controls[0].border_width = 2

    # При возникновении CustomEvent или ручном вызове можно снять состояние ошибки
    def unset_accident_visibility(self):
        self.content.controls[0].border_color = None
        self.content.controls[0].color = None
        self.content.controls[0].label_style = None
        self.content.controls[0].border = None
        self.content.controls[0].border_width = 1

    @staticmethod
    def _set_icon_color_according_status(button_status: bool):
        if button_status:
            return flet.colors.BLACK
        else:
            return flet.colors.GREY

    @staticmethod
    def _on_hover_button_container(e: flet.ControlEvent):
        e.control.bgcolor = "#ef589e" if e.data == "true" else "#efefef"
        e.control.content.color = flet.colors.WHITE if e.data == "true" else flet.colors.BLACK
        e.control.update()

    def _on_click_button_container(self, e: flet.ControlEvent):
        # Открываем popup календарь для выбора даты
        e.page.dialog = self.popup_calendar
        self.popup_calendar.open = True
        e.page.update()
