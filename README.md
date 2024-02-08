# Chats

## Responsibilities

- Conversations

## Docs

The API definition can be found at /docs.

## Environment

Create new virtual environment

```
python3.10 -m venv venv
```

Activate the virtual environment

```
source venv/bin/activate
```

Install dependencies

```
pip install -r requirements.txt
```

## Tests

Running all tests

```
pytest
```

Running specific test suite

```
pytest ./tests/models/test_conversations.py::TestConversations
```

Running specific test case within suite

```
pytest ./tests/models/test_conversations.py::TestConversations::test_document
```

## Database

Migrations

Create a new migration

```
alembic revision --autogenerate -m "create users table"
```

To apply the migration

```
alembic upgrade head
```

To roll back the migration

```
alembic downgrade -1
```

## Running the application

Development mode

```
uvicorn app.main:app --reload
```

## Jobs

MacOS only workaround for fork issues

```
export OBJC_DISABLE_INITIALIZE_FORK_SAFETY=YES
```

Running the worker
```
python -m app.worker --with-scheduler
```