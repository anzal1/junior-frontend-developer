# services/open_router_client.py
import requests
import json
import config


class OpenRouterClient:
    """A client for interacting with the OpenRouter chat completion API."""

    def __init__(self):
        self.api_url = "https://openrouter.ai/api/v1/chat/completions"
        self.headers = {
            "Authorization": f"Bearer {config.OPENROUTER_API_KEY}",
            "Content-Type": "application/json",
            "HTTP-Referer": config.YOUR_SITE_URL,
            "X-Title": config.YOUR_SITE_NAME,
        }

    def create_chat_completion(self, messages, tools=None, temperature=0.2):
        """
        Calls the OpenRouter chat completion endpoint.
        Returns the full, non-streaming response.
        """
        payload = {
            "model": config.MODEL_NAME,
            "messages": messages,
            "temperature": temperature,
        }
        if tools:
            payload["tools"] = tools
            # Force the model to use a tool if any are provided
            payload["tool_choice"] = "auto"

        print("\n--- Sending Payload to OpenRouter ---")
        # Truncate long messages for cleaner logging
        debug_payload = json.loads(json.dumps(payload))
        if len(debug_payload["messages"][-1]["content"]) > 300:
            debug_payload["messages"][-1]["content"] = debug_payload["messages"][-1]["content"][:300] + \
                "... (truncated)"
        print(json.dumps(debug_payload, indent=2))
        print("--------------------------------------\n")

        try:
            response = requests.post(
                self.api_url, headers=self.headers, data=json.dumps(payload), timeout=180)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error calling OpenRouter API: {e}")
            if e.response is not None:
                print(f"Status Code: {e.response.status_code}")
                print(f"Response Body: {e.response.text}")
            return None
