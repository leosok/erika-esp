import pytest
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.core import mail
from ninja.testing import TestClient

from erika_cloud import settings
from erika_cloud.utils.dj_mail_utils import send_password_reset
from typewriter.api import typewriter_router
from typewriter.models import Typewriter


@pytest.fixture
def api_client():
    """Fixture to provide the API test client."""
    return TestClient(typewriter_router)


@pytest.mark.django_db
def test_register_typewriter(api_client):
    # Arrange
    typewriter_data = {
        "uuid": "123e4567-e89b-12d3-a456-426614174000",
        "erika_name": "test_writer",
        "firstname": "John",
        "lastname": "Doe",
        "email": "l.sokolov@mailbox.org",
        "chat_active": True,
    }

    # Check that user doesn't exist before the test
    assert not User.objects.filter(email=typewriter_data["email"]).exists()

    # Act
    response = api_client.post("/new", json=typewriter_data)

    # Assert
    assert response.status_code == 200, f"Unexpected status code: {response.status_code}"
    response_data = response.json()

    # Check User object creation
    user = User.objects.get(email=typewriter_data["email"])
    assert user.username == "l.sokolov@mailbox.org"  # username is lowercase email
    assert user.first_name == "John"
    assert user.last_name == "Doe"
    assert user.is_active is True

    # Check Typewriter object creation and its relation to user
    typewriter = Typewriter.objects.get(uuid=typewriter_data["uuid"])
    assert typewriter.erika_name == "test_writer"
    assert typewriter.email == "test_writer@erika-cloud.de"
    assert typewriter.user == user  # Check the relationship
    assert typewriter.user.email == "l.sokolov@mailbox.org"
    assert typewriter.user.first_name == "John"
    assert typewriter.user.last_name == "Doe"

    # Check response content
    assert response_data["uuid"] == typewriter_data["uuid"]
    assert response_data["erika_name"] == "test_writer"
    assert response_data["user_email"] == "l.sokolov@mailbox.org"
    assert response_data["chat_active"] is True


@pytest.mark.django_db
def test_register_typewriter_existing_user(api_client):
    """Test registering a second typewriter with the same user email."""
    # Create first typewriter
    first_typewriter_data = {
        "uuid": "123e4567-e89b-12d3-a456-426614174000",
        "erika_name": "test_writer",
        "firstname": "John",
        "lastname": "Doe",
        "email": "l.sokolov@mailbox.org",
        "chat_active": True,
    }
    response1 = api_client.post("/new", json=first_typewriter_data)
    assert response1.status_code == 200

    # Create second typewriter with same email
    second_typewriter_data = {
        "uuid": "223e4567-e89b-12d3-a456-426614174111",
        "erika_name": "test_writer", # <-- Same name
        "firstname": "John",
        "lastname": "Doe",
        "email": "l.sokolov@mailbox.org",
        "chat_active": True,
    }
    response2 = api_client.post("/new", json=second_typewriter_data)
    assert response2.status_code == 200

    # Verify only one user exists
    assert User.objects.filter(email="l.sokolov@mailbox.org").count() == 1

    # Verify both typewriters exist and are linked to the same user
    user = User.objects.get(email="l.sokolov@mailbox.org")
    second_typewriter_as_2_added = Typewriter.objects.filter(user=user, erika_name="test_writer2")
    assert second_typewriter_as_2_added.exists()
    assert Typewriter.objects.filter(user=user).count() == 2



@pytest.mark.django_db
def test_password_reset_email():
    # Arrange
    mail.outbox = []  # Clear mail outbox
    user = User.objects.create(
        username="l.sokolov@mailbox.org",
        email="l.sokolov@mailbox.org",
        first_name="Test",
        last_name="User",
        is_active=True
    )

    # Act
    send_password_reset(user)

    # Assert
    assert len(mail.outbox) == 1, "Email was not sent"
    email = mail.outbox[0]
    assert email.to == ["l.sokolov@mailbox.org"]
    email_subject = email.subject
    assert "Erika Registrierung" in email_subject
    assert "reset" in email.body.lower()

