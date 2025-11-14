from dotenv import load_dotenv
import os
import threading
from google.genai import Client

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")


class AIAssistant:
    def __init__(self, api_key=None, model="gemini-2.0-flash"):
        if api_key:
            os.environ["GEMINI_API_KEY"] = api_key
        else:
            api_key = os.getenv("GEMINI_API_KEY", "")
        self.model = model
        self.response = ""
        self.is_processing = False
        self.client = Client(api_key=api_key) if api_key else None

    def query(self, text, callback=None):
        if not self.client:
            self.response = "Warning: No API key found. AI features disabled."
            if callback:
                callback(self.response)
            return

        self.is_processing = True

        def _query_thread():
            try:
                print(f"\n[AI] Sending Prompt: {text}")

                response = self.client.models.generate_content(
                    model=self.model,
                    contents=text
                )

                self.response = response.text
                print(f"[AI] Response Received: {self.response}")

            except Exception as e:
                self.response = f"API Error: {str(e)}"
                print(f"[AI] Error: {str(e)}")

            self.is_processing = False
            if callback:
                callback(self.response)

        threading.Thread(target=_query_thread, daemon=True).start()

    def get_response(self):
        return self.response

    def clear_response(self):
        self.response = ""

    def is_busy(self):
        return self.is_processing


# Test script
if __name__ == "__main__":
    assistant = AIAssistant(api_key=api_key)

    def test_callback(res):
        print("\n✅ Gemini Output:")
        print(res)

    print("Sending test prompt...")
    assistant.query("Hello! What can you do?", test_callback)

    import time
    while assistant.is_busy():
        time.sleep(0.1)
