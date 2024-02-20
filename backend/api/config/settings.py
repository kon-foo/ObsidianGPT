from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    api_key: str
    vault_dir: str
    ignore_dirs: list[str] = [".obsidian", ".trash", "templates"]


settings = Settings()
