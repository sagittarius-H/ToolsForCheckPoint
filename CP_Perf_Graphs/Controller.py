import datetime
import pandas
import Model
import View.MainScreen as MainScreen
from bokeh.plotting import figure, show
from bokeh.models import HoverTool, DatetimeTickFormatter, Title

class Controller:
    dat_file_path = None

    @staticmethod
    def on_click_generate(e):
        # получаем значение временной зоны, которую пользователь выбрал в dropdown
        user_timezone = MainScreen.MainScreen.page_controls.get("timezone_picker").value
        if Controller.dat_file_path and user_timezone:
            # получаем информацию о загрузке RAM из dat файла
            epoch_timestamps = []
            ram_usages = []
            tz_user = datetime.timezone(datetime.timedelta(hours=int(user_timezone.replace("UTC", ""))))
            raw_data_from_db = Model.Model.get_db_data(Controller.dat_file_path,
                                                     "Select Timestamp, real_used From UM_STAT_UM_MEMORY")
            total_ram = Model.Model.get_db_data(Controller.dat_file_path,
                                                "Select real_total From UM_STAT_UM_MEMORY Limit 1")[0][0]
            total_ram = int(total_ram / 1000000)
            for couple_time_usage in raw_data_from_db:
                epoch_timestamps.append(datetime.datetime.fromtimestamp(couple_time_usage[0], tz=tz_user))
                ram_usages.append(couple_time_usage[1] / 1000000)
            # генерируем график загрузки RAM
            bokeh_source = pandas.DataFrame({"dates": epoch_timestamps, "values": ram_usages})
            bokeh_figure = figure(
                x_axis_type='datetime',
                title=Title(text="RAM usage history", text_font_size="24px", align="center"),
                x_axis_label='Timeline (values were taken every minute)',
                y_axis_label=f'Megabytes (total = {total_ram} Mb)',
                sizing_mode = "stretch_width",
                # sizing_mode='stretch_both',
                y_range=(0, total_ram),
            )
            bokeh_figure.line(x='dates', y='values', source=bokeh_source)
            bokeh_figure.scatter(x='dates', y='values', size=5, source=bokeh_source)
            bokeh_figure.varea(x='dates', y1=0, y2='values', alpha=0.3, source=bokeh_source)
            bokeh_hover = HoverTool(
                tooltips=[('date', '@dates{%d/%m/%Y-%H:%M}'),
                          ('used', '@values{0} Mb'),
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
            MainScreen.MainScreen.page_obj.dialog = MainScreen.MainScreen.page_controls.get("alert_box")
            MainScreen.MainScreen.page_controls.get("alert_box").open = True
            MainScreen.MainScreen.page_obj.update()

    @staticmethod
    def on_close_message_box(e):
        MainScreen.MainScreen.page_controls.get("alert_box").open = False
        MainScreen.MainScreen.page_obj.update()

    @staticmethod
    def pick_files_result(e):
        # получаем имя и путь до выбранного dat файла
        if e.files:
            Controller.dat_file_path = e.files[0].path
            Controller.dat_file_name = e.files[0].name
        # обновляем текст отображаемый во View > TextFiled
        MainScreen.MainScreen.page_controls.get("dat_path_textfield").value = Controller.dat_file_path
        MainScreen.MainScreen.page_controls.get("dat_path_textfield").disabled = False
        # вызываем перерисовку View
        MainScreen.MainScreen.page_obj.update()
