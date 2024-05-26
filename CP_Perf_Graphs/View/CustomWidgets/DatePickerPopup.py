import flet
import copy
import datetime, calendar
import CustomEvents.Event as Event


class PopupCalendar(flet.AlertDialog):
    def __init__(self):
        super().__init__(
            content=CustomCalendar(
                width=230,
                bgcolor="#ef589e",
                font_color="#efefef",
                header_font_color=flet.colors.BLACK,
                hover_color="#c21a4e",
                parent_popup_id=id(self)
            ),
            content_padding=flet.padding.all(0),
            shape=flet.RoundedRectangleBorder(radius=15),
            # Отступы от окна вне самого AlerDialog
            inset_padding=flet.padding.all(10),
            # Отступы от нижней части AlertDialog
            actions_padding=flet.padding.all(0),
            modal=True,
        )

    def update_borders_for_datepicker(self, left_border, right_border):
        self.content.set_date_choose_range(left_border, right_border)


class CustomCalendar(flet.Container):
    _day_of_week = {0: "MO", 1: "TU", 2: "WE", 3: "TH", 4: "FR", 5: "SA", 6: "SU"}
    _months = {1: "JANUARY", 2: "FEBRUARY", 3: "MARCH", 4: "APRIL", 5: "MAY", 6: "JUNE",
               7: "JULY", 8: "AUGUST", 9: "SEPTEMBER", 10: "OCTOBER", 11: "NOVEMBER", 12: "DECEMBER"}

    def __init__(self, width: int, bgcolor="#e2e2e2",
                 font_color="#3c4457", font_color_accent="#ffffff",
                 accent_color="#108ef2", header_font_color="#d2334c",
                 hover_color="#eeeeee", border_radius=15,
                 oldest_date_for_choose: datetime = None,
                 newest_date_for_choose: datetime = None,
                 current_month: int = None, current_year: int = None,
                 parent_popup_id : int = None):
        super().__init__(
            width=width,
            border_radius=border_radius,
            alignment=flet.alignment.center
        )
        self.font_color = font_color
        self.font_accent_color = font_color_accent
        self.header_font_color = header_font_color
        self.font_size = width * 0.045
        self.accent_color = accent_color
        self.hover_color = hover_color
        self.calendar_bgcolor = bgcolor
        self._first_day_in_month, self._last_day_in_month = None, None
        self.content = self._draw_base()
        self._oldest_date_for_choose = oldest_date_for_choose
        self._newest_date_for_choose = newest_date_for_choose
        self._current_year = current_year
        self._current_month = current_month
        self.chosen_date = None
        self._chosen_day_obj = None
        self.parent_popup_id = parent_popup_id

    def set_date_choose_range(self, left_border: datetime, right_border: datetime):
        self._newest_date_for_choose = right_border
        self._oldest_date_for_choose = left_border
        self._current_month = left_border.month
        self._current_year = left_border.year
        self._first_day_in_month, self._last_day_in_month = calendar.monthrange(self._current_year,
                                                                                self._current_month)
        self._print_dates_in_base()

    # Возвращает объект flet.Column - это каркас календаря
    # Внутри таблица для дат + кнопка выбора даты
    def _draw_base(self) -> flet.Column:
        # Шаблон контейнера для даты - отдельный день в календаре
        day_container = flet.Container(
            content=flet.Text(
                value="",
                text_align=flet.TextAlign.CENTER,
                weight=flet.FontWeight.W_500,
                size=self.font_size + 2,
                color=self.font_color
            ),
            width=(self.width - self.width * 0.05) / 8,
            height=self.width / 8,
            alignment=flet.alignment.center,
            shape=flet.BoxShape.CIRCLE,
            on_hover=self._on_hover_date,
            on_click=self._on_choose_day
        )
        # Сам каркас календаря
        custom_calendar = flet.Column(
            controls=[flet.Container(
                flet.Column(
                    controls=[
                        # Заголовок с названием месяца и годом, кнопками для перелистывания календаря
                        flet.Row(
                            controls=[
                                flet.Container(flet.IconButton(
                                    icon=flet.icons.KEYBOARD_ARROW_LEFT_SHARP,
                                    height=self.width / 11,
                                    width=self.width / 7,
                                    icon_size=self.font_size + self.font_size * 0.7,
                                    padding=0,
                                    icon_color=self.font_color,
                                    data="left_flip",
                                    on_click=self._flip_calendar
                                ),
                                    height=self.width / 8,
                                    alignment=flet.alignment.center
                                ),
                                flet.Container(flet.Text(
                                    value="",
                                    spans=[
                                        flet.TextSpan("",
                                                      flet.TextStyle(weight=flet.FontWeight.BOLD))
                                    ],
                                    weight=flet.FontWeight.W_400,
                                    color=self.font_color,
                                    size=self.font_size + 2,
                                    text_align=flet.alignment.center,
                                ),
                                    height=self.width / 8,
                                    alignment=flet.alignment.center
                                ),
                                flet.Container(flet.IconButton(
                                    icon=flet.icons.KEYBOARD_ARROW_RIGHT_SHARP,
                                    icon_size=self.font_size + self.font_size * 0.7,
                                    height=self.width / 10,
                                    width=self.width / 7,
                                    padding=0,
                                    data="right_flip",
                                    on_click=self._flip_calendar,
                                    icon_color=self.font_color
                                ),
                                    height=self.width / 8,
                                    alignment=flet.alignment.center
                                ),
                            ],
                            alignment=flet.MainAxisAlignment.CENTER,
                            vertical_alignment=flet.CrossAxisAlignment.START,
                        ),
                        # Заголовок с днями недели
                        flet.Row(
                            controls=[
                                flet.Text(
                                    value=CustomCalendar._day_of_week.get(i),
                                    text_align=flet.TextAlign.CENTER,
                                    width=(self.width - self.width * 0.08) / 7.8,
                                    weight=flet.FontWeight.W_400,
                                    size=self.font_size,
                                    color=self.header_font_color,
                                    height=self.width / 8,
                                ) for i in range(0, 7)
                            ],
                            alignment=flet.MainAxisAlignment.CENTER,
                            height=self.width / 10,
                            # Убирает лишние отступы между элементами Row
                            spacing=0
                        ),
                        # Пять строк на даты, создаём их и распаковываем в controls
                        *[flet.Row(
                            controls=[copy.deepcopy(day_container) for i in range(0, 7)],
                            alignment=flet.MainAxisAlignment.CENTER,
                            spacing=0
                        ) for i in range(0, 5)],
                    ],
                    # Убирает лишние отступы между элементами Column
                    spacing=0
                ),
                border_radius=self.border_radius,
                bgcolor=self.calendar_bgcolor,
                padding=flet.padding.only(0, self.width * 0.08, 0, self.width * 0.05),
            )
            ],
            horizontal_alignment=flet.CrossAxisAlignment.CENTER
        )
        custom_calendar.controls[0].content.controls.append(
            # Кнопки для отмены и выбора
            flet.Container(
                content=flet.Row(
                    controls=[
                        flet.TextButton(
                            text="Choose",
                            style=flet.ButtonStyle(color="#efefef"),
                            on_click=CustomCalendar._on_close_popup_calendar
                        )
                    ],
                    alignment=flet.MainAxisAlignment.CENTER,
                    spacing=15
                ),
                margin=flet.margin.only(0, 5, 0, 0)
            )
        )
        return custom_calendar

    # Отображаем даты в зависимости от текущего года и месяца
    def _print_dates_in_base(self):
        # Устанавливаем значение месяца и года в заголовке календаря
        self.content.controls[0].content.controls[0].controls[1].content.value = CustomCalendar._months.get(
            self._current_month)
        self.content.controls[0].content.controls[0].controls[1].content.spans[0].text = " " + str(
            self._current_year)
        day_counter = 1

        for row_id, row in enumerate(self.content.controls[0].content.controls):
            # Первые две строки это заголовки календаря
            # Строка с индексом 7 это кнопки для отмены и выбора
            if row_id < 2 or row_id == 7:
                continue
            for column_id, cell in enumerate(row.controls):
                if row_id - 2 == 0 and column_id < self._first_day_in_month:
                    cell.content.value = "ꟷ"
                    cell.content.weight = flet.FontWeight.W_200
                    cell.on_hover = None
                    cell.on_click = None
                    cell.bgcolor = flet.colors.GREY_400
                elif self._last_day_in_month >= day_counter:
                    cell.content.value = str(day_counter)
                    cell.content.weight = flet.FontWeight.W_500
                    if (self.chosen_date and (day_counter == self.chosen_date.day and
                            self._current_month == self.chosen_date.month and
                            self._current_year == self.chosen_date.year)):
                        self._chosen_day_obj = cell
                        cell.bgcolor = self.accent_color
                        cell.data = "chosen"
                    else:
                        cell.bgcolor = self.calendar_bgcolor
                    cell.content.color = self.font_color
                    cell.on_hover = self._on_hover_date
                    cell.on_click = self._on_choose_day
                    # Если этот день не попадает в диапазон выбора дат, то он отображается неактивным
                    if ((self._current_month == self._oldest_date_for_choose.month and
                         day_counter < self._oldest_date_for_choose.day) or
                            (self._current_month == self._newest_date_for_choose.month and
                             day_counter > self._newest_date_for_choose.day)):
                        cell.on_hover = None
                        cell.on_click = None
                        cell.bgcolor = flet.colors.GREY_400
                    day_counter += 1
                else:
                    cell.content.value = "ꟷ"
                    cell.content.weight = flet.FontWeight.W_200
                    cell.on_hover = None
                    cell.on_click = None
                    cell.bgcolor = flet.colors.GREY_400

    def _on_hover_date(self, e: flet.ControlEvent):
        # Когда мышь на элементе e.data = "true"
        e.control.bgcolor = self.hover_color if e.data == "true" and e.control.data != "chosen" else \
            (self.accent_color if e.control.data == "chosen" else self.calendar_bgcolor)
        e.control.update()

    def _flip_calendar(self, e: flet.ControlEvent):
        flip_occur = False
        if e.control.data == "left_flip":
            if (self._current_month - 1 > 0 and
                    self._current_month - 1 >= self._oldest_date_for_choose.month):
                self._current_month = self._current_month - 1
                flip_occur = True
            elif (self._current_month - 1 >= self._oldest_date_for_choose.month and
                  self._current_year - 1 >= self._oldest_date_for_choose.year):
                self._current_month = 12
                self._current_year = self._current_year - 1
                flip_occur = True
        elif e.control.data == "right_flip":
            if (self._current_month + 1 < 12 and
                    self._current_month + 1 <= self._newest_date_for_choose.month):
                self._current_month = self._current_month + 1
                flip_occur = True
            elif (self._current_month + 1 <= self._newest_date_for_choose.month and
                  self._current_year + 1 <= self._newest_date_for_choose.year):
                self._current_month = 1
                self._current_year = self._current_year + 1
                flip_occur = True
        self._first_day_in_month, self._last_day_in_month = calendar.monthrange(self._current_year,
                                                                                self._current_month)
        if flip_occur:
            if self._chosen_day_obj:
                self._chosen_day_obj.data = ""
                self._chosen_day_obj = None
            self._print_dates_in_base()
            self.content.update()

    def _on_choose_day(self, e: flet.ControlEvent):
        if self._chosen_day_obj:
            self._chosen_day_obj.bgcolor = self.calendar_bgcolor
            self._chosen_day_obj.data = ""
            self._chosen_day_obj.update()
        self._chosen_day_obj = e.control
        self.chosen_date = datetime.datetime(
            day=int(e.control.content.value),
            month=self._current_month,
            year=self._current_year
        )
        e.control.bgcolor = self.accent_color
        e.control.data = "chosen"
        e.control.update()
        Event.Event("update_datepicker_form_" + str(self.parent_popup_id),
                    self.chosen_date.strftime("%d/%m/%Y"))

    @staticmethod
    def _on_close_popup_calendar(e: flet.ControlEvent):
        # Закрываем отображение datepicker диалога
        e.control.parent.parent.parent.parent.parent.parent.parent.open = False
        e.page.update()
