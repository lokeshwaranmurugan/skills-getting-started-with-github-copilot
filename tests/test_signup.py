"""
Tests for POST /activities/{activity_name}/signup endpoint.
Using AAA (Arrange-Act-Assert) pattern.
"""

import pytest


def test_signup_success(client, reset_activities):
    """
    Test successful signup for an activity.
    
    Arrange: Setup client and test email
    Act: Send POST request to signup endpoint
    Assert: Verify email is added to participants and status is 200
    """
    # Arrange
    activity_name = "Chess Club"
    test_email = "newstudent@mergington.edu"
    
    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": test_email}
    )
    
    # Assert
    assert response.status_code == 200
    assert test_email in response.json().get("message", "")


def test_signup_returns_correct_message(client, reset_activities):
    """
    Test that signup response contains correct message format.
    
    Arrange: Setup client and test email
    Act: Send POST request to signup endpoint
    Assert: Verify response has success message with email and activity name
    """
    # Arrange
    activity_name = "Programming Class"
    test_email = "coder@mergington.edu"
    
    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": test_email}
    )
    
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert test_email in data["message"]
    assert activity_name in data["message"]
    assert "Signed up" in data["message"]


def test_signup_activity_not_found(client, reset_activities):
    """
    Test signup with non-existent activity.
    
    Arrange: Setup client with non-existent activity
    Act: Send POST request to signup with invalid activity name
    Assert: Verify 404 status and error detail
    """
    # Arrange
    invalid_activity = "Nonexistent Club"
    test_email = "student@mergington.edu"
    
    # Act
    response = client.post(
        f"/activities/{invalid_activity}/signup",
        params={"email": test_email}
    )
    
    # Assert
    assert response.status_code == 404
    assert "Activity not found" in response.json().get("detail", "")
