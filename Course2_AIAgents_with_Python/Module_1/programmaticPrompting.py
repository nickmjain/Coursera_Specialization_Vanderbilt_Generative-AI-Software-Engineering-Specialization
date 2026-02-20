import os
import yaml
from dotenv import load_dotenv
from litellm import completion 

# Setup
ROOT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')

load_dotenv(os.path.join(ROOT_DIR, '.env'))

# Manually specify the API key by making sure it's available for LiteLLM
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY") 
os.environ["GEMINI_API_KEY"] = GEMINI_API_KEY

CONFIG_FILE = os.path.join(ROOT_DIR, 'config.yaml')
try:
    with open(CONFIG_FILE, 'r') as f:
        config = yaml.safe_load(f)
    # LiteLLM requires the provider prefix, e.g., "gemini/gemini-2.5-flash-lite"
    provider = config['Model']['provider']
    model = config['Model']['model']
    MODEL_NAME = provider + "/" + model
except Exception as e:
    print(f"FATAL: Could not load {CONFIG_FILE}. Using fallback. Error: {e}")
    MODEL_NAME = "gemini/gemini-2.5-flash-lite"

# -----------------
def generate_response(prompt: str) -> str:
    """Calls the LiteLLM completion API."""
    if not prompt:
        return "Error: No prompt provided."

    messages = [{"role": "user", "content": prompt}]

    response = completion(
        model=MODEL_NAME, 
        messages=messages
    )
    
    return response.choices[0].message.content

# -----------------
if __name__ == '__main__':
    print(f"Using LiteLLM model string: {MODEL_NAME}")
    
    user_prompt = "Explain the concept of time value of money in