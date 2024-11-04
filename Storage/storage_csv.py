from Storage.istorage import IStorage
import os
import csv

class StorageCsv(IStorage):
    """Storage Class handling all CSV storage operations for movie_app.

    Parameters:
        IStorage (class): Abstract storage interface.

    Methods:
        get_movies(): Retrieves movies from the CSV file.
        save_movies(movies): Saves a collection of movies to the CSV file.
        add_movie(title, year, rating, poster): Adds a new movie to the CSV file.
        delete_movie(title_para): Deletes a movie by title from the CSV file.
        update_movie(title_para, rating): Updates the rating of a movie by title in the CSV file.
    """

    def __init__(self, file_path):
        """Initializes the StorageCsv with a file path for the CSV storage.

        Args:
            file_path (str): The path to the CSV file where movies are stored.
        """
        self.file_path = file_path

    def get_movies(self):
        """Retrieves all movies stored in the CSV file.

        Returns:
            dict: A dictionary of movies with keys as movie identifiers and values as movie details.
        """
        movies = {}
        try:
            with open(self.file_path, 'r') as file:
                reader = csv.DictReader(file)
                for idx, row in enumerate(reader, start=1):
                    movies[f"movie{idx}"] = {
                        "Title": row.get("Title", ""),
                        "Rating": float(row.get("Rating", 0)),
                        "Year": int(row.get("Year", 0)),
                        "Poster": row.get("Poster", ""),
                    }
        except FileNotFoundError:
            print("Error: The file movies.csv was not found in the Movies folder.")
        except Exception as e:
            print(f"Unexpected error: {e}")
        return movies

    def save_movies(self, movies):
        """Saves a collection of movies to the CSV file.

        Args:
            movies (dict): A dictionary of movies to save, with each value containing movie details.
        """
        try:
            with open(self.file_path, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["Title", "Rating", "Year", "Poster"])
                for movie in movies.values():
                    writer.writerow([movie["Title"], movie["Rating"], movie["Year"], movie["Poster"]])
        except OSError as e:
            print(f"OSError: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")

    def add_movie(self, title, year, rating, poster):
        """Adds a new movie to the CSV file.

        Args:
            title (str): Title of the movie.
            year (int): Release year of the movie.
            rating (float): Rating of the movie.
            poster (str): URL or path to the movie's poster.

        Returns:
            dict: The updated dictionary of movies.
        """
        try:
            movies = self.get_movies()
            new_key = f"movie{len(movies) + 1}"
            movies[new_key] = {
                "Title": title,
                "Year": year,
                "Rating": rating,
                "Poster": poster,
            }
            self.save_movies(movies)
            return movies
        except Exception as e:
            print(f"Error adding movie: {e}")
            return {}

    def delete_movie(self, title_para):
        """Deletes a movie by title from the CSV file.

        Args:
            title_para (str): The title of the movie to delete.
        """
        try:
            movies = self.get_movies()
            to_delete = None
            for key, movie in movies.items():
                if movie.get("Title", "") == title_para:
                    to_delete = key
            if to_delete:
                del movies[to_delete]
            self.save_movies(movies)
        except Exception as e:
            print(f"Error deleting movie: {e}")

    def update_movie(self, title_para, rating):
        """Updates the rating of a movie by title in the CSV file.

        Args:
            title_para (str): The title of the movie to update.
            rating (float): The new rating to assign to the movie.
        """
        try:
            movies = self.get_movies()
            for movie in movies.values():
                if movie.get("Title", "") == title_para:
                    movie["Rating"] = rating
            self.save_movies(movies)
        except Exception as e:
            print(f"Error updating movie: {e}")
