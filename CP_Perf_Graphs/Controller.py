import flet
import View.MainScreen as MainScreen

class Controller:
    dat_file_path = ""
    dat_file_name = ""

    @staticmethod
    def on_click_pass(e):
        pass

    @staticmethod
    def pick_files_result(e):
        # получаем имя и путь до выбранного dat файла
        Controller.dat_file_path = e.files[0].path
        Controller.dat_file_name = e.files[0].name
        # обновляем текст отображаемый во View > TextFiled
        MainScreen.MainScreen.page_controls.get("dat_path_textfield").value = Controller.dat_file_path
        MainScreen.MainScreen.page_controls.get("dat_path_textfield").disabled = False
        # вызываем перерисовку View
        MainScreen.MainScreen.page_obj.update()
