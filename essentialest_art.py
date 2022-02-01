import requests
from bs4 import BeautifulSoup

def get_all_films(city='msk'):
    if city == "msk":
        response = requests.get("https://msk.subscity.ru")
    elif city == "spb":
        response = requests.get("http://spb.subscity.ru")

    content = response.content.decode("utf-8", errors='ignore')

    soup = BeautifulSoup(content, 'lxml')

    divs_movie_original_title = soup.select('.movie-title-original')
    movies_original_name_list = []

    for div in divs_movie_original_title:
        movies_original_name_list.append(div.text)

    divs_movie_link = soup.select('.movie-poster-mobile')
    movies_links_list = []

    for div in divs_movie_link:
        a_tag_soup = div.find('a')
        movies_links_list.append(a_tag_soup['href'])

    all_films_list = []
    while len(movies_links_list) > 0 and len(movies_original_name_list) > 0:
        all_films_list.append((movies_original_name_list[-1],
                                    movies_links_list[-1]))
        movies_links_list.pop(-1)
        movies_original_name_list.pop(-1)

    return all_films_list

def get_theatres_for_film(*, film_name, film_link, city="msk"):
    link = ""
    if city == "msk":
        link = "https://msk.subscity.ru"
    elif city == "spb":
        link = "http://spb.subscity.ru"

    link += "/movies/"
    link += film_link

    response = requests.get(link)

    content = response.content.decode("utf-8", errors='ignore')

    soup = BeautifulSoup(content, 'lxml')

    divs_movie_cinema_title = soup.select('.cinema-name')
    movies_cinema_name_list = []

    for div in divs_movie_cinema_title:
        movies_cinema_name_list.append(div.text)

    divs_movie_theatre_location = soup.select('.location')
    movies_theatre_location_list = []

    for div in divs_movie_theatre_location:
        movies_theatre_location_list.append(div.text.replace('\xa0', ' '))

    all_theatres_for_film = []
    while len(movies_theatre_location_list) > 0 and len(movies_cinema_name_list) > 0:
        all_theatres_for_film.append((movies_cinema_name_list[-1],
                                    movies_theatre_location_list[-1]))
        movies_theatre_location_list.pop(-1)
        movies_cinema_name_list.pop(-1)

    return all_theatres_for_film

print(get_theatres_for_film(film_name="spider man", film_link="82819-spider-man-no-way-home"))
