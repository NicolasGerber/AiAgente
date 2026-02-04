import os
from prompts import system_prompt
from dotenv import load_dotenv
from google import genai
from google.genai import types
import argparse
from functions.call_funtion import available_functions

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

if api_key is None:
    raise RuntimeError("API key not set")

parser = argparse.ArgumentParser(description='chat')
parser.add_argument("user_prompt", type=str, help="user prompt")
parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
args = parser.parse_args()


messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]
response = client.models.generate_content(model='gemini-2.5-flash'
                                          , contents=messages
                                          , config=types.GenerateContentConfig(system_instruction=system_prompt
                                        , temperature=0, tools=[available_functions]))



usage = response.usage_metadata

if not response.usage_metadata:
        raise RuntimeError("Gemini API response appears to be malformed")

if args.verbose:
        print(f"User prompt: {messages[0].parts[0].text}") # Correct way to get user prompt
        print("Prompt tokens:", response.usage_metadata.prompt_token_count)
        print("Response tokens:", response.usage_metadata.candidates_token_count)

if response.function_calls:
    for function_call in response.function_calls:
        print(f"Calling function: {function_call.name}({function_call.args})")
    exit()

if response.text:
    print("Response:")
    print(response.text)