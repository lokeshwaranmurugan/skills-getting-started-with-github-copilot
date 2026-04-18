"""
Tests for GET / redirect endpoint.
Using AAA (Arrange-Act-Assert) pattern.
"""

import pytest


def test_root_redirects_to_static(client, reset_activities):
    """
    Test that GET / redirects to /static/index.html.
    
    Arrange: Setup client
    Act: Send GET request to root endpoint with follow_redirects=False
    Assert: Verify redirect status 307 to /static/index.html
    """
    # Arrange
    expected_redirect_url = "/static/index.html"
    
    # Act
    response = client.get("/", follow_redirects=False)
    
    # Assert
    assert response.status_code == 307
    assert response.headers["location"] == expected_redirect_url
