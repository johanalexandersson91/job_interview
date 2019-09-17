# coding: utf8

from backend.MovieFetcher import MovieFetcher
from backend import test
from backend.api import api
import sys


ref_title = "The Wolf of Wall Street"

ref_id = "0993846"

ref_movie_info = "{'Failure': 'Movie %s was not found'}" % ref_title

ref_add_movie_result = '{"Success": "Successfully downloaded movie %s from omdb"}' % ref_title

ref_delete_movie_result = "{'Failure':'Movie with id %s was not found'}" % ref_id


class TestApi(test.TestCase):
    api_key = ""
    
    def __init__(self, name):
        test.TestCase.__init__(self, name)
        self.api_key = sys.argv[1]
        self.moviefetcher = MovieFetcher()
        self.api_obj = api.ApiService()
        
    def test_get_movie(self):
        request = api.GetMovieRequest(title = ref_title)
        response = self.api_obj.get_movie(request)
        self.assertEqual(response.movie_info, ref_movie_info)
        
    def test_get_movie_list(self):
        request = api.GetMovieListRequest()
        response = self.api_obj.get_movie_list(request)
        self.assertEqual(response.result, [])
        
    def test_add_movie(self):
        request = api.AddMovieRequest(api_key = self.api_key, title = ref_title)
        response = self.api_obj.add_movie(request)
        self.assertEqual(response.result, ref_add_movie_result)
        
    def test_delete_movie(self):
        request = api.DeleteMovieRequest(omdb_id = ref_id)
        response = self.api_obj.delete_movie(request)
        self.assertEqual(response.result, ref_delete_movie_result)