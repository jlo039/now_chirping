from datetime import datetime
from typing import Optional
from sqlmodel import Field, SQLModel


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    spotify_user_id: str = Field(index=True, unique=True)
    display_name: str
    access_token: str
    refresh_token: str
    token_expires_at: datetime
