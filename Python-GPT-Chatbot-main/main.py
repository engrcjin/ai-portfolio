from openai import OpenAI
import os

# Initialize the client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def chat_with_gpt(prompt):
    response = client.chat.completions.create(
        model="gpt-4o-mini",  # or gpt-4o, gpt-4.1
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content.strip()

if __name__ == "__main__":
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["quit", "exit", "bye"]:
            break

        response = chat_with_gpt(user_input)
        print("Chatbot:", response)

# To set your API key in Windows Command Prompt, use the following command: setx OPENAI_API_KEY "your_api_key_here"
# Shows if the key is working: echo $env:OPENAI_API_KEY
