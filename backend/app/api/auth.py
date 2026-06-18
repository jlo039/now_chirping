from datetime import datetime, timedelta, timezone
from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import RedirectResponse
from sqlmodel import Session, select
from app.db.session import get_session
from app.models.user import User
from app.services.spotify import spotify_service
from app.config import settings

router = APIRouter(prefix="/auth", tags=["auth"])

@router.get("/login")
async def login():
    return RedirectResponse(spotify_service.get_auth_url())

@router.get("/callback")
async def callback(code: str, session: Session = Depends(get_session)):
    try:
        print(f"Callback received with code: {code[:10]}...")
        # Exchange code for tokens
        token_data = await spotify_service.exchange_code(code)
        print("Token exchange successful")
        access_token = token_data["access_token"]
        refresh_token = token_data.get("refresh_token")
        expires_in = token_data["expires_in"]
        
        # Get user profile
        profile = await spotify_service.get_user_profile(access_token)
        spotify_user_id = profile["id"]
        display_name = profile.get("display_name", spotify_user_id)
        print(f"Profile retrieved for user: {display_name} ({spotify_user_id})")
        
        # Calculate expiration
        expires_at = datetime.now(timezone.utc) + timedelta(seconds=expires_in)
        
        # Update or create user
        statement = select(User).where(User.spotify_user_id == spotify_user_id)
        user = session.exec(statement).first()
        
        if user:
            print(f"Updating existing user: {spotify_user_id}")
            user.access_token = access_token
            if refresh_token:
                user.refresh_token = refresh_token
            user.token_expires_at = expires_at
            user.display_name = display_name
        else:
            print(f"Creating new user: {spotify_user_id}")
            user = User(
                spotify_user_id=spotify_user_id,
                display_name=display_name,
                access_token=access_token,
                refresh_token=refresh_token,
                token_expires_at=expires_at
            )
        
        session.add(user)
        session.commit()
        print("Database commit successful")
        
        # Redirect back to frontend
        return RedirectResponse(f"{settings.FRONTEND_URL}/")
    
    except Exception as e:
        print(f"Error in callback: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=400, detail=str(e))
