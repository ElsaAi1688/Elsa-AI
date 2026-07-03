from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

response = client.responses.create(
    model="gpt-5",
    input="請用一句話介紹你自己，你是 Elsa AI 股票經理人。"
)

print(response.output_text)
