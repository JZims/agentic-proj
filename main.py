import os
import argparse
from prompts import system_prompt
from dotenv import load_dotenv # type: ignore
from google import genai
from google.genai import types
from functions.call_function import available_functions

config = types.GenerateContentConfig(
        tools=[available_functions], system_instruction=system_prompt, temperature=0
    )

def main():

    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="type your prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")

    if api_key == None:
        raise RuntimeError("Environmental Variable not found. Check API Key and ensure env paths are accurate")
        
    client = genai.Client(api_key=api_key)
    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]
    generate_content(client, messages, args)

   


def generate_content (client, messages, args):
    response = client.models.generate_content(
        model='gemini-2.5-flash', 
        contents=messages,
        config=config,
        
    )

    if not response.usage_metadata:
        raise RuntimeError("Request to Gemini failed. No metadata returned.")
    
    if args.verbose:
        prompt_token_count = response.usage_metadata.total_token_count
        candidates_token_count = response.usage_metadata.candidates_token_count

        print("User prompt:", args.user_prompt)
        print("Prompt tokens: ", prompt_token_count)
        print("Response tokens: ", candidates_token_count)

    if response.function_calls:
        for call in response.function_calls:
            print(f"Calling function: {call.name}({call.args})")
    else:
        print(response.text)
    


if __name__ == "__main__":
    main()
