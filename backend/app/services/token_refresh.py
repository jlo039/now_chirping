from datetime import datetime, timedelta, timezone
from sqlmodel import Session
from app.models.user import User
from app.services.spotify import spotify_service

async def ensure_valid_token(user: User, session: Session) -> str:
    # Ensure user.token_expires_at is offset-aware for comparison
    expires_at = user.token_expires_at
    if expires_at.tzinfo is None:
        expires_at = expires_at.replace(tzinfo=timezone.utc)

    # Check if token is expired or about to expire (within 60 seconds)
    if expires_at > datetime.now(timezone.utc) + timedelta(seconds=60):
        return user.access_token

    # Token is expired, refresh it
    try:
        token_data = await spotify_service.refresh_token(user.refresh_token)
        user.access_token = token_data["access_token"]
        
        # Spotify might not return a new refresh token
        if "refresh_token" in token_data:
            user.refresh_token = token_data["refresh_token"]
            
        expires_in = token_data["expires_in"]
        user.token_expires_at = datetime.now(timezone.utc) + timedelta(seconds=expires_in)
        
        session.add(user)
        session.commit()
        session.refresh(user)
        
        return user.access_token
    except Exception as e:
        print(f"Failed to refresh token for user {user.spotify_user_id}: {e}")
        raise e
