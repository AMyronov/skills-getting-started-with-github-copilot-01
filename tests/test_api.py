import pytest
from fastapi.testclient import TestClient


class TestBasicEndpoints:
    """Test basic API endpoints."""

    def test_root_redirect(self, client: TestClient):
        """Test that root endpoint redirects to static/index.html."""
        response = client.get("/", follow_redirects=False)
        assert response.status_code == 307
        assert response.headers["location"] == "/static/index.html"

    def test_get_activities(self, client: TestClient):
        """Test getting all activities."""
        response = client.get("/activities")
        assert response.status_code == 200
        
        data = response.json()
        assert isinstance(data, dict)
        assert "Chess Club" in data
        assert "Programming Class" in data
        assert "Test Activity" in data
        
        # Check structure of an activity
        chess_club = data["Chess Club"]
        assert "description" in chess_club
        assert "schedule" in chess_club
        assert "max_participants" in chess_club
        assert "participants" in chess_club
        assert isinstance(chess_club["participants"], list)

    def test_get_activities_content(self, client: TestClient):
        """Test the content of activities response."""
        response = client.get("/activities")
        data = response.json()
        
        chess_club = data["Chess Club"]
        assert chess_club["description"] == "Learn strategies and compete in chess tournaments"
        assert chess_club["schedule"] == "Fridays, 3:30 PM - 5:00 PM"
        assert chess_club["max_participants"] == 12
        assert "michael@mergington.edu" in chess_club["participants"]
        assert "daniel@mergington.edu" in chess_club["participants"]


class TestSignupEndpoint:
    """Test activity signup functionality."""

    def test_signup_success(self, client: TestClient):
        """Test successful signup for an activity."""
        response = client.post("/activities/Test%20Activity/signup?email=newstudent@mergington.edu")
        assert response.status_code == 200
        
        data = response.json()
        assert "message" in data
        assert "Signed up newstudent@mergington.edu for Test Activity" in data["message"]

    def test_signup_nonexistent_activity(self, client: TestClient):
        """Test signup for non-existent activity."""
        response = client.post("/activities/Nonexistent%20Activity/signup?email=student@mergington.edu")
        assert response.status_code == 404
        
        data = response.json()
        assert data["detail"] == "Activity not found"

    def test_signup_duplicate_participant(self, client: TestClient):
        """Test signup when participant is already registered."""
        # First signup should succeed
        response1 = client.post("/activities/Test%20Activity/signup?email=student@mergington.edu")
        assert response1.status_code == 200
        
        # Second signup should fail
        response2 = client.post("/activities/Test%20Activity/signup?email=student@mergington.edu")
        assert response2.status_code == 400
        
        data = response2.json()
        assert data["detail"] == "Student already signed up for this activity"

    def test_signup_existing_participant(self, client: TestClient):
        """Test signup when participant is already in the activity."""
        response = client.post("/activities/Chess%20Club/signup?email=michael@mergington.edu")
        assert response.status_code == 400
        
        data = response.json()
        assert data["detail"] == "Student already signed up for this activity"

    def test_signup_updates_participant_list(self, client: TestClient):
        """Test that signup actually adds participant to the activity."""
        # Get initial state
        response1 = client.get("/activities")
        initial_participants = response1.json()["Test Activity"]["participants"]
        initial_count = len(initial_participants)
        
        # Sign up new participant
        response2 = client.post("/activities/Test%20Activity/signup?email=newparticipant@mergington.edu")
        assert response2.status_code == 200
        
        # Check updated state
        response3 = client.get("/activities")
        updated_participants = response3.json()["Test Activity"]["participants"]
        
        assert len(updated_participants) == initial_count + 1
        assert "newparticipant@mergington.edu" in updated_participants


class TestRemoveParticipantEndpoint:
    """Test participant removal functionality."""

    def test_remove_participant_success(self, client: TestClient):
        """Test successful removal of a participant."""
        response = client.delete("/activities/Chess%20Club/participants/michael@mergington.edu")
        assert response.status_code == 200
        
        data = response.json()
        assert "message" in data
        assert "Removed michael@mergington.edu from Chess Club" in data["message"]

    def test_remove_participant_nonexistent_activity(self, client: TestClient):
        """Test removal from non-existent activity."""
        response = client.delete("/activities/Nonexistent%20Activity/participants/student@mergington.edu")
        assert response.status_code == 404
        
        data = response.json()
        assert data["detail"] == "Activity not found"

    def test_remove_participant_not_in_activity(self, client: TestClient):
        """Test removal of participant who is not in the activity."""
        response = client.delete("/activities/Chess%20Club/participants/nonexistent@mergington.edu")
        assert response.status_code == 404
        
        data = response.json()
        assert data["detail"] == "Participant not found in this activity"

    def test_remove_participant_updates_list(self, client: TestClient):
        """Test that removal actually removes participant from the activity."""
        # Get initial state
        response1 = client.get("/activities")
        initial_participants = response1.json()["Chess Club"]["participants"]
        initial_count = len(initial_participants)
        
        assert "michael@mergington.edu" in initial_participants
        
        # Remove participant
        response2 = client.delete("/activities/Chess%20Club/participants/michael@mergington.edu")
        assert response2.status_code == 200
        
        # Check updated state
        response3 = client.get("/activities")
        updated_participants = response3.json()["Chess Club"]["participants"]
        
        assert len(updated_participants) == initial_count - 1
        assert "michael@mergington.edu" not in updated_participants

    def test_remove_then_add_participant(self, client: TestClient):
        """Test removing and then re-adding the same participant."""
        email = "daniel@mergington.edu"
        activity = "Chess Club"
        
        # Remove participant
        response1 = client.delete(f"/activities/{activity}/participants/{email}")
        assert response1.status_code == 200
        
        # Add participant back
        response2 = client.post(f"/activities/{activity}/signup?email={email}")
        assert response2.status_code == 200
        
        # Verify participant is back in the list
        response3 = client.get("/activities")
        participants = response3.json()[activity]["participants"]
        assert email in participants


class TestEdgeCases:
    """Test edge cases and error conditions."""

    def test_url_encoding_in_activity_names(self, client: TestClient):
        """Test that URL encoding works properly for activity names with spaces."""
        # Test with URL encoded space
        response1 = client.post("/activities/Chess%20Club/signup?email=test@mergington.edu")
        assert response1.status_code == 200
        
        # Test removal with URL encoded space
        response2 = client.delete("/activities/Chess%20Club/participants/test@mergington.edu")
        assert response2.status_code == 200

    def test_email_encoding(self, client: TestClient):
        """Test that email addresses are properly handled."""
        # Test with email containing special characters
        email = "test+user@mergington.edu"
        encoded_email = "test%2Buser@mergington.edu"
        
        response1 = client.post(f"/activities/Test%20Activity/signup?email={encoded_email}")
        assert response1.status_code == 200
        
        response2 = client.delete(f"/activities/Test%20Activity/participants/{encoded_email}")
        assert response2.status_code == 200

    def test_activity_capacity_tracking(self, client: TestClient):
        """Test that we can track activity capacity correctly."""
        response = client.get("/activities")
        data = response.json()
        
        test_activity = data["Test Activity"]
        max_participants = test_activity["max_participants"]
        current_participants = len(test_activity["participants"])
        
        assert max_participants == 5
        assert current_participants == 0  # Test activity starts empty
        
        # Calculate spots left
        spots_left = max_participants - current_participants
        assert spots_left == 5