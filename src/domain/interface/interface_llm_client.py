from abc import ABC
from abc import abstractmethod
from typing import Any

class ILLMClient(ABC):
    def __init__(self, model_name: str, api_key: str):
        ...

    @abstractmethod
    def invoke(self, contents: list, config: Any) -> Any:
        raise NotImplementedError