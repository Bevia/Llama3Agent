import ollama

response = ollama.chat(model="llama3", messages=[
    {
        "role": "user",
        "content": "I want to know more abut private agents",
    }
])

print(response["message"]["content"])