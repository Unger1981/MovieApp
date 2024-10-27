import json
import os


def get_movies():
    """
    Reads the movies from the 'movies.json' file and returns them as a dictionary.

    Returns:
        dict: A dictionary containing movie information.
    """
    json_file_path = os.path.join('Movies', 'movies.json')
    try:
        with open(json_file_path, 'r') as file:
            movies = json.load(file)
        return movies
    except FileNotFoundError:
        print("Error: The file movies.json was not found in the Movies folder.")
        return {}
    except json.JSONDecodeError:
        print("Error: Failed to decode JSON from the file.")
        return {}
    except Exception as e:
        print(f"Unexpected error: {e}")
        return {}


def save_movies(movies):
    """
    Saves the given movie dictionary to the 'movies.json' file.
    """
    json_file_path = os.path.join('Movies', 'movies.json')
    try:
        with open(json_file_path, 'w') as file:
            json.dump(movies, file)
    except OSError as e:
        print(f"OSError: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")


def add_movie(title, year, rating):
    """
    Adds a new movie to the database.

    Args:
        title (str): The title of the movie.
        year (int): The year of release.
        rating (float): The rating of the movie.

    Returns:
        dict: The updated movie dictionary.
    """
    try:
        movies = get_movies()
        new_key = f"movie{len(movies) + 1}"
        movies[new_key] = {
            "title": title,
            "rating": rating,
            "year_of_release": year,
        }
        save_movies(movies)
        return movies
    except Exception as e:
        print(f"Error adding movie: {e}")
        return {}


def delete_movie(title_para):
    """
    Deletes a movie from the database based on its title.

    Args:
        title_para (str): The title of the movie to delete.
    """
    try:
        movies = get_movies()
        to_delete = None
        for key, movie in movies.items():
            title = movie.get("title", "Unknown Title")
            if title == title_para:
                to_delete = key
        if to_delete:
            del movies[to_delete]
        save_movies(movies)
    except Exception as e:
        print(f"Error deleting movie: {e}")


def update_movie(title_para, rating):
    """
    Updates the rating of a movie in the database.

    Args:
        title_para (str): The title of the movie to update.
        rating (float): The new rating for the movie.
    """
    try:
        movies = get_movies()
        for key, movie in movies.items():
            title = movie.get("title", "Unknown Title")
            if title == title_para:
                movie["rating"] = rating
        save_movies(movies)
    except Exception as e:
        print(f"Error updating movie: {e}")