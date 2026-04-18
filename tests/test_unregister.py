"""
Tests for POST /activities/{activity_name}/unregister endpoint.
Using AAA (Arrange-Act-Assert) pattern.
"""

import pytest


def test_unregister_success(client, reset_activities):
    """
    Test successful unregister from an activity.
    
    Arrange: Setup client and existing participant
    Act: Send POST request to unregister endpoint
    Assert: Verify email is removed from participants and status is 200
    """
    # Arrange
    activity_name = "Chess Club"
    existing_participant = "michael@mergington.edu"
    
    # Verify participant exists before unregistering
    response_before = client.get("/activities")
    assert existing_participant in response_before.json()[activity_name]["participants"]
    
    # Act
    response = client.post(
        f"/activities/{activity_name}/unregister",
        params={"email": existing_participant}
    )
    
    # Assert
    assert response.status_code == 200
    assert "Unregistered" in response.json().get("message", "")
    
    # Verify participant is removed
    response_after = client.get("/activities")
    assert existing_participant not in response_after.json()[activity_name]["participants"]


def test_unregister_returns_correct_message(client, reset_activities):
    """
    Test that unregister response contains correct message format.
    
    Arrange: Setup client and existing participant
    Act: Send POST request to unregister endpoint
    Assert: Verify response has success message with email and activity name
    """
    # Arrange
    activity_name = "Programming Class"
    existing_participant = "emma@mergington.edu"
    
    # Act
    response = client.post(
        f"/activities/{activity_name}/unregister",
        params={"email": existing_participant}
    )
    
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert existing_participant in data["message"]
    assert activity_name in data["message"]
    assert "Unregistered" in data["message"]


def test_unregister_activity_not_found(client, reset_activities):
    """
    Test unregister from non-existent activity.
    
    Arrange: Setup client with non-existent activity
    Act: Send POST request to unregister with invalid activity name
    Assert: Verify 404 status and error detail
    """
    # Arrange
    invalid_activity = "Nonexistent Club"
    test_email = "student@mergington.edu"
    
    # Act
    response = client.post(
        f"/activities/{invalid_activity}/unregister",
        params={"email": test_email}
    )
    
    # Assert
    assert response.status_code == 404
    assert "Activity not found" in response.json().get("detail", "")
