import sys
import ollama

# Get the user input passed from the Kivy app
if len(sys.argv) > 1:
    user_input = sys.argv[1]
else:
    user_input = "I want to know more about private agents"  # Default message if no input is provided

response = ollama.chat(model="llama3", messages=[
    {
        "role": "user",
        "content": user_input,
    }
])

print(response["message"]["content"])