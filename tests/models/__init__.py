import pytest
from sqlalchemy.orm import scoped_session
from app.models import SessionLocal, Base, engine
from app.services.access_token import AccessToken


class BaseTest:
    @pytest.fixture(autouse=True)
    def setup_and_teardown(self):
        # Setup
        Base.metadata.create_all(engine)
        self.session = scoped_session(SessionLocal)

        # Run the test
        yield

        # Teardown
        self.session.close()
        Base.metadata.drop_all(engine)

    @staticmethod
    def get_access_token(user_uuid: str, account_uuid: str):
        access_token = AccessToken()
        return access_token.encode(
            {
                'sub': user_uuid,
                'acc': account_uuid,
            },
        )
