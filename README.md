# Task requirements are in `TASK.md` file

Good luck!

## Project setup

## Prerequisites

- Python 2.7
- Node.js > 6.9, with npm > 3.0.0

## Setup

- `npm install`
- `pip install -r requirements.txt`
- (optional) run `pydevproject.py` to set up paths for pydev/eclipse

## Run all tests

- `npm run test %API_KEY%

Comment by Johan:
I had to add the API_KEY parameter to the test since it is needed to test the MovieFetcher

## Serve backend

- `npm run backend`
- `localhost:7070` as default

## Preview the database

- backend should be running
- `localhost:7000` as default

## Technologies used

- Python 2.7
- protorpc
- ndb
- Google AppEngine
- Datastore

## Instructions

To use MovieFetcher and the api, you need to do so by HTTP requests. I will here explain
how to do this using curl. For any of these methods, just open a new terminal and enter
the command as stated here.


## Downloading movies

curl -H \
   'content-type:application/json' \
   -d '{"api_key": "%VALUE%", "omdb_start_id": "%VALUE%", "nof_movies": "%VALUE%"}'\
   http://localhost:7070/MovieFetcher.fetch
   
Fields:

api_key (string): required
omdb_start_id (string): not required
nof_movies (integer): not required

Returns:
Result string


## Getting a movie:

```javascript
curl -H \
   'content-type:application/json' \
   -d '{"title": "%VALUE%"}'\
   http://localhost:7070/api.get_movie
```
Fields:
title (string): not required

Returns:
JSON-serializable string with movie data

## Getting a list of movie titles
```javascript
curl -H \
   'content-type:application/json' \
   -d '{"nof_movies": "%VALUE%"}'\
   http://localhost:7070/api.get_movie_list
```   
Fields:
nof_movies (integer): not required

Returns:
List of strings i.e. movie titles


## Adding a movie
```javascript
curl -H \
   'content-type:application/json' \
   -d '{"api_key": "%VALUE%", "title": "%VALUE%"}'\
   http://localhost:7070/api.add_movie
```   
Fields:
api_key (string): required
title (string): required

Returns:
Result string indicating how the operattion went


## Deleting a movie
```javascript
curl -H \
   'content-type:application/json' \
   -d '{"omdb_id": "%VALUE%"}'\
   http://localhost:7070/api.delete_movie
```   
Fields:
omdb_id (string): required

Returns:
Result string indicating how the operattion went

NOTE: There is no user authentication going on here. I did not have time to dig into all of that.
   
