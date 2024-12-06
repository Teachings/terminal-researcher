import requests
import logging
from datetime import datetime
from termcolor import colored

# Setup logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.FileHandler('activity.log')
handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
logger.addHandler(handler)

class PerplexicaClient:
    def __init__(self, config):
        self.base_url = config["base_url"]
        self.timeout = config.get("timeout", 15)
        self.chat_model = config["chat_model"]
        self.embedding_model = config["embedding_model"]
        self.optimization_mode = config["optimization_mode"]
        self.focus_mode = config["focus_mode"]
        self.history = []
        self.history_limit = config.get("history_limit", 100)  # Optional history limit

        # Using a session for connection pooling
        self.session = requests.Session()

    def add_message(self, role, message):
        if role not in ('human', 'assistant'):
            raise ValueError("Role must be 'human' or 'assistant'")
        if len(self.history) >= self.history_limit:
            self.history.pop(0)  # Remove oldest message if history exceeds limit
        self.history.append([role, message])
        self.log_history(role, message)

    def log_history(self, role, message):
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        with open('chat_history.log', 'a') as history_file:
            history_file.write(f"[{timestamp}] {role.capitalize()}: {message}\n")
        logger.info(f"{role.capitalize()}: {message}")

    def prepare_request_data(self, query):
        return {
            "chatModel": self.chat_model,
            "embeddingModel": self.embedding_model,
            "optimizationMode": self.optimization_mode,
            "focusMode": self.focus_mode,
            "query": query,
            "history": self.history
        }

    def send_query(self, query):
        request_data = self.prepare_request_data(query)
        url = f"{self.base_url}/api/search"

        try:
            start_time = datetime.now()
            print(colored("Assistant: Thinking...", "blue"), end="", flush=True)

            response = self.session.post(url, json=request_data, timeout=self.timeout)
            response.raise_for_status()

            elapsed = datetime.now() - start_time
            print(f"\r{colored('Assistant:', 'blue')} [Response took {elapsed.seconds} seconds]")

            data = response.json()
            sources = data.get("sources", [])
            if sources:
                source_count = len(sources)
                print(colored(f"Assistant: {source_count} sources referenced.", "yellow"))
                logger.info(f"Sources referenced: {source_count}")

                for source in sources:
                    title = source['metadata']['title']
                    url = source['metadata']['url']
                    logger.info(f"Source: {title} - {url}")

            self.add_message("human", query)
            self.add_message("assistant", data.get("message", ""))
            return data

        except requests.exceptions.Timeout:
            logger.warning(f"Timeout: No response received within {self.timeout} seconds.")
            print(colored("\nAssistant: [No response received within the timeout period]", "red"))
            return None
        except requests.exceptions.HTTPError as http_err:
            logger.error(f"HTTP error occurred: {http_err}")
            print(colored(f"Assistant: [HTTP error: {http_err}]", "red"))
            return None
        except requests.RequestException as req_err:
            logger.error(f"Request error: {req_err}")
            print(colored("Assistant: [Request error occurred]", "red"))
            return None
        except Exception as err:
            logger.error(f"An error occurred: {str(err)}")
            print(colored("Assistant: [An error occurred. Please try again later.]", "red"))
            return None
