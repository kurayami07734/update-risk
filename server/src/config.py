from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    GROQ_LLM_API_KEY: str
    
    MONGO_URI: str
    MONGO_DB_NAME: str

    HOURS_OF_CONTENT: int = 1
    FREQ_OF_DATA_RETRIEVAL: int = 5
    
    

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")
    

CONFIG = Settings()
