import os
import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.config import Config
from evernote_dump import evernote_dump
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
        self.ids['export_dir_chooser'].path = os.getcwd()
        self.ids['enex_file_chooser'].path = os.getcwd()
        self.__file_list = []
        self.__export_dir = ''
        self.write_message("Please choose .enex files on the left.")
        self.write_message("Select the output directory on the right.")
        self.write_message("Click 'RUN PARSE' when you are ready.")

    def start_parse(self):
        if len(self.__file_list) > 0:
            self.write_message("Parsing has begun. This may take a while depending on .enex file size.")
            self.write_message("Processing ...")
            evernote_dump.run_parse(self.__file_list, self.__export_dir)
            self.write_message("Finished!!")
            self.write_message("Check the console for more information.")
            self.write_message("Choose more files or close the app.")
        else:
            self.write_message("Please Choose a .enex file.")

    def update_export_dir(self, paths):
        self.__export_dir = ''
        if os.path.isdir(paths[0]):
            self.__export_dir = paths[0]
        self.ids['export_path_label'].text = f'Export Path: {self.__export_dir}'

    def update_file_list(self, paths):
        self.__file_list = []
        for path in paths:
            if '.enex' in path:
                self.__file_list.append(path)
        self.ids['file_count_label'].text = f'Enex Files: {len(self.__file_list)}'

    def write_message(self, message):
        self.ids['log_box'].text += f'> {message}\n\n'


class MainApp(App):
    def build(self):
        return Main()


if __name__ == '__main__':
    MainApp().run()
