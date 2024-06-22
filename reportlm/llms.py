from functools import lru_cache

from llama_index.core.llms import MockLLM, LLM
from llama_index.llms.ollama import Ollama
from llama_index.llms.openai import OpenAI


def mock() -> LLM:
    return MockLLM()


@lru_cache()
def ollama(model: str = "llama3:8b") -> LLM:
    return Ollama(
        model=model,
        # context_window=131072,
        temperature=0.1,
        request_timeout=100,
    )


@lru_cache()
def openai(token: str, model: str = "gpt-3.5-turbo") -> LLM:
    return OpenAI(
        api_key=token,
        model=model,
        temperature=0.1,
        max_tokens=256,
        request_timeout=10,
    )
