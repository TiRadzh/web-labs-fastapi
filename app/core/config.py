from pydantic_settings import BaseSettings,SettingsConfigDict
class Settings(BaseSettings):
    database_url:str='sqlite+aiosqlite:///./app.db'
    app_debug:bool=False
    app_secret_key:str='local-development-only-change-this-key'
    upload_dir:str='uploads'
    model_config=SettingsConfigDict(env_file='.env',extra='ignore')
settings=Settings()
DATABASE_URL=settings.database_url
APP_DEBUG=settings.app_debug
