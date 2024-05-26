import datetime
import pandas
import Model
from bokeh.plotting import figure, show
from bokeh.models import HoverTool, DatetimeTickFormatter, Title


class Controller:
    dat_file_path = None
    oldest_timestamp_in_dat = None
    newest_timestamp_in_dat = None
    timezone = None
    frequency = None
    chosen_oldest_date = None
    chosen_newest_date = None

    @staticmethod
    def on_click_generate(e):
        # Получаем значения выбранных дат
        Controller.chosen_oldest_date = Controller._convert_time(
            e.page.data["start_date_picker"].date,
            format_str="%d/%m/%Y"
        )
        Controller.chosen_newest_date = Controller._convert_time(
            e.page.data["end_date_picker"].date,
            format_str="%d/%m/%Y"
        )
        # Проверяем что начальная дата задана не позже конечной даты
        if Controller.chosen_newest_date < Controller.chosen_oldest_date:
            e.page.dialog = e.page.data["alert_box_timerange"]
            e.page.data["alert_box_timerange"].open = True
            e.page.data["start_date_picker"].set_accident_visibility()
            e.page.data["end_date_picker"].set_accident_visibility()
            e.page.update()
        # Если пользователь открыл dat, задал timezone и частоту, то построим графики
        if Controller.dat_file_path and Controller.timezone and Controller.frequency:
            # Получаем информацию о загрузке RAM из dat файла
            Controller.chosen_newest_date += 86400
            epoch_timestamps = []
            ram_usages = []
            ram_usages_percents = []

            raw_data_from_db = Model.Model.get_db_data(
                Controller.dat_file_path,
                "Select Timestamp, real_used From UM_STAT_UM_MEMORY Where Timestamp >= ? AND Timestamp <= ?",
                (
                    Controller.chosen_oldest_date,
                    Controller.chosen_newest_date
                )
            )

            total_ram = Model.Model.get_db_data(
                Controller.dat_file_path,
                "Select real_total From UM_STAT_UM_MEMORY Limit 1")[0][0]

            total_ram = int(total_ram / 1000000)

            for time_and_usage_tpl in raw_data_from_db:
                epoch_timestamps.append(
                    # В bokeh есть древний баг - проблема в дизайне,
                    # он не учитывает timezone для объекта datetime, всё отображается в UTC
                    # поэтому здесь выполняется конвертация datetime в строку, а строки в UTC
                    pandas.Timestamp(
                        Controller._convert_time(
                            time_and_usage_tpl[0],
                            Controller.timezone,
                            "%Y-%m-%d %H:%M:%S")
                    ).tz_localize("UTC")
                )
                ram_usages.append(time_and_usage_tpl[1] / 1000000)

            for ram_usage in ram_usages:
                ram_usages_percents.append(ram_usage / (total_ram / 100))

            # Генерируем график загрузки RAM
            bokeh_source = pandas.DataFrame({"dates": epoch_timestamps,
                                             "values": ram_usages,
                                             "percents": ram_usages_percents})
            bokeh_figure = figure(
                x_axis_type='datetime',
                title=Title(text="RAM usage history", text_font_size="24px", align="center"),
                x_axis_label='Timeline (values were taken every minute)',
                y_axis_label=f'Megabytes (total = {total_ram} Mb)',
                sizing_mode="stretch_width",
                y_range=(0, total_ram),
                tools=[
                    "xpan",
                    "xwheel_zoom",
                    "reset"
                ]
            )
            bokeh_figure.line(x='dates', y='values', source=bokeh_source)
            bokeh_figure.scatter(x='dates', y='values', size=5, source=bokeh_source)
            bokeh_figure.varea(x='dates', y1=0, y2='values', alpha=0.3, source=bokeh_source)

            bokeh_hover = HoverTool(
                tooltips=[('date', '@dates{%d/%m/%Y-%H:%M}'),
                          ('used', '@values{0} Mb'),
                          ('used', '@percents %'),
                          ('total', str(total_ram) + " Mb")],
                formatters={'@dates': 'datetime'}
            )
            bokeh_figure.xaxis.formatter = DatetimeTickFormatter(
                minutes=["%H:%M"],
                hourmin=["%H:%M"],
                hours=["%Y-%m-%d %H:%M"],
                days=["%Y-%m-%d"],
                months=["%Y-%m-%d"]
            )
            bokeh_figure.add_tools(bokeh_hover)
            show(bokeh_figure)
        else:
            e.page.dialog = e.page.data["alert_box_params"]
            e.page.data["alert_box_params"].open = True
            e.page.update()

    @staticmethod
    def pick_files_result(e):
        if e.files:
            # Получаем имя и путь до выбранного dat файла
            Controller.dat_file_path = e.files[0].path
            # Здесь же получаем timestamps из самого dat
            Controller.newest_timestamp_in_dat = (
                Model.Model.get_db_data(Controller.dat_file_path, "Select max(timestamp) From RAD_general")[0][0])
            Controller.oldest_timestamp_in_dat = (
                Model.Model.get_db_data(Controller.dat_file_path, "Select min(timestamp) From RAD_general")[0][0])
            # Получаем значение частоты из dropdown
            Controller.frequency = e.page.data["frequency_picker"].value
            # Обновляем текст отображаемый во View > TextFiled
            e.page.data["dat_path_textfield"].value = Controller.dat_file_path
            e.page.data["dat_path_textfield"].disabled = False
            # Разблокируем выбор timezone и границ дат
            # Сбрасываем значения выбранного ранее timezone и границ дат
            e.page.data["timezone_dropdown"].value = None
            e.page.data["start_date_picker"].content.controls[0].value = None
            e.page.data["end_date_picker"].content.controls[0].value = None
            e.page.data["start_date_picker"].set_button_status(False)
            e.page.data["end_date_picker"].set_button_status(False)
            e.page.data["timezone_dropdown"].disabled = False
            # Разблокируем выбор частоты
            e.page.data["frequency_picker"].disabled = False
            e.page.data["frequency_picker"].value = "1 minute (default)"
            e.page.update()

    @staticmethod
    def on_change_frequency(e):
        Controller.frequency = e.control.value

    @staticmethod
    def on_change_timezone(e):
        # Обновить выбранную timezone для Controller
        Controller.timezone = datetime.timezone(
            datetime.timedelta(
                hours=int(e.page.data["timezone_dropdown"].value.replace("UTC", ""))
            )
        )

        # Отобразить левую границу для выбора даты
        e.page.data["start_date_picker"].set_specific_date(
            Controller._convert_time(
                Controller.oldest_timestamp_in_dat,
                Controller.timezone,
                "%d/%m/%Y"
            )
        )
        e.page.data["start_date_picker"].set_button_status(True)

        # Отобразить правую границу для выбора даты
        e.page.data["end_date_picker"].set_specific_date(
            Controller._convert_time(
                Controller.newest_timestamp_in_dat,
                Controller.timezone,
                "%d/%m/%Y"
            )
        )
        e.page.data["end_date_picker"].set_button_status(True)

        # Передать границы для выбора дат объектам календаря
        e.page.data["pick_date_dialog1"].update_borders_for_datepicker(
            Controller._convert_time(
                Controller.oldest_timestamp_in_dat,
                Controller.timezone
            ),
            Controller._convert_time(
                Controller.newest_timestamp_in_dat,
                Controller.timezone
            )
        )
        e.page.data["pick_date_dialog2"].update_borders_for_datepicker(
            Controller._convert_time(
                Controller.oldest_timestamp_in_dat,
                Controller.timezone
            ),
            Controller._convert_time(
                Controller.newest_timestamp_in_dat,
                Controller.timezone
            )
        )
        e.page.update()

    @staticmethod
    def _convert_time(time, timezone: datetime.timezone = None, format_str: str = None):
        # Преобразование epoch к строке в определённом формате
        if format_str and isinstance(time, int):
            return datetime.datetime.fromtimestamp(time, tz=timezone).strftime(format_str)
        # Преобразование epoch в datetime объект
        elif isinstance(time, int):
            return datetime.datetime.fromtimestamp(time, tz=timezone)
        # Преобразование строки определённого формата в epoch
        elif isinstance(time, str) and format_str:
            return int(datetime.datetime.strptime(time, format_str).timestamp())
