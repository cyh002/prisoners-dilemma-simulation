import os
import sys
from src.agents.llm.base import LLMAgentBase

class RemoteLLMAgent(LLMAgentBase):
    def __init__(self, provider="openai", model="gpt-4o", temperature=0.1, 
                 extended_prompt=True, api_base=None, use_api=True, **kwargs):
        """
        provider: 'openai' or 'anthropic'
        """
        name = f"Remote{provider.capitalize()}Agent"
        super().__init__(name, temperature, extended_prompt)
        self.provider = provider.lower()
        self.model = model
        self.api_base = api_base
        
        # Retrieve API keys from environment variables
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")
        
        # Verify API key at initialization
        if self.provider == "openai" and not self.openai_api_key:
            print("\033[91mERROR: OPENAI_API_KEY environment variable not set\033[0m")
            print("Please set the OPENAI_API_KEY environment variable.")
            sys.exit(1)
        elif self.provider == "anthropic" and not self.anthropic_api_key:
            print("\033[91mERROR: ANTHROPIC_API_KEY environment variable not set\033[0m")
            print("Please set the ANTHROPIC_API_KEY environment variable.")
            sys.exit(1)

    def get_llm_decision(self, prompt: str) -> str:
        if self.provider == "openai":
            return self.get_openai_decision(prompt)
        elif self.provider == "anthropic":
            return self.get_anthropic_decision(prompt)
        else:
            print(f"\033[91mERROR: Unsupported provider '{self.provider}'\033[0m")
            print("Supported providers are 'openai' and 'anthropic'")
            sys.exit(1)

    def get_openai_decision(self, prompt: str) -> str:
        try:
            from openai import OpenAI
            
            client = OpenAI(
                api_key=self.openai_api_key,
                base_url=self.api_base if self.api_base else None
            )
            
            response = client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are playing an Iterated Prisoner's Dilemma game. You should respond with either 'C' to cooperate or 'D' to defect."},
                    {"role": "user", "content": prompt}
                ],
                temperature=self.temperature,
                max_tokens=10
            )
            
            text = response.choices[0].message.content.strip().upper()
            return "D" if "D" in text else "C"
        except Exception as e:
            print(f"\033[91mERROR with OpenAI API: {e}\033[0m")
            print("The simulation cannot continue without a working API connection.")
            sys.exit(1)

    def get_anthropic_decision(self, prompt: str) -> str:
        try:
            import anthropic
            client = anthropic.Anthropic(api_key=self.anthropic_api_key)
            
            response = client.messages.create(
                model="claude-3-haiku-20240307",
                max_tokens=10,
                temperature=self.temperature,
                system="You are playing Prisoner's Dilemma. Respond with C to cooperate or D to defect.",
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            
            text = response.content[0].text.strip().upper()
            return "D" if "D" in text else "C"
        except Exception as e:
            print(f"\033[91mERROR with Anthropic API: {e}\033[0m")
            print("The simulation cannot continue without a working API connection.")
            sys.exit(1)