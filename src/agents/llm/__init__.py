from src.agents.llm.remote import RemoteLLMAgent
from src.agents.llm.local import LocalLLMAgent

def create_llm_agent(params):
    """
    Factory function to create the appropriate LLM agent
    
    Args:
        params: Dictionary of parameters or config object
    """
    # Handle if params is a config object
    if hasattr(params, 'remote_llm_params'):
        if params.remote_llm_params.use_api:
            remote_params = params.remote_llm_params.dict()
            return RemoteLLMAgent(**remote_params)
        else:
            local_params = params.local_llm_params.dict()
            return LocalLLMAgent(**local_params)
    
    # Handle if params is a dictionary
    elif isinstance(params, dict):
        if params.get("use_api", False):
            return RemoteLLMAgent(**params)
        elif params.get("provider", "").lower() == "local":
            return LocalLLMAgent(**params)
        else:
            return RemoteLLMAgent(**params)