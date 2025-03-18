import requests
import sys
from src.agents.llm.base import LLMAgentBase

class LocalLLMAgent(LLMAgentBase):
    def __init__(self, model="SeaLLMs/SeaLLMs-v3-1.5B-Chat", endpoint="http://localhost:8000", 
                 temperature=0.5, extended_prompt=True, **kwargs):
        super().__init__("LocalLLMAgent", temperature, extended_prompt)
        self.endpoint = endpoint
        self.model = model
        
        # Verify server connection at initialization
        if not self.check_server_availability():
            print(f"\033[91mERROR: Cannot connect to local LLM server at {self.endpoint}\033[0m")
            print("Please make sure your vLLM server is running.")
            print(f"You can start it with: python -m vllm.entrypoints.openai.api_server --model {self.model}")
            sys.exit(1)
    
    def check_server_availability(self):
        """Check if the LLM server is available and responding."""
        try:
            # Try a simple health check or models endpoint
            response = requests.get(f"{self.endpoint}/v1/models", timeout=5)
            return response.status_code == 200
        except requests.exceptions.RequestException:
            return False

    def move(self) -> str:
        prompt = self.build_prompt()
        return self.get_llm_decision(prompt)

    def build_prompt(self) -> str:
        rounds = len(self.my_history)
        rep = f" (reputation: {self.reputation:.2f})"  if self.reputation else ""
        if rounds == 0:
            return f"No history. Please choose C or D.{rep}"
        history = f"Your moves: {','.join(self.my_history)}; Opponent moves: {','.join(self.opponent_history)}."
        if self.extended_prompt:
            prompt = f"You are playing Iterated Prisoner's Dilemma. {history} Your current reputation is {self.reputation:.2f}. Based on this, decide whether to cooperate (C) or defect (D)."
        else:
            prompt = f"{history} Decide C or D."
        return prompt

    def get_llm_decision(self, prompt: str) -> str:
        try:
            response = requests.post(
                f"{self.endpoint}/v1/completions",
                json={
                    "prompt": prompt,
                    "max_tokens": 10,
                    "temperature": self.temperature,
                    "model": self.model
                },
                timeout=10  # Add timeout to avoid hanging
            )
            
            if response.status_code == 200:
                result = response.json()
                # Extract the text from response
                text = result.get("choices", [{}])[0].get("text", "").strip().upper()
                return "D" if "D" in text else "C"
            else:
                # Server is up but returned an error - EXIT instead of returning C
                print(f"\033[91mERROR: LLM server returned status {response.status_code}\033[0m")
                print(f"Response: {response.text[:200]}")  # Print first part of error
                print("The simulation cannot continue without a working LLM.")
                sys.exit(1)  # Exit with error code
        except requests.exceptions.ConnectionError:
            # Server went down during execution
            print("\033[91mERROR: Lost connection to local LLM server\033[0m")
            print("The server appears to have gone down during execution.")
            sys.exit(1)
        except Exception as e:
            # Any other exception - EXIT instead of returning C
            print(f"\033[91mERROR with local LLM API: {e}\033[0m")
            print("The simulation cannot continue without a working LLM.")
            sys.exit(1)  # Exit with error code