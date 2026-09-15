from fastapi.testclient import TestClient

from src.app import app

client = TestClient(app)


def test_unregister_participant_removes_email():
    activity_name = "Soccer Team"
    email = "newstudent@mergington.edu"

    # Ensure the email is not already present.
    activity = client.get("/activities").json()[activity_name]
    if email in activity["participants"]:
        client.delete(f"/activities/{activity_name}/participants?email={email}")

    signup_response = client.post(f"/activities/{activity_name}/signup?email={email}")
    assert signup_response.status_code == 200

    delete_response = client.delete(f"/activities/{activity_name}/participants?email={email}")
    assert delete_response.status_code == 200
    assert email not in client.get("/activities").json()[activity_name]["participants"]
