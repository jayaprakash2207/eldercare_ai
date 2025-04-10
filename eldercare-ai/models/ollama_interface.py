import requests
from utils.logger import logger

class OllamaLLM:
    def __init__(self, model_name="llama3:latest", endpoint="http://localhost:11434/api/generate"):
        self.model_name = model_name
        self.endpoint = endpoint
        self.logger = logger

    def send_prompt(self, prompt):
        self.logger.info(f"Sending prompt to Ollama LLM: {prompt}")

        try:
            response = requests.post(self.endpoint, json={
                "model": self.model_name,
                "prompt": prompt,
                "stream": False
            })

            response.raise_for_status()
            result = response.json()
            if "response" not in result:
                self.logger.warning(f"Unexpected response format: {result}")
                return "No response from LLM"
            self.logger.debug(f"LLM response: {result}")
            return result["response"]
        except requests.exceptions.HTTPError as e:
            self.logger.error(f"HTTP error during LLM communication: {e.response.status_code} - {e.response.text}")
            return f"Error: HTTP {e.response.status_code} from AI model."
        except requests.exceptions.Timeout:
            self.logger.error(f"Timeout during LLM communication to {self.endpoint}")
            return "Error: Request timed out."
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Error during LLM communication: {e}")
            return "Error: Unable to get response from AI model."
        except ValueError as e:
            self.logger.error(f"Invalid JSON response: {e}")
            return "Error: Invalid response from AI model."
        
def 