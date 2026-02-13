import os
import argparse
import sys
from prompts import system_prompt
from dotenv import load_dotenv # type: ignore
from google import genai
from google.genai import types
from functions.call_function import available_functions, call_function

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

    
    for _ in range(20):
        try:
            final_response = generate_content(client, messages, args)
            if final_response:
                print("Final response:")
                print(final_response)
                return
        except Exception as e:
            print(f"Error in generate_content: {e}")

    print(f"Maximum iterations reached")
    sys.exit(1)


def generate_content (client, messages, args):
    response = client.models.generate_content(
        model='gemini-2.5-flash', 
        contents=messages,
        config=config,     
    )
    function_responses = []

    if not response.usage_metadata:
        raise RuntimeError("Request to Gemini failed. No metadata returned.")
    
    if args.verbose:
        prompt_token_count = response.usage_metadata.total_token_count
        candidates_token_count = response.usage_metadata.candidates_token_count

        print("User prompt:", args.user_prompt)
        print("Prompt tokens: ", prompt_token_count)
        print("Response tokens: ", candidates_token_count)

    if response.candidates:
        for candidate in response.candidates:
            if candidate.content:
                messages.append(candidate.content)

    if not response.function_calls:
        return response.text

    if response.function_calls:
        for result in response.function_calls:
            function_call_result = call_function(result)
            if not function_call_result.parts:
                raise Exception("Invalid response generated")
            if not function_call_result.parts[0].function_response:
                raise Exception("Invalid function response generated")
            if not function_call_result.parts[0].function_response.response:
                raise Exception("Invalid function response generated")
            if args.verbose:
                print(f"-> {function_call_result.parts[0].function_response.response}")
            function_responses.append(function_call_result.parts[0])

        messages.append(types.Content(role="user", parts=function_responses))  

if __name__ == "__main__":
    main()
