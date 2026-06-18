import httpx2
from datetime import datetime, timedelta, timezone
from typing import Dict, Any, Optional
from app.config import settings

class SpotifyService:
    AUTH_URL = "https://accounts.spotify.com/authorize"
    TOKEN_URL = "https://accounts.spotify.com/api/token"
    API_BASE_URL = "https://api.spotify.com/v1"

    @staticmethod
    def get_auth_url() -> str:
        params = {
            "client_id": settings.SPOTIFY_CLIENT_ID,
            "response_type": "code",
            "redirect_uri": settings.SPOTIFY_REDIRECT_URI,
            "scope": "user-read-currently-playing",
            "show_dialog": "true"
        }
        async_client = httpx2.AsyncClient()
        query_params = async_client.build_request("GET", SpotifyService.AUTH_URL, params=params).url.query.decode()
        return f"{SpotifyService.AUTH_URL}?{query_params}"

    @staticmethod
    async def exchange_code(code: str) -> Dict[str, Any]:
        data = {
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": settings.SPOTIFY_REDIRECT_URI,
            "client_id": settings.SPOTIFY_CLIENT_ID,
            "client_secret": settings.SPOTIFY_CLIENT_SECRET,
        }
        async with httpx2.AsyncClient() as client:
            response = await client.post(SpotifyService.TOKEN_URL, data=data)
            response.raise_for_status()
            return response.json()

    @staticmethod
    async def get_user_profile(access_token: str) -> Dict[str, Any]:
        headers = {"Authorization": f"Bearer {access_token}"}
        async with httpx2.AsyncClient() as client:
            response = await client.get(f"{SpotifyService.API_BASE_URL}/me", headers=headers)
            response.raise_for_status()
            return response.json()

    @staticmethod
    async def refresh_token(refresh_token: str) -> Dict[str, Any]:
        data = {
            "grant_type": "refresh_token",
            "refresh_token": refresh_token,
            "client_id": settings.SPOTIFY_CLIENT_ID,
            "client_secret": settings.SPOTIFY_CLIENT_SECRET,
        }
        async with httpx2.AsyncClient() as client:
            response = await client.post(SpotifyService.TOKEN_URL, data=data)
            response.raise_for_status()
            return response.json()

    @staticmethod
    async def get_current_playback(access_token: str) -> Optional[Dict[str, Any]]:
        headers = {"Authorization": f"Bearer {access_token}"}
        async with httpx2.AsyncClient() as client:
            response = await client.get(f"{SpotifyService.API_BASE_URL}/me/player/currently-playing", headers=headers)
            if response.status_code == 204 or response.status_code == 404:
                return None
            response.raise_for_status()
            return response.json()

spotify_service = SpotifyService()
