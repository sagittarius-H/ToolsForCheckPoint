import flet
import Controller
import View.CustomWidgets.TitledContainer as TitledContainer
import View.CustomWidgets.PinkButton as PinkButton
import View.CustomWidgets.MessageBox as MessageBox
import View.CustomWidgets.DatePickerForm as DatePicker
import View.CustomWidgets.DatePickerPopup as PopupCalendar
import CustomEvents.Observer as Observer


class MainScreen:
    @staticmethod
    def main(page: flet.Page):
        # Словарь для сохранения ссылок на все объекты-виджеты вне их контейнеров
        page.data = {}
        # Выравнивание внутри Page
        page.vertical_alignment = flet.MainAxisAlignment.CENTER
        page.horizontal_alignment = flet.CrossAxisAlignment.CENTER
        # Параметры окна
        page.window_height = 320
        page.window_width = 720
        page.window_resizable = False
        page.window_maximizable = False
        page.window_center()
        page.title = "CheckPoint Performance Graphs"

        # Диалог для открытия файла базы данных
        pick_files_dialog = flet.FilePicker(on_result=Controller.Controller.pick_files_result)
        page.overlay.append(pick_files_dialog)

        # Кнопки генерации графиков и открытия базы данных
        generate_button = PinkButton.PinkButton(text="Generate CPU/RAM Graphs",
                                                width=320,
                                                height=40,
                                                on_click_method=Controller.Controller.on_click_generate,
                                                )

        browse_button = PinkButton.PinkButton(text="Open .dat file",
                                              width=153,
                                              height=40,
                                              on_click_method=pick_files_dialog.pick_files
                                              )

        # Выбор временной зоны, нужен для правильной конвертации Epoch в datetime
        timezone_dropdown = flet.Dropdown(
            width=153,
            height=40,
            content_padding=flet.padding.only(20, 0, 20, 0),
            text_size=13,
            label="Timezone",
            hint_text="Timezone",
            hint_style=flet.TextStyle(size=13),
            icon_size=30,
            options=[
                flet.dropdown.Option("UTC-12"),
                flet.dropdown.Option("UTC-11"),
                flet.dropdown.Option("UTC-10"),
                flet.dropdown.Option("UTC-9"),
                flet.dropdown.Option("UTC-8"),
                flet.dropdown.Option("UTC-7"),
                flet.dropdown.Option("UTC-6"),
                flet.dropdown.Option("UTC-5"),
                flet.dropdown.Option("UTC-4"),
                flet.dropdown.Option("UTC-3"),
                flet.dropdown.Option("UTC-2"),
                flet.dropdown.Option("UTC-1"),
                flet.dropdown.Option("UTC+0"),
                flet.dropdown.Option("UTC+1"),
                flet.dropdown.Option("UTC+2"),
                flet.dropdown.Option("UTC+3"),
                flet.dropdown.Option("UTC+4"),
                flet.dropdown.Option("UTC+5"),
                flet.dropdown.Option("UTC+6"),
                flet.dropdown.Option("UTC+7"),
                flet.dropdown.Option("UTC+8"),
                flet.dropdown.Option("UTC+9"),
                flet.dropdown.Option("UTC+10"),
                flet.dropdown.Option("UTC+11"),
                flet.dropdown.Option("UTC+12"),
            ],
            on_change=Controller.Controller.on_change_timezone,
            disabled=True
        )
        page.data["timezone_dropdown"] = timezone_dropdown

        # TextField для отображения пути до выбранной базы данных cpview
        dat_path_textfield = flet.TextField(
            label="Path to selected cpview_services.dat ...",
            text_size=12,
            read_only=True,
            disabled=True,
            width=477,
            height=40,
            content_padding=flet.padding.only(20, 3, 3, 3),
        )
        page.data["dat_path_textfield"] = dat_path_textfield

        # AlertDialog для отображения ошибки если пользователь не указал параметры или путь БД
        alert_box = MessageBox.MessageBox(
            text="You won't be able to create graphs until you:\n\n • Open a cpview_services.dat.\n "
                 "• Specify correct parameters in second step.",
            text_color=flet.colors.WHITE,
            bgcolor="#ff3d83",
            height=80,
            padding=flet.padding.only(100, 0, 100, 0),
            padding_content=flet.padding.only(0, 0, 0, 60)
        )
        page.data["alert_box"] = alert_box

        # Диалоги с календарём для выбора дат
        pick_date_dialog1 = PopupCalendar.PopupCalendar()
        page.data["pick_date_dialog2"] = pick_date_dialog1

        pick_date_dialog2 = PopupCalendar.PopupCalendar()
        page.data["pick_date_dialog1"] = pick_date_dialog2

        # Выбор начальной даты для построения графика - кнопка контейнер
        start_date_picker = DatePicker.DatePickerForm(pick_date_dialog1)
        page.data["start_date_picker"] = start_date_picker
        Observer.Observer(
            "update_datepicker_form_" + str(id(pick_date_dialog1)),
            callback=start_date_picker.set_specific_date,
            obj=start_date_picker
        )

        # Выбор конечной даты для построения графика - кнопка контейнер
        end_date_picker = DatePicker.DatePickerForm(pick_date_dialog2)
        page.data["end_date_picker"] = end_date_picker
        Observer.Observer(
            "update_datepicker_form_" + str(id(pick_date_dialog2)),
            callback=end_date_picker.set_specific_date,
            obj=end_date_picker
        )

        # Выбор частоты вывода показаний на график
        frequency_picker = flet.Dropdown(
            width=310,
            height=40,
            text_size=13,
            content_padding=flet.padding.only(20, 0, 20, 0),
            label="Frequency",
            value="1 minute (default)",
            options=[
                flet.dropdown.Option("1 minute (default)"),
                flet.dropdown.Option("5 minutes"),
                flet.dropdown.Option("10 minutes"),
                flet.dropdown.Option("30 minutes"),
                flet.dropdown.Option("1 hour")
            ],
            disabled=True
        )

        # Верхний контейнер
        first_container = TitledContainer.TitledContainer(
            width=page.window_width - 40,
            title="1 Step - Choose cpview_services.dat file:",
            content=flet.Row(
                controls=[
                    dat_path_textfield,
                    browse_button
                ],
                alignment=flet.MainAxisAlignment.SPACE_BETWEEN
            ),
            height=80
        )

        # Нижний контейнер
        second_container = TitledContainer.TitledContainer(
            width=page.window_width - 40,
            title="2 Step - Specify correct parameters and generate graphs:",
            content=flet.Column(
                controls=[
                    flet.Row(
                        controls=[
                            timezone_dropdown,
                            flet.Text("Start date:"),
                            start_date_picker,
                            flet.Text("End date:"),
                            end_date_picker
                        ]
                    ),
                    flet.Row(
                        controls=[
                            frequency_picker,
                            generate_button
                        ],
                        alignment=flet.MainAxisAlignment.SPACE_BETWEEN
                    ),
                ]
            ),
            height=130
        )

        # Добавление элементов в Page
        page.add(
            first_container,
            second_container
        )
