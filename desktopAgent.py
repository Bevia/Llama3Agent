import subprocess
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput


class MyApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical')

        # Create a label to display information
        label1 = Label(text='This is my Android AI app')

        # Create a TextInput widget to ask for user input
        # I want to know more abut private agents
        text_input = TextInput(hint_text='Enter your text here', multiline=False)

        # Create a button that will handle user interaction
        button = Button(text='Submit')

        # Define what happens when the button is pressed
        def on_button_press(instance):
            user_text = text_input.text  # Get the text entered by the user

            # Call the second Python file with the user input as an argument
            subprocess.run(['python3', 'llamaAgent.py', user_text])

        button.bind(on_press=on_button_press)  # Bind the button press event to the function

        # Add widgets to the layout
        layout.add_widget(label1)
        layout.add_widget(text_input)
        layout.add_widget(button)

        return layout


if __name__ == '__main__':
    MyApp().run()