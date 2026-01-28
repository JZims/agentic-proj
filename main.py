import os
import argparse
from dotenv import load_dotenv # type: ignore

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
if api_key == None:
    raise RuntimeError("Environmental Variable not found. Check API Key and ensure env paths are accurate")
        
from google import genai
client = genai.Client(api_key=api_key)

def main():
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="type your prompt")
    args = parser.parse_args()
    
    response = client.models.generate_content(model='gemini-2.5-flash', contents=args.user_prompt)
    if response.usage_metadata == None:
        raise RuntimeError("Request to Gemini failed. No metadata returned.")
    
    prompt_token_count = response.usage_metadata.total_token_count
    candidates_token_count = response.usage_metadata.candidates_token_count

    print("User Prompt:", args.user_prompt)
    print("Prompt tokens: ", prompt_token_count)
    print("Response tokens: ", candidates_token_count)

    print("Response: ", response.text)


if __name__ == "__main__":
    main()
