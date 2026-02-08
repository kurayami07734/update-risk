from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    GROQ_LLM_API_KEY: str

    HOURS_OF_CONTENT: int = 1
    FREQ_OF_DATA_RETRIEVAL: int = 1

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


CONFIG = Settings()
