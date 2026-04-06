# openmusicapi


a community music database api for music

---

## what it does

- look up artists, albums and tracks
- filter by genre, country, year, name, etc
- submit new artists/albums/tracks (needs a hack club account)
- see who submitted what
- live stats on how many artists/albums/tracks are in the db


## auth

uses hack club auth (oauth2). you need a hack club account to post stuff, but anyone can read everything.

1. go to `/auth/login`
2. log in with hack club
3. you get a token back — save it
4. use it like: `Authorization: Bearer <your token>`

---

## endpoints

### artists
- `GET /artists` — list all artists. filter with `?genre=darkwave`, `?country=Sweden`, `?search=ashbury`
- `GET /artists/{id}` — get one artist
- `POST /artists` — add an artist (auth required)

### albums
- `GET /albums` — list albums. filter with `?artist_id=1`, `?year=2007`, `?genre=ebm`
- `GET /albums/{id}` — get one album
- `POST /albums` — add an album (auth required)

### tracks
- `GET /tracks` — list tracks. filter with `?album_id=1` or `?artist_id=1`
- `GET /tracks/{id}` — get one track
- `POST /tracks` — add a track (auth required)

### you
- `GET /me` — your profile + everything you've submitted (auth required)

### misc
- `GET /stats` — how many artists/albums/tracks are in the db + most hit endpoints

---

## example requests

```bash
# get all darkwave artists
curl "/artists?genre=darkwave"

# get albums from 2007
curl "/albums?year=2007"
---

## running locally

```bash
git clone https://github.com/leotheteo/openmusicapi
cd openmusicapi
pip install -r requirements.txt
uvicorn main:app --reload
```

then go to `http://localhost:8000/docs`

you also need these env vars for auth to work:
```
HC_CLIENT_ID=...
HC_CLIENT_SECRET=...
HC_REDIRECT_URI=http://localhost:8000/auth/callback
```

get those by making an app at [auth.hackclub.com/developer/apps/new](https://auth.hackclub.com/developer/apps/new) (turn on developer mode in your hack club settings first)

---

## stack

- fastapi
- sqlite
- uvicorn
- httpx (for hack club auth)
- pydantic v2

---

add more!! that's the whole point

okay and now to get to coding 😭
