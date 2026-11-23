from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict

class TokenSettings(BaseSettings):
    App_UserName: str
    Email: str
    Role: str
    Secret_Key: str
    model_config = SettingsConfigDict(env_file="dev.env", env_file_encoding="utf-8", extra='ignore')

class ConnectionSettings(BaseSettings):
    DatabaseUrl : str
    model_config = SettingsConfigDict(env_file="dev.env", env_file_encoding="utf-8", extra='ignore')

@lru_cache
def get_token_settings() -> TokenSettings:
    return TokenSettings()

@lru_cache
def get_connection_settings() -> ConnectionSettings:
    return ConnectionSettings()