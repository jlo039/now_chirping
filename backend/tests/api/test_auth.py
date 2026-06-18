from unittest.mock import patch, AsyncMock
from app.services.spotify import spotify_service

def test_login_redirect(client):
    response = client.get("/api/auth/login", follow_redirects=False)
    assert response.status_code == 307
    assert "accounts.spotify.com/authorize" in response.headers["location"]

@patch("app.api.auth.spotify_service.exchange_code", new_callable=AsyncMock)
@patch("app.api.auth.spotify_service.get_user_profile", new_callable=AsyncMock)
def test_callback_success(mock_get_profile, mock_exchange_code, client):
    # Mock data
    mock_exchange_code.return_value = {
        "access_token": "fake_access_token",
        "refresh_token": "fake_refresh_token",
        "expires_in": 3600
    }
    mock_get_profile.return_value = {
        "id": "spotify_user_123",
        "display_name": "Test User"
    }
    
    response = client.get("/api/auth/callback?code=fake_code", follow_redirects=False)
    
    assert response.status_code == 307
    assert response.headers["location"] == "http://localhost:5173/"
    
    # Verify user was created in DB
    # (The conftest handles session override)
