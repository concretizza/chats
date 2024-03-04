server:
	uvicorn app.main:app --port 8001 --reload

jobs:
	python -m app.worker --with-scheduler
