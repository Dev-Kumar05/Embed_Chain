from pydantic_settings import BaseSettings

from heliosrag.helio_paths import DATA_DIR, DEFAULT_ENV_FILE


class Settings(BaseSettings):
    app_name: str = "API Name"
    app_description: str = "API Description"
    app_version: str = "1.0"
    contact_name: str = "Contact Name"
    contact_email: str = "test@contact.email"
    contact_url: str = "https://www.test.contact.url/"
    license_name: str = ""
    license_url: str = ""
    data_dir: str = str(DATA_DIR)
    embedding_model: str = ""
    embedding_model_device: str = ""
    chat_model: str = ""
    chat_model_task: str = ""
    google_api_key: str = ""

    class Config:
        env_file = str(DEFAULT_ENV_FILE)
        env_file_encoding = "utf-8"


settings = Settings()
