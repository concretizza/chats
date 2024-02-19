server:
	uvicorn app.main:app --reload

jobs:
	python -m app.worker --with-scheduler
