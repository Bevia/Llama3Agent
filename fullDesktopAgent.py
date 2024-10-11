import sys
import subprocess
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput


class MyApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical')

        # Create a TextInput widget for displaying the response from the script, with a larger size hint
        self.response_display = TextInput(readonly=True, multiline=True, hint_text='Response will appear here...',
                                          size_hint=(1, 0.7))  # Takes 70% of the available vertical space

        # Create a TextInput widget to ask for user input with a smaller size hint
        self.text_input = TextInput(hint_text='Enter your text here', multiline=False, size_hint=(1, 0.15))  # 15%

        # Create a button with a smaller size hint
        button = Button(text='Submit', size_hint=(1, 0.15))  # 15%

        # Bind the button press event to the function
        button.bind(on_press=self.on_button_press)

        # Add widgets to the layout
        layout.add_widget(self.text_input)
        layout.add_widget(button)
        layout.add_widget(self.response_display)

        return layout

    def on_button_press(self, instance):
        user_text = self.text_input.text  # Get the text entered by the user

        # Call the second Python file with the user input as an argument and capture the output
        result = subprocess.run([sys.executable, 'llamaAgent.py', user_text],
                                capture_output=True, text=True)

        # Get the response from the script
        response_text = result.stdout.strip()

        # Update the TextInput widget with the response from the second script
        self.response_display.text = response_text


if __name__ == '__main__':
    MyApp().run()