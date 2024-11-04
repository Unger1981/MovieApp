from movie_app import MovieApp
from Storage.storage_json import StorageJson
from Storage.storage_csv import StorageCsv
import os


json_file_path = os.path.join('Movies', 'movies.json')
csv_file_path = os.path.join('Movies', 'movies.csv')

json_storage = StorageJson(json_file_path)
csv_storage = StorageCsv(csv_file_path)
new_app = MovieApp(csv_storage)


def main():
  new_app.run()


if __name__ == "__main__":
  main()