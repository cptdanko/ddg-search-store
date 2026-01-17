from typing import List, Optional
#from bs4 import BeautifulSoup
from fastapi import FastAPI, HTTPException
from sqlmodel import SQLModel, Field, Session, create_engine, select
import random
from ddgs import DDGS

# ---------- Models ----------

class SearchResult(SQLModel, table=True):
    id: Optional[str] = Field(default=None, primary_key=True)
    query: str
    title: str
    url: str
    snippet: str


class SearchCreate(SQLModel):
    query: str


class SearchResultRead(SQLModel):
    id: str
    query: str
    title: str
    url: str
    snippet: str


class SearchUpdate(SQLModel):
    title: Optional[str] = None
    snippet: Optional[str] = None

# ---------- DB setup ----------

sqlite_file_name = "searches.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"
engine = create_engine(sqlite_url, echo=False, connect_args={"check_same_thread": False})


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


app = FastAPI(on_startup=[create_db_and_tables])

# ---------- Helpers ----------

def perform_web_search(query: str, max_results: int = 10) -> List[dict]:
    try:
        with DDGS() as ddgs:
            raw = ddgs.text(query, max_results=max_results, region="us-en")
            cleaned = []
            for r in raw:
                # Defensive extraction and string conversion
                title = r.get("title") or ""
                href = r.get("href") or ""
                body = r.get("body") or ""
                cleaned.append({"title": str(title), "url": str(href), "snippet": str(body)})
            return cleaned
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"Search provider error: {exc}")


def getUniqueTitle(id:int, title: str): 
    return str(id) + "_" + title

# ---------- CRUD Endpoints ----------

# Create + search: perform web search for a term and store results
@app.post("/search", response_model=List[SearchResultRead])
def create_search(search: SearchCreate):
    print("received a request to search for ", search.query)
    results = perform_web_search(search.query)

    to_return: List[SearchResultRead] = []
    with Session(engine) as session:
        for r in results:
            id_no = random.randint(1, 999_999)
            id_str = getUniqueTitle(id_no, r["title"])
            print("title generated is " + id_str)

            db_obj = SearchResult(
                id=id_str,
                query=search.query,
                title=r["title"],
                url=r["url"],
                snippet=r["snippet"],
            )
            session.add(db_obj)
            # no auto-generated PK, so no need to refresh for id
            to_return.append(
                SearchResultRead(
                    id=db_obj.id,
                    query=db_obj.query,
                    title=db_obj.title,
                    url=db_obj.url,
                    snippet=db_obj.snippet,
                )
            )

        session.commit()

    return to_return


# Update: update title/snippet for a stored result
@app.get("/search/{result_id}", response_model=SearchResultRead)
def get_search_result(result_id: str):
    with Session(engine) as session:
        result = session.get(SearchResult, result_id)
        if not result:
            raise HTTPException(status_code=404, detail="Result not found")
        return result

@app.put("/search/{result_id}", response_model=SearchResultRead)
def update_search_result(result_id: str, payload: SearchUpdate):
    with Session(engine) as session:
        result = session.get(SearchResult, result_id)
        if not result:
            raise HTTPException(status_code=404, detail="Result not found")

        if payload.title is not None:
            result.title = payload.title
        if payload.snippet is not None:
            result.snippet = payload.snippet

        session.add(result)
        session.commit()
        session.refresh(result)
        return result

@app.delete("/search/{result_id}")
def delete_search_result(result_id: str):
    with Session(engine) as session:
        result = session.get(SearchResult, result_id)
        if not result:
            raise HTTPException(status_code=404, detail="Result not found")
        session.delete(result)
        session.commit()
        return {"detail": "Deleted"}


