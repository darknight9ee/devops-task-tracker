from app import create_app

app = create_app()


def test_home():
    client = app.test_client()

    response = client.get("/")

    assert response.status_code == 200