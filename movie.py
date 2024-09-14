import statistics
import tkinter as tk
from tkinter import filedialog
import random
import matplotlib.pyplot as plt
from fuzzywuzzy import fuzz

def main():
    movies = {
        "The Shawshank Redemption": 9.5,
        "Pulp Fiction": 8.8,
        "The Room": 3.6,
        "The Godfather": 9.2,
        "The Godfather: Part II": 9.0,
        "The Dark Knight": 9.0,
        "12 Angry Men": 8.9,
        "Everything Everywhere All At Once": 8.9,
        "Forrest Gump": 8.8,
        "Star Wars: Episode V": 8.7
    }
    print_menu()
    menu_user_input(movies)
    return

def print_menu():
    print()
    print("********** My Movies Database **********")
    print()
    print("Menu:")
    print("1. List movies")
    print("2. Add movie")
    print("3. Delete movie")
    print("4. Update movie")
    print("5. Stats")
    print("6. Random movie")
    print("7. Search movie")
    print("8. Movies sorted by rating")
    print("9. Create Rating Histogram")
    print("10. Exit")

def menu_user_input(movies):
    print()
    user_choice = input("Enter choice (1-9) ")
    print()
    if user_choice == "1":
        list_movies(movies)
    elif user_choice == "2":
        add_movie(movies)
    elif user_choice == "3":
        del_movie(movies)    
    elif user_choice == "4":
        upd_movie(movies)       
    elif user_choice == "5":
        stats(movies)
    elif user_choice == "6":
        random_movies(movies)    
    elif user_choice == "7":
        search_movies(movies)
    elif user_choice == "8":
        movies_sorted_rating(movies)
    elif user_choice == "9":
        rating_histo(movies)
    elif user_choice == "10":
        return  
    else:
        print("***Invalid input. Please choose a number between 1 and 9.***")
        print_menu()
        menu_user_input(movies)

def list_movies(movies):
    print("List of movies in database")
    print("**************************")
    for index, (key, value) in enumerate(movies.items()):
        print(f"{index + 1}. {key}: {value}")
    print_menu()
    menu_user_input(movies)
# Refactor if else( no else needed)
def add_movie(movies):
    movie_add_by_user = input(" Please enter the movie with you want to enter ")
    ranking_add_by_user = float(input("Pleae enter Ranking (Float 1-10) ")  )
    movies_to_add =True
    for movie in movies.keys():
        if movie_add_by_user.lower() in movie.lower():
            print("Movie already exist. Pleases update movie if necessary.")
            print_menu()       
            menu_user_input(movies)
            movies_to_add =False
            return
        # else:
        #    movies_to_add = True
    if movies_to_add:    
        movies[movie_add_by_user]= ranking_add_by_user
        print()
        print("***Movie added to database***")
        print()
    print_menu()       
    menu_user_input(movies)

def del_movie(movies):

    for index, (key, value) in enumerate(movies.items()):
        print(f"{index + 1}. {key}: {value}")
    user_del_input = int(input("Please choose the number you want to delete? "))
    for index, (key, value) in enumerate(movies.items()):
        if user_del_input == index + 1:
            print(f"Are you sure you want to delete >>> {key} <<< permanently?")
            user_del_choice= input("Press 1 to proceed or any other to abort >>>")
            del_upd_movie = key
    if user_del_choice == "1" :
        del movies[del_upd_movie]
        print(f"{del_movie} is deleted")
    else:
        print("Deletion aborted by user")    
    print_menu()       
    menu_user_input(movies)    


def upd_movie(movies):
    for index, (key, value) in enumerate(movies.items()):
        print(f"{index + 1}. {key}: {value}")
    user_del_input = int(input("Please choose the number you want to delete? "))
    for index, (key, value) in enumerate(movies.items()):
        if user_del_input == index + 1:
            print(f"Are you sure you want to update the ranking for >>> {key} <<< ?")
            user_del_choice= input("Press 1 to proceed or any other to abort >>>")
            upd_movie = key
    if user_del_choice == "1" :
        new_ranking = float(input("Pleasen enter a new ranking from 1 - 10 "))
        movies[upd_movie] =new_ranking
        print(f"New ranking saved for {upd_movie} with a ranking of {new_ranking} ")
    else:
        print("Deletion aborted by user")
    print_menu()
    menu_user_input(movies)
    
def stats(movies):
    average_ranking_list = [rating for rating in movies.values()]
    sorted_ranking_list = sorted(movies.items(), key=lambda item: item[1], reverse=True)
    average_ranking = statistics.mean(average_ranking_list)
    median = statistics.median(average_ranking_list)
    best_ranking = sorted_ranking_list[0][1]
    lowest_ranking = sorted_ranking_list[-1][1]

    print(f"The average ranking of all Movies in the database is {average_ranking}")
    print("********************************************************")
    print(f"The median of all Movies in the database is {median}")
    print("********************************************************")
    print(f"The best ranked movie(s) in the database")
    print()
    for movie, ranking in movies.items():
        if ranking == best_ranking:
            print(f">>> {movie} with a ranking of {ranking}")
            print()
    print()
    print(f"The lowest ranked movie(s) in the database")
    print()
    for movie, ranking in movies.items():
        if ranking == lowest_ranking:
            print(f">>> {movie} with a ranking of {ranking}")
            print()
    print_menu()
    menu_user_input(movies)

def random_movies(movies):
    number_of_movies = len(movies)
    random_number = random.randint(1,number_of_movies) 
    for index, (key, value) in enumerate(movies.items()):
        if index == random_number:
            print(f"Your random movie is {key}, with a ranking of {value}")
    print_menu()
    menu_user_input(movies)         

def search_movies(movies):
    search_user_input = input("Enter the movie name you are looking for: ").lower()
    found_data_list = {}
    fuzzy_data_list = {}
    for movie, ranking in movies.items():
        if search_user_input in movie.lower():
            found_data_list[movie] = ranking

    if found_data_list:
        print("The following movies were found")
        for movie, ranking in found_data_list.items():
            print(f"{movie} {ranking}")
    else:
        print("*** No match found in database ***")
        for movie, ranking in movies.items():
            if fuzz.ratio(search_user_input,movie) >35:
                fuzzy_data_list[movie] = ranking
        if fuzzy_data_list:    
            print("Did you mean ")    
            for movie, ranking in fuzzy_data_list.items():
                print(f"{movie} {ranking}")    
    print_menu()
    menu_user_input(movies)

def movies_sorted_rating(movies):
    sorted_ranking_list = sorted(movies.items(), key=lambda item: item[1], reverse=True)
    for movie, rating in sorted_ranking_list:
        print(f"{movie}: {rating}")
    print_menu()
    menu_user_input(movies)

def rating_histo(movies):
    ratings = list(movies.values())

    # Creating 

    plt.figure(figsize=(10, 7))
    plt.hist(ratings, bins=20, edgecolor='black', alpha=0.7)
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

    plt.savefig(file_path)
    print(f"Plot saved successfully at {file_path}")

    # Display 
    plt.show()
    print_menu()
    menu_user_input(movies)

if __name__ == "__main__":
    main()



