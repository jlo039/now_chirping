from datetime import datetime, timedelta, timezone
from unittest.mock import patch, AsyncMock
from app.models.user import User

@patch("app.api.users.spotify_service.get_current_playback", new_callable=AsyncMock)
@patch("app.api.users.ensure_valid_token", new_callable=AsyncMock)
def test_get_currently_playing_empty(mock_ensure_token, mock_get_playback, client):
    response = client.get("/api/users/currently-playing")
    assert response.status_code == 200
    assert response.json() == []

@patch("app.api.users.spotify_service.get_current_playback", new_callable=AsyncMock)
@patch("app.api.users.ensure_valid_token", new_callable=AsyncMock)
def test_get_currently_playing_active(mock_ensure_token, mock_get_playback, client, session):
    # Add a user to the DB
    user = User(
        spotify_user_id="user1",
        display_name="User One",
        access_token="token1",
        refresh_token="refresh1",
        token_expires_at=datetime.now(timezone.utc) + timedelta(hours=1)
    )
    session.add(user)
    session.commit()
    
    # Mock playback
    mock_ensure_token.return_value = "token1"
    mock_get_playback.return_value = {
        "is_playing": True,
        "item": {
            "name": "Song Name",
            "artists": [{"name": "Artist Name"}],
            "album": {
                "images": [{"url": "http://album.art"}]
            }
        }
    }
    
    response = client.get("/api/users/currently-playing")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["name"] == "User One"
    assert data[0]["track"] == "Song Name"
    assert data[0]["artist"] == "Artist Name"
