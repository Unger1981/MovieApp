import statistics
import random
import os
from fuzzywuzzy import fuzz
import tkinter as tk
from tkinter import filedialog
import matplotlib.pyplot as plt
from OMDbAPI import Fetch_Movie

class MovieApp:
    """
    A movie management application that allows users to perform various operations on a movie database.

    This application provides a command-line interface (CLI) to interact with movies stored in a database.
    Users can list, add, delete, update, and search for movies, as well as generate statistics, sort movies by rating or year, and create rating histograms.
    
    Attributes:
        storage (Storage): An object representing the storage system to hold and retrieve movie data.

    Methods:
        print_menu(): Prints the main menu options to the console.
        menu_user_input(): Handles menu selection and calls the appropriate method.
        list_movies(): Lists all movies in the database.
        add_movie_input(): Prompts the user to add a new movie to the database.
        del_movie(): Deletes a specified movie from the database.
        upd_movie(): Updates the rating of a specified movie in the database.
        stats(): Calculates and displays various statistics about the movies.
        random_movies(): Displays a randomly selected movie from the database.
        search_movies(): Searches for movies by title, with fuzzy matching for close matches.
        movies_sorted_rating(): Lists movies sorted by their rating.
        movies_sorted_year(): Lists movies sorted by year of release.
        rating_histo(): Creates a histogram of movie ratings and saves it to a file.
        run(): Initiates the main menu and handles user interactions.
    """
    def __init__(self, storage):
        self.storage = storage


    def print_menu(self):
        """
        Prints the main menu to the console.
        """
        print()
        print("********** My Movies Database **********")
        print()
        print("Menu:")
        print("0. Exit")
        print("1. List movies")
        print("2. Add movie")
        print("3. Delete movie")
        print("4. Update movie")
        print("5. Stats")
        print("6. Random movie")
        print("7. Search movie")
        print("8. Movies sorted by rating")
        print("9. Movies sorted by year")
        print("10. Create Rating Histogram")
        print("11. Create HTML")


    def menu_user_input(self):
        """
        Handles user input for the main menu and calls the appropriate function based on the user's choice.
        """
        while True:
            try:
                print()
                user_choice = int(input("Enter choice (0-11) "))
                print()
                break
            except ValueError as e:
                print(f"Invalid Input. Error {e}")
        if user_choice == 1:
            print("TEST")
            self.list_movies()
        elif user_choice == 2:
            self.add_movie_input()
        elif user_choice == 3:
            self.del_movie()
        elif user_choice == 4:
            self.upd_movie()
        elif user_choice == 5:
            self.stats()
        elif user_choice == 6:
            self.random_movies()
        elif user_choice == 7:
            self.search_movies()
        elif user_choice == 8:
            self.movies_sorted_rating()
        elif user_choice == 9:
            self.movies_sorted_year()
        elif user_choice == 10:
            self.rating_histo()
        elif user_choice == 11:
            self.generate_web()    
        elif user_choice == 0:
            print("Bye!")
            return
        else:
            print("***Invalid input. Please choose a number between 0 and 9.***")
            self.print_menu()
            self.menu_user_input()    


    def list_movies(self):
        """
        Prints a list of all movies stored in the database.
        """
        print("List of movies in database")
        print("**************************")
        try:
            movies = self.storage.get_movies()
        except FileNotFoundError as e:
            print(f"Could not load Movie Data. Error {e}")
            self.print_menu()
            self.menu_user_input()
            return 1
        for index, (key, movie) in enumerate(movies.items()):
            Title = movie.get("Title", "Unknown Title")
            Rating = movie.get("Rating", "No Rating")
            Year = movie.get("Year", "Unknown Year")
            print(f"{index + 1}. {Title} (Rating: {Rating}), Year: {Year}")
        self.print_menu()
        self.menu_user_input()

    def add_movie_input(self):
        """
        Prompts the user to enter details for a new movie and adds it to the database.
        """
        try:
            movies = self.storage.get_movies()
        except FileNotFoundError as e:
            print(f"Could not load Movie Data. Error {e}")
            return
        try:
            movie_add_by_user = input("Please enter the movie title you want to add ")
        except ValueError as e:
                print(f"No valid input. Please try again. Error {e}")
        try:        
            movie = Fetch_Movie(movie_add_by_user)    
            print(movie)
            if movie == None:
                print("Error while trying to fetch movie data")  
                return  
        except Exception as e:
            print(f"API fail. Error: {e}")        
        for key in movie:
            Title = movie.get("Title", "No Title")
            Year = movie.get("Year", "No Year")
            Rating = movie.get("imdbRating", "No rating")
            Poster = movie.get("Poster", "No Poster")
        try:
            movies = self.storage.add_movie(Title, Year, Rating, Poster)
            
            print()
            print("***Movie added to database***")
            print()
            self.print_menu()
            self.menu_user_input()
        except FileNotFoundError as e:
            print(f"Couldnt find storage destination. Error {e}")
            self.print_menu()
            self.menu_user_input()
    
    def del_movie(self):
        """
        Prompts the user to select a movie to delete and removes it from the database.
        """
        try:
            movies = self.storage.get_movies()
        except FileNotFoundError as e:
            print(f"Could not load Movie Data. Error {e}")
            return
        for index, (key, movie) in enumerate(movies.items()):
            Title = movie.get("Title", "Unknown Title")
            Rating = movie.get("Rating", "No Rating")
            Year = movie.get("Year", "Unknown Year")
            print(f"{index + 1}. {Title} (Rating: {Rating}), Year: {Year}")
        print()
        while True:
            try:
                user_del_input = int(input("Please choose the number you want to delete? "))
                break
            except ValueError as e:
                print(f"No valid input. Error {e}")
        for index, (key, movie) in enumerate(movies.items()):
            if user_del_input == index + 1:
                print(f"Are you sure you want to delete >>> {Title} <<< permanently?")
                user_del_choice = input("Press 1 to proceed or any other to abort >>>")
        if user_del_choice == "1":
            try:
                movies = self.storage.delete_movie(Title)
                print(f"{Title} is deleted")
            except FileNotFoundError as e:
                print(f"Couldnt find storage destination. Error {e}")
        else:
            print("Deletion aborted by user")
        self.print_menu()
        self.menu_user_input()
        return movies


    def upd_movie(self):
        """
        Prompts the user to select a movie to update and allows them to change its rating.
        """
        try:
            movies = self.storage.get_movies()
        except FileNotFoundError as e:
            print(f"Could not load Movie Data. Error {e}")
            return
        for index, (key, movie) in enumerate(movies.items()):
            title = movie.get("title", "Unknown Title")
            rating = movie.get("rating", "No Rating")
            year_of_release = movie.get("year_of_release", "Unknown Year")
            print(f"{index + 1}. {title} (Rating: {rating}), Year: {year_of_release}")
        print()
        while True:
            try:
                user_choice = int(input("Please choose the number of the movie you want to update: "))
                break
            except ValueError as e:
                print(f"No valid input. Error {e}")
        for index, (key, movie) in enumerate(movies.items()):
            if user_choice == index + 1:
                # Confirm the movie to update
                title = movie.get("title", "Unknown Title")
                print(f"Are you sure you want to update the ranking for >>> {title} <<< ?")
                user_confirm = input("Press 1 to proceed or any other key to abort >>> ")
                if user_confirm == "1":
                    new_ranking = float(input("Please enter a new ranking (1-10): "))
                    try:
                        self.storage.update_movie(title, new_ranking)
                    except Exception as e:
                        print(f"Could not update function {e}")
                    print()
                    print(f"New ranking saved for {title} with a ranking of {new_ranking}")
                else:
                    print("Update aborted by user.")
                break
        self.print_menu()
        self.menu_user_input()


   
    def stats(self):
        """
        Calculates and prints various statistics about the movies in the database, including average, median, best, and worst ratings.
        """
        try:
            movies = self.storage.get_movies()
        except FileNotFoundError as e:
            print(f"Could not load Movie Data. Error {e}")
            return
        ratings = [movie["Rating"] for movie in movies.values()]
        if not ratings:
            print("No movies in the database to calculate statistics.")
            self.print_menu()
            self.menu_user_input()
            return
        average_ranking = round(statistics.mean(ratings), 1)
        median = round(statistics.median(ratings), 1)
        best_ranking = max(ratings)
        lowest_ranking = min(ratings)
        print(f"The average ranking of all Movies in the database is {average_ranking}")
        print("********************************************************")
        print(f"The median of all Movies in the database is {median}")
        print("********************************************************")
        print("The best ranked movie(s) in the database:")
        for movie in movies.values():
            if movie["Rating"] == best_ranking:
                print(f">>> {movie['Title']} with a ranking of {movie['Rating']}")
        print()
        print("The lowest ranked movie(s) in the database:")
        for movie in movies.values():
            if movie["Rating"] == lowest_ranking:
                print(f">>> {movie['Title']} with a ranking of {movie['Rating']}")
        print()
        self.print_menu()
        self.menu_user_input()


    def random_movies(self):
        """
        Selects and prints a random movie from the database.
        """
        try:
            movies = self.storage.get_movies()
        except FileNotFoundError as e:
            print(f"Could not load Movie Data. Error {e}")
            return
        number_of_movies = len(movies)
        random_number = random.randint(1, number_of_movies)
        for index, (title, movie) in enumerate(movies.items()):
            Title = movie.get("Title", "Unknown Title")
            Rating = movie.get("Rating", "No Rating")
            if index == random_number:
                print(f"Your random movie is *{Title}* with a ranking of {Rating}")
        self.print_menu()
        self.menu_user_input()


    def search_movies(self):
        """
        Searches for movies in the database based on a user-provided search term, using fuzzy matching for potential typos.
        """
        try:
            movies = self.storage.get_movies()
        except FileNotFoundError as e:
            print(f"Could not load Movie Data. Error {e}")
            return
        while True:
            try:
                search_user_input = input("Enter the movie name you are looking for: ").lower()
                break
            except ValueError as e:
                print(f"No valid input. Error {e}")
        found_data_list = {}
        fuzzy_data_list = {}
        for key, movie in movies.items():
            title = movie.get("Title", "").lower()
            if search_user_input in title:
                found_data_list[key] = movie
        if found_data_list:
            print("The following movies were found:")
            for key, movie in found_data_list.items():
                print(f"{movie['Title']} (Rating: {movie['Rating']}), Year: {movie['Year']}")
        else:
            print("*** No match found in database ***")
            for key, movie in movies.items():
                title = movie.get("Title", "")
                if fuzz.ratio(search_user_input, title.lower()) > 35:
                    fuzzy_data_list[key] = movie
            if fuzzy_data_list:
                print("Did you mean:")
                for key, movie in fuzzy_data_list.items():
                    print(f"{movie['Title']} (Rating: {movie['Rating']}), Year: {movie['Year']}")
        self.print_menu()
        self.menu_user_input()


    def movies_sorted_rating(self):
        """
        Displays a list of movies sorted by their rating in descending order.
        """
        try:
            movies = self.storage.get_movies()
        except FileNotFoundError as e:
            print(f"Could not load Movie Data. Error {e}")
            return
        sorted_ranking_list = sorted(movies.items(), key=lambda item: item[1]["Rating"], reverse=True)
        for key, movie in sorted_ranking_list:
            title = movie.get("Title", "Unknown Title")
            rating = movie.get("Rating", "No Rating")
            year = movie.get("Year", "Unknown Year")
            print(f"{title} (Rating: {rating}), Year: {year}")
        self.print_menu()
        self.menu_user_input()


    def movies_sorted_year(self):
        """
        Displays a list of movies sorted by their year of release, in either ascending or descending order.
        """
        try:
            movies = self.storage.get_movies()
        except FileNotFoundError as e:
            print(f"Could not load Movie Data. Error {e}")
            return
        while True:
            try:
                order_direction = input("Press 1 for increasing or 0 for decreasing direction")
                if order_direction == "0" or "1":
                    break
            except ValueError as e:
                print(f"Wrong Input. Try again! Error {e}")

        if order_direction == "1":
            sorted_ranking_list = sorted(movies.items(), key=lambda item: item[1]["Year"], reverse=False)
        elif order_direction == "0":
            sorted_ranking_list = sorted(movies.items(), key=lambda item: item[1]["Year"], reverse=True)

        for key, movie in sorted_ranking_list:
            title = movie.get("Title", "Unknown Title")
            rating = movie.get("Rating", "No Rating")
            year_of_release = movie.get("Year", "Unknown Year")
            print(f"{title} (Rating: {rating}), Year: {year_of_release}")
        self.print_menu()
        self.menu_user_input()


    def rating_histo(self):
        """
        Creates and displays a histogram of movie ratings, saving it to a user-specified file.
        """
        try:
            movies = self.storage.get_movies()
        except FileNotFoundError as e:
            print(f"Could not load Movie Data. Error {e}")
        ratings = [movie["Rating"] for movie in movies.values()]
        # Create histogram
        try:
            plt.figure(figsize=(10, 7))
            plt.hist(ratings, bins=10, edgecolor='black', alpha=0.7)
            plt.title('Distribution of Movie Ratings')
            plt.xlabel('Rating')
            plt.ylabel('Number of Movies')
            plt.grid(True)
            # Using Tkinter to specify and save the file generated
            root = tk.Tk()
            root.withdraw()
            file_path = filedialog.asksaveasfilename(
                defaultextension=".png",
                filetypes=[("PNG files", "*.png"), ("All files", "*.*")],
                title="Save plot as"
            )
            if file_path:
                plt.savefig(file_path)
                print(f"Plot saved successfully at {file_path}")
            # Show the plot
            plt.show()
        except Exception as e:
            print(f"An unexpected Error occurred. Error {e}")
        self.print_menu()
        self.menu_user_input()


    

    def generate_web(self, output_path="output.html"):
        """
        Generates a web page that lists all movies with their posters, titles, years, and ratings.

        Parameters:
            file_path (str): Path to the HTML template file.
            output_path (str): Path to save the generated HTML file (default is 'output.html').

        Returns:
            None
        """
        # Load the HTML template content
        file_path = os.path.join('static', 'index_template.html')
        try:
            with open(file_path, "r") as template_file:
                template_content = template_file.read()
        except FileNotFoundError as e:
            print(f"Template file not found: {e}")
            return
        except IOError as e:
            print(f"IO Error: {e}")
            return
        
        # Fetch all movies from storage
        try:
            movies = self.storage.get_movies()
        except FileNotFoundError as e:
            print(f"Could not load movie data. Error: {e}")
            return
        
        # Create HTML movie entries
        movie_entries = ""
        for movie in movies.values():
            title = movie.get("Title", "Unknown Title")
            year = movie.get("Year", "Unknown Year")
            rating = movie.get("Rating", "No Rating")
            poster_url = movie.get("Poster", "")

            # HTML structure for each movie entry
            movie_entry = f"""
            <li class="movie">
                <div class="movie-poster">
                    <img src="{poster_url}" alt="Poster of {title}" style="width:150px; height:auto;">
                </div>
                <div class="movie-details">
                    <h2>{title}</h2>
                    <p>Year: {year}</p>
                    <p>Rating: {rating}</p>
                </div>
            </li>
            """
            movie_entries += movie_entry
        
        # Replace placeholders in the template with actual content
        template_content = template_content.replace("__TEMPLATE_TITLE__", "My Movie App")
        template_content = template_content.replace("__TEMPLATE_MOVIE_GRID__", movie_entries)
        
        # Save the final HTML to the output file
        try:
            with open(output_path, "w") as output_file:
                output_file.write(template_content)
            print(f"Generated HTML successfully saved to {output_path}")
        except IOError as e:
            print(f"Error saving the HTML file: {e}")
    

    def run(self):
        self.print_menu()
        self.menu_user_input()
     