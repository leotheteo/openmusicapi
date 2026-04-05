from fastapi import FastAPI, HTTPException, Query, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from typing import Optional, List
import sqlite3
import time
from contextlib import contextmanager
from models import (
    Artist, ArtistCreate,
    Album, AlbumCreate,
    Track, TrackCreate,
    StatsResponse,
)
from database import init_db, get_db, record_request
app=FastAPI(
    title="Open Music API",
    description="A simple API for adding and querying artists, albums, and tracks.",
    version="1.0.0",
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.on_event("startup")
def startup():
    init_db()
#------------------------------- artists-------------
@app.get(
    "/artists",
    response_model=List[Artist],
    tags=["Artists"],
    summary="List all artists",
    description="Retrieve a list of artists in the database. Supports searching by genre, country and name",
)
def list_artists(
    genre: Optional[str] = Query(None, description="Filter artists by genre"),
    country: Optional[str] = Query(None, description="Filter artists by country"),
    search: Optional[str] = Query(None, description="Search artists by name"),
    limit: int = Query(50, le=200, description="Limit the number of results returned (max 200)"),
    offset: int = Query(0, description="Offset for pagination"),
    db: sqlite3.Connection = Depends(get_db),
):
    record_request(db, "/artists", "GET")
    query = "SELECT * FROM artists WHERE 1=1"
    params = []
    if genre:
        query += " AND LOWER(genre) LIKE LOWER(?)"
        params.append(f"%{genre}%")
    if country:
        query += " AND LOWER(country) = LOWER(?)"
        params.append(country)
    if search:
        query += " AND LOWER(name) LIKE LOWER(?)"
        params.append(f"%{search}%")
    query += " ORDER BY name LIMIT ? OFFSET ?"
    params += [limit, offset]
    rows = db.execute(query, params).fetchall()
    return [dict(r) for r in rows]
 
 @app.get(
    "/artists/{artist_id}",
    response_model=Artist,
    tags=["Artists"],
    summary="Get a single artist by ID",
)
def get_artist(artist_id: int, db: sqlite3.Connection = Depends(get_db)):
    record_request(db, f"/artists/{artist_id}", "GET")
    row = db.execute("SELECT * FROM artists WHERE id = ?", (artist_id,)).fetchone()
    if not row:
        raise HTTPException(status_code=404, detail="Artist not found")
    return dict(row)


@app.post(
    "/artists",
    response_model=Artist,
    status_code=201,
    tags=["Artists"],
    summary="Create a new artist",
    description="""
    Submits a new artist to the database.
    """,
)
def create_artist(artist: ArtistCreate, db: sqlite3.Connection = Depends(get_db)):
    user: dict = Depends(require auth))):
    record_request(db, "/artists", "POST")
    existing = db.execute(
        "SELECT id FROM artists WHERE LOWER(name) = LOWER(?)", (artist.name,)
    ).fetchone()
        if existing:
        raise HTTPException(status_code=409, detail=f"Artist '{artist.name}' already exists (id={existing['id']})")
    cursor = db.execute(
        "INSERT INTO artists (name, genre, country, formed_year, bio, website, submitted_by) VALUES (?,?,?,?,?,?,?)",
        (artist.name, artist.genre, artist.country, artist.formed_year, artist.bio, artist.website, user["id"]),
    )
    db.commit()
    return dict(db.execute("SELECT * FROM artists WHERE id = ?", (cursor.lastrowid,)).fetchone()
    )                
@app.get(
    "/albums",
    response_model=List[Album],
    tags=["Albums"],
    summary="List albums",
    description="""
Returns albums. Filter by **artist_id**, **year**, or **genre**."""
)                
def list_albums(
    artist_id: Optional[int] = Query(None, description="Filter albums by artist ID"),
    year: Optional[int] = Query(None, description="Filter albums by release year"),
    genre: Optional[str] = Query(None, description="Filter albums by genre"),
    limit: int = Query(50, le=200, description="Limit the number of results returned (max 200)"),
    offset: int = Query(0, description="Offset for pagination"),
    db: sqlite3.Connection = Depends(get_db),
):
    record_request(db, "/albums", "GET")
    query = "SELECT * FROM albums WHERE 1=1"
    params = []
    if artist_id:
        query += " AND artist_id = ?"
        params.append(artist_id)
    if year:
        query += " AND release_year = ?"
        params.append(year)
    if genre:
        query += " AND LOWER(genre) LIKE LOWER(?)"
        params.append(f"%{genre}%")
    query += " ORDER BY title LIMIT ? OFFSET ?"
    params += [limit, offset]
    rows = db.execute(query, params).fetchall()
    return [dict(r) for r in rows]