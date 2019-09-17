from protorpc import messages
from protorpc import remote
from protorpc.wsgi import service

from backend.MovieFetcher import MovieFetcher

import backend.db_movie as db_movie

GET_MOVIE_FAILURE_MSG = "{'Failure': 'Movie %s was not found'}"
DELETE_MOVIE_SUCCESS_MSG = "{'Success': 'Movie with id %s was found and hopefully deleted'}"
DELETE_MOVIE_FAILURE_MSG = "{'Failure':'Movie with id %s was not found'}"
ADD_MOVIE_SUCCESS_MSG = '{"Success": "Successfully downloaded movie %s from omdb"}'
ADD_MOVIE_FAILURE_MSG = '{"Failure": "Failed to download movie %s from omdb"}'

DEFAULT_MOVIE_LIST_LENGTH = 10

class GetMovieRequest(messages.Message):
    title = messages.StringField(1, required=False)
    
class GetMovieResponse(messages.Message):
    movie_info = messages.StringField(1, required=True)
    
class GetMovieListRequest(messages.Message):
    nof_movies = messages.IntegerField(1, required=False)
    
class GetMovieListResponse(messages.Message):
    result = messages.StringField(1, repeated=True)
    
class DeleteMovieRequest(messages.Message):
    omdb_id = messages.StringField(1, required=True)
    
class DeleteMovieResponse(messages.Message):
    result = messages.StringField(1, required=True)
    
class AddMovieRequest(messages.Message):
    title = messages.StringField(1, required=True)
    api_key = messages.StringField(2, required=True)
    
class AddMovieResponse(messages.Message):
    result = messages.StringField(1, required=True)


class ApiService(remote.Service):

    # Returns movie if title is provided, else just gets the first movie
    @remote.method(GetMovieRequest, GetMovieResponse)
    def get_movie(self, request):
        
        q = db_movie.Movie.query()
        if request.title:
            q = q.filter(db_movie.Movie.title==request.title)
        movie = q.get()
        
        return GetMovieResponse(movie_info = movie.data if movie else GET_MOVIE_FAILURE_MSG % request.title)

    # Gets a list of a number of movies specified by the user
    @remote.method(GetMovieListRequest, GetMovieListResponse)
    def get_movie_list(self, request):

        
        nof_movies = request.nof_movies if request.nof_movies else DEFAULT_MOVIE_LIST_LENGTH
            
        q = db_movie.Movie.query()
        movies = q.fetch(nof_movies)
        
        movie_titles = []
        for movie in movies:
            movie_titles.append(movie.title)
        
        return GetMovieListResponse(result = movie_titles)
    
    # Deletes a movie my omdb id
    @remote.method(DeleteMovieRequest, DeleteMovieResponse)
    def delete_movie(self, request):
        q = db_movie.Movie.query()
        movie = q.filter(db_movie.Movie.omdb_id == request.omdb_id).get()
        
        if movie:
            movie.key.delete()
        
        return DeleteMovieResponse(result = DELETE_MOVIE_SUCCESS_MSG % request.omdb_id if movie else DELETE_MOVIE_FAILURE_MSG % request.omdb_id)
    
    # Adds a movie by title
    @remote.method(AddMovieRequest, AddMovieResponse)
    def add_movie(self, request):
        moviefetcher = MovieFetcher()
        success = moviefetcher.get_movie_by_title(request.api_key, request.title)
        return AddMovieResponse(result = ADD_MOVIE_SUCCESS_MSG % request.title if success else ADD_MOVIE_FAILURE_MSG % request.title)
    
        
# Map the RPC service and path (/api)
app = service.service_mappings([('/api.*', ApiService)])

