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