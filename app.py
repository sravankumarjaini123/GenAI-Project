from dotenv import load_dotenv
from openai import OpenAI
import os


load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

response = client.responses.create(
    model = "gpt-5.5",
    input = "Explain Python variables in simple words for beginners",
)

print(response.output_text)