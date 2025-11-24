from pydantic import Field
from pydantic_settings import BaseSettings
from pydantic_settings import SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )

    notion_api_key: str = Field(..., description="NotionのAPI KEY")
    diary_database_id: str = Field(..., description="NotionのデータベースID")
    gemini_api_key: str = Field(..., description="GeminiのAPI KEY")
