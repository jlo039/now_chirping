from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str = "Now Chirping"
    
    # Spotify Configuration
    SPOTIFY_CLIENT_ID: str
    SPOTIFY_CLIENT_SECRET: str
    SPOTIFY_REDIRECT_URI: str = "http://127.0.0.1:8000/api/auth/callback"
    
    # Frontend URL
    FRONTEND_URL: str = "http://127.0.0.1:5173"
    
    # Database Configuration
    DATABASE_URL: str = "sqlite:///./now_chirping.db"

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
