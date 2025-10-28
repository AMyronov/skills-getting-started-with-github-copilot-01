import pytest
from fastapi.testclient import TestClient
from src.app import app

@pytest.fixture
def client():
    """Create a test client for the FastAPI application."""
    return TestClient(app)

@pytest.fixture
def sample_activities():
    """Sample activities data for testing."""
    return {
        "Chess Club": {
            "description": "Learn strategies and compete in chess tournaments",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 12,
            "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
        },
        "Programming Class": {
            "description": "Learn programming fundamentals and build software projects",
            "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
            "max_participants": 20,
            "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
        }
    }

@pytest.fixture(autouse=True)
def reset_activities():
    """Reset activities to initial state before each test."""
    from src.app import activities
    
    # Store original activities
    original_activities = activities.copy()
    
    # Reset to known state for testing
    activities.clear()
    activities.update({
        "Chess Club": {
            "description": "Learn strategies and compete in chess tournaments",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 12,
            "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
        },
        "Programming Class": {
            "description": "Learn programming fundamentals and build software projects",
            "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
            "max_participants": 20,
            "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
        },
        "Test Activity": {
            "description": "Test activity for testing purposes",
            "schedule": "Daily, 1:00 PM - 2:00 PM",
            "max_participants": 5,
            "participants": []
        }
    })
    
    yield
    
    # Restore original activities after test
    activities.clear()
    activities.update(original_activities)