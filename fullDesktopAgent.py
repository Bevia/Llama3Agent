import sys
import subprocess
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.core.clipboard import Clipboard  # Import Clipboard


class MyApp(App):
    def build(self):
        # Set the window title
        self.title = "Bevia's Llama 3 Chat Agent"

        # Main layout: vertical box layout
        layout = BoxLayout(orientation='vertical')

        # Create a TextInput widget for displaying the response from the script, with a larger size hint
        self.response_display = TextInput(readonly=True, multiline=True, hint_text='Response will appear here...',
                                          size_hint=(1, 0.7))  # Takes 70% of the available vertical space

        # Create a TextInput widget to ask for user input with a smaller size hint
        self.text_input = TextInput(hint_text='Aske me anything you want :)', multiline=False, size_hint=(1, 0.15))  # 15%

        # Create a horizontal BoxLayout to hold the "Submit", "Clear", and "Copy" buttons
        button_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.15))  # 15% height for buttons

        # Create a "Submit" button with a green background color (RGBA)
        submit_button = Button(text='Submit', background_color=(0, 0.5, 0, 1), background_normal='')

        # Bind the button press event to the function
        submit_button.bind(on_press=self.on_button_press)

        # Create a "Clear" button with a red background color (RGBA)
        clear_button = Button(text='Clear', background_color=(0.5, 0, 0, 1), background_normal='')

        # Bind the clear button press event to clear the text fields
        clear_button.bind(on_press=self.on_clear_press)

        # Create a "Copy" button to copy the response to the clipboard
        copy_button = Button(text='Copy', background_color=(0.5, 0.5, 0.5, 1), background_normal='')

        # Bind the copy button to the function that copies text to the clipboard
        copy_button.bind(on_press=self.on_copy_press)

        # Add the buttons to the horizontal layout
        button_layout.add_widget(submit_button)
        button_layout.add_widget(clear_button)
        button_layout.add_widget(copy_button)  # Add the copy button

        # Add widgets to the main layout
        layout.add_widget(self.text_input)
        layout.add_widget(button_layout)  # Add the horizontal layout with buttons
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

    def on_clear_press(self, instance):
        # Clear the text input and response display fields
        self.text_input.text = ''
        self.response_display.text = ''

    def on_copy_press(self, instance):
        # Copy the response text to the clipboard
        Clipboard.copy(self.response_display.text)


if __name__ == '__main__':
    MyApp().run()