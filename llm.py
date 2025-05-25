from openai import OpenAI
import json
import re

# Initialize OpenRouter API with base URL and API key
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key="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",
)

# Open the file in read mode
with open('prompt.txt', 'r') as file:
    # Read the content of the file into a variable
    prompt = file.read()


def ask_deepseek(user_query):
    # Updated prompt with enforced strict JSON format
    completion = client.chat.completions.create(
        model="deepseek/deepseek-r1-zero:free",
        messages=[
            {
                "role": "system",
                "content": prompt
            }, { "role": "user", "content": user_query } ], stream=False )


    response_content = completion.choices[0].message.content.strip()


    output = None
    # Check if the text contains an error
    error_match = re.search(r'"error":\s*"([^"]+)"', response_content)
    if error_match:
        output = error_match.group(1)  # Return the error message

    # Check if the text contains commodities
    commodities_match = re.search(r'"commodities":\s*(\[[^\]]+\])', response_content)
    if commodities_match:
        commodities_str = commodities_match.group(1)
        # Parse the string into a Python list
        output = json.loads(commodities_str)

    return output
