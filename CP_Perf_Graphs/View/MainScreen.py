import flet
import Controller
import View.CustomWidgets.TitledContainer as TitledContainer
import View.CustomWidgets.PinkButton as PinkButton
import View.CustomWidgets.MessageBox as MessageBox

class MainScreen:
    # Атрибуты для хранения ссылки на объект page и UI компонентов
    page_controls = {}
    page_obj = None

    @staticmethod
    def main(page: flet.Page):
        # сохраняем объект в атрибуте класса, это нужно для Controller
        MainScreen.page_obj = page
        # выравнивание внутри Page
        page.vertical_alignment = flet.MainAxisAlignment.CENTER
        page.horizontal_alignment = flet.CrossAxisAlignment.CENTER
        # параметры окна
        page.window_height = 275
        page.window_width = 620
        page.window_resizable = False
        page.window_maximizable = False
        page.window_center()
        page.title = "CheckPoint Performance Graphs"
        # диалог для открытия файла базы данных
        pick_files_dialog = flet.FilePicker(on_result=Controller.Controller.pick_files_result)
        page.overlay.append(pick_files_dialog)
        # добавление ссылки на элемент UI в словарь
        MainScreen.page_controls["pick_files_dialog"] = pick_files_dialog
        # кнопки генерации графиков и открытия базы данных
        generate_button = PinkButton.PinkButton(text="Generate CPU/RAM Graphs",
                                                height=40,
                                                on_click_method=Controller.Controller.on_click_generate)
        MainScreen.page_controls["generate_button"] = generate_button
        browse_button = PinkButton.PinkButton(text="Open .dat file",
                                                height=40,
                                                on_click_method=pick_files_dialog.pick_files)
        MainScreen.page_controls["browse_button"] = browse_button
        # выбор временной зоны нужен для правильной конвертации Epoch в datetime
        timezone_picker = flet.Dropdown(
            width=300,
            height=40,
            content_padding=flet.padding.only(20, 0, 20, 0),
            text_size=13,
            hint_text="Choose GW/SMS timezone",
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
        )
        MainScreen.page_controls["timezone_picker"] = timezone_picker
        # TextField для отображения пути до выбранной базы данных
        dat_path_textfield = flet.TextField(
            label="Path to selected cpview_services.dat ...",
            text_size=12,
            read_only=True,
            disabled=True,
            width=390,
            height=40,
            content_padding=flet.padding.only(20,3,3,3),
        )
        MainScreen.page_controls["dat_path_textfield"] = dat_path_textfield
        # AlertDialog для отображения ошибки
        alert_box = MessageBox.MessageBox(
            text="You won't be able to create graphs until you open a cpview_services.dat "
                 "file and specify correct timezone in dropdown menu",
            text_color=flet.colors.WHITE,
            bgcolor="#ff3d83",
            height=80,
            on_close_method=Controller.Controller.on_close_message_box
        )
        MainScreen.page_controls["alert_box"] = alert_box
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
            title="2 Step - Specify correct timezone and generate graphs:",
            content=flet.Row(
                controls=[
                    timezone_picker,
                    generate_button
                ],
                alignment=flet.MainAxisAlignment.SPACE_BETWEEN
            ),
            height=80
        )
        # добавление элементов в Page
        page.add(
            first_container,
            second_container
        )
