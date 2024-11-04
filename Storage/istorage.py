from abc import ABC, abstractmethod

class IStorage(ABC):
    @abstractmethod
    def get_movies(self):
        pass

    @abstractmethod
    def save_movies(self, movies):
        pass    


    @abstractmethod
    def add_movie(self, title, year, rating, poster):
        pass


    @abstractmethod
    def delete_movie(self, title_para):
        pass


    @abstractmethod
    def update_movie(self, title_para, rating):
        pass