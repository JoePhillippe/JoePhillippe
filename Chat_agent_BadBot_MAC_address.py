import anthropic
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
#print(os.getenv("ANTHROPIC_API_KEY"))

# Get API key from environment variable
client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

def mac_mentor_bot(message):
    """MACMentor 1.0 - Your network study buddy"""
    system_prompt = """
    PERSONA: You are MACMentor, a fellow student in Network 101 class who's really enthusiastic about network addressing.
    
    PURPOSE: Help other students understand and validate Media Access Control (MAC) addresses and hexadecimal numbers.
    
    Always check if given strings are valid MAC addresses (12 hex digits) and explain your reasoning clearly.
    """
    
    response = client.messages.create(
        model="claude-3-5-haiku-20241022",
        max_tokens=1000,
        system=system_prompt,  # Move system prompt here
        messages=[
            {"role": "user", "content": message}
        ]
    )
    return response.content[0].text

# Test the bot
test_message = "Is this a valid MAC address: E0-73-E7-11-DC-2A"

try:
    result = mac_mentor_bot(test_message)
    print("MACMentor Response:", result)
except Exception as e:
    print(f"Error: {e}")
    
    
