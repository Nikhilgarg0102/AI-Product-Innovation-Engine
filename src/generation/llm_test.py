import os
from dotenv import load_dotenv
from groq import Groq


# Load environment variables
load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("GROQ_API_KEY not found in .env")


# Create Groq client
client = Groq(api_key=api_key)


# Send a simple test request
response = client.chat.completions.create(
    model="openai/gpt-oss-120b",
    messages=[
        {
            "role": "user",
            "content": "Give me one short innovative product idea for smart home technology."
        }
    ],
    temperature=0.7,
    max_tokens=200
)


print("\nLLM RESPONSE")
print("-" * 60)
print(response.choices[0].message.content)