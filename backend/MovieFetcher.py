import httplib2
import ast

from protorpc import messages
from protorpc import remote
from protorpc.wsgi import service

import backend.db_movie as db_movie

DEFAULT_OMDB_ID = "0094291" # Wall street
DEFAULT_NOF_MOVIES = 100
FAILURE_MSG = "{'Failure': 'Some exception occured. Downloading of movies has stopped'}"
SUCCESS_MSG = "{'Success': 'Movies were successfully downloaded'}"
MAXIMUM_RETRIES = 5

class MovieFetcher:

    # Obtains a movie from OMDB and returns as dict
    def get_movie(self, apikey, lookup_type, lookup_value):
        h = httplib2.Http()
        (resp_headers, content) = h.request("http://www.omdbapi.com/?apikey=%s&%s=%s" % (apikey, lookup_type, lookup_value), "GET")
        status_code = int(resp_headers['status'])
        # Convert response spring to dict
        content_dict = ast.literal_eval(content)
        
        # TODO: Improve exception handling for movie fetching. It is completely useless at the moment ;)
        response = content_dict['Response']
        # Sometimes OMDB gives a "False" response even when the return code is 200. Not sure why. Ignore for now
        if status_code == 400 or response == "False":
            print "Movie %s was not found" % lookup_value
            return None
        elif status_code == 401:
            print "Invalid API key supplied. "
            return None
        elif status_code == 200:
            return content_dict
        else:
            print "Unhandled exception %s" % status_code
            return None
            
    # Writes the movie data to the database
    def write_to_db(self, movie_info, omdb_id):  # pragma: no cover
        title=movie_info["Title"]
        db_entry = db_movie.Movie(title=title, data=str(movie_info), omdb_id = omdb_id)
        db_entry.put()

    # Gets a user-specified amount of movies and stores in database
    # TODO: Decrease spaghetti-factor
    def get_movies_by_id(self, apikey, start_id, nof_ids):
        movies_stored = 0
        retries = 0
        i= 0
        # Run loop until we have obtained enough id's
        while movies_stored < nof_ids:
            movie_id = str(int(start_id)+i).zfill(7)
            movie_info = self.get_movie(apikey, "i", "tt%s" % movie_id)
            if movie_info == None:
                retries+=1
            else:
                movies_stored+=1
                self.write_to_db(movie_info, movie_id)
            if retries > MAXIMUM_RETRIES:
                break;
                return False
            i+=1
        return True
        
    def get_movie_by_title(self, api_key, title):
        movie_info = self.get_movie(api_key, "t", title.replace(" ", "+"))
        if movie_info == None:
            return False
        else:
            movie_id = movie_info["imdbID"]
            self.write_to_db(movie_info, movie_id.replace("tt", ""))
            return True
                

class MovieFetcherRequest(messages.Message):  # pragma: no cover
    api_key = messages.StringField(1, required=True)
    omdb_start_id = messages.StringField(2, required=False)
    nof_movies = messages.IntegerField(3, required=False)
    

class MovieFetcherResponse(messages.Message):  # pragma: no cover
    result = messages.StringField(1, required=True)


class MovieFetcherService(remote.Service): # pragma: no cover
    @remote.method(MovieFetcherRequest, MovieFetcherResponse)
    def fetch(self, request):
        # Use default start id if it is not supplied in the request
        start_id = request.omdb_start_id if request.omdb_start_id else DEFAULT_OMDB_ID
        # Use default number of movies if it is not supplied in the request
        nof_movies = request.nof_movies if request.nof_movies else DEFAULT_NOF_MOVIES
        
        moviefetcher = MovieFetcher()
        success = moviefetcher.get_movies_by_id(request.api_key, start_id, nof_movies)

        return MovieFetcherResponse(result = SUCCESS_MSG if success else FAILURE_MSG)               
        
# Map the RPC service and path (/MovieFetcher.fetch)
app = service.service_mappings([('/MovieFetcher.*', MovieFetcherService)])


        
