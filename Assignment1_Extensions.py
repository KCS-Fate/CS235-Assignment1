from datetime import datetime
import csv

class WatchList:
    def __init__(self):
        self.__watchlist = []

    @property
    def watchlist(self):
        return self.__watchlist

    def add_movie(self, movie):
        if type(movie) is Movie and movie not in self.__watchlist:
            self.__watchlist.append(movie)

    def remove_movie(self, movie):
        if type(movie) is Movie and movie in self.__watchlist:
            self.__watchlist.remove(movie)

    def first_movie_in_watchlist(self):
        return self.__watchlist[0]

    def select_movie_to_watch(self, index):
        if index < len(self.__watchlist):
            return self.__watchlist[index]
        else:
            return None

    def size(self):
        return len(self.__watchlist)

    def __iter__(self):
        self.pos = 0
        return self

    def __next__(self):
        if self.pos >= self.size():
            raise StopIteration
        else:
            self.pos += 1
            return self.__watchlist[self.pos - 1]


class User:
    def __init__(self, user_name: str, password: str):
        if user_name == "" or type(user_name) is not str:
            self.__user_name = None
        else:
            self.__user_name = user_name.strip().lower()

        if password == "" or type(password) is not str:
            self.__password = None
        else:
            self.__password = password.strip()

        self.__watched_movies = []
        self.__reviews = []
        self.__time_spent_watching_movies_minutes = 0
        self.__watchlist = WatchList()

    @property
    def user_name(self):
        return self.__user_name

    @property
    def password(self):
        return self.__password

    @property
    def watched_movies(self):
        return self.__watched_movies

    @property
    def reviews(self):
        return self.__reviews

    @property
    def time_spent_watching_movies_minutes(self):
        return self.__time_spent_watching_movies_minutes

    @property
    def watchlist(self):
        return self.__watchlist

    def __repr__(self):
        return f"<User {self.__user_name}>"

    def __eq__(self, other):
        return self.__user_name == other.__user_name

    def __lt__(self, other):
        return self.__user_name < other.__user_name

    def __hash__(self):
        return hash(self.__user_name)

    def watch_movie(self, watched_movie):
        if movie not in self.__watched_movies:
            self.__watched_movies.append(watched_movie)
        self.__time_spent_watching_movies_minutes += watched_movie.runtime_minutes

    def add_review(self, new_review):
        self.__reviews.append(new_review)
        new_review.movie.update_ratings(new_review)

    def top_ten(self, movie_database):
        recommendations = []
        for i in range(10):
            recommendations.append(movie_database.dataset_of_movies[i])
        return recommendations

    def give_recommendation_actor(self, movie_database):
        watched = 0
        will_watch = 0
        preference_list = {}
        recommended_movies = {}
        lowest_movie = None
        lowest_score = None
        if len(self.__watched_movies) != 0:
            watched = 1
        if self.__watchlist.size() != 0:
            will_watch = 1
        if watched == 0 and will_watch == 0:
            return self.top_ten(movie_database)
        if watched == 1:
            for movie in self.__watched_movies:
                weighting = 1
                for review in self.__reviews:
                    if review.movie == movie:
                        weighting = review.rating - 5
                for actor in movie.actors:
                    if actor not in preference_list:
                        preference_list[actor] = weighting
                    else:
                        preference_list[actor] += weighting
        if will_watch == 1:
            for movie in self.__watchlist.watchlist:
                weighting = 1
                for actor in movie.actors:
                    if actor not in preference_list:
                        preference_list[actor] = weighting
                    else:
                        preference_list[actor] += weighting
        for movie in movie_database.dataset_of_movies:
            relation = 0
            if movie in self.__watched_movies or movie in self.__watchlist.watchlist:
                continue
            for actor in movie.actors:
                relation += preference_list.get(actor, 0)
            if len(recommended_movies) == 0:
                recommended_movies[movie] = relation
                lowest_movie = movie
                lowest_score = relation
            else:
                if len(recommended_movies) < 10:
                    recommended_movies[movie] = relation
                    if relation < lowest_score:
                        lowest_score = relation
                        lowest_movie = movie
                else:
                    if relation > lowest_score:
                        recommended_movies.pop(lowest_movie)
                        recommended_movies[movie] = relation
                        lowest_movie = min(recommended_movies.keys(), key=(lambda k: recommended_movies[k]))
                        lowest_score = recommended_movies[lowest_movie]
        print(recommended_movies)
        print(preference_list)
        x = {key: value for key, value in sorted(recommended_movies.items(), key=lambda item: item[1])}
        top_ten_recommendations = list(x.keys())

        return top_ten_recommendations

    def give_recommendation_genre(self, movie_database):
        watched = 0
        will_watch = 0
        preference_list = {}
        recommended_movies = {}
        lowest_movie = None
        lowest_score = None
        if len(self.__watched_movies) != 0:
            watched = 1
        if self.__watchlist.size() != 0:
            will_watch = 1
        if watched == 0 and will_watch == 0:
            return self.top_ten(movie_database)
        if watched == 1:
            for movie in self.__watched_movies:
                weighting = 1
                for review in self.__reviews:
                    if review.movie == movie:
                        weighting = review.rating - 5
                for genre in movie.genres:
                    if genre not in preference_list:
                        preference_list[genre] = weighting
                    else:
                        preference_list[genre] += weighting
        if will_watch == 1:
            for movie in self.__watchlist.watchlist:
                weighting = 1
                for genre in movie.genres:
                    if genre not in preference_list:
                        preference_list[genre] = weighting
                    else:
                        preference_list[genre] += weighting
        for movie in movie_database.dataset_of_movies:
            relation = 0
            if movie in self.__watched_movies or movie in self.__watchlist.watchlist:
                continue
            for genre in movie.genres:
                relation += preference_list.get(genre, 0)
            if len(recommended_movies) == 0:
                recommended_movies[movie] = relation
                lowest_movie = movie
                lowest_score = relation
            else:
                if len(recommended_movies) < 10:
                    recommended_movies[movie] = relation
                    if relation < lowest_score:
                        lowest_score = relation
                        lowest_movie = movie
                else:
                    if relation > lowest_score:
                        recommended_movies.pop(lowest_movie)
                        recommended_movies[movie] = relation
                        lowest_movie = min(recommended_movies.keys(), key=(lambda k: recommended_movies[k]))
                        lowest_score = recommended_movies[lowest_movie]
        x = {key: value for key, value in sorted(recommended_movies.items(), key=lambda item: item[1])}
        top_ten_recommendations = list(x.keys())

        return top_ten_recommendations


class MovieFileCSVReader:

    def __init__(self, file_name: str):
        self.__file_name = file_name
        self.__dataset_of_movies = []
        self.__dataset_of_actors = []
        self.__dataset_of_directors = []
        self.__dataset_of_genres = []

    @property
    def dataset_of_movies(self):
        return self.__dataset_of_movies

    @property
    def dataset_of_actors(self):
        return self.__dataset_of_actors

    @property
    def dataset_of_directors(self):
        return self.__dataset_of_directors

    @property
    def dataset_of_genres(self):
        return self.__dataset_of_genres

    def get_movie(self, movie_name):
        if movie_name in self.__dataset_of_movies:
            x = self.__dataset_of_movies.index(movie_name)
            return self.__dataset_of_movies[x]
        return

    def read_csv_file(self):
        with open(self.__file_name, mode='r', encoding='utf-8-sig') as csvfile:
            movie_file_reader = csv.DictReader(csvfile)
            index = 0
            for row in movie_file_reader:
                if index == 0:
                    index += 1

                movie = Movie(row['Title'].strip(), int(row['Year'].strip()))
                genres = [Genre(x.strip()) for x in row['Genre'].split(',')]
                actors = [Actor(x.strip()) for x in row['Actors'].split(',')]
                director = Director(row['Director'].strip())
                movie.description = row['Description'].strip()
                movie.runtime_minutes = int(row['Runtime (Minutes)'].strip())
                movie.rating = float(row['Rating'].strip())
                movie.votes = int(row['Votes'].strip())
                revenue = row['Revenue (Millions)'].strip()
                metascore = row['Metascore'].strip()

                if revenue[0].isdigit():
                    movie.revenue = float(revenue)
                else:
                    movie.revenue = 'Not Available'

                if metascore[0].isdigit():
                    movie.metascore = float(metascore)
                else:
                    movie.metascore = 'Not Available'

                if movie not in self.__dataset_of_movies:
                    self.__dataset_of_movies.append(movie)

                for genre in genres:
                    if genre not in self.__dataset_of_genres:
                        self.__dataset_of_genres.append(genre)
                    movie.add_genre(genre)

                if director not in self.__dataset_of_directors:
                    self.__dataset_of_directors.append(director)
                movie.director = director

                for actor in actors:
                    if actor not in self.__dataset_of_actors:
                        self.__dataset_of_actors.append(actor)
                    movie.add_actor(actor)

                index += 1

class Review:
    def __init__(self, movie, review_text: str, rating: int):
        if type(movie) is not Movie:
            self.__movie = None
        else:
            self.__movie = movie

        if review_text == "" or type(review_text) is not str:
            self.__review_text = None
        else:
            self.__review_text = review_text

        if rating == "" or type(rating) is not int or rating > 10 or rating < 1:
            self.__rating = None
        else:
            self.__rating = rating

        self.__timestamp = datetime.now()

    @property
    def movie(self):
        return self.__movie

    @property
    def review_text(self):
        return self.__review_text

    @property
    def rating(self):
        return self.__rating

    @property
    def timestamp(self):
        return self.__timestamp

    def __repr__(self):
        return f"<Movie: {self.__movie}\nReview: {self.__review_text}\nRating: {self.__rating}\nWritten at: {self.__timestamp}>"

    def __eq__(self, other):
        return self.__movie == other.__movie and self.__review_text == other.__review_text and self.__rating == other.__rating

class Movie:
    def __init__(self, movie_full_name: str, movie_release_year: int):
        if movie_full_name == "" or type(movie_full_name) is not str:
            self.__movie_full_name = None
        else:
            self.__movie_full_name = movie_full_name.strip()

        if movie_release_year == "" or type(movie_release_year) is not int or movie_release_year < 1900:
            self.__movie_release_year = None
        else:
            self.__movie_release_year = movie_release_year
        self.__title = None
        self.__description = None
        self.__director = None
        self.__actors = []
        self.__genres = []
        self.__runtime_minutes = None
        self.__rating = 0
        self.__votes = 0
        self.__revenue = 'Not Available'
        self.__metascore = 'Not Available'

    @property
    def title(self):
        return self.__title

    @title.setter
    def title(self, movie_title: str):
        if movie_title == "" or type(movie_title) is not str:
            self.__title = None
        else:
            self.__title = movie_title.strip()
        return

    @property
    def description(self):
        return self.__description

    @description.setter
    def description(self, movie_description: str):
        if movie_description == "" or type(movie_description) is not str:
            self.__description = None
        else:
            self.__description = movie_description.strip()
        return

    @property
    def director(self):
        return self.__director

    @director.setter
    def director(self, movie_director):
        if type(movie_director) is not Director or movie_director.director_full_name == "":
            self.__director = None
        else:
            self.__director = movie_director
        return

    @property
    def actors(self):
        return self.__actors

    @property
    def genres(self):
        return self.__genres

    @property
    def runtime_minutes(self):
        return self.__runtime_minutes

    @runtime_minutes.setter
    def runtime_minutes(self, minutes: int):
        if minutes < 0 or type(minutes) is not int:
            raise ValueError
        else:
            self.__runtime_minutes = minutes
        return

    @property
    def rating(self):
        return round(self.__rating, 1)

    @rating.setter
    def rating(self, movie_rating: float):
        self.__rating = movie_rating

    @property
    def votes(self):
        return self.__votes

    @votes.setter
    def votes(self, total_votes: int):
        self.__votes = total_votes

    @property
    def revenue(self):
        return self.__revenue

    @revenue.setter
    def revenue(self, total_revenue):
        if type(total_revenue) is float:
            self.__revenue = total_revenue
        else:
            self.__revenue == 'Not Available'

    @property
    def metascore(self):
        return self.__metascore

    @metascore.setter
    def metascore(self, current_metascore: float):
        if type(current_metascore) is float:
            self.__metascore = current_metascore
        else:
            self.__metascore == 'Not Available'

    def add_genre(self, genre):
        if type(genre) is not Genre or genre.genre_full_name == "":
            return
        else:
            self.__genres.append(genre)
        return

    def remove_genre(self, genre_name):
        if genre_name in self.__genres:
            self.__genres.remove(genre_name)
        return

    def add_actor(self, actor):
        if type(actor) is not Actor or actor.actor_full_name == "":
            return
        else:
            self.__actors.append(actor)
        return

    def remove_actor(self, actor_name):
        if actor_name in self.__actors:
            self.__actors.remove(actor_name)
        return

    def update_ratings(self, review):
        self.__rating = ((self.__rating * self.__votes) + review.rating) / (self.__votes + 1)
        self.__votes += 1

    def __repr__(self):
        return f"<Movie {self.__movie_full_name}, {self.__movie_release_year}>"

    def __eq__(self, other):
        return self.__movie_full_name == other.__movie_full_name and self.__movie_release_year == other.__movie_release_year

    def __lt__(self, other):
        return (self.__movie_full_name, self.__movie_release_year) < (other.__movie_full_name, other.__movie_release_year)

    def __hash__(self):
        return hash(self.__movie_full_name + str(self.__movie_release_year))


class Director:

    def __init__(self, director_full_name: str):
        if director_full_name == "" or type(director_full_name) is not str:
            self.__director_full_name = None
        else:
            self.__director_full_name = director_full_name.strip()

    @property
    def director_full_name(self) -> str:
        return self.__director_full_name

    def __repr__(self):
        return f"<Director {self.__director_full_name}>"

    def __eq__(self, other):
        return self.__director_full_name == other.__director_full_name

    def __lt__(self, other):
        return other.__director_full_name > self.__director_full_name

    def __hash__(self):
        return hash(self.__director_full_name)


class Genre:

    def __init__(self, genre_name: str):
        if genre_name == "" or type(genre_name) is not str:
            self.__genre_full_name = None
        else:
            self.__genre_full_name = genre_name.strip()

    @property
    def genre_full_name(self) -> str:
        return self.__genre_full_name

    def __repr__(self):
        return f"<Genre {self.__genre_full_name}>"

    def __eq__(self, other):
        return self.__genre_full_name == other.__genre_full_name

    def __lt__(self, other):
        return other.__genre_full_name > self.__genre_full_name

    def __hash__(self):
        return hash(self.__genre_full_name)


class Actor:
    def __init__(self, actor_name: str):
        if actor_name == "" or type(actor_name) is not str:
            self.__actor_full_name = None
        else:
            self.__actor_full_name = actor_name.strip()
        self.__actor_colleagues = []

    @property
    def actor_full_name(self) -> str:
        return self.__actor_full_name

    def __repr__(self):
        return f"<Actor {self.__actor_full_name}>"

    def __eq__(self, other):
        return self.__actor_full_name == other.__actor_full_name

    def __lt__(self, other):
        return other.__actor_full_name > self.__actor_full_name

    def __hash__(self):
        return hash(self.__actor_full_name)

    def add_actor_colleague(self, colleague):
        if not self.check_if_this_actor_worked_with(colleague):
            self.__actor_colleagues.append(colleague)
        return

    def check_if_this_actor_worked_with(self, colleague):
        if colleague in self.__actor_colleagues:
            return True
        else:
            return False