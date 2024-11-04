import requests
import os
from dotenv import load_dotenv
load_dotenv()
API_KEY = os.getenv('API_KEY')




### THE POSTER FEATURE IS ONLY AVAILABLE FOR PATREONS. PAID SERVICE 


def Fetch_Movie(Title):
    """Function fetching movie data from omdbapi.

    Args:
        Title (string): Name of Movie

    Return:
        Dictionary with Movie Data    
    """
    print(API_KEY)
    API_Url = f"http://www.omdbapi.com/?apikey={API_KEY}&t={Title}"
    # Poster_API_URL = f"http://img.omdbapi.com/?apikey={API_KEY}&t={Title}"
    try:
        response = requests.get(API_Url)
        movie_data = response.json()
        return movie_data
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")  
    except requests.exceptions.ConnectionError as conn_err:
        print(f"Connection error occurred: {conn_err}")  
    except requests.exceptions.Timeout as timeout_err:
        print(f"Timeout error occurred: {timeout_err}")  
    except requests.exceptions.RequestException as req_err:
        print(f"An error occurred: {req_err}")  
    return None  

    
    
    # response_poster = requests.get(Poster_API_URL)
    
    # movie_poster =response_poster.status_code



# show_me = Fetch_Movie("inception")
# print(show_me)