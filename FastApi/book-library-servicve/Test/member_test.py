from fastapi import status
import pytest


def test_getAllMembers_success(client, multiple_members):
    """Test getting all members returns 200 and includes the created member."""
    response = client.get("/members/")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()['members']) == 3


def test_getMemberById_success(client, multiple_members):
    """Test getting a specific member by ID returns 200 and the correct member."""
    member_id = multiple_members[0].member_id
    response = client.get(f"/members/{member_id}")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['member']['member_id'] == member_id


def test_getMemberById_failure(client, multiple_members):
    """Test getting a non-existent member by ID returns 404."""
    response = client.get("/members/999")
    assert response.status_code == status.HTTP_404_NOT_FOUND