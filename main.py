import os
from pyexpat.errors import messages

from dotenv import load_dotenv
from google import genai
from google.genai import types
import argparse


load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

if api_key is None:
    raise RuntimeError("API key not set")

parser = argparse.ArgumentParser(description='chat') #The argparse works creating a obj and defining the args we want to pass
parser.add_argument("user_prompt", type=str, help="user prompt")
parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
args = parser.parse_args()

messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]
response = client.models.generate_content(model='gemini-2.5-flash', contents=messages)
usage = response.usage_metadata

if usage is None:
    raise RuntimeError("usage metadata not set")

if args.verbose:
    print(f"User prompt: {args.user_prompt}")
    print(f'Prompt tokens: {usage.prompt_token_count}')
    print(f'Response tokens: {usage.candidates_token_count}')
    print(response.text)
else:
    print(response.text)
