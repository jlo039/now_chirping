from typing import List, Dict, Any
from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from app.db.session import get_session
from app.models.user import User
from app.services.spotify import spotify_service
from app.services.token_refresh import ensure_valid_token

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/currently-playing")
async def get_currently_playing(session: Session = Depends(get_session)):
    statement = select(User)
    users = session.exec(statement).all()
    print(f"Found {len(users)} users in database")
    
    active_listeners = []
    
    for user in users:
        try:
            print(f"Checking playback for user: {user.display_name}")
            # Ensure token is valid
            access_token = await ensure_valid_token(user, session)
            
            # Get current playback
            playback = await spotify_service.get_current_playback(access_token)
            
            if playback:
                print(f"Playback state found for {user.display_name}. is_playing: {playback.get('is_playing')}")
                if playback.get("is_playing"):
                    item = playback.get("item")
                    if item:
                        active_listeners.append({
                            "name": user.display_name,
                            "artist": ", ".join([artist["name"] for artist in item["artists"]]),
                            "track": item["name"],
                            "album_art": item["album"]["images"][0]["url"] if item["album"]["images"] else None
                        })
            else:
                print(f"No playback state for {user.display_name}")
        except Exception as e:
            print(f"Error fetching playback for {user.display_name}: {e}")
            continue
            
    return active_listeners
