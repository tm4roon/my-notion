import logging

from google import genai
from google.genai import types
from google.genai.types import GenerateContentConfig

from domain.interface import ILLMClient

logger = logging.getLogger(__name__)


class GeminiClient(ILLMClient):
    def __init__(
        self,
        model_name: str,
        api_key: str,
    ):
        self.model_name = model_name
        self.client = genai.Client(api_key=api_key)
        self.cached_content = None

    def create_cached_content(
        self,
        system_instruction: str,
        ttl: str = "3600s",
    ) -> None:
        try:
            logger.info(f"Creating cached content with system_instruction")
            self.cached_content = self.client.caches.create(
                model=self.model_name,
                config=types.CreateCachedContentConfig(
                    system_instruction=system_instruction,
                    ttl=ttl,
                )
            )
            logger.info(f"Cached content created successfully")
        except Exception as e:
            logger.error(f"Failed to create cached content: {e}", exc_info=True)
            raise RuntimeError("Failed to create cached content") from e
        return None
    
    def invoke(
        self,
        contents: list[types.Content],
        config: GenerateContentConfig,
    ) -> types.GenerateContentResponse:
        try:
            model_to_use = self.model_name
            if self.cached_content:
                model_to_use = self.cached_content.name
                logger.info(f"Using cached content: {model_to_use}")
            res = self.client.models.generate_content(
                model=model_to_use,
                contents=contents,
                config=config,
            )
            logger.info(f"Content generated successfully")
            return res
        except Exception as e:
            logger.error(f"Failed to generate content: {e}", exc_info=True)
            raise
    