from pydantic_settings import BaseSettings , SettingsConfigDict



class Settings(BaseSettings):

    model_config = SettingsConfigDict(env_file=".env" , extra="ignore")
    DB_CONNECTION:str
    SECRET_KEY:str
    ALGORITHM:str
    ACCESS_TOKEN_EXPIRE_MINUTES:int
    MAX_UPLOAD_SIZE_BYTES:int = 5*1024*1024




settings = Settings()