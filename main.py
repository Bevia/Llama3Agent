from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button


class MyApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical')
        label1 = Label(text='this is my android AI app')
        label2 = Label(text='label 2')
        button = Button(text='Press me')
        layout.add_widget(label1)
        layout.add_widget(label2)
        layout.add_widget(button)

        return layout


if __name__ == '__main__':
    MyApp().run()
