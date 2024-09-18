import statistics
import tkinter as tk
from tkinter import filedialog
import random
import matplotlib.pyplot as plt
from fuzzywuzzy import fuzz
import json
import os
from movie_handling.movie_storage import get_movies,add_movie,delete_movie,update_movie, save_movies

def main():
    print_menu()
    menu_user_input()
    return

def print_menu():
    ###function printing basic menu, void###
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
    print("9. Create Rating Histogram")

def menu_user_input():
    ###function for user input control to call function by user input, void ###
    while True:
        try:
            print()
            user_choice = input("Enter choice (0-9) ")
            print() 
            break
        except ValueError as e:
            print(f"Invalid Input. Error {e}")
    if user_choice == "1":
        list_movies()
    elif user_choice == "2":
        add_movie_input()
    elif user_choice == "3":
        del_movie()
    elif user_choice == "4":
        upd_movie()     
    elif user_choice == "5":
        stats()
    elif user_choice == "6":
        random_movies()   
    elif user_choice == "7":
        search_movies()
    elif user_choice == "8":
        movies_sorted_rating()
    elif user_choice == "9":
        rating_histo()
    elif user_choice == "0":
            print("Bye!")
            return  
    else:
            print("***Invalid input. Please choose a number between 0 and 9.***")
            print_menu()
            menu_user_input()
    print_menu()
    menu_user_input()    

def list_movies():
    ###function print a list of all movies by loading from json and printing, void###
    print("List of movies in database")
    print("**************************")
    try:
        movies=get_movies()
    except FileNotFoundError as e:    
        print(f"Could not load Movie Data. Error {e}")
        print_menu()
        menu_user_input() 
        return   1
    for index, (key, movie) in enumerate(movies.items()):
        title = movie.get("title", "Unknown Title")
        rating = movie.get("rating", "No Rating")
        year_of_release = movie.get("year_of_release", "Unknown Year")
        print(f"{index + 1}. {title} (Rating: {rating}), Year: {year_of_release}")
    print_menu()
    menu_user_input()
    
def add_movie_input():
### Adding movie wit title raanking year_of_release to movies and storing to movies.json by using add_movie function0###
    try:
        movies=get_movies()
    except FileNotFoundError as e:    
        print(f"Could not load Movie Data. Error {e}")
    while True:
        try:
            movie_add_by_user = input(" Please enter the movie title you want to enter ")
            ranking_add_by_user = float(input("Pleae enter Ranking (Float 1-10) ")  )
            year_add_by_user = int(input("Please enter the year of release (e.g. 1994) "))
            break
        except ValueError as e:    
            print(f"No valid input. Please try again. Error {e}")
    for movie in movies.values():
        if movie_add_by_user.lower() == movie['title'].lower():
            print("Movie already exists. Please update the movie if necessary.")
            print_menu()
            menu_user_input()
            return
    try:
        movies = add_movie(movie_add_by_user,year_add_by_user,ranking_add_by_user)  
        print()
        print("***Movie added to database***")
        print()
        print_menu()       
        menu_user_input()
    except FileNotFoundError as e:
        print(f"Couldnt find storage destination. Error {e}")    
        print_menu()       
        menu_user_input()

def del_movie():
    ###deleting movie from movies dictonary and movies.json###
    try:
        movies=get_movies()
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
            user_del_input = int(input("Please choose the number you want to delete? "))
            break
        except ValueError as e:
            print(f"No valid input. Error {e}")
    for index, (key, movie) in enumerate(movies.items()):
        if user_del_input == index + 1:
            print(f"Are you sure you want to delete >>> {title} <<< permanently?")
            user_del_choice= input("Press 1 to proceed or any other to abort >>>")
    if user_del_choice == "1" :
        try:
            movies = delete_movie(title)
            print(f"{title} is deleted")
        except FileNotFoundError as e:
            print(f"Couldnt find storage destination. Error {e}")   
    else:
        print("Deletion aborted by user")
    print_menu()       
    menu_user_input()    
    return movies

def upd_movie():
    ###updating movie ranking###
    try:
        movies = get_movies()
    except FileNotFoundError as e:    
        print(f"Could not load Movie Data. Error {e}") 
        return
    for index, (key, movie) in enumerate(movies.items()):
        title = movie.get("title", "Unknown Title")
        rating = movie.get("rating", "No Rating")
        year_of_release = movie.get("year_of_release", "Unknown Year")
        print(f"{index + 1}. {title} (Rating: {rating}), Year: {year_of_release}")
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
                    update_movie(title, new_ranking)
                except Exception as e:    
                    print(f"Could not update function {e}")
                print()
                print(f"New ranking saved for {title} with a ranking of {new_ranking}")
            else:
                print("Update aborted by user.")
            break     
    print_menu()
    menu_user_input()
   
def stats():
    ###providing max and min stats for movies in database###
    try:
        movies=get_movies()
    except FileNotFoundError as e:    
        print(f"Could not load Movie Data. Error {e}")
        return
    ratings = [movie["rating"] for movie in movies.values()]
    if not ratings:
        print("No movies in the database to calculate statistics.")
        print_menu()
        menu_user_input()
        return
    average_ranking = statistics.mean(ratings)
    median = statistics.median(ratings)
    best_ranking = max(ratings)
    lowest_ranking = min(ratings)
    print(f"The average ranking of all Movies in the database is {average_ranking}")
    print("********************************************************")
    print(f"The median of all Movies in the database is {median}")
    print("********************************************************")
    print("The best ranked movie(s) in the database:")
    for movie in movies.values():
        if movie["rating"] == best_ranking:
            print(f">>> {movie['title']} with a ranking of {movie['rating']}")
    print()
    print("The lowest ranked movie(s) in the database:")
    for movie in movies.values():
        if movie["rating"] == lowest_ranking:
            print(f">>> {movie['title']} with a ranking of {movie['rating']}")
    print()
    print_menu()
    menu_user_input()

def random_movies():
    ###display random movie###
    try:
        movies=get_movies()
    except FileNotFoundError as e:    
        print(f"Could not load Movie Data. Error {e}")
        return
    number_of_movies = len(movies)
    random_number = random.randint(1,number_of_movies) 
    for index, (title, movie) in enumerate(movies.items()):
        title = movie.get("title", "Unknown Title")
        rating = movie.get("rating", "No Rating")
        if index == random_number:
            print(f"Your random movie is *{title}* with a ranking of {rating}")
    print_menu()
    menu_user_input()         

def search_movies():
    ###search for movie with fuzzy feature for typos###
    try:
        movies=get_movies()
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
        title = movie.get("title", "").lower()  
        if search_user_input in title:
            found_data_list[key] = movie
    if found_data_list:
        print("The following movies were found:")
        for key, movie in found_data_list.items():
            print(f"{movie['title']} (Rating: {movie['rating']}), Year: {movie['year_of_release']}")
    else:
        print("*** No match found in database ***")
        for key, movie in movies.items():
            title = movie.get("title", "")
            if fuzz.ratio(search_user_input, title.lower()) > 35:
                fuzzy_data_list[key] = movie 
        if fuzzy_data_list:
            print("Did you mean:")
            for key, movie in fuzzy_data_list.items():
                print(f"{movie['title']} (Rating: {movie['rating']}), Year: {movie['year_of_release']}")
    print_menu()
    menu_user_input()

def movies_sorted_rating():
    ###moviea sorted by ranking###
    try:
        movies=get_movies()
    except FileNotFoundError as e:    
        print(f"Could not load Movie Data. Error {e}")
        return
    sorted_ranking_list = sorted(movies.items(), key=lambda item: item[1]["rating"], reverse=True)
    for key, movie in sorted_ranking_list:
        title = movie.get("title", "Unknown Title")
        rating = movie.get("rating", "No Rating")
        year_of_release = movie.get("year_of_release", "Unknown Year")
        print(f"{title} (Rating: {rating}), Year: {year_of_release}")
    print_menu()
    menu_user_input()

def rating_histo():
    ###bloody histo for movie nonsense###
    # Extract ratings from the movie dictionaries
    try:
        movies=get_movies()
    except FileNotFoundError as e:    
        print(f"Could not load Movie Data. Error {e}")
    ratings = [movie["rating"] for movie in movies.values()]
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
        print(f"An unexpected Error occured. Error {e}")
    print_menu()
    menu_user_input()


if __name__ == "__main__":
    main()



