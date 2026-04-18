"""
Tests for GET /activities endpoint.
Using AAA (Arrange-Act-Assert) pattern.
"""

import pytest


def test_get_activities(client, reset_activities):
    """
    Test that GET /activities returns all activities.
    
    Arrange: Setup client
    Act: Send GET request to /activities
    Assert: Verify response contains all activities
    """
    # Arrange
    expected_count = 9  # Based on activities in conftest.py
    
    # Act
    response = client.get("/activities")
    
    # Assert
    assert response.status_code == 200
    assert len(response.json()) == expected_count


def test_get_activities_has_expected_fields(client, reset_activities):
    """
    Test that each activity has the required fields.
    
    Arrange: Setup client
    Act: Send GET request to /activities
    Assert: Verify each activity has description, schedule, max_participants, participants
    """
    # Arrange
    required_fields = {"description", "schedule", "max_participants", "participants"}
    
    # Act
    response = client.get("/activities")
    activities = response.json()
    
    # Assert
    assert response.status_code == 200
    for activity_name, activity_data in activities.items():
        assert isinstance(activity_name, str), f"Activity name should be string, got {type(activity_name)}"
        assert isinstance(activity_data, dict), f"Activity data should be dict, got {type(activity_data)}"
        assert required_fields.issubset(activity_data.keys()), \
            f"Activity '{activity_name}' missing required fields. Has: {activity_data.keys()}, needs: {required_fields}"
