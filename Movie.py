import requests
import webbrowser

def search(movie):
    url = f'https://www.omdbapi.com/?t={movie}&apikey=7f6b49b2'
    response = requests.get(url)
    data = response.json()
    imdb_id = data.get('imdbID')
    return imdb_id

def open_movie_link(movie):
    imdb_id = search(movie)
    if imdb_id:
        link = f'https://vidsrc.net/embed/{imdb_id}'
        webbrowser.open(link)
    else:
        print("Movie not found.")

# Replace this with the method to get the movie title from the .bat interface
query = input("Enter the movie title: ")  # For testing, use input() to simulate .bat interface
open_movie_link(query)
