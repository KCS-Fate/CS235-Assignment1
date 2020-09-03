import pytest

from Assignment1_Extensions import Director
from Assignment1_Extensions import Movie
from Assignment1_Extensions import Genre
from Assignment1_Extensions import Actor
from Assignment1_Extensions import Review
from Assignment1_Extensions import MovieFileCSVReader
from Assignment1_Extensions import User
from Assignment1_Extensions import WatchList


class TestExtensions:
    def test_movie_rating_update(self):
        user1 = User('Martin', 'pw12345')
        filename = 'Data1000Movies.csv'
        movie_file_reader = MovieFileCSVReader(filename)
        movie_file_reader.read_csv_file()
        movie = movie_file_reader.get_movie(Movie("Moana", 2016))
        review_text = "This movie was very enjoyable."
        rating = 8
        review = Review(movie, review_text, rating)
        user1.add_review(review)
        assert movie_file_reader.get_movie(Movie("Moana", 2016)).rating == 7.5

    def test_movie_new_rating(self):
        user1 = User('Martin', 'pw12345')
        filename = 'Data1000Movies.csv'
        movie_file_reader = MovieFileCSVReader(filename)
        movie_file_reader.read_csv_file()
        movie = movie_file_reader.get_movie(Movie("Rogue One", 2016))
        review_text = "This movie was very enjoyable."
        rating = 8
        review = Review(movie, review_text, rating)
        user1.add_review(review)
        assert movie_file_reader.get_movie(Movie("Rogue One", 2016)).rating == 8

    def test_movie_attributes(self):
        filename = 'Data1000Movies.csv'
        movie_file_reader = MovieFileCSVReader(filename)
        movie_file_reader.read_csv_file()
        movie = movie_file_reader.get_movie(Movie("Split", 2016))
        rating = movie.rating
        votes = movie.votes
        revenue = movie.revenue
        metascore = movie.metascore
        genres = movie.genres
        print(genres)
        assert rating == 7.3
        assert votes == 157606
        assert revenue == 138.12
        assert metascore == 62

    def test_watchlist(self):
        watchlist = WatchList()
        # Testing add and remove
        watchlist.add_movie(Movie("Moana", 2016))
        watchlist.add_movie(Movie("Ice Age", 2002))
        watchlist.add_movie(Movie("Guardians of the Galaxy", 2012))
        watchlist.add_movie(Movie("Guardians of the Galaxy", 2012))
        assert watchlist.size() == 3
        watchlist.remove_movie(Movie("Guardians of the Galaxy", 2012))
        assert watchlist.size() == 2
        watchlist.remove_movie(Movie("Guardians of the Galaxy", 2012))
        assert watchlist.size() == 2

        # Testing select for movies
        assert watchlist.first_movie_in_watchlist() == Movie("Moana", 2016)
        selected_movie = watchlist.select_movie_to_watch(1)
        assert selected_movie == Movie("Ice Age", 2002)
        selected_out_of_bounds = watchlist.select_movie_to_watch(3)
        assert selected_out_of_bounds == None

        # Testing iteration and next
        i = 0
        for item in watchlist:
            assert item == watchlist.select_movie_to_watch(i)
            i += 1

    def test_recommendations(self):
        user1 = User('Martin', 'pw12345')
        filename = 'Data1000MoviesTest.csv'
        movie_file_reader = MovieFileCSVReader(filename)
        movie_file_reader.read_csv_file()
        movie = movie_file_reader.get_movie(Movie("Moana", 2016))
        user1.watch_movie(movie_file_reader.get_movie(Movie("Moana", 2016)))
        user1.watchlist.add_movie(movie_file_reader.get_movie(Movie("Prometheus", 2012)))
        movie2 = movie_file_reader.get_movie(Movie("Guardians of the Galaxy", 2014))
        user1.watchlist.add_movie(movie2)
        print(user1.watchlist.watchlist)
        review_text = "This movie was very enjoyable."
        rating = 8
        review = Review(movie, review_text, rating)
        user1.add_review(review)
        recommendations = user1.give_recommendation_genre(movie_file_reader)
        assert recommendations == [Movie('Interstellar', 2014), Movie('Rogue One', 2016),
                                   Movie('Independence Day: Resurgence', 2016), Movie('X-Men: Apocalypse', 2016),
                                   Movie('Captain America: Civil War', 2016), Movie('Star Trek Beyond', 2016),
                                   Movie('Deadpool', 2016), Movie('The Secret Life of Pets', 2016),
                                   Movie('Trolls', 2016), Movie('Sausage Party', 2016)]

    def test_recommendations_empty(self):
        user1 = User('Martin', 'pw12345')
        filename = 'Data1000MoviesTest.csv'
        movie_file_reader = MovieFileCSVReader(filename)
        movie_file_reader.read_csv_file()
        recommendations = user1.give_recommendation_genre(movie_file_reader)
        assert recommendations == [Movie("Guardians of the Galaxy", 2014), Movie("Prometheus", 2012),
                                   Movie("Split", 2016), Movie("Sing", 2016), Movie("Suicide Squad", 2016),
                                   Movie("The Great Wall", 2016), Movie("La La Land", 2016), Movie("Mindhorn", 2016),
                                   Movie("The Lost City of Z", 2016), Movie("Passengers", 2016)]

    def test_recommendations_actor(self):
        user1 = User('Martin', 'pw12345')
        filename = 'Data1000Movies.csv'
        movie_file_reader = MovieFileCSVReader(filename)
        movie_file_reader.read_csv_file()
        movie = movie_file_reader.get_movie(Movie("Moana", 2016))
        user1.watch_movie(movie_file_reader.get_movie(Movie("Moana", 2016)))
        user1.watchlist.add_movie(movie_file_reader.get_movie(Movie("Prometheus", 2012)))
        movie2 = movie_file_reader.get_movie(Movie("Guardians of the Galaxy", 2014))
        user1.watchlist.add_movie(movie2)
        print(user1.watchlist.watchlist)
        review_text = "This movie was very enjoyable."
        rating = 8
        review = Review(movie, review_text, rating)
        user1.add_review(review)
        recommendations = user1.give_recommendation_actor(movie_file_reader)
        print(recommendations)