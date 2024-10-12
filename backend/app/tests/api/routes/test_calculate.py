

from fastapi.testclient import TestClient
from sqlmodel import Session

from app.core.config import settings
from app.tests.utils.operation import create_random_operation


def test_read_operations(
     client: TestClient,
     db: Session,
     superuser_token_headers: dict[str, str]
) -> None:
    create_random_operation(db)
    
    response = client.post(
        f"{settings.API_V1_STR}/operations/",
        headers=superuser_token_headers,
    )
    assert response.status_code == 200