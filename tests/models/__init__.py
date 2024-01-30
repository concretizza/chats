import pytest
from sqlalchemy.orm import scoped_session
from app.models import SessionLocal, Base, engine


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
