# coding: utf8

from backend.MovieFetcher import MovieFetcher
from backend import test
import sys

ref_id = "0993846"

ref_name = "The wolf of Wall Street"

ref_string = "{'Plot': 'Based on the true story of Jordan Belfort, from his rise to a wealthy stock-broker living the high life to his fall involving crime, corruption and the federal government.', 'Rated': 'R', 'Title': 'The Wolf of Wall Street', 'Ratings': [{'Source': 'Internet Movie Database', 'Value': '8.2/10'}, {'Source': 'Rotten Tomatoes', 'Value': '79%'}, {'Source': 'Metacritic', 'Value': '75/100'}], 'DVD': '25 Mar 2014', 'Writer': 'Terence Winter (screenplay), Jordan Belfort (book)', 'Production': 'Paramount Studios', 'Actors': 'Leonardo DiCaprio, Jonah Hill, Margot Robbie, Matthew McConaughey', 'Type': 'movie', 'imdbVotes': '1,052,347', 'Website': 'http://www.thewolfofwallstreet.com/', 'Poster': 'https://m.media-amazon.com/images/M/MV5BMjIxMjgxNTk0MF5BMl5BanBnXkFtZTgwNjIyOTg2MDE@._V1_SX300.jpg', 'Director': 'Martin Scorsese', 'Released': '25 Dec 2013', 'Awards': 'Nominated for 5 Oscars. Another 38 wins & 165 nominations.', 'Genre': 'Biography, Crime, Drama', 'imdbRating': '8.2', 'Language': 'English, French', 'Country': 'USA', 'BoxOffice': '$91,330,760', 'Runtime': '180 min', 'imdbID': 'tt0993846', 'Metascore': '75', 'Response': 'True', 'Year': '2013'}"

class TestMovieFetcher(test.TestCase):
	api_key = ""
	
	def __init__(self, name):
		test.TestCase.__init__(self, name)
		self.api_key = sys.argv[1]
		self.moviefetcher = MovieFetcher()
		
	def test_get_movie(self):
		movie = self.moviefetcher.get_movie(self.api_key, "i", "tt%s" % ref_id)
		self.assertEqual(str(movie), ref_string)
		
	def test_get_movies_by_id(self):
		self.assertEqual(True, self.moviefetcher.get_movies_by_id(self.api_key, ref_id, 10))
		
	def test_get_movies_by_name(self):
		self.assertEqual(True, self.moviefetcher.get_movie_by_title(self.api_key, ref_name))
		