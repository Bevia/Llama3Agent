import sys
import subprocess
import threading
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.core.clipboard import Clipboard
from kivy.clock import Clock
from kivy.uix.image import Image
from kivy.uix.floatlayout import FloatLayout


class MyApp(App):
    def build(self):
        # Root layout using FloatLayout to allow overlay of widgets
        root_layout = FloatLayout()

        # Main content layout (everything that is not the spinner)
        main_layout = BoxLayout(orientation='vertical', size_hint=(1, 1))

        # Create a TextInput widget for displaying the response from the script
        self.response_display = TextInput(readonly=True, multiline=True, hint_text='Response will appear here...',
                                          size_hint=(1, 0.7))  # Takes 70% of the available vertical space

        # Create a TextInput widget to ask for user input with a smaller size hint
        self.text_input = TextInput(hint_text='Ask me anything you want :)', multiline=False, size_hint=(1, 0.15))  # 15%

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

        # Add widgets to the main layout (the normal content)
        main_layout.add_widget(self.text_input)
        main_layout.add_widget(button_layout)  # Add the horizontal layout with buttons
        main_layout.add_widget(self.response_display)

        # Add the main layout to the root FloatLayout
        root_layout.add_widget(main_layout)

        # Create an Image widget for animating the spinner frames
        self.loading_spinner = Image(source='loader_01.png', size_hint=(None, None), size=(200, 200))
        self.loading_spinner.opacity = 0  # Hide spinner initially

        # Center the spinner in the FloatLayout (overlay)
        self.loading_spinner.pos_hint = {'center_x': 0.5, 'center_y': 0.5}
        root_layout.add_widget(self.loading_spinner)  # Add spinner as overlay on top of everything

        # Setup the frame sequence for animation
        self.spinner_frames = ['loader_02.png', 'loader_03.png',
                               'loader_04.png', 'loader_05.png',
                               'loader_06.png', 'loader_07.png',
                               'loader_08.png', 'loader_09.png',
                               'loader_10.png', 'loader_11.png',
                               'loader_12.png', 'loader_13.png',
                               'loader_14.png', 'loader_15.png',
                               'loader_16.png', 'loader_17.png',
                               'loader_18.png', 'loader_19.png',
                               'loader_20.png', 'loader_21.png']  # Add more if needed
        self.current_frame = 0

        return root_layout

    def on_button_press(self, instance):
        user_text = self.text_input.text  # Get the text entered by the user

        # Show loading spinner while waiting for response
        self.show_spinner()

        # Create a new thread to handle the subprocess call
        threading.Thread(target=self.run_llama_agent, args=(user_text,)).start()

    def run_llama_agent(self, user_text):
        # Call the second Python file with the user input as an argument and capture the output
        result = subprocess.run([sys.executable, 'llamaAgent.py', user_text],
                                capture_output=True, text=True)

        # Get the response from the script
        response_text = result.stdout.strip()

        # Schedule the UI update on the main thread
        Clock.schedule_once(lambda dt: self.update_response(response_text))

    def update_response(self, response_text):
        # Hide the loading spinner and update the TextInput widget with the response
        self.hide_spinner()
        self.response_display.text = response_text

    def show_spinner(self):
        # Show the spinner and start frame animation
        self.loading_spinner.opacity = 1
        self.animate_spinner()

    def animate_spinner(self, *args):
        # Cycle through the spinner frames
        self.current_frame = (self.current_frame + 1) % len(self.spinner_frames)
        self.loading_spinner.source = self.spinner_frames[self.current_frame]

        # Schedule the next frame update (e.g., every 0.1 seconds)
        Clock.schedule_once(self.animate_spinner, 0.1)

    def hide_spinner(self):
        # Hide the spinner
        self.loading_spinner.opacity = 0
        Clock.unschedule(self.animate_spinner)  # Stop the animation

    def on_clear_press(self, instance):
        # Clear the text input and response display fields
        self.text_input.text = ''
        self.response_display.text = ''

    def on_copy_press(self, instance):
        # Copy the response text to the clipboard
        Clipboard.copy(self.response_display.text)


if __name__ == '__main__':
    MyApp().run()