from kivy.app import App
from kivy.uix.label import Label


class MyApp(App):
    def build(self):
        return Label(text='this is my android AI app')


if __name__ == '__main__':
    MyApp().run()
