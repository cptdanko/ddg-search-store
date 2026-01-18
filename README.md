# 🚀 DDG Search Store

[![GitHub Repo stars](https://img.shields.io/github/stars/cptdanko/ddg-search-store?style=social)](https://github.com/cptdanko/ddg-search-store)
[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115.0-brightgreen.svg)](https://fastapi.tiangolo.com/)
[![SQLModel](https://img.shields.io/badge/SQLModel-0.0.22-blueviolet.svg)](https://sqlmodel.tiangolo.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![DuckDuckGo](https://img.shields.io/badge/DuckDuckGo-Privacy%20First-orange.svg)](https://duckduckgo.com/)

**A lightweight FastAPI service that performs DuckDuckGo searches, stores results in SQLite via SQLModel, and exposes full CRUD endpoints for saved search results.**

Perfect starter for **search APIs**, **microservices**, and **backend development**. Privacy-focused (no API keys), production-ready patterns, zero-config setup.

## ✨ Features

| Feature | Description |
|---------|-------------|
| 🔍 **Real-time Search** | DuckDuckGo integration via `ddgs` (no API keys, privacy-first) |
| 🗄️ **SQLite ORM** | SQLModel (Pydantic + SQLAlchemy) with auto-schema generation |
| ⚡ **Full CRUD** | Create/Read/Update/Delete search results with proper validation |
| 📱 **Auto-Docs** | Interactive Swagger UI (`/docs`) & ReDoc (`/redoc`) |
| 🎯 **Unique IDs** | Custom `random_{title_slug}` string primary keys |
| 🔒 **Session Safety** | Proper SQLAlchemy session management (no DetachedInstanceError) |
| 🚀 **Zero Config** | Single `main.py`, runs in seconds |

## 🎯 Quick Start

## 1. Clone & Install
```bash
git clone https://github.com/cptdanko/ddg-search-store.git
cd ddg-search-store
pip install -r requirements.txt  # or: pip install fastapi uvicorn sqlmodel ddgs
```

## 2. Run Server
```bash
uvicorn main:app --reload
✅ Server running at http://127.0.0.1:8000
```

## 3. Open Interactive Docs
Swagger UI ← Try endpoints live


### 🔧 API Reference

##### Search & Store Results
```bash
curl -X POST "http://127.0.0.1:8000/search" \
  -H "Content-Type: application/json" \
  -d '{"query": "FastAPI best practices"}'
Response: Array of saved results with unique ids.
```
##### List Results

```bash
# All results
curl "http://127.0.0.1:8000/search"

# Filter by query
curl "http://127.0.0.1:8000/search?query=FastAPI"
Single Result Operations
text
GET    /search/{result_id}     # Retrieve
PUT    /search/{result_id}     # Update title/snippet
DELETE /search/{result_id}     # Delete
Example IDs: "12345_FastAPI_SQLModel_tutorial", "67890_Backend_development_guide"
```

#### 🏗️ Architecture Overview
```ascii
Frontend/Postman    →    FastAPI Routes    →    DuckDuckGo Search
    │                        │                        │
    ↓                        ↓                        ↓
Swagger UI      ←    SQLModel ORM    ←    SQLite DB (searches.db)
                                       (TEXT PK, auto-schema)
````

###### Data Flow

POST /search?q=query → DDG search → Parse 10 results

Generate unique id (random_{title_slug})

Bulk INSERT to SQLite via SQLModel Session

Return SearchResultRead[] with full metadata

### 📦 Installation Options

#### Locally 

You can setup a virtual environment
```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```
```

#### 🧪 Testing

Pytest (add pytest to dev deps)
```python
def test_search_persists():
    resp = client.post("/search", json={"query": "test"})
    assert resp.status_code == 200
    assert len(resp.json()) > 0
    assert "id" in resp.json()
```
##### Load Test

```bash
hey -n 100 -c 10 https://localhost:8000/search
```

### 🔍 Troubleshooting
| Issue |	Solution |
| ----- | --------- |
| datatype mismatch	| Delete searches.db, restart (TEXT PK recreated) |
| DetachedInstanceError |	Use SearchResultRead.from_orm(obj) before session closes |
| DDG 202/rate limit | Library handles retries   add proxies if blocked |
| No results | Check ddgs.text() returns list; test in Python shell |

### 📚 Related Resources
##### Deep Dives & Tutorials:

Build a FastAPI Streaming API with Llama 3 and Ollama - Advanced FastAPI patterns 
https://mydaytodo.com/fastapi-ollama-llama3-streaming-api/

Mastering BFF Pattern: Node.js, React, TypeScript, Java - Microservices architecture insights 
https://mydaytodo.com/mastering-bff-pattern-nodejs-react-typescript-java-microservices/

##### Official Docs:

FastAPI - Web framework
https://fastapi.tiangolo.com/

SQLModel - Pydantic ORM
https://sqlmodel.tiangolo.com/tutorial/fastapi/

DDGS - DuckDuckGo search client
https://pypi.org/project/duckduckgo-search/

## 🤝 Contributing
Fork → Clone → Branch (feat/add-auth)

Install dev deps: pip install -r requirements-dev.txt

Code → Test → PR

Follow 
FastAPI Best Practices


## ⭐ Star if useful! 🚀