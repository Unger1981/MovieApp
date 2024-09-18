import json
import os

def get_movies():
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
    json_file_path = os.path.join('Movies', 'movies.json')
    try:
        with open(json_file_path, 'w') as file:
            json.dump(movies, file)
    except OSError as e:
        print(f"OSError: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")


def add_movie(title, year, rating):
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
    try:
        movies = get_movies()
        for key, movie in movies.items():
            title = movie.get("title", "Unknown Title")
            if title == title_para:
                movie["rating"] = rating
        save_movies(movies)    
    except Exception as e:
        print(f"Error updating movie: {e}")
