import os
import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.config import Config
##################
# Configure Kivy #
##################
kivy.require('1.10.0')
Config.set('graphics', 'width', '1200')
Config.set('graphics', 'height', '700')
Config.write()
##################
##################


class Main(BoxLayout):
    def __init__(self):
        super(Main, self).__init__()
        self.log_box = self.ids['log_box']
        self.__file_list = []
        self.__export_dir = ''
        self.log_box.text = """Please choose .enex file(s) on the left and the output directory on the right."""

    def update_export_dir(self, paths):
        self.__export_dir = ''
        if os.path.isdir(paths[0]):
            self.__export_dir = paths[0]

    def update_file_list(self, paths):
        self.__file_list = []
        for path in paths:
            if '.enex' in path:
                self.__file_list.append(path)


class MainApp(App):
    def build(self):
        return Main()


if __name__ == '__main__':
    MainApp().run()
