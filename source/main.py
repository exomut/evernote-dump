import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout

kivy.require('1.10.0')


class Main(BoxLayout):
    def __init__(self):
        super(Main, self).__init__()


class MainApp(App):
    def build(self):
        return Main()


if __name__ == '__main__':
    MainApp().run()
