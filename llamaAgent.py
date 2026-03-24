import sys
import ollama

# Get the user input passed from the Kivy app
if len(sys.argv) > 1:
    user_input = sys.argv[1]
else:
    user_input = "I want to know more about private agents"  # Default message if no input is provided

# Sends it to the local llama3.2 model via Ollama
response = ollama.chat(model="llama3.2", messages=[
    {
        "role": "user",
        "content": user_input,
    }
])

# Prints the response back to the GUI (captured via stdout)
print(response["message"]["content"])