# First, tests and performs successful retrieval of Bearer token.
# Then, integrates with ai_gateway.py to perform call_openai.

import time
import os
import requests
from dotenv import load_dotenv
from ai_gateway import DeereAIGatewayOpenAI

load_dotenv()

AI_GATEWAY_CLIENT_ID = os.getenv("AI_GATEWAY_CLIENT_ID")
AI_GATEWAY_CLIENT_SECRET = os.getenv("AI_GATEWAY_CLIENT_SECRET")
AI_GATEWAY_ISSUER = os.getenv("AI_GATEWAY_ISSUER")

# Global cache for the token
token_cache = {
    "token": None,
    "expires_at": 0
}

def get_ai_gateway_access_token(force_new_token: bool = False):
    """
    Retrieve an access token for the Deere AI Gateway.
    This function checks if a valid token is cached and returns it if available.
    If not, it requests a new token using client credentials.
    """
    current_time = time.time()

    if not force_new_token and token_cache["token"] and token_cache["expires_at"] > current_time:
        return token_cache["token"]

    token_endpoint = f"{AI_GATEWAY_ISSUER}/v1/token"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {
        "grant_type": "client_credentials",
        "client_id": AI_GATEWAY_CLIENT_ID,
        "client_secret": AI_GATEWAY_CLIENT_SECRET,
        "scope": "mlops.deere.com/model-deployments.llm.region-restricted-invocations" 
    }

    response = requests.post(token_endpoint, headers=headers, data=data)
    response_json = response.json()

    if response.status_code == 200:
        
        # print("Works!")

        token_cache["token"] = response_json["access_token"]
        token_cache["expires_at"] = current_time + 300  # cache token for 5 minutes
        return token_cache["token"]
    else:
        raise Exception(
            f"Failed to retrieve bearer token: {response_json.get('error_description', 'Unknown error')}"
        )


# testing LLM call

"""

# Retrieve the bearer token
access_token = get_ai_gateway_access_token()

# Initialize the OpenAI SDK client with the extended DeereAIGatewayOpenAI class
client = DeereAIGatewayOpenAI(
    access_token=access_token,
    base_url=os.getenv("AI_GATEWAY_BASE_URL"),
    deere_ai_gateway_registration_id=os.getenv("AI_GATEWAY_REGISTRATION_ID")
)

messages = [
    {
        "role": "developer",
        "content": "You are an awesome assistant here to help users.",
    },
    {
        "role": "user",
        "content": "Hello, Deere AI!"
    },
]

# Example API call to the 'completions' endpoint
response = client.chat.completions.create(messages=messages, model = "gpt-4o-mini-2024-07-18"  )  # model="gpt-4o-mini-2024-07-18" # gpt-image-1
print(response.choices[0].message)

"""